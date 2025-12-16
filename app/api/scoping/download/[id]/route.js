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

        // Call Python Flask API backend to download report
        const backendUrl = process.env.PYTHON_API_URL || 'http://localhost:5000';
        
        console.log(`Downloading report from: ${backendUrl}/api/scoping/download/${id}`);
        
        const response = await fetch(`${backendUrl}/api/scoping/download/${id}`);

        if (!response.ok) {
            const errorData = await response.json();
            console.error('Backend error:', errorData);
            
            if (response.status === 404) {
                return NextResponse.json(
                    { error: 'Report not found' },
                    { status: 404 }
                );
            }
            
            throw new Error(errorData.error || 'Failed to download report');
        }

        // Get the file as a blob
        const blob = await response.blob();
        
        // Get filename from content-disposition header or use default
        const contentDisposition = response.headers.get('content-disposition');
        let filename = 'scoping_report.docx';
        if (contentDisposition) {
            const filenameMatch = contentDisposition.match(/filename="?(.+)"?/);
            if (filenameMatch) {
                filename = filenameMatch[1];
            }
        }

        // Return the file
        return new NextResponse(blob, {
            headers: {
                'Content-Type': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                'Content-Disposition': `attachment; filename="${filename}"`,
            },
        });

    } catch (error) {
        console.error('Download error:', error);
        return NextResponse.json(
            { success: false, error: error.message },
            { status: 500 }
        );
    }
}
