import os
import socket
import struct
import hashlib

def parse_peers_dat(filepath):
    with open(filepath, 'rb') as file:
        data = file.read()
        print("File read successfully. Data length:", len(data))

        # Parse header
        message_bytes = data[:4]
        version = data[4]
        key_size = data[5]
        new_address_count = struct.unpack("<I", data[38:42])[0]
        tried_address_count = struct.unpack("<I", data[42:46])[0]
        new_bucket_count = struct.unpack("<I", data[46:50])[0] ^ (1 << 30)

        # Parse peer entries
        offset = 50
        unique_addresses = set()
        ipv4_addresses = set()
        ipv6_addresses = set()

        for _ in range(new_address_count + tried_address_count):
            peer_data = data[offset:offset+62]
            ip = parse_ip_address(peer_data[16:32])
            if ip is not None:
                if ip.ip not in unique_addresses:
                    unique_addresses.add(ip.ip)
                    if ip.version == 4:
                        ipv4_addresses.add(ip)
                    elif ip.version == 6:
                        ipv6_addresses.add(ip)
            offset += 62

        # Verify data integrity
        assert len(ipv4_addresses) + len(ipv6_addresses) <= new_address_count + tried_address_count

        # Verify checksum
        checksum = data[-32:]
        calculated_checksum = hashlib.sha256(hashlib.sha256(data[:-32]).digest()).digest()
        assert checksum == calculated_checksum

        return ipv4_addresses, ipv6_addresses

def parse_ip_address(ip_bytes):
    if not ip_bytes:
        # Empty byte string
        return None
    elif ip_bytes[0] == 0 and len(ip_bytes) >= 16:
        # IPv4 address
        return IPAddress(socket.inet_ntop(socket.AF_INET, ip_bytes[12:16]), 4)
    elif len(ip_bytes) == 16:
        # IPv6 address
        return IPAddress(socket.inet_ntop(socket.AF_INET6, ip_bytes), 6)
    else:
        # Invalid IP address
        return None

class IPAddress:
    def __init__(self, ip, version):
        self.ip = ip
        self.version = version

    def __repr__(self):
        return self.ip

# Specify the path to the peers.dat file
peers_dat_path = '/home/digihash/.digibyte-qubit/peers.dat'

# Parse the peers.dat file
print("Parsing peers.dat file at:", peers_dat_path)
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
print("\nTotal Unique DGB Peers Seen By This Node: {}".format(total_unique_peers))
print("Total Unique IPv4 Peers: {}".format(len(unique_ipv4_addresses)))
print("Total Unique IPv6 Peers: {}".format(len(unique_ipv6_addresses)))