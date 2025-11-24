# Radic - Quick Start: Critical Fixes

**⚠️ IMPORTANT:** The application is currently **NOT FUNCTIONAL**. Follow these steps to make it work.

---

## 🚨 Critical Issues Fixed (Already Done)

✅ Fixed missing `APIRouter` import in `backend/app/api/v1/api.py`  
✅ Removed duplicate "use client" in `frontend/src/app/create/page.tsx`  
✅ Fixed hardcoded Polotno API key in `frontend/src/components/editor/Editor.tsx`  
✅ Created `.env.example` files for both backend and frontend

---

## 🔧 Setup Instructions (Do This Now)

### 1. Install Missing Dependencies

**Frontend:**
```bash
cd frontend
npm install polotno
```

**Backend:**
```bash
cd backend
poetry add google-generativeai loguru redis
```

### 2. Configure Environment Variables

**Backend (`backend/.env`):**
```bash
# Copy the example file
cp .env.example .env

# Edit .env and fill in:
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
SUPABASE_SERVICE_KEY=your-service-key
GEMINI_API_KEY=your-gemini-key
BACKEND_CORS_ORIGINS=http://localhost:3000
```

**Frontend (`frontend/.env.local`):**
```bash
# Create .env.local from example
cp .env.example .env.local

# Edit .env.local and fill in:
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
NEXT_PUBLIC_POLOTNO_KEY=your-polotno-key
```

### 3. Create Database Schema

**Option A: Using Supabase Dashboard**
1. Go to https://app.supabase.com
2. Select your project
3. Go to SQL Editor
4. Copy the SQL from `CODE_REVIEW_REPORT.md` (CRITICAL-005 section)
5. Run the migration

**Option B: Using Supabase CLI**
```bash
# Install Supabase CLI
npm install -g supabase

# Initialize Supabase
supabase init

# Create migration file
supabase migration new initial_schema

# Copy SQL from CODE_REVIEW_REPORT.md to the migration file
# Then apply:
supabase db push
```

### 4. Start the Application

**Terminal 1 - Backend:**
```bash
cd backend
poetry run uvicorn app.main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

**Access:** http://localhost:3000

---

## 🔴 Known Issues (Still Broken)

### 1. Authentication Not Working
**Problem:** No authentication middleware, all endpoints are public  
**Impact:** Anyone can access/modify any data  
**Fix Required:** See `CODE_REVIEW_REPORT.md` CRITICAL-002

### 2. AI Generation Returns Mock Data
**Problem:** AI services return placeholder data, not real designs  
**Impact:** Core feature doesn't work  
**Fix Required:** See `CODE_REVIEW_REPORT.md` MAJOR-003

### 3. No Error Handling
**Problem:** Any error will crash the app  
**Impact:** Poor user experience, hard to debug  
**Fix Required:** See `CODE_REVIEW_REPORT.md` MAJOR-004

---

## 📚 Where to Get API Keys

### Supabase
1. Go to https://app.supabase.com
2. Create a new project (or use existing)
3. Go to Settings → API
4. Copy `URL`, `anon/public key`, and `service_role key`

### Gemini API
1. Go to https://makersuite.google.com/app/apikey
2. Create a new API key
3. Copy the key

### Polotno
1. Go to https://polotno.com/
2. Sign up for an account
3. Get API key from dashboard
4. Free tier available for development

---

## 🎯 Next Steps After Setup

1. **Test the application:**
   - Try creating a design (will return mock data)
   - Try opening the editor (should load Polotno)
   - Check browser console for errors

2. **Implement authentication:**
   - Follow instructions in `CODE_REVIEW_REPORT.md` CRITICAL-002
   - Create `backend/app/core/auth.py`
   - Apply to all endpoints

3. **Implement AI integration:**
   - Follow instructions in `CODE_REVIEW_REPORT.md` MAJOR-003
   - Update `backend/app/services/ai_layout.py`
   - Update `backend/app/services/ai_image.py`

4. **Add error handling:**
   - Follow instructions in `CODE_REVIEW_REPORT.md` MAJOR-004
   - Create logging infrastructure
   - Add try-catch blocks

---

## 📖 Full Documentation

- **CODE_REVIEW_REPORT.md** - Comprehensive review with all issues (1,330 lines)
- **IMPLEMENTATION_SUMMARY.md** - Summary of completed work and next steps
- **prd_design/radic_app_spec.md** - Product specifications
- **prd_design/radic_nano_banana_pro_spec.md** - AI image generation specs

---

## 🆘 Troubleshooting

**Backend won't start:**
- Check `.env` file exists and has all required variables
- Check `poetry install` completed successfully
- Check Python version (3.10+)

**Frontend won't start:**
- Check `npm install` completed successfully
- Check Node version (18+)
- Check `.env.local` file exists

**Editor shows "Invalid API key":**
- Check `NEXT_PUBLIC_POLOTNO_KEY` in `.env.local`
- Get a valid key from https://polotno.com/

**Database queries fail:**
- Check database schema was created (Step 3 above)
- Check Supabase credentials in `.env`
- Check RLS policies are enabled

---

**Last Updated:** 2025-11-24  
**Project:** Radic (formerly DesignLumo)  
**Status:** Pre-Alpha (22% Complete)

