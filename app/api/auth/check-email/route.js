import { NextResponse } from 'next/server';
import { query } from '@/lib/db';

export async function POST(request) {
    try {
        const { email } = await request.json();
        if (!email) return NextResponse.json({ error: "Email is required" }, { status: 400 });

        const res = await query('SELECT email FROM users WHERE email = $1', [email]);
        const exists = res.rows.length > 0;

        return NextResponse.json({ exists });
    } catch (error) {
        return NextResponse.json({ error: "Database error" }, { status: 500 });
    }
}