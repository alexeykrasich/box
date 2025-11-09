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

    print()
    print("Starting server...")
    print("Server will be available at: http://0.0.0.0:5000")
    print()
    print("Configure your Android app to connect to:")
    print("  - Emulator: http://10.0.2.2:5000/")
    print("  - Real device: http://YOUR_COMPUTER_IP:5000/")
    print()
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    print()

    # Change to server directory and run
    os.chdir('server')
    subprocess.run([sys.executable, "app.py"])

if __name__ == "__main__":
    main()