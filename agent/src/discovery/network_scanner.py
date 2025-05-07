"""
Network Scanner Module for IoT Platform Agent
This module provides functionality to discover devices on the local network.
"""
import logging
import socket
import netifaces
import nmap
from typing import Dict, List, Optional

logger = logging.getLogger("iot-agent.discovery")

class NetworkScanner:
    """Network scanner for discovering devices on the local network."""
    
    def __init__(self):
        """Initialize the network scanner."""
        self.nmap_scanner = nmap.PortScanner()
        logger.debug("Network scanner initialized")
    
    def get_local_interfaces(self) -> List[Dict]:
        """Get information about all network interfaces on the local machine."""
        interfaces = []
        
        for iface in netifaces.interfaces():
            try:
                # Get IPv4 addresses
                if netifaces.AF_INET in netifaces.ifaddresses(iface):
                    for addr_info in netifaces.ifaddresses(iface)[netifaces.AF_INET]:
                        interfaces.append({
                            'name': iface,
                            'ip': addr_info.get('addr', ''),
                            'netmask': addr_info.get('netmask', ''),
                        })
            except Exception as e:
                logger.error(f"Error getting interface {iface} info: {str(e)}")
        
        return interfaces
    
    def get_primary_interface(self) -> Optional[Dict]:
        """Get the primary network interface (the one with internet access)."""
        interfaces = self.get_local_interfaces()
        
        # Try to find a non-loopback interface
        for iface in interfaces:
            if not iface['ip'].startswith('127.'):
                return iface
        
        # Fallback to the first interface if no suitable one found
        return interfaces[0] if interfaces else None
    
    def get_subnet_to_scan(self, interface: Optional[Dict] = None) -> str:
        """Determine the subnet to scan based on the provided or primary interface."""
        if interface is None:
            interface = self.get_primary_interface()
            
        if not interface:
            logger.warning("No network interface found, using default subnet")
            return "192.168.1.0/24"  # Default fallback
        
        # Convert IP and netmask to CIDR notation
        ip_parts = interface['ip'].split('.')
        netmask_parts = interface['netmask'].split('.')
        
        # Calculate network address (IP AND netmask)
        network_parts = [str(int(ip_parts[i]) & int(netmask_parts[i])) for i in range(4)]
        network_address = '.'.join(network_parts)
        
        # Calculate CIDR prefix length
        binary_mask = ''.join([bin(int(x))[2:].zfill(8) for x in netmask_parts])
        prefix_length = binary_mask.count('1')
        
        return f"{network_address}/{prefix_length}"
    
    def scan_network(self, subnet: Optional[str] = None) -> List[Dict]:
        """
        Scan the network for devices.
        
        Args:
            subnet: The subnet to scan in CIDR notation (e.g., "192.168.1.0/24").
                   If None, the subnet of the primary interface will be used.
        
        Returns:
            A list of dictionaries with information about discovered devices.
        """
        if subnet is None:
            subnet = self.get_subnet_to_scan()
        
        logger.info(f"Scanning network: {subnet}")
        
        try:
            # Run nmap scan (basic ping scan)
            self.nmap_scanner.scan(hosts=subnet, arguments='-sn')
            
            devices = []
            for host in self.nmap_scanner.all_hosts():
                if self.nmap_scanner[host].state() == 'up':
                    # Try to get hostname
                    hostname = ''
                    try:
                        hostname = socket.gethostbyaddr(host)[0]
                    except (socket.herror, socket.gaierror):
                        pass
                    
                    devices.append({
                        'ip_address': host,
                        'hostname': hostname,
                        'status': 'up',
                        'mac_address': self.nmap_scanner[host].get('addresses', {}).get('mac', '')
                    })
            
            logger.info(f"Found {len(devices)} devices on the network")
            return devices
            
        except Exception as e:
            logger.error(f"Error scanning network: {str(e)}")
            return []
    
    def perform_detailed_scan(self, ip_address: str) -> Dict:
        """
        Perform a detailed scan of a specific device.
        
        Args:
            ip_address: The IP address of the device to scan.
            
        Returns:
            A dictionary with detailed information about the device.
        """
        logger.info(f"Performing detailed scan of device: {ip_address}")
        
        try:
            # Run nmap scan with OS and service detection
            self.nmap_scanner.scan(hosts=ip_address, arguments='-sS -O -sV')
            
            if ip_address not in self.nmap_scanner.all_hosts():
                logger.warning(f"Device {ip_address} not found in detailed scan")
                return {}
            
            device_info = {
                'ip_address': ip_address,
                'status': self.nmap_scanner[ip_address].state(),
                'hostname': '',
                'mac_address': '',
                'os': {},
                'open_ports': [],
                'services': []
            }
            
            # Get addresses information
            addresses = self.nmap_scanner[ip_address].get('addresses', {})
            if 'mac' in addresses:
                device_info['mac_address'] = addresses['mac']
            
            # Try to get hostname
            try:
                device_info['hostname'] = socket.gethostbyaddr(ip_address)[0]
            except (socket.herror, socket.gaierror):
                pass
            
            # Get OS information
            if 'osmatch' in self.nmap_scanner[ip_address]:
                os_matches = self.nmap_scanner[ip_address]['osmatch']
                if os_matches and len(os_matches) > 0:
                    device_info['os'] = {
                        'name': os_matches[0].get('name', ''),
                        'accuracy': os_matches[0].get('accuracy', ''),
                        'type': os_matches[0].get('osclass', [{}])[0].get('type', '')
                    }
            
            # Get port and service information
            for proto in self.nmap_scanner[ip_address].all_protocols():
                ports = sorted(self.nmap_scanner[ip_address][proto].keys())
                for port in ports:
                    port_info = self.nmap_scanner[ip_address][proto][port]
                    device_info['open_ports'].append({
                        'port': port,
                        'protocol': proto,
                        'state': port_info.get('state', '')
                    })
                    
                    if 'name' in port_info and port_info['name'] != '':
                        device_info['services'].append({
                            'port': port,
                            'protocol': proto,
                            'name': port_info.get('name', ''),
                            'product': port_info.get('product', ''),
                            'version': port_info.get('version', '')
                        })
            
            return device_info
            
        except Exception as e:
            logger.error(f"Error performing detailed scan: {str(e)}")
            return {'ip_address': ip_address, 'error': str(e)}

# Usage example
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    scanner = NetworkScanner()
    devices = scanner.scan_network()
    for device in devices:
        print(f"Found device: {device['ip_address']} ({device['hostname']})")
        if device['mac_address']:
            print(f"  MAC: {device['mac_address']}")
    
    # Detailed scan of first device (for testing)
    if devices:
        first_device = devices[0]['ip_address']
        details = scanner.perform_detailed_scan(first_device)
        print(f"\nDetailed scan of {first_device}:")
        print(f"  OS: {details.get('os', {}).get('name', 'Unknown')}")
        print(f"  Open ports: {len(details.get('open_ports', []))}")
        print(f"  Services: {len(details.get('services', []))}") 