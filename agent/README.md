# IoT Platform Agent

This Python agent is designed to be deployed on local networks to discover, monitor, and manage IoT devices. It communicates with the backend server to report device status and receive commands.

## Features

- **Device Discovery**: Automatically find and identify all devices on the local network
- **Device Monitoring**: Continuously monitor device status, traffic, and performance
- **Security Scanning**: Detect vulnerabilities in IoT devices
- **Command Execution**: Execute commands received from the backend server
- **Secure Communication**: Encrypted communication with the backend server

## For Developers

### Requirements

- Python 3.9 or higher
- Network access with permission to scan (admin/root privileges may be required)
- Access to the backend server

### Development Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

2. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure the agent:
   ```bash
   cp config.example.ini config/config.ini
   ```
   Edit `config/config.ini` with your settings.

### Usage During Development

1. Run the agent:
   ```bash
   python src/main.py
   ```

2. Run with verbose logging:
   ```bash
   python src/main.py --verbose
   ```

3. Run a one-time discovery:
   ```bash
   python src/main.py --discover
   ```

## Building Executable for Distribution

To build a standalone executable:

1. Make sure you have PyInstaller installed:
   ```bash
   pip install pyinstaller
   ```

2. Run the build script:
   ```bash
   python build_executable.py
   ```

3. The executable will be created in the `dist` directory
   - Windows: `dist/iot-agent.exe`
   - Linux/Mac: `dist/iot-agent`

4. Distribute the executable along with the `config` directory

For end-user installation instructions, see [INSTALL.md](INSTALL.md).

## Directory Structure

```
agent/
├── src/                # Source code (compiled into executable)
│   ├── discovery/      # Network discovery modules
│   ├── monitoring/     # Device monitoring modules
│   ├── security/       # Security scanning modules
│   ├── communication/  # Backend communication modules
│   ├── executor/       # Command execution modules
│   └── main.py         # Main entry point
├── config/             # Configuration files (remains external)
├── utils/              # Utility functions
├── resources/          # Additional resources (remains external)
├── build/              # Build artifacts
├── dist/               # Distribution files
├── requirements.txt    # Python dependencies
├── setup.py            # Setup script
├── build_executable.py # Script to build standalone executable
├── INSTALL.md          # End-user installation guide
└── README.md           # This file
```

## Security Considerations

- The agent requires elevated privileges to perform network scanning
- All communication with the backend is encrypted
- Authentication tokens are used for backend communication
- AES encryption is used for sensitive data

## Troubleshooting

- **Network scanning fails**: Ensure you have proper permissions to perform network scans
- **Cannot connect to backend**: Check network connectivity and backend URL configuration
- **Authentication failures**: Verify your authentication token is correct

## License

This software is proprietary and confidential. 