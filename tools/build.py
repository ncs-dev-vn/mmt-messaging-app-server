import os
import subprocess
import shutil
import sys

def build_executables():
    """Build executable files for distribution"""
    
    print("🚀 Building Chat Application Executables...")
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller
    except ImportError:
        print("❌ PyInstaller not found. Installing...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'pyinstaller'])
    
    # Clean old builds
    if os.path.exists('dist'):
        shutil.rmtree('dist')
        print("🧹 Cleaned old dist folder")
    if os.path.exists('build'):
        shutil.rmtree('build')
        print("🧹 Cleaned old build folder")
    
    # Build server
    print("📦 Building server executable...")
    result = subprocess.run(['pyinstaller', '--onefile', '--name', 'ChatServer', 'main.py'], 
                          capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ Server build failed: {result.stderr}")
        return False
    
    # Build client  
    print("📦 Building client executable...")
    result = subprocess.run(['pyinstaller', '--onefile', '--name', 'ChatClient', 'chat_client.py'],
                          capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ Client build failed: {result.stderr}")
        return False
    
    # Create distribution folder
    release_folder = 'release'
    os.makedirs(release_folder, exist_ok=True)
    
    # Copy executables
    try:
        if os.name == 'nt':  # Windows
            shutil.copy('dist/ChatServer.exe', f'{release_folder}/')
            shutil.copy('dist/ChatClient.exe', f'{release_folder}/')
            print("💻 Windows executables created")
        else:  # macOS/Linux
            shutil.copy('dist/ChatServer', f'{release_folder}/')
            shutil.copy('dist/ChatClient', f'{release_folder}/')
            # Make executable
            os.chmod(f'{release_folder}/ChatServer', 0o755)
            os.chmod(f'{release_folder}/ChatClient', 0o755)
            print("🍎🐧 Unix executables created")
    except Exception as e:
        print(f"❌ Failed to copy executables: {e}")
        return False
    
    # Create simple user guide
    create_user_guide(release_folder)
    
    print(f"✅ Build completed successfully!")
    print(f"📁 Files available in '{release_folder}/' folder")
    print(f"🎉 Ready for distribution!")
    
    return True

def create_user_guide(folder):
    """Create simple user guide for end users"""
    guide_content = """# Chat Application - User Guide

## Quick Start (No coding required!)

### Step 1: Start the Server
- Double-click `ChatServer` (or `ChatServer.exe` on Windows)
- You'll see: "Server started on 127.0.0.1:12345, waiting for connections..."

### Step 2: Join the Chat
- Double-click `ChatClient` (or `ChatClient.exe` on Windows)  
- Enter your nickname when asked
- Start chatting!

### Step 3: Add More People
- Each person runs `ChatClient`
- Everyone can chat together!

## Commands:
- Type message + Enter = Send message
- Type `quit` = Leave chat
- Press Ctrl+C = Quick exit

## Troubleshooting:
- If server won't start: Wait 30 seconds and try again
- If can't connect: Make sure server is running first
- For network chat: Share your IP address with friends

Enjoy chatting! 🎉
"""
    
    with open(f"{folder}/HOW_TO_USE.txt", "w", encoding="utf-8") as f:
        f.write(guide_content)
    
    print("📄 User guide created: HOW_TO_USE.txt")

if __name__ == "__main__":
    success = build_executables()
    if not success:
        print("❌ Build failed. Check error messages above.")
        sys.exit(1)
    else:
        print("\n🎊 All done! Share the 'release/' folder with your users.")