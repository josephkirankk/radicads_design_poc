# Fix: Generate Design CORS Issue

## 🐛 Problem Summary

**Issue**: "Generate Design" functionality was failing with CORS error even though the connection test page was passing.

**Error Message**:
```
Access to fetch at 'http://localhost:8000/api/v1/auth/test' from origin 'http://127.0.0.1:3000' 
has been blocked by CORS policy: Response to preflight request doesn't pass access control check: 
No 'Access-Control-Allow-Origin' header is present on the requested resource.
```

**Date**: November 24, 2025

---

## 🔍 Root Cause Analysis

### Issue 1: CORS Origin Mismatch
- **Problem**: Backend CORS was configured for `http://localhost:3000` only
- **Reality**: Browser was accessing frontend via `http://127.0.0.1:3000`
- **Impact**: Browser treats `localhost` and `127.0.0.1` as different origins
- **Result**: CORS preflight requests were being blocked

### Issue 2: Direct Backend Calls (Architecture Violation)
- **Problem**: `frontend/src/lib/api.ts` was making direct fetch calls to backend
- **Code**:
  ```typescript
  // ❌ WRONG: Direct backend call from client
  const response = await fetch("http://localhost:8000/api/v1/ai/layout/generate", {...});
  ```
- **Impact**: 
  - Subject to CORS restrictions
  - Violates Next.js best practices
  - Inconsistent with our documented architecture
  - Exposes backend URL to client

### Why Connection Test Passed But Generate Failed
- **Connection test**: Used Next.js API routes (`/api/test-backend`) ✅
- **Generate design**: Used direct backend calls ❌
- **Result**: Test passed but actual feature failed

---

## ✅ Solutions Implemented

### Solution 1: Fixed CORS Configuration

**File**: `backend/.env`

**Before**:
```env
BACKEND_CORS_ORIGINS=["http://localhost:3000","http://localhost:3001"]
```

**After**:
```env
BACKEND_CORS_ORIGINS=["http://localhost:3000","http://localhost:3001","http://127.0.0.1:3000","http://127.0.0.1:3001"]
```

**Why**: Allows both `localhost` and `127.0.0.1` origins

### Solution 2: Created Next.js API Routes

#### 2a. AI Generate Route

**File**: `frontend/src/app/api/ai/generate/route.ts`

```typescript
import { NextResponse } from "next/server";

const BACKEND_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

export async function POST(request: Request) {
    try {
        const body = await request.json();
        const { prompt } = body;

        const response = await fetch(`${BACKEND_URL}/ai/layout/generate`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ prompt }),
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({ detail: "Unknown error" }));
            return NextResponse.json(
                { error: errorData.detail || "Failed to generate design" },
                { status: response.status }
            );
        }

        return NextResponse.json(await response.json());
    } catch (error: any) {
        return NextResponse.json(
            { error: error.message || "Internal server error" },
            { status: 500 }
        );
    }
}
```

#### 2b. Get Design Route

**File**: `frontend/src/app/api/designs/[id]/route.ts`

```typescript
import { NextResponse } from "next/server";

const BACKEND_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

export async function GET(
    request: Request,
    { params }: { params: { id: string } }
) {
    try {
        const response = await fetch(`${BACKEND_URL}/designs/${params.id}`);
        
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({ detail: "Unknown error" }));
            return NextResponse.json(
                { error: errorData.detail || "Failed to fetch design" },
                { status: response.status }
            );
        }

        return NextResponse.json(await response.json());
    } catch (error: any) {
        return NextResponse.json(
            { error: error.message || "Internal server error" },
            { status: 500 }
        );
    }
}
```

### Solution 3: Updated API Client

**File**: `frontend/src/lib/api.ts`

