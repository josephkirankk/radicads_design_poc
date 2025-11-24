"""
Debug API key loading and usage.

This script checks:
1. What API key is being loaded from .env
2. Character-by-character comparison
3. Hidden characters or encoding issues

Usage:
    cd backend
    uv run python misc_tests/test_api_key_debug.py
"""

import os
import sys
from pathlib import Path

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Add parent directory to path to import app modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.config import settings


def main():
    print("=" * 70)
    print("  API KEY DEBUG")
    print("=" * 70)
    
    # Expected key (from curl that works)
    expected_key = "AIzaSyB5aEKujD1ff15qWBLbF7NKMzbeGZKZXSs"
    
    # Actual key from settings
    actual_key = settings.GEMINI_API_KEY
    
    print(f"\nExpected Key: {expected_key}")
    print(f"Actual Key:   {actual_key}")
    print(f"\nExpected Length: {len(expected_key)}")
    print(f"Actual Length:   {len(actual_key)}")
    print(f"\nKeys Match: {expected_key == actual_key}")
    
    # Check for hidden characters
    print("\n" + "=" * 70)
    print("  CHARACTER-BY-CHARACTER COMPARISON")
    print("=" * 70)
    
    if expected_key != actual_key:
        print("\nKeys are DIFFERENT!")
        
        # Find differences
        max_len = max(len(expected_key), len(actual_key))
        for i in range(max_len):
            exp_char = expected_key[i] if i < len(expected_key) else "EOF"
            act_char = actual_key[i] if i < len(actual_key) else "EOF"
            
            if exp_char != act_char:
                print(f"Position {i}: Expected '{exp_char}' (ord={ord(exp_char) if exp_char != 'EOF' else 'N/A'}), "
                      f"Got '{act_char}' (ord={ord(act_char) if act_char != 'EOF' else 'N/A'})")
    else:
        print("\nKeys are IDENTICAL!")
    
    # Check for whitespace
    print("\n" + "=" * 70)
    print("  WHITESPACE CHECK")
    print("=" * 70)
    
    print(f"Expected has leading whitespace: {expected_key != expected_key.lstrip()}")
    print(f"Expected has trailing whitespace: {expected_key != expected_key.rstrip()}")
    print(f"Actual has leading whitespace: {actual_key != actual_key.lstrip()}")
    print(f"Actual has trailing whitespace: {actual_key != actual_key.rstrip()}")
    
    # Show repr
    print("\n" + "=" * 70)
    print("  REPR (shows hidden characters)")
    print("=" * 70)
    print(f"Expected: {repr(expected_key)}")
    print(f"Actual:   {repr(actual_key)}")
    
    # Check bytes
    print("\n" + "=" * 70)
    print("  BYTE COMPARISON")
    print("=" * 70)
    print(f"Expected bytes: {expected_key.encode('utf-8')}")
    print(f"Actual bytes:   {actual_key.encode('utf-8')}")
    
    # Try stripped version
    stripped_key = actual_key.strip()
    print("\n" + "=" * 70)
    print("  STRIPPED VERSION")
    print("=" * 70)
    print(f"Stripped Key: {stripped_key}")
    print(f"Stripped Length: {len(stripped_key)}")
    print(f"Stripped matches expected: {stripped_key == expected_key}")


if __name__ == "__main__":
    main()

