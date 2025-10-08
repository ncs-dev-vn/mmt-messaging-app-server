# MMT Messaging Server

A simple and robust Python messaging server that handles multiple client connections simultaneously using threading.

## Features

*   **🔐 Username System:** Unique username registration with validation and authentication
*   **� Private Messaging:** Send direct messages to specific users with `@username <message>` syntax
*   **�💬 Chat Commands:** Built-in commands like `/users`, `/nick`, `/quit`, `/help` for enhanced user interaction  
*   **🔗 Concurrent Connections:** Handles multiple client connections simultaneously with minimal resource usage
*   **🛡️ Connection Stability:** Resilient to staggering network connections and interruptions
*   **📢 User Notifications:** Broadcasts join/leave notifications and username changes to all users
*   **⏳ Queue Management:** Implements a waiting queue system when the server reaches maximum capacity
*   **🔒 Thread-Safe Operations:** Uses proper synchronization mechanisms for multi-threaded operations

## Technologies

*   **Language:** Python 3.8+
*   **Libraries:** Standard library only (socket, threading)
*   **Architecture:** Multi-threaded server with condition-based synchronization

## Project Structure

```
server/
├── main.py              # Main entry point
├── LICENSE              # License file
├── requirements.txt     # Python dependencies
├── setup.py            # Package setup
├── src/                # Source code
│   ├── __init__.py
│   ├── main.py         # Application main module
│   ├── chat_server.py  # Server implementation
│   └── client_handler.py # Client handler
└── doc/                # Documentation
    ├── README.md       # This file
    ├── CONFIGURATION.md # Configuration guide
    ├── architecture.mmd # Architecture diagram
    └── gemini_conversation.md # Research log
```

## Getting Started

### Prerequisites

- Python 3.8 or higher
- No external dependencies required

### Installation

1. Clone or download the project
2. Navigate to the server directory

### Running the Server

```bash
# From the project root directory
python main.py

# Or run from the src directory
cd src
python main.py
```

### Configuration

The server can be configured by modifying parameters in `src/chat_server.py`:

- **Host:** Default is `127.0.0.1` (localhost)
- **Port:** Default is `12345`
- **Max Clients:** Default is `2` concurrent connections
- **Buffer Size:** Default is `1024` bytes

### Testing

You can test the server using telnet or any TCP client:

```bash
# Connect to the server
telnet 127.0.0.1 12345
```

## Architecture

The server uses a multi-threaded architecture with:

- **Main Thread:** Accepts incoming connections
- **Handler Threads:** One per client connection
- **Condition Variables:** For thread synchronization
- **Queue System:** Manages clients when at capacity

See `doc/architecture.mmd` for a detailed architectural diagram.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
