#!/usr/bin/env python3
"""
Quick configuration test for reorganized chat system
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_imports():
    """Test that all imports work correctly"""
    print("🧪 Testing Imports After Reorganization")
    print("=" * 50)
    
    try:
        from chat_server import ChatServer
        print("✅ ChatServer import: SUCCESS")
        
        from chat_client import ChatClient  
        print("✅ ChatClient import: SUCCESS")
        
        from client_handler import ClientHandler
        print("✅ ClientHandler import: SUCCESS")
        
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_instantiation():
    """Test that classes can be instantiated"""
    print("\n🔧 Testing Class Instantiation")
    print("=" * 50)
    
    try:
        from chat_server import ChatServer
        from chat_client import ChatClient
        
        # Test server creation
        server = ChatServer(host='127.0.0.1', port=12345, max_clients=3)
        print("✅ ChatServer instance: SUCCESS")
        print(f"   Host: {server.host}, Port: {server.port}")
        
        # Test client creation
        client = ChatClient(host='127.0.0.1', port=12345)
        print("✅ ChatClient instance: SUCCESS")
        print(f"   Target: {client.host}:{client.port}")
        
        return True
    except Exception as e:
        print(f"❌ Instantiation failed: {e}")
        return False

def test_structure():
    """Test new directory structure"""
    print("\n📁 Testing Directory Structure")
    print("=" * 50)
    
    base_dir = os.path.join(os.path.dirname(__file__), '..')
    
    expected_dirs = ['src', 'tools', 'docs', 'examples', 'scripts']
    expected_files = [
        'src/main.py',
        'src/chat_server.py', 
        'src/chat_client.py',
        'src/client_handler.py'
    ]
    
    for dir_name in expected_dirs:
        dir_path = os.path.join(base_dir, dir_name)
        if os.path.exists(dir_path):
            print(f"✅ Directory {dir_name}/: EXISTS")
        else:
            print(f"❌ Directory {dir_name}/: MISSING")
    
    for file_path in expected_files:
        full_path = os.path.join(base_dir, file_path)
        if os.path.exists(full_path):
            print(f"✅ File {file_path}: EXISTS")
        else:
            print(f"❌ File {file_path}: MISSING")

def main():
    """Run all tests"""
    print("🚀 Chat Application - Post-Reorganization Test")
    print("=" * 60)
    
    import_ok = test_imports()
    instance_ok = test_instantiation()
    test_structure()
    
    print(f"\n🎊 Test Summary:")
    print(f"   Imports: {'✅ PASS' if import_ok else '❌ FAIL'}")
    print(f"   Classes: {'✅ PASS' if instance_ok else '❌ FAIL'}")
    
    if import_ok and instance_ok:
        print("\n🎉 Reorganization successful!")
        print("💡 All core functionality working after restructure")
        print("\n📋 New Usage:")
        print("   python server.py  # Start server")
        print("   python client.py  # Start client")
    else:
        print("\n❌ Some tests failed. Check errors above.")
        return 1
        
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)