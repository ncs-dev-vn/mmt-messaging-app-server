#!/usr/bin/env python3
"""
Chat Client Entry Point

Usage:
    python client.py    # Start client with interactive menu
"""

import sys
import os

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

if __name__ == "__main__":
    from src.chat_client import main
    main()