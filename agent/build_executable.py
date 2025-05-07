#!/usr/bin/env python3
"""
Build script to create a standalone executable for the IoT Agent
"""
import os
import sys
import shutil
import subprocess

def clean_build_dirs():
    """Clean build and dist directories before building"""
    for directory in ['build', 'dist']:
        if os.path.exists(directory):
            shutil.rmtree(directory)
            os.mkdir(directory)
    
    # Remove any existing spec files
    for file in os.listdir('.'):
        if file.endswith('.spec'):
            os.remove(file)

def build_executable():
    """Build the executable using PyInstaller"""
    print("Building IoT Agent executable...")
    
    # Base directory
    base_dir = os.path.abspath(os.path.dirname(__file__))
    
    # PyInstaller command
    cmd = [
        'pyinstaller',
        '--name=iot-agent',
        '--onefile',  # Single executable file
        '--windowed',  # No console window in Windows
        '--add-data=config;config',  # Include config directory
        '--add-data=resources;resources',  # Include resources directory
        os.path.join('src', 'main.py')  # Entry point
    ]
    
    # Use : separator for Linux/Mac instead of ; for Windows
    if sys.platform != 'win32':
        cmd[4] = '--add-data=config:config'
        cmd[5] = '--add-data=resources:resources'
    
    # Run PyInstaller
    subprocess.run(cmd, check=True)
    
    print("\nBuild completed! Executable is in the 'dist' directory.")
    
    # Copy example config to the dist directory
    if not os.path.exists(os.path.join('dist', 'config')):
        os.mkdir(os.path.join('dist', 'config'))
    
    # Copy config.ini file
    config_src = os.path.join('config', 'config.ini')
    config_dest = os.path.join('dist', 'config', 'config.ini')
    if os.path.exists(config_src):
        shutil.copy2(config_src, config_dest)
    
    print("Configuration files copied to distribution directory.")

if __name__ == '__main__':
    clean_build_dirs()
    build_executable() 