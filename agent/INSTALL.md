# IoT Agent Installation Guide

This guide explains how to install and set up the IoT Platform Agent on your local network.

## System Requirements

- Windows 10/11, macOS, or Linux
- Administrator/root privileges (required for network scanning)
- Network access

## Installation Steps

### Windows

1. Download the IoT Agent installer package
2. Run the installer (iot-agent-setup.exe)
3. Follow the installation wizard prompts
4. The agent will be installed in your Program Files directory

### Manual Installation (All Platforms)

1. Download the zip file for your platform
2. Extract the contents to a location of your choice
3. The extracted folder will contain:
   - `iot-agent` executable (.exe on Windows)
   - `config/` directory with configuration files
   - `resources/` directory with additional resources

## Configuration

Before running the agent, you need to configure it:

1. Open the `config/config.ini` file in a text editor
2. Set the `backend_url` to the URL of your backend server
3. Enter your authentication token in the `auth_token` field
4. Save the file

## Running the Agent

### Windows

- Double-click the IoT Agent icon on your desktop
- Alternatively, run it from the Start menu

### Manual Start (All Platforms)

- Navigate to the installation directory
- Run the `iot-agent` executable (.exe on Windows)

## Running as a Service

For continuous operation, you may want to run the agent as a system service:

### Windows

1. Open Command Prompt as Administrator
2. Navigate to the installation directory
3. Run: `iot-agent --install-service`

### Linux

1. Copy the provided systemd service file to /etc/systemd/system/
2. Run: `sudo systemctl enable iot-agent`
3. Run: `sudo systemctl start iot-agent`

## Troubleshooting

If you encounter issues:

1. Check your network connection
2. Verify your authentication token is correct
3. Ensure you have administrator/root privileges
4. Check the logs in the `logs/` directory

## Uninstallation

### Windows

1. Go to Control Panel > Programs > Uninstall a program
2. Select IoT Agent and click Uninstall

### Manual Uninstallation

Simply delete the installation directory.

## Support

For additional help, contact support at support@iot-platform.com 