**Before** (Direct Backend Calls):
```typescript
const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000/api/v1";

export const api = {
    generateDesign: async (prompt: string) => {
        // ❌ Direct backend call - CORS issues
        const response = await fetch(`${API_URL}/ai/layout/generate`, {...});
    },
    getDesign: async (id: string) => {
        // ❌ Direct backend call - CORS issues
        const response = await fetch(`${API_URL}/designs/${id}`);
    },
};
```

**After** (Next.js API Routes):
```typescript
export const api = {
    generateDesign: async (prompt: string) => {
        // ✅ Call Next.js API route - No CORS issues
        const response = await fetch('/api/ai/generate', {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ prompt }),
        });
        // ... error handling
    },
    getDesign: async (id: string) => {
        // ✅ Call Next.js API route - No CORS issues
        const response = await fetch(`/api/designs/${id}`);
        // ... error handling
    },
};
```

---

## 🧪 Testing

### Test Page Created

**File**: `frontend/src/app/test-generate/page.tsx`

**URL**: `http://localhost:3000/test-generate`

**Tests**:
1. ✅ Current Origin - Shows if browser is using localhost or 127.0.0.1
2. ✅ Environment Variables - Verifies NEXT_PUBLIC_API_URL is set
3. ❌ Direct Backend Call - Should fail (demonstrates the problem)
4. ✅ Via Next.js API Route - Should succeed (demonstrates the solution)
5. ✅ AI Generate Endpoint - Tests actual generate functionality

### How to Test

1. Open browser: `http://localhost:3000/test-generate`
2. Click "Run Connection Tests"
3. Verify results:
   - Test 3 (Direct Backend Call) should FAIL ❌ (expected)
   - Test 4 (Via Next.js API Route) should PASS ✅
   - Test 5 (AI Generate Endpoint) should PASS ✅

---

## 📊 Architecture Comparison

### Before (Broken)
```
Browser (127.0.0.1:3000) --X--> Backend (localhost:8000)
         [CORS BLOCKED]
```

### After (Fixed)
```
Browser (127.0.0.1:3000) --> Next.js API Route --> Backend (localhost:8000)
         [SUCCESS]              [Proxy]              [SUCCESS]
```

---

## 📁 Files Modified/Created

### Created (3 files)
1. `frontend/src/app/api/ai/generate/route.ts` - AI generation proxy
2. `frontend/src/app/api/designs/[id]/route.ts` - Design fetch proxy
3. `frontend/src/app/test-generate/page.tsx` - Comprehensive test page

### Modified (2 files)
1. `backend/.env` - Added 127.0.0.1 to CORS origins
2. `frontend/src/lib/api.ts` - Changed from direct calls to API routes

---

## ✅ Verification Steps

1. **Backend CORS Updated**: ✅
   ```bash
   # Check backend logs for:
   # CORS enabled for origins: ['http://localhost:3000', 'http://localhost:3001', 'http://127.0.0.1:3000', 'http://127.0.0.1:3001']
   ```

2. **API Routes Created**: ✅
   - `/api/ai/generate` - POST endpoint
   - `/api/designs/[id]` - GET endpoint

3. **API Client Updated**: ✅
   - No more direct backend calls
   - All calls go through Next.js API routes

4. **Test Page Available**: ✅
   - `http://localhost:3000/test-generate`

---

## 🎯 Key Takeaways

1. **localhost ≠ 127.0.0.1**: Browsers treat these as different origins for CORS
2. **Always Use API Routes**: Never make direct backend calls from client components
3. **Test Comprehensively**: Connection tests should cover actual use cases, not just health checks
4. **Follow Documentation**: We had documented the correct pattern but didn't apply it everywhere

---

## 🚀 Next Steps

1. ✅ Test "Generate Design" functionality in the main app
2. ✅ Verify all tests pass on test page
3. ✅ Confirm no CORS errors in browser console
4. 📝 Update any other direct backend calls if found
5. 📝 Add automated tests for API routes

---

**Status**: ✅ FIXED

**Resolution Date**: November 24, 2025

**Verified By**: Test page showing all API route tests passing

