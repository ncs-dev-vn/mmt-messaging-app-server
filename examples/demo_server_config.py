#!/usr/bin/env python3
"""
Demo: ChatServer flexible configuration (no more hard-coded hosts)
"""

import os
import sys
sys.path.insert(0, 'src')

def demo_server_flexibility():
    """Demonstrate ChatServer flexible configuration"""
    
    print("🎯 CHAT SERVER FLEXIBLE CONFIGURATION DEMO")
    print("=" * 50)
    
    from chat_server import ChatServer
    
    print("\n1️⃣ DEFAULT BEHAVIOR (no args):")
    server1 = ChatServer()
    print(f"   ChatServer() → host='{server1.host}', port={server1.port}, max_clients={server1.max_clients}")
    
    print("\n2️⃣ EXPLICIT CONFIGURATION:")
    server2 = ChatServer(host='0.0.0.0', port=8080, max_clients=10)
    print(f"   ChatServer('0.0.0.0', 8080, 10) → host='{server2.host}', port={server2.port}, max_clients={server2.max_clients}")
    
    print("\n3️⃣ PARTIAL CONFIGURATION:")
    server3 = ChatServer(host='192.168.1.100')
    print(f"   ChatServer(host='192.168.1.100') → host='{server3.host}', port={server3.port}, max_clients={server3.max_clients}")
    
    print("\n4️⃣ ENVIRONMENT VARIABLE TEST:")
    # Set environment variables
    os.environ['CHAT_SERVER_HOST'] = '172.16.1.200'
    os.environ['CHAT_NETWORK_MODE'] = 'true'
    server4 = ChatServer()
    print(f"   CHAT_SERVER_HOST=172.16.1.200")
    print(f"   ChatServer() → host='{server4.host}', port={server4.port}, max_clients={server4.max_clients}")
    
    # Clean up
    del os.environ['CHAT_SERVER_HOST']
    del os.environ['CHAT_NETWORK_MODE']
    
    print("\n5️⃣ NETWORK MODE AUTO:")
    os.environ['CHAT_NETWORK_MODE'] = 'true'
    server5 = ChatServer()
    print(f"   CHAT_NETWORK_MODE=true")
    print(f"   ChatServer() → host='{server5.host}' (auto network mode)")
    del os.environ['CHAT_NETWORK_MODE']

def show_comparison():
    """Show before vs after comparison"""
    print(f"\n📊 BEFORE vs AFTER COMPARISON")
    print("=" * 50)
    
    print("❌ BEFORE (hard-coded):")
    print("   def __init__(self, host='127.0.0.1', port=12345, max_clients=2):")
    print("   → Always localhost unless explicitly overridden")
    print("   → Default max_clients=2 (too low)")
    print("   → No environment variable support")
    
    print("\n✅ AFTER (flexible):")
    print("   def __init__(self, host=None, port=None, max_clients=None):")
    print("   → Smart defaults with _get_default_host()")
    print("   → Environment variable support (CHAT_SERVER_HOST, CHAT_NETWORK_MODE)")
    print("   → Better defaults (max_clients=5)")
    print("   → None values trigger auto-detection")

def show_usage_patterns():
    """Show different usage patterns"""
    print(f"\n💼 USAGE PATTERNS")
    print("=" * 50)
    
    print("🏠 Pattern 1: Development (Local)")
    print("   server = ChatServer()  # Uses 127.0.0.1 by default")
    
    print("\n🌐 Pattern 2: Production (Network)")
    print("   export CHAT_NETWORK_MODE=true")
    print("   server = ChatServer()  # Uses 0.0.0.0 automatically")
    
    print("\n⚙️ Pattern 3: Custom Host")
    print("   export CHAT_SERVER_HOST=192.168.1.100")
    print("   server = ChatServer()  # Uses environment value")
    
    print("\n🔧 Pattern 4: Explicit Configuration")
    print("   server = ChatServer(host='0.0.0.0', port=8080, max_clients=20)")

def main():
    """Run the demo"""
    try:
        demo_server_flexibility()
        show_comparison()
        show_usage_patterns()
        
        print(f"\n🎊 SUMMARY")
        print("=" * 50)
        print("✅ ChatServer is NO LONGER hard-coded!")
        print("✅ Multiple configuration methods available")
        print("✅ Smart defaults with environment support") 
        print("✅ Better default values (max_clients=5)")
        print("✅ Backward compatibility maintained")
        
        print(f"\n🚀 BOTH CLIENT AND SERVER ARE NOW FLEXIBLE!")
        print("🔧 No more hard-coded host addresses anywhere!")
        
    except Exception as e:
        print(f"Demo error: {e}")
        return 1
        
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)