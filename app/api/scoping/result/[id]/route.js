import { NextResponse } from 'next/server';

export async function GET(req, { params }) {
    try {
        const { id } = params;

        if (!id) {
            return NextResponse.json(
                { error: 'Submission ID is required' },
                { status: 400 }
            );
        }

        // Call Python Flask API backend
        const backendUrl = process.env.PYTHON_API_URL || 'http://localhost:5000';
        
        console.log(`Fetching result from: ${backendUrl}/api/scoping/result/${id}`);
        
        const response = await fetch(`${backendUrl}/api/scoping/result/${id}`);

        if (!response.ok) {
            const errorData = await response.json();
            console.error('Backend error:', errorData);
            
            if (response.status === 404) {
                return NextResponse.json(
                    { error: 'Submission not found' },
                    { status: 404 }
                );
            }
            
            throw new Error(errorData.error || 'Failed to fetch result');
        }

        const result = await response.json();

        return NextResponse.json({
            success: true,
            submission: result.submission
        });

    } catch (error) {
        console.error('Result fetch error:', error);
        return NextResponse.json(
            { success: false, error: error.message },
            { status: 500 }
        );
    }
}
