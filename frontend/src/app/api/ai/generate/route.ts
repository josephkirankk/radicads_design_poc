import { NextResponse } from "next/server";

const BACKEND_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

export async function POST(request: Request) {
    try {
        const body = await request.json();
        const { prompt } = body;

        if (!prompt) {
            return NextResponse.json(
                { error: "Prompt is required" },
                { status: 400 }
            );
        }

        console.log("[API Route] Generating design with prompt:", prompt);
        console.log("[API Route] Backend URL:", BACKEND_URL);

        const response = await fetch(`${BACKEND_URL}/ai/layout/generate`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ prompt }),
        });

        console.log("[API Route] Backend response status:", response.status);

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({ detail: "Unknown error" }));
            console.error("[API Route] Backend error:", errorData);
            return NextResponse.json(
                { error: errorData.detail || "Failed to generate design" },
                { status: response.status }
            );
        }

        const data = await response.json();
        console.log("[API Route] Success:", data);
        return NextResponse.json(data);
    } catch (error: any) {
        console.error("[API Route] Error:", error);
        return NextResponse.json(
            { error: error.message || "Internal server error" },
            { status: 500 }
        );
    }
}

