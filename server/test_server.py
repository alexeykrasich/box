#!/usr/bin/env python3
"""
Test script to verify server components and security features.
Run this before starting the server to check for issues.
"""

import sys
import os

# Set test environment variables
os.environ.setdefault('API_KEY_REQUIRED', 'false')
os.environ.setdefault('RATE_LIMIT_ENABLED', 'false')


def test_imports():
    """Test that all required modules can be imported"""
    print("Testing imports...")

    try:
        import flask
        print("  ✓ Flask")
    except ImportError:
        print("  ✗ Flask - Run: pip install Flask")
        return False

    try:
        import flask_cors
        print("  ✓ Flask-CORS")
    except ImportError:
        print("  ✗ Flask-CORS - Run: pip install Flask-CORS")
        return False

    try:
        import flask_socketio
        print("  ✓ Flask-SocketIO")
    except ImportError:
        print("  ✗ Flask-SocketIO - Run: pip install Flask-SocketIO")
        return False

    try:
        import requests
        print("  ✓ Requests")
    except ImportError:
        print("  ✗ Requests - Run: pip install requests")
        return False

    return True


def test_automation_classes():
    """Test that automation classes can be instantiated"""
    print("\nTesting automation classes...")
    
    try:
        from automations import AVAILABLE_AUTOMATIONS
        print(f"  Found {len(AVAILABLE_AUTOMATIONS)} automation types")
        
        for AutoClass in AVAILABLE_AUTOMATIONS:
            instance = AutoClass()
            name = instance.get_name()
            desc = instance.get_description()
            schema = instance.get_config_schema()
            
            print(f"  ✓ {name}")
            print(f"    Description: {desc}")
            print(f"    Config fields: {len(schema)}")
        
        return True
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def test_automation_manager():
    """Test automation manager"""
    print("\nTesting automation manager...")
    
    try:
        from automation_manager import AutomationManager
        
        manager = AutomationManager()
        types = manager.get_available_automations()
        
        print(f"  ✓ Manager initialized")
        print(f"  ✓ Available types: {len(types)}")
        
        # Test creating an automation
        if types:
            first_type = types[0]['type']
            automation = manager.create_automation(first_type)
            print(f"  ✓ Created test automation: {automation['name']}")
            
            # Test listing
            automations = manager.list_automations()
            print(f"  ✓ Listed automations: {len(automations)}")
            
            # Clean up
            manager.delete_automation(automation['id'])
            print(f"  ✓ Deleted test automation")
        
        return True
    except Exception as e:
        print(f"  ✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_security_config():
    """Test security configuration"""
    print("\nTesting security configuration...")

    try:
        from config import Config, validate_input, sanitize_string

        print("  ✓ Config module loaded")

        # Test input validation
        assert validate_input("abc123", "uuid") is False
        assert validate_input("a1b2c3d4", "uuid") is True
        assert validate_input("test.py", "filename") is True
        assert validate_input("../etc/passwd", "filename") is False
        assert validate_input("test;rm -rf /", "filename") is False
        print("  ✓ Input validation working")

        # Test sanitization
        dirty = "Hello\x00World\x1f"
        clean = sanitize_string(dirty)
        assert "\x00" not in clean
        assert "\x1f" not in clean
        print("  ✓ String sanitization working")

        # Test config defaults
        assert Config.SECRET_KEY is not None
        assert len(Config.SECRET_KEY) >= 32
        print("  ✓ Secret key configured")

        return True
    except Exception as e:
        print(f"  ✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_script_manager_security():
    """Test script manager security features"""
    print("\nTesting script manager security...")

    try:
        from script_manager import ScriptManager, _validate_filename

        # Test filename validation
        assert _validate_filename("test.py") is True
        assert _validate_filename("../test.py") is False
        assert _validate_filename("/etc/passwd") is False
        assert _validate_filename("test;rm.py") is False
        assert _validate_filename("test\x00.py") is False
        print("  ✓ Filename validation working")

        manager = ScriptManager()
        print("  ✓ Script manager initialized")

        # Test path traversal prevention
        try:
            manager._validate_script_path("../../../etc/passwd")
            print("  ✗ Path traversal not prevented!")
            return False
        except ValueError:
            print("  ✓ Path traversal prevented")

        return True
    except Exception as e:
        print(f"  ✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    print("=" * 60)
    print("Server Component & Security Test")
    print("=" * 60)
    print()

    all_passed = True

    # Test imports
    if not test_imports():
        all_passed = False
        print("\n⚠ Install missing dependencies:")
        print("  pip install -r requirements.txt")

    # Test automation classes
    if not test_automation_classes():
        all_passed = False

    # Test automation manager
    if not test_automation_manager():
        all_passed = False

    # Test security config
    if not test_security_config():
        all_passed = False

    # Test script manager security
    if not test_script_manager_security():
        all_passed = False

    print()
    print("=" * 60)
    if all_passed:
        print("✅ All tests passed! Server is ready to run.")
        print()
        print("For development (no auth):")
        print("  API_KEY_REQUIRED=false python app.py")
        print()
        print("For production:")
        print("  1. Copy .env.example to .env")
        print("  2. Configure API_KEY and SECRET_KEY")
        print("  3. Set up HTTPS certificates")
        print("  4. python app.py")
    else:
        print("❌ Some tests failed. Fix the issues above.")
        sys.exit(1)
    print("=" * 60)


if __name__ == "__main__":
    main()

