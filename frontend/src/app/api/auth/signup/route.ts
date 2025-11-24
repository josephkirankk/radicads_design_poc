import { NextResponse } from "next/server";

const BACKEND_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

export async function POST(request: Request) {
    try {
        const body = await request.json();
        console.log("[API Route] Signup request");
        console.log("[API Route] Backend URL:", BACKEND_URL);

        const response = await fetch(`${BACKEND_URL}/auth/signup`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(body),
        });

        console.log("[API Route] Backend response status:", response.status);

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({ detail: "Unknown error" }));
            console.error("[API Route] Backend error:", errorData);
            return NextResponse.json(
                { error: errorData.detail || "Failed to sign up" },
                { status: response.status }
            );
        }

        const data = await response.json();
        console.log("[API Route] Success: User signed up");
        return NextResponse.json(data);
    } catch (error: any) {
        console.error("[API Route] Error:", error);
        return NextResponse.json(
            { error: error.message || "Internal server error" },
            { status: 500 }
        );
    }
}

