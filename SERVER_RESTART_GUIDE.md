# Server Restart Guide

Complete guide for starting, stopping, and testing the Radic application servers.

---

## 🚀 Quick Start

### Start Both Servers

**Terminal 1 - Backend:**
```bash
cd backend
.venv\Scripts\activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

### Verify Servers are Running

**Backend Health Check:**
```bash
curl http://localhost:8000/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-11-24T11:52:48.231021",
  "service": "radic-backend"
}
```

**Frontend Test Page:**
Open browser: `http://localhost:3000/test-connection`

Click "Run Connection Tests" - all tests should pass ✅

---

## 📋 Pre-Start Checklist

### Backend Requirements

- [ ] Python virtual environment exists: `backend/.venv`
- [ ] Environment file configured: `backend/.env`
- [ ] Required environment variables set:
  - `SUPABASE_URL`
  - `SUPABASE_KEY`
  - `SUPABASE_SERVICE_KEY`
  - `GEMINI_API_KEY`
  - `BACKEND_CORS_ORIGINS`

### Frontend Requirements

- [ ] Node modules installed: `frontend/node_modules`
- [ ] Environment file configured: `frontend/.env.local`
- [ ] Required environment variables set:
  - `NEXT_PUBLIC_API_URL`
  - `NEXT_PUBLIC_SUPABASE_URL`
  - `NEXT_PUBLIC_SUPABASE_ANON_KEY`

---

## 🔧 Configuration Files

### Backend Configuration (`backend/.env`)

```env
# Supabase Configuration
SUPABASE_URL=https://tcyqlulxjqytjxpruemv.supabase.co
SUPABASE_KEY=your-anon-key-here
SUPABASE_SERVICE_KEY=your-service-key-here

# AI Configuration
GEMINI_API_KEY=your-gemini-api-key-here

# CORS Origins (JSON array format)
BACKEND_CORS_ORIGINS=["http://localhost:3000","http://localhost:3001"]

# Environment
ENVIRONMENT=development
API_V1_STR=/api/v1
LOG_LEVEL=INFO
```

### Frontend Configuration (`frontend/.env.local`)

```env
# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1

# Supabase Configuration
NEXT_PUBLIC_SUPABASE_URL=https://tcyqlulxjqytjxpruemv.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key-here

# Polotno Editor API Key
NEXT_PUBLIC_POLOTNO_KEY=your-polotno-api-key-here

# Environment
NEXT_PUBLIC_ENVIRONMENT=development
```

---

## 🛑 Stopping Servers

### Stop Backend
In the backend terminal, press: `Ctrl + C`

### Stop Frontend
In the frontend terminal, press: `Ctrl + C`

### Kill All Processes (if needed)
```bash
# Windows PowerShell
Get-Process | Where-Object {$_.ProcessName -like "*uvicorn*"} | Stop-Process -Force
Get-Process | Where-Object {$_.ProcessName -like "*node*"} | Stop-Process -Force
```

---

## 🔄 Restart Servers

### Restart Backend Only
1. Stop backend: `Ctrl + C`
2. Start backend:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Restart Frontend Only
1. Stop frontend: `Ctrl + C`
2. Start frontend:
```bash
npm run dev
```

### Full Restart (Both Servers)
1. Stop both servers
2. Follow "Quick Start" instructions above

---

## 🧪 Testing Connection

### Method 1: Test Page (Recommended)

1. Open browser: `http://localhost:3000/test-connection`
2. Click "Run Connection Tests"
3. Verify all tests pass:
   - ✅ Backend Health Check
   - ✅ API Root Endpoint
   - ✅ CORS Configuration
   - ✅ Environment Variables

### Method 2: Command Line

**Test Backend:**
```bash
# Health check
curl http://localhost:8000/health

# API root
curl http://localhost:8000/

# API v1 endpoint
curl http://localhost:8000/api/v1/
```

**Test Frontend API Route:**
```bash
curl http://localhost:3000/api/test-backend
```

### Method 3: Browser Console

Open browser console (F12) and run:
```javascript
// Test via Next.js API route (correct way)
fetch('/api/test-backend')
  .then(r => r.json())
  .then(console.log);
```

---

## 🐛 Troubleshooting

### Backend Won't Start

**Error**: `Address already in use`
```bash
# Find process using port 8000
netstat -ano | findstr :8000

# Kill the process (replace PID with actual process ID)
taskkill /PID <PID> /F
```

**Error**: `ModuleNotFoundError`
```bash
# Reinstall dependencies
cd backend
.venv\Scripts\activate
uv pip install -e .
```

### Frontend Won't Start

**Error**: `Port 3000 is already in use`
```bash
# Kill process on port 3000
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

**Error**: `Module not found`
```bash
# Reinstall dependencies
cd frontend
npm install
```

### Connection Test Fails

**Issue**: "Failed to fetch" errors

**Solution**: Ensure you're using Next.js API routes, not direct backend calls.

See: `TROUBLESHOOTING_FRONTEND_BACKEND_CONNECTION.md` for detailed fix.

---

## 📊 Server Status

### Check if Servers are Running

**Backend:**
```bash
curl http://localhost:8000/health
```
- ✅ Returns JSON with status "healthy"
- ❌ Connection refused = backend not running

**Frontend:**
```bash
curl http://localhost:3000
```
- ✅ Returns HTML
- ❌ Connection refused = frontend not running

### View Server Logs

**Backend Logs:**
- Check terminal where uvicorn is running
- Logs show incoming requests and responses

**Frontend Logs:**
- Check terminal where npm dev is running
- Shows compilation status and requests

---

## 🔐 Security Notes

### Development vs Production

**Development** (Current Setup):
- Backend: `http://0.0.0.0:8000`
- Frontend: `http://localhost:3000`
- CORS: Permissive for localhost

**Production** (Future):
- Use HTTPS for both frontend and backend
- Restrict CORS to specific domains
- Use environment-specific configuration
- Enable rate limiting and authentication

---

## 📝 Common Commands

```bash
# Backend
cd backend
.venv\Scripts\activate                                    # Activate virtual env
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 # Start server
uv pip install -e .                                       # Install dependencies
uv pip list                                               # List installed packages

# Frontend
cd frontend
npm run dev                                               # Start dev server
npm run build                                             # Build for production
npm run start                                             # Start production server
npm install                                               # Install dependencies

# Testing
curl http://localhost:8000/health                         # Test backend
curl http://localhost:3000/api/test-backend              # Test frontend API
```

---

## 📚 Related Documentation

- `TROUBLESHOOTING_FRONTEND_BACKEND_CONNECTION.md` - Detailed connection issue fix
- `QUICK_REFERENCE_API_PATTERNS.md` - API communication patterns
- `SETUP_GUIDE.md` - Initial setup instructions
- `backend/SETUP.md` - Backend-specific setup

---

**Last Updated**: November 24, 2025

**Status**: ✅ Both servers running successfully with proper frontend-backend communication

