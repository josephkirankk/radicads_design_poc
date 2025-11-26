# Radic Pro — Setup Guide

> **Version**: 1.0  
> **Last Updated**: November 2025  
> **Platforms**: macOS, Windows, Linux

---

## 1. Prerequisites

### 1.1 Required Software

| Tool | Version | Purpose | Installation |
|------|---------|---------|--------------|
| **Node.js** | 20.x LTS | Frontend runtime | [nodejs.org](https://nodejs.org) |
| **pnpm** | 8.x+ | Frontend package manager | `npm install -g pnpm` |
| **Python** | 3.12+ | Backend runtime | [python.org](https://python.org) |
| **uv** | 0.4+ | Python package manager | See below |
| **Git** | 2.x+ | Version control | [git-scm.com](https://git-scm.com) |

### 1.2 Install uv (Python Package Manager)

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Verify installation:**
```bash
uv --version
```

### 1.3 Recommended IDE

- **VS Code** with extensions:
  - Python
  - Pylance
  - ES7+ React/Redux/React-Native snippets
  - Tailwind CSS IntelliSense
  - Prettier
  - ESLint

---

## 2. Project Structure

```
radicads/
├── frontend/                    # Next.js 14 application
│   ├── src/
│   │   ├── app/                 # App Router pages
│   │   ├── components/          # React components
│   │   │   ├── ui/              # Shadcn UI components
│   │   │   ├── editor/          # Editor components
│   │   │   └── shared/          # Shared components
│   │   ├── lib/                 # Utilities
│   │   ├── hooks/               # Custom hooks
│   │   ├── stores/              # Zustand stores
│   │   └── types/               # TypeScript types
│   ├── public/                  # Static assets
│   ├── package.json
│   ├── tailwind.config.ts
│   ├── next.config.js
│   └── tsconfig.json
│
├── backend/                     # FastAPI application
│   ├── app/
│   │   ├── api/                 # API routes
│   │   │   ├── auth.py
│   │   │   ├── designs.py
│   │   │   ├── brands.py
│   │   │   ├── ai.py
│   │   │   └── assets.py
│   │   ├── services/            # Business logic
│   │   ├── models/              # Pydantic models
│   │   ├── ai/                  # AI providers
│   │   │   ├── providers/
│   │   │   └── prompts/
│   │   ├── db/                  # Database client
│   │   ├── core/                # Config, exceptions
│   │   └── main.py              # FastAPI app entry
│   ├── tests/                   # Test files
│   ├── pyproject.toml           # uv project config
│   └── uv.lock                  # Dependency lock
│
├── scripts/                     # Dev scripts
│   ├── restart-backend.sh       # macOS/Linux
│   ├── restart-backend.ps1      # Windows
│   ├── restart-frontend.sh      # macOS/Linux
│   └── restart-frontend.ps1     # Windows
│
├── .env.example                 # Environment template
└── README.md
```

---

## 3. Backend Setup (FastAPI + uv)

### 3.1 Initialize Backend

```bash
# Navigate to project root
cd radicads

# Create backend directory
mkdir -p backend
cd backend

# Initialize uv project
uv init --name radic-backend

# Set Python version
uv python pin 3.12
```

### 3.2 Install Dependencies

```bash
# Add core dependencies
uv add fastapi uvicorn[standard] pydantic pydantic-settings httpx

# Add Supabase and async support
uv add supabase python-jose[cryptography] passlib[bcrypt]

# Add AI providers
uv add replicate openai google-generativeai

# Add development dependencies
uv add --dev pytest pytest-asyncio httpx ruff mypy
```

### 3.3 Create Virtual Environment

```bash
# Create and sync virtual environment
uv sync

# Verify virtual environment
uv run python --version
```

**pyproject.toml example:**
```toml
[project]
name = "radic-backend"
version = "0.1.0"
description = "Radic Pro Backend API"
requires-python = ">=3.12"
dependencies = [
    "fastapi>=0.115.0",
    "uvicorn[standard]>=0.30.0",
    "pydantic>=2.9.0",
    "pydantic-settings>=2.5.0",
    "httpx>=0.27.0",
    "supabase>=2.9.0",
    "python-jose[cryptography]>=3.3.0",
    "replicate>=0.32.0",
]

[tool.uv]
dev-dependencies = [
    "pytest>=8.3.0",
    "pytest-asyncio>=0.24.0",
    "ruff>=0.6.0",
    "mypy>=1.11.0",
]
```

### 3.4 Run Backend Server

```bash
# Development mode with auto-reload
uv run fastapi dev app/main.py --port 8000

# OR using uvicorn directly
uv run uvicorn app.main:app --reload --port 8000
```

### 3.5 Backend main.py Template

```python
# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import get_settings
from app.api import auth, designs, brands, ai, assets

settings = get_settings()

app = FastAPI(
    title="Radic Pro API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(designs.router, prefix="/designs", tags=["designs"])
app.include_router(brands.router, prefix="/brands", tags=["brands"])
app.include_router(ai.router, prefix="/ai", tags=["ai"])
app.include_router(assets.router, prefix="/assets", tags=["assets"])

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}
```

---

## 4. Frontend Setup (Next.js 14)

### 4.1 Create Next.js Project

```bash
# From project root
cd radicads

# Create Next.js app with all recommended settings
pnpm create next-app@latest frontend --typescript --tailwind --eslint --app --src-dir --import-alias "@/*" --yes

cd frontend
```

### 4.2 Install Additional Dependencies

```bash
# UI Components
pnpm add @radix-ui/react-dialog @radix-ui/react-dropdown-menu @radix-ui/react-slot
pnpm add class-variance-authority clsx tailwind-merge lucide-react

# State Management
pnpm add zustand @tanstack/react-query

# Forms & Validation
pnpm add react-hook-form @hookform/resolvers zod

# Supabase
pnpm add @supabase/supabase-js @supabase/ssr

# Canvas Editor
pnpm add fabric

# Development
pnpm add -D @types/fabric prettier prettier-plugin-tailwindcss
```

### 4.3 Initialize Shadcn UI

```bash
# Initialize shadcn/ui
pnpm dlx shadcn@latest init

# Add commonly used components
pnpm dlx shadcn@latest add button input card dialog dropdown-menu toast
pnpm dlx shadcn@latest add form label select textarea tabs avatar badge
```

### 4.4 Run Frontend Server

```bash
# Development mode with Turbopack
pnpm dev

# OR with specific port
pnpm dev --port 3000
```

---

## 5. Environment Configuration

### 5.1 Create Environment Files

**Backend (.env):**
```bash
# backend/.env
# ===================
# Supabase
# ===================
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
SUPABASE_SERVICE_KEY=your-service-key

# ===================
# AI Providers (Replicate)
# ===================
REPLICATE_API_TOKEN=r8_your_token_here

# ===================
# Model Configuration
# ===================
LAYOUT_MODEL=gemini-3-pro
IMAGE_MODEL=nano-banana-pro
FALLBACK_IMAGE_MODEL=flux-1.1-pro

# ===================
# App Settings
# ===================
ENVIRONMENT=development
DEBUG=true
CORS_ORIGINS=["http://localhost:3000"]
```

**Frontend (.env.local):**
```bash
# frontend/.env.local
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## 6. Restart Scripts

These scripts kill any existing process on the port and restart the server in the background.

### 6.1 Backend Restart Scripts

**macOS/Linux (scripts/restart-backend.sh):**
```bash
#!/bin/bash
# Restart Backend Server
# Usage: ./scripts/restart-backend.sh

PORT=8000
BACKEND_DIR="backend"

echo "🔄 Restarting backend server on port $PORT..."

# Kill existing process on port
PID=$(lsof -ti:$PORT)
if [ -n "$PID" ]; then
    echo "⏹️  Killing existing process (PID: $PID)"
    kill -9 $PID 2>/dev/null
    sleep 1
fi

# Navigate to backend directory
cd "$(dirname "$0")/../$BACKEND_DIR" || exit 1

# Activate virtual environment and start server in background
echo "🚀 Starting backend server..."
nohup uv run uvicorn app.main:app --reload --port $PORT > ../logs/backend.log 2>&1 &

# Get new PID
sleep 2
NEW_PID=$(lsof -ti:$PORT)
echo "✅ Backend started (PID: $NEW_PID)"
echo "📝 Logs: tail -f logs/backend.log"
```

**Windows (scripts/restart-backend.ps1):**
```powershell
# Restart Backend Server
# Usage: .\scripts\restart-backend.ps1

$PORT = 8000
$BACKEND_DIR = "backend"

Write-Host "🔄 Restarting backend server on port $PORT..." -ForegroundColor Cyan

# Kill existing process on port
$process = Get-NetTCPConnection -LocalPort $PORT -ErrorAction SilentlyContinue | 
           Select-Object -ExpandProperty OwningProcess -Unique

if ($process) {
    Write-Host "⏹️  Killing existing process (PID: $process)" -ForegroundColor Yellow
    Stop-Process -Id $process -Force -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 1
}

# Navigate to backend directory
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location "$scriptDir\..\$BACKEND_DIR"

# Create logs directory if not exists
$logsDir = "..\logs"
if (-not (Test-Path $logsDir)) {
    New-Item -ItemType Directory -Path $logsDir | Out-Null
}

# Start server in background
Write-Host "🚀 Starting backend server..." -ForegroundColor Green
$job = Start-Job -ScriptBlock {
    Set-Location $using:PWD
    uv run uvicorn app.main:app --reload --port $using:PORT
} 

Start-Sleep -Seconds 3
$newProcess = Get-NetTCPConnection -LocalPort $PORT -ErrorAction SilentlyContinue | 
              Select-Object -ExpandProperty OwningProcess -Unique

Write-Host "✅ Backend started (PID: $newProcess)" -ForegroundColor Green
Write-Host "📝 Job ID: $($job.Id) - Use 'Receive-Job $($job.Id)' for logs" -ForegroundColor Gray
```

### 6.2 Frontend Restart Scripts

**macOS/Linux (scripts/restart-frontend.sh):**
```bash
#!/bin/bash
# Restart Frontend Server
# Usage: ./scripts/restart-frontend.sh

PORT=3000
FRONTEND_DIR="frontend"

echo "🔄 Restarting frontend server on port $PORT..."

# Kill existing process on port
PID=$(lsof -ti:$PORT)
if [ -n "$PID" ]; then
    echo "⏹️  Killing existing process (PID: $PID)"
    kill -9 $PID 2>/dev/null
    sleep 1
fi

# Navigate to frontend directory
cd "$(dirname "$0")/../$FRONTEND_DIR" || exit 1

# Start server in background
echo "🚀 Starting frontend server..."
nohup pnpm dev --port $PORT > ../logs/frontend.log 2>&1 &

# Get new PID
sleep 3
NEW_PID=$(lsof -ti:$PORT)
echo "✅ Frontend started (PID: $NEW_PID)"
echo "📝 Logs: tail -f logs/frontend.log"
echo "🌐 Open: http://localhost:$PORT"
```

**Windows (scripts/restart-frontend.ps1):**
```powershell
# Restart Frontend Server
# Usage: .\scripts\restart-frontend.ps1

$PORT = 3000
$FRONTEND_DIR = "frontend"

Write-Host "🔄 Restarting frontend server on port $PORT..." -ForegroundColor Cyan

# Kill existing process on port
$process = Get-NetTCPConnection -LocalPort $PORT -ErrorAction SilentlyContinue | 
           Select-Object -ExpandProperty OwningProcess -Unique

if ($process) {
    Write-Host "⏹️  Killing existing process (PID: $process)" -ForegroundColor Yellow
    Stop-Process -Id $process -Force -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 1
}

# Navigate to frontend directory
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location "$scriptDir\..\$FRONTEND_DIR"

# Create logs directory if not exists
$logsDir = "..\logs"
if (-not (Test-Path $logsDir)) {
    New-Item -ItemType Directory -Path $logsDir | Out-Null
}

# Start server in background
Write-Host "🚀 Starting frontend server..." -ForegroundColor Green
$job = Start-Job -ScriptBlock {
    Set-Location $using:PWD
    pnpm dev --port $using:PORT
}

Start-Sleep -Seconds 4
$newProcess = Get-NetTCPConnection -LocalPort $PORT -ErrorAction SilentlyContinue | 
              Select-Object -ExpandProperty OwningProcess -Unique

Write-Host "✅ Frontend started (PID: $newProcess)" -ForegroundColor Green
Write-Host "🌐 Open: http://localhost:$PORT" -ForegroundColor Cyan
Write-Host "📝 Job ID: $($job.Id) - Use 'Receive-Job $($job.Id)' for logs" -ForegroundColor Gray
```

### 6.3 Make Scripts Executable (macOS/Linux)

```bash
chmod +x scripts/restart-backend.sh
chmod +x scripts/restart-frontend.sh

# Create logs directory
mkdir -p logs
```

---

## 7. Quick Start Commands

### 7.1 First-Time Setup

```bash
# Clone repository
git clone https://github.com/your-org/radicads.git
cd radicads

# Backend setup
cd backend
uv sync
cp .env.example .env  # Edit with your credentials
cd ..

# Frontend setup
cd frontend
pnpm install
cp .env.example .env.local  # Edit with your credentials
cd ..

# Create logs directory
mkdir -p logs
```

### 7.2 Daily Development

**macOS/Linux:**
```bash
# Terminal 1: Backend
cd backend && uv run fastapi dev app/main.py --port 8000

# Terminal 2: Frontend
cd frontend && pnpm dev
```

**Windows (PowerShell):**
```powershell
# Terminal 1: Backend
cd backend; uv run fastapi dev app/main.py --port 8000

# Terminal 2: Frontend
cd frontend; pnpm dev
```

### 7.3 Using Restart Scripts

**macOS/Linux:**
```bash
./scripts/restart-backend.sh
./scripts/restart-frontend.sh
```

**Windows:**
```powershell
.\scripts\restart-backend.ps1
.\scripts\restart-frontend.ps1
```

---

## 8. Common Commands Reference

### Backend Commands

| Command | Description |
|---------|-------------|
| `uv sync` | Install/sync dependencies |
| `uv add <package>` | Add a dependency |
| `uv add --dev <package>` | Add a dev dependency |
| `uv run fastapi dev app/main.py` | Start dev server with reload |
| `uv run pytest` | Run tests |
| `uv run ruff check .` | Lint code |
| `uv run ruff format .` | Format code |
| `uv run mypy app/` | Type check |

### Frontend Commands

| Command | Description |
|---------|-------------|
| `pnpm install` | Install dependencies |
| `pnpm add <package>` | Add a dependency |
| `pnpm dev` | Start dev server (Turbopack) |
| `pnpm build` | Production build |
| `pnpm start` | Start production server |
| `pnpm lint` | Run ESLint |
| `pnpm test` | Run tests |

---

## 9. Troubleshooting

### 9.1 Port Already in Use

**macOS/Linux:**
```bash
# Find process on port
lsof -i :8000
lsof -i :3000

# Kill process
kill -9 <PID>
```

**Windows:**
```powershell
# Find process on port
netstat -ano | findstr :8000
netstat -ano | findstr :3000

# Kill process
taskkill /PID <PID> /F
```

### 9.2 uv Not Found

```bash
# Re-install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Reload shell
source ~/.bashrc  # or ~/.zshrc
```

### 9.3 Virtual Environment Issues

```bash
# Remove and recreate
cd backend
rm -rf .venv
uv sync
```

### 9.4 Node Modules Issues

```bash
cd frontend
rm -rf node_modules
rm pnpm-lock.yaml
pnpm install
```

---

## 10. Deployment Checklist

### Pre-deployment
- [ ] All tests passing
- [ ] Environment variables configured
- [ ] Database migrations applied
- [ ] Supabase RLS policies verified
- [ ] API keys secured (not in code)

### Production Commands

**Backend (Railway/Render):**
```bash
uv run fastapi run app/main.py --port $PORT
```

**Frontend (Vercel):**
```bash
pnpm build
pnpm start
```

---

## Next Steps

1. Complete Supabase project setup
2. Configure AI provider API keys (Replicate)
3. Run both servers and verify `/health` endpoint
4. Start building features from the roadmap
