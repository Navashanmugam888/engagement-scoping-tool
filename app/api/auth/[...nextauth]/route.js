import NextAuth from "next-auth";
import AzureADProvider from "next-auth/providers/azure-ad";
import CredentialsProvider from "next-auth/providers/credentials"; // <--- IMPORT THIS
import { query } from "@/lib/db";

// 1. Logic to Sync Azure User -> Postgres DB
async function registerOrUpdateUser(email, azureId, name, source) {
  try {
    const res = await query("SELECT * FROM users WHERE email = $1", [email]);
    if (res.rows.length === 0) {
      await query(
        `INSERT INTO users (user_oid, email, user_name, role, status, last_login) 
                 VALUES ($1, $2, $3, 'GUEST', 'PENDING', NOW())`,
        [azureId, email, name]
      );
    } else {
      await query(
        "UPDATE users SET last_login = NOW(), user_oid = $1 WHERE email = $2",
        [azureId, email]
      );
    }
    return true;
  } catch (error) {
    console.error("[DB SYNC ERROR]", error);
    return false;
  }
}

// 2. Helper to fetch user details
async function getUserFromDb(email) {
  try {
    const res = await query("SELECT * FROM users WHERE email = $1", [email]);
    return res.rows[0] || null;
  } catch (error) {
    return null;
  }
}

export const authOptions = {
  providers: [
    // --- 1. EMAIL/PASSWORD LOGIN ---
    CredentialsProvider({
      name: "Credentials",
      credentials: {
        email: { label: "Email", type: "text" },
        password: { label: "Password", type: "password" },
      },
      async authorize(credentials) {
        if (!credentials?.email || !credentials?.password) return null;

        // Fetch user from DB
        const user = await getUserFromDb(credentials.email);

        // Check if user exists
        if (!user) {
          throw new Error("User not found");
        }

        // Verify Password
        // Note: In production, you should use bcrypt.compare(credentials.password, user.password)
        // For now, strictly comparing strings as per your setup:
        if (user.password !== credentials.password) {
          throw new Error("Invalid password");
        }

        // Return the user object to be saved in the JWT
        return {
          id: user.user_oid || user.id,
          name: user.user_name,
          email: user.email,
          role: user.role,
          status: user.status,
        };
      },
    }),

    // --- 2. AZURE SSO LOGIN ---
    AzureADProvider({
      clientId: process.env.AZURE_AD_CLIENT_ID,
      clientSecret: process.env.AZURE_AD_CLIENT_SECRET,
      tenantId: process.env.AZURE_AD_TENANT_ID,
      profile(profile) {
        return {
          id: profile.oid,
          name: profile.name,
          email: profile.email || profile.preferred_username,
          image: null,
        };
      },
    }),
  ],
  callbacks: {
    async signIn({ user, account, profile }) {
      // A. Azure Logic: Sync user to DB
      if (account.provider === "azure-ad") {
        await registerOrUpdateUser(user.email, profile.oid, user.name, "login");
      }

      // B. Status Check Logic
      // We fetch the latest status from DB to ensure we don't rely on stale session data
      const dbUser = await getUserFromDb(user.email);

      // If user is not in DB yet (shouldn't happen due to logic above), allow them (it will fail elsewhere if critical)
      if (!dbUser) return true;

      // BLOCK BANNED USERS
      if (dbUser.status === "BANNED") {
        return false; // Rejects login, redirects to error page
      }

      // ALLOW PENDING USERS
      // (Middleware will catch them and send them to /access-pending)
      // We do NOT return false here anymore.

      return true;
    },
    async jwt({ token, user, trigger }) {
      // On initial sign in, 'user' is available.
      // On subsequent checks (or when update() is called), we refetch from DB to handle role/status changes in real-time.
      if (token.email) {
        const dbUser = await getUserFromDb(token.email);
        if (dbUser) {
          token.role = dbUser.role;
          token.status = dbUser.status;
          token.name = dbUser.user_name;
        }
      }
      return token;
    },
    async session({ session, token }) {
      if (session.user) {
        session.user.role = token.role;
        session.user.status = token.status;
        session.user.azureId = token.sub;
      }

      // Double check BANNED status in session to force logout if changed mid-session
      if (session.user?.status === "BANNED") {
        return null; // Invalidates session
      }

      return session;
    },
  },
  session: { strategy: "jwt" },
  pages: {
    signIn: "/", // Custom login page
    signOut: "/", // Redirect to login page after logout
    error: "/", // Redirect errors back to login
  },
};

const handler = NextAuth(authOptions);
export { handler as GET, handler as POST };
