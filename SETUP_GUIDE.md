# Radic - Complete Setup Guide

This guide will help you set up and run the Radic application from scratch.

---

## Prerequisites

- **Python 3.11+** installed
- **Node.js 18+** and npm installed
- **uv** package manager for Python ([Install uv](https://github.com/astral-sh/uv))
- **Supabase account** ([Sign up](https://supabase.com))
- **Google Gemini API key** ([Get API key](https://makersuite.google.com/app/apikey))
- **Polotno API key** ([Get API key](https://polotno.com))

---

## Step 1: Clone and Navigate

```bash
cd c:\JK\dev\repo\radicads
```

---

## Step 2: Backend Setup

### 2.1 Create Virtual Environment with uv

```bash
cd backend
uv venv .venv
```

### 2.2 Activate Virtual Environment

**Windows PowerShell:**
```powershell
.venv\Scripts\activate
```

**Windows CMD:**
```cmd
.venv\Scripts\activate.bat
```

### 2.3 Install Dependencies

```bash
uv pip install fastapi uvicorn supabase loguru google-generativeai python-multipart pydantic pydantic-settings
```

### 2.4 Configure Environment Variables

```bash
# Copy the example file
copy .env.example .env

# Edit .env and fill in your values:
```

**Required values in `.env`:**
```env
# Supabase Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
SUPABASE_SERVICE_KEY=your-service-role-key

# AI Configuration
GEMINI_API_KEY=your-gemini-api-key

# Backend Configuration
BACKEND_CORS_ORIGINS=["http://localhost:3000"]
ENVIRONMENT=development
API_V1_STR=/api/v1
LOG_LEVEL=INFO
```

---

## Step 3: Frontend Setup

### 3.1 Navigate to Frontend

```bash
cd ..\frontend
```

### 3.2 Install Dependencies

```bash
npm install
npm install polotno --legacy-peer-deps
```

### 3.3 Configure Environment Variables

```bash
# Copy the example file
copy .env.example .env.local

# Edit .env.local and fill in your values:
```

**Required values in `.env.local`:**
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
NEXT_PUBLIC_POLOTNO_KEY=your-polotno-api-key
NEXT_PUBLIC_ENVIRONMENT=development
```

---

## Step 4: Database Setup

### 4.1 Apply Database Migration

**Option A: Using Supabase Dashboard (Recommended)**

1. Go to https://app.supabase.com
2. Select your project
3. Navigate to **SQL Editor**
4. Open `supabase/migrations/001_initial_schema.sql`
5. Copy the entire contents
6. Paste into the SQL editor
7. Click **Run** to execute

**Option B: Using Supabase CLI**

```bash
# Install Supabase CLI
npm install -g supabase

# Login
supabase login

# Link to your project
supabase link --project-ref your-project-ref

# Apply migrations
supabase db push
```

### 4.2 Verify Migration

Run this query in Supabase SQL Editor:

```sql
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
ORDER BY table_name;
```

You should see 6 tables:
- assets
- brands
- campaign_designs
- campaigns
- designs
- smart_image_recipes

---

## Step 5: Run the Application

### 5.1 Start Backend (Terminal 1)

```bash
cd backend
.venv\Scripts\activate
uvicorn app.main:app --reload --port 8000
```

**Expected output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

### 5.2 Start Frontend (Terminal 2)

```bash
cd frontend
npm run dev
```

**Expected output:**
```
  ▲ Next.js 16.0.3
  - Local:        http://localhost:3000
```

### 5.3 Access the Application

Open your browser and navigate to:
- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

---

## Step 6: Test the Setup

### 6.1 Test Backend Health

```bash
curl http://localhost:8000/health
```

**Expected response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-11-24T...",
  "service": "radic-backend"
}
```

### 6.2 Test Authentication

**Signup:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/signup \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"test@example.com\",\"password\":\"password123\"}"
```

**Login:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"test@example.com\",\"password\":\"password123\"}"
```

Save the `access_token` from the response.

### 6.3 Test Protected Endpoint

```bash
curl http://localhost:8000/api/v1/designs \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## Troubleshooting

### Backend won't start

**Error:** `ModuleNotFoundError: No module named 'fastapi'`
- **Solution:** Make sure you activated the virtual environment: `.venv\Scripts\activate`

**Error:** `SUPABASE_URL environment variable not set`
- **Solution:** Create `.env` file in backend directory with all required variables

### Frontend won't start

**Error:** `Module not found: Can't resolve 'polotno'`
- **Solution:** Install polotno: `npm install polotno --legacy-peer-deps`

**Error:** `NEXT_PUBLIC_API_URL is not defined`
- **Solution:** Create `.env.local` file in frontend directory

### Database errors

**Error:** `relation "designs" does not exist`
- **Solution:** Apply the database migration (Step 4)

**Error:** `JWT expired` or `Invalid token`
- **Solution:** Login again to get a fresh token

### CORS errors

**Error:** `Access-Control-Allow-Origin`
- **Solution:** Make sure `BACKEND_CORS_ORIGINS` in backend `.env` includes `http://localhost:3000`

---

## Next Steps

Now that everything is set up:

1. **Create a brand kit** - Go to the app and create your first brand
2. **Generate a design** - Use the AI to generate a design from a prompt
3. **Edit in the editor** - Use the Polotno editor to customize your design
4. **Review the code** - Check out `CODE_REVIEW_REPORT.md` for architecture details

---

## Important Notes

- **Always use `.venv`** - Remember to activate the virtual environment before running Python commands
- **Use uv for packages** - Always use `uv pip install` instead of `pip install`
- **Check logs** - Backend logs are in `backend/logs/radic.log` and `backend/logs/error.log`
- **API Documentation** - Interactive API docs available at http://localhost:8000/docs

---

## Quick Reference

**Start Backend:**
```bash
cd backend && .venv\Scripts\activate && uvicorn app.main:app --reload --port 8000
```

**Start Frontend:**
```bash
cd frontend && npm run dev
```

**Install Backend Package:**
```bash
cd backend && .venv\Scripts\activate && uv pip install package-name
```

**Install Frontend Package:**
```bash
cd frontend && npm install package-name
```

---

**🎉 You're all set! Happy coding!**

