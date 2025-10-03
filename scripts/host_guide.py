#!/usr/bin/env python3
"""
Simple Network Info Tool - Explain host configuration without external dependencies
"""

import socket
import subprocess
import platform

def get_local_ip():
    """Get the local IP address using the same method as main.py"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except:
        return "Unable to determine"

def classify_ip(ip):
    """Classify IP address type"""
    if ip == "Unable to determine":
        return "Unknown"
    
    try:
        octets = ip.split('.')
        first = int(octets[0])
        second = int(octets[1])
        
        if ip == '127.0.0.1':
            return 'Loopback (Local only)'
        elif first == 192 and second == 168:
            return 'Private Network (Home/Office WiFi)'
        elif first == 10:
            return 'Private Network (Corporate/VPN)'  
        elif first == 172 and 16 <= second <= 31:
            return 'Private Network (Corporate)'
        else:
            return 'Public IP (Internet)'
    except:
        return "Invalid IP"

def show_host_explanation():
    """Explain how host addresses work"""
    print("🌐 HOST ADDRESS EXPLANATION")
    print("=" * 60)
    
    print("\n❓ HOST LÀ GÌ?")
    print("   Host = địa chỉ IP mà server lắng nghe kết nối")
    print("   Quyết định: AI có thể kết nối đến server?")
    
    print("\n🔧 CÁCH THIẾT LẬP HOST:")
    print("   1. Dev cài đặt cố định trong code")
    print("   2. User chọn qua menu interactive") 
    print("   3. Auto-detect từ hệ thống")
    print("   4. Command line arguments")

def show_host_types():
    """Show different host configuration types"""
    print("\n📋 CÁC LOẠI HOST CONFIGURATION")
    print("=" * 60)
    
    # Get current IP for examples
    current_ip = get_local_ip()
    ip_type = classify_ip(current_ip)
    
    print(f"🖥️  Máy bạn hiện tại: {current_ip}")
    print(f"   Loại: {ip_type}")
    
    print(f"\n1️⃣ LOCALHOST (127.0.0.1)")
    print(f"   📝 Code: ChatServer(host='127.0.0.1')")
    print(f"   ✅ Ai kết nối được: Chỉ máy này")
    print(f"   ❌ Ai KHÔNG kết nối được: Máy khác")
    print(f"   🎯 Dùng khi: Test, development")
    
    print(f"\n2️⃣ ALL INTERFACES (0.0.0.0)")
    print(f"   📝 Code: ChatServer(host='0.0.0.0')")
    print(f"   ✅ Ai kết nối được: Tất cả máy trong mạng")
    print(f"   📋 Client phải dùng IP: {current_ip}")
    print(f"   🎯 Dùng khi: Chat với bạn bè")
    
    if current_ip != "Unable to determine":
        print(f"\n3️⃣ SPECIFIC IP ({current_ip})")
        print(f"   📝 Code: ChatServer(host='{current_ip}')")
        print(f"   ✅ Ai kết nối được: Máy trong mạng LAN")
        print(f"   🔒 Bảo mật: Tốt hơn 0.0.0.0")
        print(f"   🎯 Dùng khi: Production environment")

def show_rules_and_sources():
    """Explain where host addresses come from"""
    print(f"\n🎯 HOST ADDRESS LẤY TỪ ĐÂU?")
    print("=" * 60)
    
    print(f"\n🔧 1. DEV CỨNG TRONG CODE:")
    print(f"   ChatServer(host='127.0.0.1')  # Dev fix cứng")
    print(f"   → Luôn là localhost, không đổi được")
    
    print(f"\n👤 2. USER CHỌN (Interactive Menu):")
    print(f"   python main.py → chọn option 1,2,3")
    print(f"   → User quyết định local hay network")
    
    print(f"\n🤖 3. AUTO-DETECTION (Hệ thống):")
    print(f"   Dùng hàm get_local_ip():")
    print(f"   - Tạo socket đến 8.8.8.8 (Google DNS)")
    print(f"   - Lấy IP mà hệ thống chọn")
    print(f"   - Đây là IP thật để chia sẻ")
    
    print(f"\n⚙️ 4. SYSTEM RULES (Quy tắc mạng):")
    print(f"   127.x.x.x   → Chỉ local machine")
    print(f"   192.168.x.x → Private network (WiFi nhà)")
    print(f"   10.x.x.x    → Corporate network")  
    print(f"   0.0.0.0     → All available interfaces")

def show_practical_examples():
    """Show practical usage examples"""
    current_ip = get_local_ip()
    
    print(f"\n💼 VÍ DỤ THỰC TẾ")
    print("=" * 60)
    
    print(f"\n🏠 Tình huống 1: Anh chị em trong nhà chat")
    print(f"   Server (máy bạn): host='0.0.0.0'")
    print(f"   Client (máy khác): host='{current_ip}'")
    print(f"   Requirement: Cùng WiFi")
    
    print(f"\n🏫 Tình huống 2: Bạn cùng lớp chat")
    print(f"   Server: host='0.0.0.0'") 
    print(f"   Clients: host='{current_ip}'")
    print(f"   Requirement: Cùng mạng trường")
    
    print(f"\n💻 Tình huống 3: Test một mình")
    print(f"   Server: host='127.0.0.1'")
    print(f"   Client: host='127.0.0.1'") 
    print(f"   Requirement: Không cần mạng")
    
    print(f"\n🌍 Tình huống 4: Bạn ở xa chat")
    print(f"   Server: host='0.0.0.0' + port forwarding")
    print(f"   Client: host='PUBLIC_IP_CUA_BAN'")
    print(f"   Requirement: Setup router")

def main():
    print("📚 CHAT APPLICATION - HOST CONFIGURATION GUIDE")
    print("🔍 Giải thích: Host address lấy từ đâu và theo quy tắc gì")
    print("=" * 70)
    
    # Show basic explanation
    show_host_explanation()
    
    # Show different types
    show_host_types()
    
    # Show rules and sources
    show_rules_and_sources()
    
    # Show practical examples
    show_practical_examples()
    
    print(f"\n🎊 KẾT LUẬN")
    print("=" * 60)
    print("Host address KHÔNG phải tự nhiên có, mà:")
    print("✅ Dev cài đặt trong code (cố định)")
    print("✅ User chọn qua menu (linh hoạt)")  
    print("✅ Hệ thống auto-detect (thông minh)")
    print("✅ Theo quy tắc mạng (chuẩn TCP/IP)")
    
    current_ip = get_local_ip()
    if current_ip != "Unable to determine":
        print(f"\n🎯 CHO MÁY BẠN:")
        print(f"   Local test: host='127.0.0.1'")
        print(f"   Network chat: server host='0.0.0.0', share IP {current_ip}")

if __name__ == "__main__":
    main()