#!/usr/bin/env python3
"""
Setup script for Radic Backend using UV package manager.

This script automates the environment setup process:
1. Checks if uv is installed
2. Creates/updates the virtual environment
3. Installs all dependencies including dev dependencies
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path


def print_header(message: str) -> None:
    """Print a formatted header message."""
    print(f"\n{'='*60}")
    print(f"  {message}")
    print(f"{'='*60}\n")


def print_success(message: str) -> None:
    """Print a success message."""
    print(f"✓ {message}")


def print_error(message: str) -> None:
    """Print an error message."""
    print(f"✗ {message}", file=sys.stderr)


def print_info(message: str) -> None:
    """Print an info message."""
    print(f"ℹ {message}")


def check_uv_installed() -> bool:
    """Check if uv is installed on the system."""
    try:
        result = subprocess.run(
            ["uv", "--version"],
            capture_output=True,
            text=True,
            check=False
        )
        if result.returncode == 0:
            print_success(f"UV is installed: {result.stdout.strip()}")
            return True
        return False
    except FileNotFoundError:
        return False


def install_uv_instructions() -> None:
    """Print instructions for installing uv."""
    print_error("UV is not installed!")
    print_info("\nTo install UV, run one of the following commands:\n")
    print("  Windows (PowerShell):")
    print("    powershell -ExecutionPolicy ByPass -c \"irm https://astral.sh/uv/install.ps1 | iex\"")
    print("\n  macOS/Linux:")
    print("    curl -LsSf https://astral.sh/uv/install.sh | sh")
    print("\n  Using pip:")
    print("    pip install uv")
    print("\nFor more information, visit: https://docs.astral.sh/uv/getting-started/installation/")


def backup_old_venv() -> None:
    """Backup the old .venv directory if it exists."""
    venv_path = Path(".venv")
    backup_path = Path(".venv.backup")
    
    if venv_path.exists():
        print_info("Found existing .venv directory")
        
        # Remove old backup if it exists
        if backup_path.exists():
            print_info("Removing old backup...")
            shutil.rmtree(backup_path)
        
        print_info("Creating backup of current .venv...")
        shutil.move(str(venv_path), str(backup_path))
        print_success("Backup created at .venv.backup")


def setup_environment() -> bool:
    """Set up the virtual environment using uv."""
    try:
        print_info("Setting up virtual environment with uv...")
        
        # Run uv sync to create venv and install all dependencies
        result = subprocess.run(
            ["uv", "sync", "--all-extras"],
            check=False,
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            print_error(f"Failed to sync environment:\n{result.stderr}")
            return False
        
        print_success("Virtual environment created and dependencies installed")
        return True
        
    except Exception as e:
        print_error(f"Error during setup: {e}")
        return False


def verify_installation() -> bool:
    """Verify that key packages are installed correctly."""
    try:
        print_info("Verifying installation...")
        
        # Check if we can import key packages
        result = subprocess.run(
            ["uv", "run", "python", "-c", 
             "import fastapi, uvicorn, supabase, loguru; print('All core packages imported successfully')"],
            check=False,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print_success("All core packages verified")
            return True
        else:
            print_error(f"Package verification failed:\n{result.stderr}")
            return False
            
    except Exception as e:
        print_error(f"Error during verification: {e}")
        return False


def print_next_steps() -> None:
    """Print next steps for the user."""
    print_header("Setup Complete!")
    print("Next steps:\n")
    print("  1. Start the development server:")
    print("     uv run uvicorn app.main:app --reload\n")
    print("  2. Run tests:")
    print("     uv run pytest\n")
    print("  3. Format code:")
    print("     uv run black .\n")
    print("  4. Lint code:")
    print("     uv run ruff check .\n")
    print("\nFor more commands, see SETUP.md")


def main() -> int:
    """Main setup function."""
    print_header("Radic Backend Setup with UV")
    
    # Change to script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    print_info(f"Working directory: {script_dir}")
    
    # Check if uv is installed
    if not check_uv_installed():
        install_uv_instructions()
        return 1
    
    # Backup old venv
    backup_old_venv()
    
    # Setup environment
    if not setup_environment():
        print_error("Setup failed! Check the error messages above.")
        return 1
    
    # Verify installation
    if not verify_installation():
        print_error("Verification failed! Some packages may not be installed correctly.")
        return 1
    
    # Print next steps
    print_next_steps()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
