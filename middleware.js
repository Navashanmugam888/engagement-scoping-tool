import { withAuth } from "next-auth/middleware";
import { NextResponse } from 'next/server';

export default withAuth(
    function middleware(req) {
        const token = req.nextauth.token;
        const url = req.nextUrl;
        const pathname = url.pathname;
        const userStatus = token?.status;

        // --- PENDING USER LOCKDOWN ---
        if (userStatus === 'PENDING') {
            const allowedPaths = ['/access-pending', '/api/auth', '/login', '/signup'];
            if (!allowedPaths.some(path => pathname.startsWith(path))) {
                return NextResponse.redirect(new URL('/access-pending', req.url));
            }
        }

        // No role restrictions - everyone can access scoping tool

        return NextResponse.next();
    },
    {
        callbacks: {
            authorized: ({ token, req }) => {
                const pathname = req.nextUrl.pathname;

                // Allow public access to auth-related pages
                if (pathname === '/' ||
                    pathname.startsWith('/signup') ||
                    pathname.startsWith('/api/auth')) {
                    return true;
                }

                return !!token;
            },
        },
        pages: {
            signIn: '/',
            error: '/',
        },
    }
);

export const config = {
    matcher: [
        '/admin/:path*',
        '/fccs-scoping/:path*',
        '/access-pending',
    ],
};