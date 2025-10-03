#!/usr/bin/env python3
"""
Network Information Tool - Show all available IP addresses and explain host options
"""

import socket
import subprocess
import platform
import netifaces

def get_all_ip_addresses():
    """Get all network interfaces and their IP addresses"""
    interfaces = []
    
    try:
        # Try using netifaces if available
        for interface in netifaces.interfaces():
            addrs = netifaces.ifaddresses(interface)
            if netifaces.AF_INET in addrs:
                for addr_info in addrs[netifaces.AF_INET]:
                    ip = addr_info['addr']
                    if ip != '127.0.0.1':  # Skip loopback
                        interfaces.append({
                            'interface': interface,
                            'ip': ip,
                            'type': classify_ip(ip)
                        })
    except ImportError:
        # Fallback method if netifaces not available
        hostname = socket.gethostname()
        try:
            # Get primary IP
            primary_ip = socket.gethostbyname(hostname)
            interfaces.append({
                'interface': 'primary',
                'ip': primary_ip,
                'type': classify_ip(primary_ip)
            })
        except:
            pass
    
    return interfaces

def classify_ip(ip):
    """Classify IP address type"""
    octets = ip.split('.')
    first = int(octets[0])
    second = int(octets[1])
    
    if ip == '127.0.0.1':
        return 'Loopback'
    elif first == 192 and second == 168:
        return 'Private (Home/Office Network)'
    elif first == 10:
        return 'Private (Corporate Network)'  
    elif first == 172 and 16 <= second <= 31:
        return 'Private (Corporate Network)'
    elif first in [169] and second == 254:
        return 'Link-Local (Auto-assigned)'
    else:
        return 'Public (Internet)'

def get_simple_local_ip():
    """Simple method to get local IP"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return None

def show_host_options():
    """Show different host configuration options"""
    print("🌐 HOST CONFIGURATION OPTIONS")
    print("=" * 60)
    
    print("\n1️⃣ LOCALHOST (127.0.0.1)")
    print("   ✅ Use case: Testing, development on same computer")
    print("   ❌ Limitation: Only same computer can connect")
    print("   📝 Server: ChatServer(host='127.0.0.1')")
    print("   📝 Client: ChatClient(host='127.0.0.1')")
    
    print("\n2️⃣ ALL INTERFACES (0.0.0.0)")
    print("   ✅ Use case: Allow connections from other computers")
    print("   ⚠️  Security: Opens server to all network interfaces")
    print("   📝 Server: ChatServer(host='0.0.0.0')")
    print("   📝 Client: ChatClient(host='SERVER_REAL_IP')")
    
    # Show actual IPs
    simple_ip = get_simple_local_ip()
    if simple_ip:
        print(f"\n3️⃣ SPECIFIC IP ({simple_ip})")
        print("   ✅ Use case: Bind to specific network interface")
        print("   🔒 Security: More controlled than 0.0.0.0")
        print(f"   📝 Server: ChatServer(host='{simple_ip}')")
        print(f"   📝 Client: ChatClient(host='{simple_ip}')")
    
    print("\n4️⃣ AUTO-DETECTION")
    print("   ✅ Use case: Let system choose best IP")
    print("   🤖 Method: Connect to external server, see which IP is used")
    print("   📝 Code: get_local_ip() function in our main.py")

def show_network_info():
    """Show current network configuration"""
    print("\n💻 YOUR NETWORK INFORMATION")
    print("=" * 60)
    
    # Hostname
    hostname = socket.gethostname()
    print(f"🖥️  Computer name: {hostname}")
    
    # Simple IP detection
    simple_ip = get_simple_local_ip()
    if simple_ip:
        print(f"🌐 Primary IP: {simple_ip} ({classify_ip(simple_ip)})")
    
    # All interfaces
    interfaces = get_all_ip_addresses()
    if interfaces:
        print(f"\n📡 Available Network Interfaces:")
        for iface in interfaces:
            print(f"   {iface['interface']}: {iface['ip']} - {iface['type']}")
    
    # Port recommendations
    print(f"\n🔌 Recommended Server Configuration:")
    if simple_ip:
        print(f"   For LAN: ChatServer(host='0.0.0.0', port=12345)")
        print(f"   Share IP: {simple_ip}:12345")
    print(f"   For Local: ChatServer(host='127.0.0.1', port=12345)")

def show_usage_scenarios():
    """Show practical usage scenarios"""
    print("\n📋 PRACTICAL USAGE SCENARIOS")
    print("=" * 60)
    
    simple_ip = get_simple_local_ip()
    
    print("\n🏠 Scenario 1: Family/Friends at Home")
    print("   All connected to same WiFi router")
    print("   Server: host='0.0.0.0'")
    if simple_ip:
        print(f"   Clients connect to: {simple_ip}")
    
    print("\n🏢 Scenario 2: Office/School Network")  
    print("   Computers on same LAN")
    print("   Server: host='0.0.0.0'")
    print("   Check with IT: firewall might block connections")
    
    print("\n🌍 Scenario 3: Internet (Advanced)")
    print("   Friends in different locations")
    print("   Need: Port forwarding on router")
    print("   Server: host='0.0.0.0'")
    print("   Clients use: your PUBLIC IP")
    
    print("\n💻 Scenario 4: Development/Testing")
    print("   Just you, testing on same computer")
    print("   Server: host='127.0.0.1'")
    print("   Client: host='127.0.0.1'")

def main():
    print("🔍 CHAT APPLICATION - NETWORK CONFIGURATION GUIDE")
    print("=" * 70)
    
    # Show current network info
    show_network_info()
    
    # Show host options
    show_host_options()
    
    # Show usage scenarios
    show_usage_scenarios()
    
    print(f"\n💡 SUMMARY")
    print("=" * 60)
    print("Host addresses are configured by:")
    print("1. 🔧 Developer choice (127.0.0.1, 0.0.0.0, specific IP)")
    print("2. 🤖 Auto-detection (get_local_ip() function)")
    print("3. 👤 User input (interactive mode in main.py)")
    print("4. 📋 Network requirements (local vs remote access)")
    
    simple_ip = get_simple_local_ip()
    if simple_ip:
        print(f"\n🎯 For your setup, recommend:")
        print(f"   Server: python main.py → option 2 (Network)")
        print(f"   Share this IP with friends: {simple_ip}")

if __name__ == "__main__":
    try:
        main()
    except ImportError:
        print("📦 Installing netifaces for better network info...")
        print("💡 Run: pip install netifaces")
        print("\n🔄 Running basic version...")
        
        # Run basic version without netifaces
        show_network_info()
        show_host_options() 
        show_usage_scenarios()