import { NextResponse } from 'next/server';

export async function POST(req) {
    try {
        const body = await req.json();
        const { userEmail, userName, scopingData, selectedRoles, comments, submittedAt } = body;

        // Validate input
        if (!userEmail || !scopingData || !selectedRoles || selectedRoles.length === 0) {
            return NextResponse.json({
                success: false,
                error: 'Missing required fields'
            }, { status: 400 });
        }

        // Call Python Flask API backend
        const backendUrl = process.env.PYTHON_API_URL || 'http://localhost:5000';
        
        console.log(`Calling Python backend at: ${backendUrl}/api/scoping/submit`);
        
        const response = await fetch(`${backendUrl}/api/scoping/submit`, {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                userEmail,
                userName,
                scopingData,
                selectedRoles,
                comments,
                submittedAt
            })
        });

        if (!response.ok) {
            const errorData = await response.json();
            console.error('Backend error:', errorData);
            throw new Error(errorData.error || 'Backend processing failed');
        }

        const result = await response.json();

        return NextResponse.json({
            success: true,
            submissionId: result.submission_id,
            message: result.message,
            result: result.result,
            files: result.files
        });

    } catch (error) {
        console.error('Submit error:', error);
        return NextResponse.json(
            { 
                success: false, 
                error: error.message || 'Failed to process scoping submission'
            },
            { status: 500 }
        );
    }
}
