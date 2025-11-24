# Radic Backend Setup Guide

This guide covers setting up the Radic backend development environment using **UV**, a fast Rust-based Python package manager.

## Prerequisites

- **Python 3.11+** installed on your system
- **UV package manager** (installation instructions below)

## Installing UV

UV is required for managing the Python environment and dependencies.

### Windows (PowerShell)
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### macOS/Linux
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Using pip
```bash
pip install uv
```

For more installation options, see the [official UV documentation](https://docs.astral.sh/uv/getting-started/installation/).

## Quick Setup

Run the automated setup script:

```bash
cd backend
python setup.py
```

This script will:
1. Check if UV is installed
2. Backup any existing `.venv` directory
3. Create a new virtual environment
4. Install all dependencies (including dev dependencies)
5. Verify the installation

## Manual Setup

If you prefer to set up manually:

```bash
cd backend

# Create virtual environment and install dependencies
uv sync

# The environment will be created at .venv/
```

## Common Commands

### Running the Development Server

```bash
# Start the FastAPI development server with auto-reload
uv run uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`
- API Documentation: `http://localhost:8000/docs`
- Alternative docs: `http://localhost:8000/redoc`

### Managing Dependencies

```bash
# Add a new production dependency
uv add <package-name>

# Add a development-only dependency
uv add --dev <package-name>

# Remove a dependency
uv remove <package-name>

# Update all dependencies
uv sync

# Update a specific dependency
uv add <package-name>@latest
```

### Development Tools

```bash
# Run tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=app

# Format code with Black
uv run black .

# Check code with Black (no changes)
uv run black --check .

# Lint code with Ruff
uv run ruff check .

# Auto-fix linting issues
uv run ruff check --fix .

# Type checking with MyPy
uv run mypy app/
```

### Python Version Management

UV can manage Python installations:

```bash
# Install a specific Python version
uv python install 3.11

# List available Python versions
uv python list

# Use a specific Python version for the project
uv python pin 3.11
```

## Environment Variables

Create a `.env` file in the backend directory based on `.env.example`:

```bash
cp .env.example .env
```

Edit `.env` with your configuration values.

## Project Structure

```
backend/
├── app/
│   ├── api/           # API endpoints
│   ├── core/          # Core configuration
│   ├── db/            # Database setup
│   ├── schemas/       # Pydantic models
│   ├── services/      # Business logic
│   └── main.py        # Application entry point
├── tests/             # Test files
├── .env               # Environment variables (not in git)
├── .env.example       # Example environment file
├── .gitignore         # Git ignore patterns
├── pyproject.toml     # Project configuration & dependencies
├── uv.lock            # Locked dependency versions
├── setup.py           # Automated setup script
└── clean_venv.py      # Environment cleanup script
```

## Cleaning the Environment

If you need to reset your environment:

```bash
# Run the cleanup script
python clean_venv.py

# Then recreate the environment
python setup.py
```

Or manually:

```bash
# Remove the virtual environment
rm -rf .venv

# Recreate it
uv sync
```

## Troubleshooting

### UV command not found

After installing UV, you may need to restart your terminal or add UV to your PATH:

**Windows**: UV is installed to `%USERPROFILE%\.cargo\bin`
**macOS/Linux**: UV is installed to `~/.cargo/bin`

### Dependencies not resolving

Try clearing the UV cache:

```bash
uv cache clean
uv sync
```

### Import errors

Make sure you're running commands with `uv run` prefix:

```bash
# Wrong
python -m uvicorn app.main:app

# Correct
uv run uvicorn app.main:app
```

### Old .venv conflicts

If you're experiencing issues with an old environment:

```bash
python clean_venv.py
python setup.py
```

## Performance

UV is significantly faster than traditional pip:
- **10-100x faster** dependency resolution
- **Instant** virtual environment creation
- **Parallel** package downloads

## Additional Resources

- [UV Documentation](https://docs.astral.sh/uv/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Supabase Python Documentation](https://supabase.com/docs/reference/python/introduction)

## Need Help?

If you encounter issues not covered in this guide:
1. Check the UV documentation
2. Review the error message carefully
3. Ensure all prerequisites are installed
4. Try cleaning and recreating the environment
