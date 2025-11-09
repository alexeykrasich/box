#!/usr/bin/env python3
"""
Simple test script to verify server components work correctly.
Run this before starting the server to check for issues.
"""

import sys

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


def main():
    print("=" * 60)
    print("Server Component Test")
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
    
    print()
    print("=" * 60)
    if all_passed:
        print("✅ All tests passed! Server is ready to run.")
        print("Start the server with: python app.py")
    else:
        print("❌ Some tests failed. Fix the issues above.")
        sys.exit(1)
    print("=" * 60)


if __name__ == "__main__":
    main()

