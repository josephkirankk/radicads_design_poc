---
description: Setup backend environment with UV
---

# Setup Backend Environment

This workflow sets up the Radic backend development environment using UV package manager.

## Prerequisites

Ensure UV is installed:
```powershell
uv --version
```

If not installed, run:
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

## Steps

// turbo-all

1. Navigate to the backend directory:
```powershell
cd c:\JK\dev\repo\radicads\backend
```

2. Run the automated setup script:
```powershell
python setup.py
```

3. Verify the setup by starting the development server:
```powershell
uv run uvicorn app.main:app --reload
```

4. Access the API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Alternative Manual Setup

If you prefer manual setup:

```powershell
cd c:\JK\dev\repo\radicads\backend
uv sync
uv run uvicorn app.main:app --reload
```

## Troubleshooting

If you encounter issues:

1. Clean the environment:
```powershell
python clean_venv.py
```

2. Retry the setup:
```powershell
python setup.py
```

For more details, see `backend/SETUP.md`.
