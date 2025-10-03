#!/usr/bin/env python3
"""
Flexible Chat Server - Supports both local and network connections
"""

from chat_server import ChatServer
import sys

def main():
    """
    Main function with flexible server configuration
    """
    print("=== Multi-User Chat Server ===")
    print()
    
    # Ask user for server type
    while True:
        print("Choose server mode:")
        print("1. Local only (same computer)")
        print("2. Network (LAN/Internet)")
        print("3. Custom configuration")
        
        choice = input("Enter choice (1-3): ").strip()
        
        if choice == "1":
            # Local only
            host = "127.0.0.1"
            port = 12345
            print(f"🏠 Starting LOCAL server on {host}:{port}")
            print("📝 Only clients on THIS computer can connect")
            break
        
        elif choice == "2":
            # Network mode
            host = "0.0.0.0"
            port = 12345
            print(f"🌐 Starting NETWORK server on {host}:{port}")
            print("📝 Clients from other computers can connect")
            print("📋 Share your IP address with friends:")
            
            # Show IP addresses
            import socket
            hostname = socket.gethostname()
            try:
                local_ip = socket.gethostbyname(hostname)
                print(f"   Your IP: {local_ip}")
            except:
                print("   Run 'ipconfig' (Windows) or 'ifconfig' (Mac/Linux) to find your IP")
            break
            
        elif choice == "3":
            # Custom
            host = input("Enter host (default 0.0.0.0): ").strip() or "0.0.0.0"
            port = input("Enter port (default 12345): ").strip()
            port = int(port) if port else 12345
            print(f"⚙️ Starting CUSTOM server on {host}:{port}")
            break
        
        else:
            print("❌ Invalid choice. Try again.\n")
    
    # Ask for max clients
    max_clients = input(f"Max clients (default 2): ").strip()
    max_clients = int(max_clients) if max_clients else 2
    
    print(f"👥 Maximum {max_clients} clients allowed")
    print()
    
    try:
        # Create and start server
        chat_server = ChatServer(
            host=host,
            port=port, 
            max_clients=max_clients
        )
        
        print("🚀 Starting server...")
        print("🛑 Press Ctrl+C to stop server")
        print("=" * 50)
        
        chat_server.start()
        
    except KeyboardInterrupt:
        print("\n👋 Server shutting down...")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Server error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()