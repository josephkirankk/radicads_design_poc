#!/usr/bin/env python3
"""
Cleanup script for removing old virtual environments and cache files.

This script:
1. Backs up the current .venv directory
2. Removes the .venv directory
3. Clears Python cache files (__pycache__, *.pyc, *.pyo)
"""

import shutil
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


def print_warning(message: str) -> None:
    """Print a warning message."""
    print(f"⚠ {message}")


def print_info(message: str) -> None:
    """Print an info message."""
    print(f"ℹ {message}")


def confirm_action() -> bool:
    """Ask user to confirm the cleanup action."""
    print_warning("This will remove the .venv directory and all Python cache files.")
    response = input("Do you want to continue? (yes/no): ").strip().lower()
    return response in ['yes', 'y']


def backup_venv() -> bool:
    """Backup the .venv directory."""
    venv_path = Path(".venv")
    backup_path = Path(".venv.backup")
    
    if not venv_path.exists():
        print_info("No .venv directory found to backup")
        return True
    
    try:
        # Remove old backup if it exists
        if backup_path.exists():
            print_info("Removing old backup...")
            shutil.rmtree(backup_path)
        
        print_info("Creating backup of .venv...")
        shutil.copytree(venv_path, backup_path)
        print_success(f"Backup created at {backup_path}")
        return True
        
    except Exception as e:
        print_warning(f"Failed to create backup: {e}")
        return False


def remove_venv() -> bool:
    """Remove the .venv directory."""
    venv_path = Path(".venv")
    
    if not venv_path.exists():
        print_info("No .venv directory to remove")
        return True
    
    try:
        print_info("Removing .venv directory...")
        shutil.rmtree(venv_path)
        print_success(".venv directory removed")
        return True
        
    except Exception as e:
        print_warning(f"Failed to remove .venv: {e}")
        return False


def clean_pycache() -> int:
    """Remove all Python cache files and directories."""
    cache_count = 0
    
    print_info("Cleaning Python cache files...")
    
    # Find and remove __pycache__ directories
    for pycache_dir in Path(".").rglob("__pycache__"):
        try:
            shutil.rmtree(pycache_dir)
            cache_count += 1
        except Exception as e:
            print_warning(f"Failed to remove {pycache_dir}: {e}")
    
    # Find and remove .pyc and .pyo files
    for pattern in ["*.pyc", "*.pyo"]:
        for cache_file in Path(".").rglob(pattern):
            try:
                cache_file.unlink()
                cache_count += 1
            except Exception as e:
                print_warning(f"Failed to remove {cache_file}: {e}")
    
    if cache_count > 0:
        print_success(f"Removed {cache_count} cache files/directories")
    else:
        print_info("No cache files found")
    
    return cache_count


def main() -> int:
    """Main cleanup function."""
    print_header("Radic Backend Cleanup")
    
    # Ask for confirmation
    if not confirm_action():
        print_info("Cleanup cancelled")
        return 0
    
    # Backup .venv
    if not backup_venv():
        print_warning("Continuing without backup...")
    
    # Remove .venv
    if not remove_venv():
        print_warning("Failed to remove .venv directory")
        return 1
    
    # Clean Python cache
    clean_pycache()
    
    print_header("Cleanup Complete!")
    print("\nTo recreate the environment, run:")
    print("  python setup.py")
    print("\nOr manually:")
    print("  uv sync")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
