import { NextResponse } from "next/server";

const BACKEND_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

export async function GET(request: Request) {
    try {
        console.log("[API Route] Get current user");
        console.log("[API Route] Backend URL:", BACKEND_URL);

        // Get authorization header from request
        const authHeader = request.headers.get("authorization");

        if (!authHeader) {
            return NextResponse.json(
                { error: "Authorization header required" },
                { status: 401 }
            );
        }

        const response = await fetch(`${BACKEND_URL}/auth/me`, {
            headers: {
                "Authorization": authHeader,
            },
        });

        console.log("[API Route] Backend response status:", response.status);

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({ detail: "Unknown error" }));
            console.error("[API Route] Backend error:", errorData);
            return NextResponse.json(
                { error: errorData.detail || "Failed to get user" },
                { status: response.status }
            );
        }

        const data = await response.json();
        console.log("[API Route] Success: User retrieved");
        return NextResponse.json(data);
    } catch (error: any) {
        console.error("[API Route] Error:", error);
        return NextResponse.json(
            { error: error.message || "Internal server error" },
            { status: 500 }
        );
    }
}

