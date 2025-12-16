import { NextResponse } from 'next/server';

export async function GET(req) {
    try {
        const { searchParams } = new URL(req.url);
        const userEmail = searchParams.get('email');

        if (!userEmail) {
            return NextResponse.json(
                { error: 'Email is required' },
                { status: 400 }
            );
        }

        // Call Python Flask API backend
        const backendUrl = process.env.PYTHON_API_URL || 'http://localhost:5000';
        
        console.log(`Fetching history from: ${backendUrl}/api/scoping/history?email=${userEmail}`);
        
        const response = await fetch(`${backendUrl}/api/scoping/history?email=${encodeURIComponent(userEmail)}`);

        if (!response.ok) {
            const errorData = await response.json();
            console.error('Backend error:', errorData);
            throw new Error(errorData.error || 'Failed to fetch history');
        }

        const result = await response.json();

        return NextResponse.json({
            success: true,
            submissions: result.submissions || []
        });

    } catch (error) {
        console.error('History fetch error:', error);
        return NextResponse.json(
            { success: false, error: error.message },
            { status: 500 }
        );
    }
}
