#!/usr/bin/env python3
"""
Flexible Chat Client - Can connect to local or remote servers
"""

from chat_client import ChatClient
import sys

def main():
    """
    Main function with flexible client configuration
    """
    print("=== Multi-User Chat Client ===")
    print()
    
    # Ask user for connection type
    while True:
        print("Choose connection mode:")
        print("1. Local server (same computer)")
        print("2. Remote server (different computer)")
        print("3. Custom configuration")
        
        choice = input("Enter choice (1-3): ").strip()
        
        if choice == "1":
            # Local connection
            host = "127.0.0.1"
            port = 12345
            print(f"🏠 Connecting to LOCAL server at {host}:{port}")
            break
        
        elif choice == "2":
            # Remote connection
            while True:
                host = input("Enter server IP address: ").strip()
                if host:
                    break
                print("❌ IP address cannot be empty")
            
            port = input("Enter port (default 12345): ").strip()
            port = int(port) if port else 12345
            print(f"🌐 Connecting to REMOTE server at {host}:{port}")
            break
            
        elif choice == "3":
            # Custom
            host = input("Enter host (default 127.0.0.1): ").strip() or "127.0.0.1"
            port = input("Enter port (default 12345): ").strip()
            port = int(port) if port else 12345
            print(f"⚙️ Connecting to CUSTOM server at {host}:{port}")
            break
        
        else:
            print("❌ Invalid choice. Try again.\n")
    
    print()
    
    try:
        # Create and start client
        client = ChatClient(host=host, port=port)
        
        print("🔗 Connecting to server...")
        print("💬 Ready to chat!")
        print("📝 Type 'quit' or press Ctrl+C to exit")
        print("=" * 50)
        
        client.start()
        
    except KeyboardInterrupt:
        print("\n👋 Disconnecting...")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Connection error: {e}")
        print("💡 Make sure server is running and IP/port are correct")
        sys.exit(1)

if __name__ == "__main__":
    main()