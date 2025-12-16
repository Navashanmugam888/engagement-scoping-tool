import { NextResponse } from 'next/server';
import { cookies } from 'next/headers';

export async function POST() {
    const session = await getServerSession(authOptions);
    
    // 1. Authentication Check
    if (!session || !session.user) {
        return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
    }
    try {
        // Clear the session cookie
        cookies().set('auth-session', '', {
            httpOnly: true,
            secure: process.env.NODE_ENV === 'production',
            maxAge: 0, // Expire the cookie immediately
            path: '/',
        });

        return NextResponse.json({ message: "Logout successful" }, { status: 200 });

    } catch (error) {
        console.error('[AUTH LOGOUT ERROR]', error);
        return NextResponse.json({ error: "An internal server error occurred." }, { status: 500 });
    }
}