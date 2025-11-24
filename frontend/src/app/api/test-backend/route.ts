import { NextResponse } from "next/server";

export async function GET() {
    try {
        // Test backend health
        const healthResponse = await fetch("http://localhost:8000/health");
        const healthData = await healthResponse.json();

        // Test API root
        const rootResponse = await fetch("http://localhost:8000/");
        const rootData = await rootResponse.json();

        return NextResponse.json({
            success: true,
            health: {
                status: healthResponse.status,
                data: healthData,
            },
            root: {
                status: rootResponse.status,
                data: rootData,
            },
        });
    } catch (error: any) {
        return NextResponse.json(
            {
                success: false,
                error: error.message,
            },
            { status: 500 }
        );
    }
}

