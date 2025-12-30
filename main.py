#!/usr/bin/env python3
"""
Automation Control System - Quick Launcher

This script helps you quickly start the automation server.
For more details, see README.md
"""

import os
import sys
import subprocess


def main():
    print("=" * 60)
    print("Automation Control System")
    print("=" * 60)
    print()

    # Check if we're in the right directory
    if not os.path.exists('server'):
        print("Error: 'server' directory not found!")
        print("Please run this script from the project root directory.")
        sys.exit(1)

    # Check if requirements are installed
    print("Checking dependencies...")
    try:
        import flask
        import flask_cors
        import flask_socketio
        print("✓ Dependencies are installed")
    except ImportError:
        print("✗ Dependencies not installed!")
        print()
        print("Installing dependencies...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "server/requirements.txt"])

    # Check environment
    api_key_required = os.environ.get('API_KEY_REQUIRED', 'true').lower() == 'true'
    api_key = os.environ.get('API_KEY')

    print()
    print("Security Configuration:")
    print(f"  API Key Required: {api_key_required}")
    print(f"  API Key Set: {'Yes' if api_key else 'No'}")

    if api_key_required and not api_key:
        print()
        print("⚠ WARNING: API_KEY_REQUIRED=true but no API_KEY set!")
        print("  Set API_KEY environment variable or use API_KEY_REQUIRED=false for dev")

    print()
    print("Starting server...")
    port = os.environ.get('PORT', '5000')
    host = os.environ.get('HOST', '0.0.0.0')
    print(f"Server will be available at: http://{host}:{port}")
    print()
    print("Configure your Android app to connect to:")
    print(f"  - Emulator: http://10.0.2.2:{port}/")
    print(f"  - Real device: http://YOUR_COMPUTER_IP:{port}/")
    print()
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    print()

    # Change to server directory and run
    os.chdir('server')
    subprocess.run([sys.executable, "app.py"])


if __name__ == "__main__":
    main()