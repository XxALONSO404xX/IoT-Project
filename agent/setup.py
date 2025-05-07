from setuptools import setup, find_packages

setup(
    name="iot-platform-agent",
    version="0.1.0",
    description="IoT Platform Agent for local network device discovery and management",
    author="IoT Platform Team",
    packages=find_packages(),
    install_requires=[
        # Dependencies will be installed from requirements.txt
    ],
    entry_points={
        'console_scripts': [
            'iot-agent=src.main:main',
        ],
    },
) 