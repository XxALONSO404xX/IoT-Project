#!/usr/bin/env python3
"""
IoT Platform Agent - Main Entry Point
A agent that runs on local networks to discover, monitor, and manage IoT devices.
"""
import os
import sys
import time
import logging
import argparse
import configparser
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger("iot-agent")

def get_base_path():
    """
    Get the base path for the application, works both for development and when packaged as executable.
    """
    # When running as script
    if getattr(sys, 'frozen', False):
        # When running as executable (PyInstaller)
        return os.path.dirname(sys.executable)
    else:
        # When running in development
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def setup_environment():
    """Load configuration and set up the agent environment."""
    base_path = get_base_path()
    
    # Paths to check for configuration
    config_paths = [
        os.path.join(base_path, 'config', 'config.ini'),  # Packaged config
        os.path.join(os.path.dirname(base_path), 'config', 'config.ini'),  # Development config
    ]
    
    # Try to load configuration file
    config = configparser.ConfigParser()
    config_file = None
    
    for path in config_paths:
        if os.path.exists(path):
            config_file = path
            logger.info(f"Loading configuration from: {path}")
            config.read(path)
            break
    
    if not config_file:
        logger.warning("No configuration file found, using default settings")
    
    # Fall back to environment variables if needed
    # Load .env file if it exists (mainly for development)
    env_path = os.path.join(base_path, '.env')
    if os.path.exists(env_path):
        load_dotenv(env_path)
    
    # Get configuration from file or environment variables
    backend_url = config.get('connection', 'backend_url', fallback=None) if config_file else None
    backend_url = backend_url or os.environ.get('BACKEND_URL', 'http://localhost:8080')
    
    token = config.get('connection', 'auth_token', fallback=None) if config_file else None
    token = token or os.environ.get('AUTH_TOKEN', '')
    
    # Create settings dictionary
    settings = {
        'backend_url': backend_url,
        'token': token,
        'config_file': config_file
    }
    
    logger.info(f"Agent initialized. Backend URL: {backend_url}")
    
    # If we have a config object, add all settings
    if config_file:
        for section in config.sections():
            for key, value in config.items(section):
                settings[f"{section}.{key}"] = value
    
    return settings

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='IoT Platform Agent')
    
    parser.add_argument('--discover', action='store_true', 
                        help='Run device discovery scan')
    parser.add_argument('--monitor', action='store_true',
                       help='Start monitoring devices')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable verbose logging')
    parser.add_argument('--install-service', action='store_true',
                       help='Install as a system service')
                       
    return parser.parse_args()

def main():
    """Main entry point for the IoT platform agent."""
    args = parse_arguments()
    
    # Set up logging level based on arguments
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("Verbose logging enabled")
    
    # Handle service installation if requested
    if args.install_service:
        logger.info("Installing agent as a service...")
        # This would be implemented separately for each platform
        # For now, just show a message
        print("Service installation not yet implemented")
        return
    
    # Set up the environment
    config = setup_environment()
    
    logger.info("IoT Platform Agent starting...")
    
    try:
        # Main agent loop
        while True:
            # In a real implementation, this would include:
            # 1. Device discovery
            # 2. Device monitoring
            # 3. Command execution
            # 4. Communication with backend
            # 5. Security scans
            
            logger.info("Agent running...")
            time.sleep(10)  # Placeholder - replace with actual work
            
    except KeyboardInterrupt:
        logger.info("Agent shutting down...")
    except Exception as e:
        logger.exception(f"Unexpected error: {str(e)}")
    
    logger.info("Agent terminated")

if __name__ == "__main__":
    main() 