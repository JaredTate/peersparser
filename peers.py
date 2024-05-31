import os
import socket
import struct

def parse_peers_dat(filepath):
    with open(filepath, 'rb') as file:
        data = file.read()

    ip_addresses = set()  # Use a set to store unique IP addresses
    ipv4_count = 0
    ipv6_count = 0
    offset = 0

    while offset < len(data):
        try:
            # Read the network address
            net_addr = data[offset:offset+16]
            
            # Extract the IP address
            if net_addr[0] == 0:
                # IPv4 address
                ip = socket.inet_ntop(socket.AF_INET, net_addr[1:5])
                ipv4_count += 1
            elif net_addr[0] == 1:
                # IPv6 address
                ip = socket.inet_ntop(socket.AF_INET6, net_addr[1:17])
                ipv6_count += 1
            else:
                raise ValueError("Invalid IP address version")
            
            ip_addresses.add(ip)  # Add the IP address to the set
        except (struct.error, socket.error, ValueError):
            # Skip invalid entries
            pass
        
        # Move to the next network address
        offset += 30

    return ip_addresses, ipv4_count, ipv6_count

# Specify the path to the peers.dat file
peers_dat_path = '/Users/jt/Code/peers.dat'

# Parse the peers.dat file
unique_ip_addresses, ipv4_count, ipv6_count = parse_peers_dat(peers_dat_path)

# Display the IP addresses
for ip in unique_ip_addresses:
    print(ip)

# Display the count of unique IP addresses
print(f"\nTotal Unique DGB Peers Seen By This Node: {len(unique_ip_addresses)}")
print(f"Total IPv4 Peers: {ipv4_count}")
print(f"Total IPv6 Peers: {ipv6_count}")