# Troubleshooting: Frontend-Backend Connection Issues

## Issue Summary

**Problem**: Frontend unable to connect to backend API, resulting in "Failed to fetch" errors when making direct HTTP requests from browser to `http://localhost:8000`.

**Symptoms**:
- ❌ Backend Health Check: "Failed to connect to backend: Failed to fetch"
- ❌ API Root Endpoint: "Failed to access API root: Failed to fetch"
- ✅ CORS Configuration: Success (no CORS errors)
- ✅ Environment Variables: Success (properly configured)

**Date**: November 24, 2025

---

## Root Cause Analysis

### Step-by-Step Investigation

#### 1. **Verified Backend Server Status**
- Backend was running on `http://0.0.0.0:8000`
- Health endpoint responded correctly to `curl` requests
- No incoming requests logged from browser

#### 2. **Verified Frontend Server Status**
- Frontend running on `http://localhost:3000`
- Both servers using HTTP (not HTTPS)
- No protocol mismatch

#### 3. **Identified the Core Issue**
The test page was making **direct fetch requests from client-side JavaScript** to the backend:

```typescript
// ❌ PROBLEMATIC CODE
const response = await fetch("http://localhost:8000/health");
```

**Why This Failed**:
- Browser security policies can block direct cross-origin requests
- Even though CORS was properly configured on the backend, the browser was preventing the connection
- Network configuration or firewall rules may have interfered
- Direct client-to-backend communication is not the recommended Next.js pattern

---

## Solution: Next.js API Route Proxy Pattern

### Architecture Change

**Before** (Direct Client-to-Backend):
```
Browser (localhost:3000) --X--> Backend (localhost:8000)
         [BLOCKED]
```

**After** (Proxy via Next.js API Route):
```
Browser (localhost:3000) --> Next.js API Route (localhost:3000/api/*) --> Backend (localhost:8000)
         [SUCCESS]                    [SERVER-SIDE]                           [SUCCESS]
```

### Implementation

#### 1. Created Next.js API Route (`frontend/src/app/api/test-backend/route.ts`)

```typescript
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
```

**Key Points**:
- API route runs on the **server-side** (Node.js environment)
- No browser security restrictions
- Same-origin request from browser perspective
- Server-to-server communication with backend

#### 2. Updated Test Page to Use API Route

**Before**:
```typescript
// Direct browser request (FAILED)
const response = await fetch("http://localhost:8000/health");
```

**After**:
```typescript
// Request to Next.js API route (SUCCESS)
const response = await fetch("/api/test-backend");
const data = await response.json();

if (data.success) {
    // Process health and root endpoint results
    console.log(data.health.data);
    console.log(data.root.data);
}
```

---

## Verification

### Testing the Fix

1. **Direct API Route Test** (via curl):
```bash
curl http://localhost:3000/api/test-backend
```

**Expected Response**:
```json
{
  "success": true,
  "health": {
    "status": 200,
    "data": {
      "status": "healthy",
      "timestamp": "2025-11-24T11:52:31.808838",
      "service": "radic-backend"
    }
  },
  "root": {
    "status": 200,
    "data": {
      "message": "Welcome to Radic Backend API",
      "version": "0.1.0"
    }
  }
}
```

2. **Browser Test**:
- Navigate to `http://localhost:3000/test-connection`
- Click "Run Connection Tests"
- All tests should pass ✅

---

## Best Practices for Next.js + FastAPI Architecture

### ✅ DO: Use Next.js API Routes as Proxy

```typescript
// frontend/src/app/api/designs/route.ts
export async function GET() {
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/designs`);
    return NextResponse.json(await response.json());
}
```

### ❌ DON'T: Make Direct Backend Calls from Client Components

```typescript
// ❌ BAD: Direct call from client component
"use client";
export default function MyComponent() {
    const data = await fetch("http://localhost:8000/api/v1/designs");
}
```

### ✅ DO: Use API Routes for Backend Communication

```typescript
// ✅ GOOD: Call Next.js API route from client component
"use client";
export default function MyComponent() {
    const data = await fetch("/api/designs"); // Same origin
}
```

---

## Configuration Files

### Backend Configuration (`backend/.env`)
```env
SUPABASE_URL=https://tcyqlulxjqytjxpruemv.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
BACKEND_CORS_ORIGINS=["http://localhost:3000","http://localhost:3001"]
ENVIRONMENT=development
API_V1_STR=/api/v1
LOG_LEVEL=INFO
```

### Frontend Configuration (`frontend/.env.local`)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_SUPABASE_URL=https://tcyqlulxjqytjxpruemv.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
NEXT_PUBLIC_ENVIRONMENT=development
```

---

## Server Startup Commands

### Backend (Terminal 1)
```bash
cd backend
.venv\Scripts\activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Note**: Using `--host 0.0.0.0` makes the backend accessible from both `localhost` and `127.0.0.1`.

### Frontend (Terminal 2)
```bash
cd frontend
npm run dev
```

---

## Lessons Learned

1. **Browser Security**: Modern browsers have strict security policies that can block cross-origin requests even with proper CORS configuration.

2. **Next.js Architecture**: Next.js API routes are the recommended way to communicate with external APIs, providing:
   - Server-side execution (no browser restrictions)
   - Better security (API keys never exposed to browser)
   - Simplified error handling
   - Built-in caching capabilities

3. **Debugging Approach**: When facing "Failed to fetch" errors:
   - ✅ Verify backend is running and accessible via curl
   - ✅ Check browser console for detailed error messages
   - ✅ Verify CORS configuration
   - ✅ Consider using API route proxy pattern
   - ✅ Check network tab in browser DevTools

4. **Environment Variables**: Ensure frontend has actual values (not placeholders) for Supabase and other services.

---

## Related Files

- `frontend/src/app/test-connection/page.tsx` - Connection test UI
- `frontend/src/app/api/test-backend/route.ts` - API proxy route
- `frontend/src/lib/api.ts` - API client functions
- `backend/app/main.py` - Backend entry point with CORS
- `backend/app/core/config.py` - Backend configuration

---

## Future Improvements

1. **Centralized API Client**: Create a unified API client that always uses Next.js API routes
2. **Error Handling**: Add comprehensive error handling and retry logic
3. **Monitoring**: Add logging and monitoring for API route performance
4. **Type Safety**: Share TypeScript types between frontend and backend
5. **Authentication**: Implement proper JWT token handling through API routes

---

**Status**: ✅ RESOLVED

**Resolution Date**: November 24, 2025

**Verified By**: Connection test page showing all tests passing

