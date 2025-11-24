# Quick Reference: API Communication Patterns

## 🎯 Golden Rule for Next.js + FastAPI

**Never make direct backend API calls from client components. Always use Next.js API routes as a proxy.**

---

## ✅ Correct Pattern

### 1. Create Next.js API Route (Server-Side)

**File**: `frontend/src/app/api/[endpoint]/route.ts`

```typescript
import { NextResponse } from "next/server";

const BACKEND_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

export async function GET(request: Request) {
    try {
        const response = await fetch(`${BACKEND_URL}/your-endpoint`);
        
        if (!response.ok) {
            throw new Error(`Backend error: ${response.status}`);
        }
        
        const data = await response.json();
        return NextResponse.json(data);
    } catch (error: any) {
        return NextResponse.json(
            { error: error.message },
            { status: 500 }
        );
    }
}

export async function POST(request: Request) {
    try {
        const body = await request.json();
        
        const response = await fetch(`${BACKEND_URL}/your-endpoint`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(body),
        });
        
        if (!response.ok) {
            throw new Error(`Backend error: ${response.status}`);
        }
        
        const data = await response.json();
        return NextResponse.json(data);
    } catch (error: any) {
        return NextResponse.json(
            { error: error.message },
            { status: 500 }
        );
    }
}
```

### 2. Call from Client Component

**File**: `frontend/src/components/YourComponent.tsx`

```typescript
"use client";

import { useState } from "react";

export default function YourComponent() {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const fetchData = async () => {
        setLoading(true);
        setError(null);
        
        try {
            // ✅ Call Next.js API route (same origin)
            const response = await fetch("/api/your-endpoint");
            
            if (!response.ok) {
                throw new Error("Failed to fetch data");
            }
            
            const result = await response.json();
            setData(result);
        } catch (err: any) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    const postData = async (payload: any) => {
        setLoading(true);
        setError(null);
        
        try {
            // ✅ POST to Next.js API route
            const response = await fetch("/api/your-endpoint", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(payload),
            });
            
            if (!response.ok) {
                throw new Error("Failed to post data");
            }
            
            const result = await response.json();
            setData(result);
        } catch (err: any) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div>
            <button onClick={fetchData}>Fetch Data</button>
            {loading && <p>Loading...</p>}
            {error && <p>Error: {error}</p>}
            {data && <pre>{JSON.stringify(data, null, 2)}</pre>}
        </div>
    );
}
```

---

## ❌ Incorrect Pattern (Don't Do This)

```typescript
"use client";

export default function BadComponent() {
    const fetchData = async () => {
        // ❌ WRONG: Direct call to backend from browser
        const response = await fetch("http://localhost:8000/api/v1/endpoint");
        // This will fail due to browser security policies
    };
}
```

---

## 🔧 Common API Route Patterns

### Pattern 1: Simple Proxy

```typescript
// frontend/src/app/api/health/route.ts
export async function GET() {
    const response = await fetch("http://localhost:8000/health");
    return NextResponse.json(await response.json());
}
```

### Pattern 2: With Authentication

```typescript
// frontend/src/app/api/protected/route.ts
export async function GET(request: Request) {
    const token = request.headers.get("authorization");
    
    const response = await fetch(`${BACKEND_URL}/protected`, {
        headers: {
            "Authorization": token || "",
        },
    });
    
    return NextResponse.json(await response.json());
}
```

### Pattern 3: With Query Parameters

```typescript
// frontend/src/app/api/search/route.ts
export async function GET(request: Request) {
    const { searchParams } = new URL(request.url);
    const query = searchParams.get("q");
    
    const response = await fetch(`${BACKEND_URL}/search?q=${query}`);
    return NextResponse.json(await response.json());
}
```

### Pattern 4: Dynamic Routes

```typescript
// frontend/src/app/api/designs/[id]/route.ts
export async function GET(
    request: Request,
    { params }: { params: { id: string } }
) {
    const response = await fetch(`${BACKEND_URL}/designs/${params.id}`);
    return NextResponse.json(await response.json());
}
```

---

## 🚀 Using with React Query

```typescript
// frontend/src/hooks/useDesigns.ts
import { useQuery, useMutation } from "@tanstack/react-query";

export const useDesigns = () => {
    return useQuery({
        queryKey: ["designs"],
        queryFn: async () => {
            // ✅ Call Next.js API route
            const response = await fetch("/api/designs");
            if (!response.ok) throw new Error("Failed to fetch designs");
            return response.json();
        },
    });
};

export const useCreateDesign = () => {
    return useMutation({
        mutationFn: async (data: any) => {
            // ✅ Call Next.js API route
            const response = await fetch("/api/designs", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data),
            });
            if (!response.ok) throw new Error("Failed to create design");
            return response.json();
        },
    });
};
```

---

## 📋 Checklist for New API Endpoints

- [ ] Create Next.js API route in `frontend/src/app/api/[endpoint]/route.ts`
- [ ] Implement GET, POST, PUT, DELETE as needed
- [ ] Add proper error handling
- [ ] Use environment variables for backend URL
- [ ] Test with curl: `curl http://localhost:3000/api/[endpoint]`
- [ ] Update client components to use the new API route
- [ ] Add TypeScript types for request/response
- [ ] Document the endpoint

---

## 🐛 Debugging Tips

### If you see "Failed to fetch":
1. Check if backend is running: `curl http://localhost:8000/health`
2. Check if API route works: `curl http://localhost:3000/api/your-endpoint`
3. Check browser console for detailed errors
4. Verify environment variables are set correctly

### If you see CORS errors:
- You're probably making direct backend calls from the browser
- Switch to using Next.js API routes

### If you see 404 errors:
- Verify the API route file exists in the correct location
- Check the route naming convention
- Restart the Next.js dev server

---

## 📚 Additional Resources

- [Next.js API Routes Documentation](https://nextjs.org/docs/app/building-your-application/routing/route-handlers)
- [FastAPI CORS Documentation](https://fastapi.tiangolo.com/tutorial/cors/)
- [React Query Documentation](https://tanstack.com/query/latest)

---

**Last Updated**: November 24, 2025

