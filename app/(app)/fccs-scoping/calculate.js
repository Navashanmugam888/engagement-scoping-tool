import { NextResponse } from 'next/server';

export async function POST(request) {
    try {
        const body = await request.json();
        const { scopingData } = body;

        // --- 1. COMPLEXITY LOGIC ---
        let score = 0;
        let items = 0;

        // Simple weighting logic (replace with your complex math later)
        Object.values(scopingData).forEach(item => {
            if (item.value === 'YES') {
                score += 5; // Base score for feature
                if (item.count) {
                    score += (item.count * 2); // Weight per item count
                }
                items++;
            }
        });

        // --- 2. ESTIMATION LOGIC ---
        let weeks = 8;
        let complexity = "Standard";
        let cost = "$50,000";

        if (score > 200) {
            weeks = 24;
            complexity = "Enterprise";
            cost = "$250,000+";
        } else if (score > 100) {
            weeks = 16;
            complexity = "Complex";
            cost = "$150,000";
        } else if (score > 50) {
            weeks = 12;
            complexity = "Medium";
            cost = "$80,000";
        }

        // --- 3. RETURN RESULT ---
        return NextResponse.json({
            score: score,
            itemsCount: items,
            weeks: weeks,
            complexity: complexity,
            cost: cost,
            message: "Calculation successful"
        });

    } catch (error) {
        return NextResponse.json({ error: "Calculation failed" }, { status: 500 });
    }
}