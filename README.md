# IoT Platform for Network Management and Security

A comprehensive platform for discovering, monitoring, and managing IoT devices on local networks with built-in security features.

## Overview

This platform helps users to:

1. 🔍 **Discover** all devices on their local network automatically
2. 📊 **Monitor** device status, traffic, and performance
3. 🛡️ **Secure** their IoT devices through vulnerability detection
4. 🎮 **Control** devices through a unified dashboard
5. 🔄 **Automate** actions based on rules and triggers

## Components

The platform consists of three main components:

### 1. Frontend (React)

A modern web application that provides:
- Device discovery and management dashboard
- Real-time monitoring and status updates
- Security vulnerability visualization
- User management and authentication
- Automation rules configuration

### 2. Backend (Spring Boot)

A robust API server that handles:
- User authentication and authorization
- Device data persistence
- Subscription management
- Automation rule processing
- Security analysis

### 3. Agent (Python)

A lightweight agent deployed on the local network that:
- Discovers devices using network scanning
- Monitors device connectivity and performance
- Detects potential security vulnerabilities
- Executes commands from the backend
- Securely communicates with the backend server

## Project Structure

```
iot-platform/
├── frontend/          # React application
├── Backend/           # Spring Boot API server
├── agent/             # Python local network agent
├── docker/            # Docker configuration
└── README.md          # This file
```

## Technology Stack

- **Frontend**: React, Material-UI, Chart.js, Axios
- **Backend**: Spring Boot, Spring Security, JPA, PostgreSQL
- **Agent**: Python, Scapy, NMAP, cryptography libraries

## Security Features

- **Network Scanning**: Discover all devices and identify potential vulnerabilities
- **Traffic Analysis**: Monitor network traffic for suspicious patterns
- **Vulnerability Detection**: Identify known vulnerabilities in IoT devices
- **Secure Communication**: All components communicate using encrypted channels
- **Role-based Access Control**: Granular permission system for different user roles

## Installation and Setup

Each component has its own installation instructions in their respective directories:

- [Frontend Setup](frontend/README.md)
- [Backend Setup](Backend/README.md)
- [Agent Setup](agent/README.md)

## Development

1. Clone the repository
2. Set up the development environment for each component
3. Run each component locally for development

## License

This software is proprietary and confidential.


