import os
import socket
import struct

def parse_peers_dat(filepath):
    with open(filepath, 'rb') as file:
        data = file.read()

    ipv4_addresses = set()  # Use a set to store unique IPv4 addresses
    ipv6_addresses = set()  # Use a set to store unique IPv6 addresses
    offset = 0

    while offset < len(data):
        try:
            # Read the network address
            net_addr = data[offset:offset+16]
            
            # Extract the IP address
            if net_addr[0] == 0:
                # IPv4 address
                ip = socket.inet_ntop(socket.AF_INET, net_addr[1:5])
                ipv4_addresses.add(ip)  # Add the IPv4 address to the set
            elif net_addr[0] == 1:
                # IPv6 address
                ip = socket.inet_ntop(socket.AF_INET6, net_addr[1:17])
                ipv6_addresses.add(ip)  # Add the IPv6 address to the set
            else:
                raise ValueError("Invalid IP address version")
        except (struct.error, socket.error, ValueError):
            # Skip invalid entries
            pass
        
        # Move to the next network address
        offset += 30

    return ipv4_addresses, ipv6_addresses

# Specify the path to the peers.dat file
peers_dat_path = '/Users/jt/Code/peersparser/peers.dat'

# Parse the peers.dat file
unique_ipv4_addresses, unique_ipv6_addresses = parse_peers_dat(peers_dat_path)

# Display the IP addresses
print("IPv4 Addresses:")
for ip in unique_ipv4_addresses:
    print(ip)

print("\nIPv6 Addresses:")
for ip in unique_ipv6_addresses:
    print(ip)

# Display the counts of unique IPv4 and IPv6 addresses
total_unique_peers = len(unique_ipv4_addresses) + len(unique_ipv6_addresses)
print(f"\nTotal Unique DGB Peers Seen By This Node: {total_unique_peers}")
print(f"Total Unique IPv4 Peers: {len(unique_ipv4_addresses)}")
print(f"Total Unique IPv6 Peers: {len(unique_ipv6_addresses)}")