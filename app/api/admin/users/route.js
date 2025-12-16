import { NextResponse } from 'next/server';
import { query } from '@/lib/db';
import { getServerSession } from "next-auth/next";
import { authOptions } from "@/app/api/auth/[...nextauth]/route";

// GET: Get all users (Protected)
export async function GET(request) {
    // 1. SECURITY CHECK
    const session = await getServerSession(authOptions);
    
    if (!session || session.user.role !== 'SUPER_ADMIN') {
        return NextResponse.json({ error: "Unauthorized Access" }, { status: 403 });
    }

    try {
        const res = await query('SELECT user_oid, user_name, email, role, status, last_login FROM users ORDER BY created_at DESC');
        return NextResponse.json(res.rows);
    } catch (error) {
        return NextResponse.json({ error: error.message }, { status: 500 });
    }
}

// PUT: Update User Role/Status (Protected)
export async function PUT(request) {
    // 1. SECURITY CHECK
    const session = await getServerSession(authOptions);
    
    if (!session || session.user.role !== 'SUPER_ADMIN') {
        return NextResponse.json({ error: "Unauthorized Access" }, { status: 403 });
    }

    try {
        const body = await request.json();
        const { email, role, status } = body;

        await query(
            'UPDATE users SET role = $1, status = $2 WHERE email = $3',
            [role, status, email]
        );
        return NextResponse.json({ success: true });
    } catch (error) {
        return NextResponse.json({ error: error.message }, { status: 500 });
    }
}

// DELETE: Delete User (Protected)
export async function DELETE(request) {
    // 1. SECURITY CHECK
    const session = await getServerSession(authOptions);
    
    if (!session || session.user.role !== 'SUPER_ADMIN') {
        return NextResponse.json({ error: "Unauthorized Access" }, { status: 403 });
    }

    try {
        const body = await request.json();
        const { email } = body;

        // Prevent deleting yourself
        if (email === session.user.email) {
            return NextResponse.json({ error: "Cannot delete your own account" }, { status: 400 });
        }

        await query('DELETE FROM users WHERE email = $1', [email]);
        return NextResponse.json({ success: true });
    } catch (error) {
        return NextResponse.json({ error: error.message }, { status: 500 });
    }
}