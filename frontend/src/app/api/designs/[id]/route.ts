import { NextResponse } from "next/server";

const BACKEND_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

export async function GET(
    request: Request,
    { params }: { params: Promise<{ id: string }> }
) {
    try {
        const { id } = await params;

        console.log("[API Route] Fetching design:", id);
        console.log("[API Route] Backend URL:", BACKEND_URL);

        // Get authorization header from request
        const authHeader = request.headers.get("authorization");

        const response = await fetch(`${BACKEND_URL}/designs/${id}`, {
            headers: authHeader ? { "Authorization": authHeader } : {},
        });

        console.log("[API Route] Backend response status:", response.status);

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({ detail: "Unknown error" }));
            console.error("[API Route] Backend error:", errorData);
            return NextResponse.json(
                { error: errorData.detail || "Failed to fetch design" },
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

export async function PATCH(
    request: Request,
    { params }: { params: Promise<{ id: string }> }
) {
    try {
        const { id } = await params;
        const body = await request.json();

        console.log("[API Route] Updating design:", id);
        console.log("[API Route] Backend URL:", BACKEND_URL);

        // Get authorization header from request
        const authHeader = request.headers.get("authorization");

        const response = await fetch(`${BACKEND_URL}/designs/${id}`, {
            method: "PATCH",
            headers: {
                "Content-Type": "application/json",
                ...(authHeader ? { "Authorization": authHeader } : {}),
            },
            body: JSON.stringify(body),
        });

        console.log("[API Route] Backend response status:", response.status);

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({ detail: "Unknown error" }));
            console.error("[API Route] Backend error:", errorData);
            return NextResponse.json(
                { error: errorData.detail || "Failed to update design" },
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

export async function DELETE(
    request: Request,
    { params }: { params: Promise<{ id: string }> }
) {
    try {
        const { id } = await params;

        console.log("[API Route] Deleting design:", id);
        console.log("[API Route] Backend URL:", BACKEND_URL);

        // Get authorization header from request
        const authHeader = request.headers.get("authorization");

        const response = await fetch(`${BACKEND_URL}/designs/${id}`, {
            method: "DELETE",
            headers: authHeader ? { "Authorization": authHeader } : {},
        });

        console.log("[API Route] Backend response status:", response.status);

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({ detail: "Unknown error" }));
            console.error("[API Route] Backend error:", errorData);
            return NextResponse.json(
                { error: errorData.detail || "Failed to delete design" },
                { status: response.status }
            );
        }

        return NextResponse.json({ success: true });
    } catch (error: any) {
        console.error("[API Route] Error:", error);
        return NextResponse.json(
            { error: error.message || "Internal server error" },
            { status: 500 }
        );
    }
}

