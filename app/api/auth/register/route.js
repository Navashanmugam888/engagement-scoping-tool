import { NextResponse } from 'next/server';
import { query } from '@/lib/db';

export async function POST(request) {
    try {
        const { name, email, password } = await request.json();

        if (!name || !email || !password) {
            return NextResponse.json({ error: "Missing fields" }, { status: 400 });
        }

        const checkRes = await query('SELECT email FROM users WHERE email = $1', [email]);
        if (checkRes.rows.length > 0) {
            return NextResponse.json({ error: "User already exists" }, { status: 409 });
        }

        // Create a dummy OID and default status/role
        const mockOid = `REG_${Date.now()}`;
        const initialRole = 'GUEST';
        const initialStatus = 'PENDING';

        await query(
            `INSERT INTO users (user_oid, email, user_name, password, role, status, created_at, last_login) 
             VALUES ($1, $2, $3, $4, $5, $6, NOW(), NOW())`,
            [mockOid, email, name, password, initialRole, initialStatus]
        );

        return NextResponse.json({ success: true });
    } catch (error) {
        console.error("Registration Error:", error);
        return NextResponse.json({ error: "Failed to register user" }, { status: 500 });
    }
}