#!/usr/bin/env python3
"""
Messaging App Server - Nơi bắt đầu chạy

Đây là điểm khởi chạy chính cho ứng dụng máy chủ tin nhắn.
Chạy file này để khởi động máy chủ.
"""

import sys
import os

# Thêm thư mục src vào đường dẫn Python
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

from components.chat_server import ChatServer

def main():
    """
    Điểm khởi động chính cho máy chủ tin nhắn.
    """
    print("Đang khởi động Messaging Server...")
    print("Nhấn Ctrl+C để dừng máy chủ.")
    print("-" * 50)
    
    try:
        chat_server = ChatServer()
        chat_server.start()
    except KeyboardInterrupt:
        print("\n[*] Máy chủ được yêu cầu tắt bởi người dùng.")
    except Exception as e:
        print(f"[!] Lỗi không mong muốn: {e}")
    finally:
        print("[*] Máy chủ đã dừng.")

if __name__ == "__main__":
    main()