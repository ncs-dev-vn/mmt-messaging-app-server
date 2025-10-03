# Build Scripts for Executable Distribution

## Sử dụng PyInstaller để tạo executable files

### Cài đặt PyInstaller:
```bash
pip install pyinstaller
```

### Build Server executable:
```bash
# Windows
pyinstaller --onefile --name "ChatServer" main.py

# macOS  
pyinstaller --onefile --name "ChatServer" --windowed main.py

# Linux
pyinstaller --onefile --name "ChatServer" main.py
```

### Build Client executable:
```bash
# Windows
pyinstaller --onefile --name "ChatClient" chat_client.py

# macOS
pyinstaller --onefile --name "ChatClient" --windowed chat_client.py  

# Linux
pyinstaller --onefile --name "ChatClient" chat_client.py
```

### Kết quả:
- `dist/ChatServer.exe` (Windows) hoặc `dist/ChatServer` (macOS/Linux)
- `dist/ChatClient.exe` (Windows) hoặc `dist/ChatClient` (macOS/Linux)

### Phân phối:
1. Tạo folder `ChatApp/`
2. Copy 2 file executable vào
3. Tạo file README_USER.txt với hướng dẫn đơn giản
4. Nén thành ZIP để chia sẻ

## Auto Build Script

Tạo file `build.py`:

```python
import os
import subprocess
import shutil

def build_executables():
    """Build executable files for distribution"""
    
    # Clean old builds
    if os.path.exists('dist'):
        shutil.rmtree('dist')
    if os.path.exists('build'):
        shutil.rmtree('build')
    
    # Build server
    print("Building server executable...")
    subprocess.run(['pyinstaller', '--onefile', '--name', 'ChatServer', 'main.py'])
    
    # Build client  
    print("Building client executable...")
    subprocess.run(['pyinstaller', '--onefile', '--name', 'ChatClient', 'chat_client.py'])
    
    # Create distribution folder
    os.makedirs('release', exist_ok=True)
    
    # Copy executables
    if os.name == 'nt':  # Windows
        shutil.copy('dist/ChatServer.exe', 'release/')
        shutil.copy('dist/ChatClient.exe', 'release/')
    else:  # macOS/Linux
        shutil.copy('dist/ChatServer', 'release/')
        shutil.copy('dist/ChatClient', 'release/')
    
    print("Build completed! Check 'release/' folder")

if __name__ == "__main__":
    build_executables()
```

## Sử dụng:
```bash
# Cài PyInstaller
pip install pyinstaller

# Build executables
python build.py

# Kết quả trong folder release/
```