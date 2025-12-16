// app/api/auth/login/route.js
import { NextResponse } from 'next/server';
import { cookies } from 'next/headers';

export async function POST(request) {
    const session = await getServerSession(authOptions);
    
    // 1. Authentication Check
    if (!session || !session.user) {
        return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
    }
    try {
        const body = await request.json();
        const { email, password } = body;
        
        const MOCK_USER = 'admin@example.com';
        const MOCK_PASS = 'password123';

        if (email === MOCK_USER && password === MOCK_PASS) {
            const sessionData = { 
                email: MOCK_USER, 
                name: "Admin User", 
                isLoggedIn: true 
            };
            
            cookies().set('auth-session', JSON.stringify(sessionData), {
                httpOnly: true, // Prevents client-side script access
                secure: process.env.NODE_ENV === 'production', // Use secure in production
                maxAge: 60 * 60 * 24, // 1 day
                path: '/', // Accessible from all pages
            });

            return NextResponse.json({ message: "Login successful" }, { status: 200 });
        } else {
            // Invalid credentials
            return NextResponse.json({ error: "Invalid email or password" }, { status: 401 });
        }

    } catch (error) {
        console.error('[AUTH API ERROR]', error);
        return NextResponse.json({ error: "An internal server error occurred." }, { status: 500 });
    }
}