# Peers.dat Parser

This Python script parses the `peers.dat` file from a Bitcoin or DigiByte directory and displays the unique IPv4 and IPv6 addresses of the peers seen by the node. It also provides counts of the total unique peers, unique IPv4 peers, and unique IPv6 peers.

The `peers.dat` file contains addresses and connection statistics of peers but does not contain any personally identifiable data. By looking at how many peers your local node has ever connected directly to we can achieve a rough metric for determining how decentralized a blockchain network may actually be. This does not mean all unique peers are currently active and if your node has been around for a long time this will be higher.

I will add more stats to this script as I think of it.

## Prerequisites

- Python 3.x installed on your system

## Usage

1. Clone the repository or download the `parse_peers_dat.py` script.
2. Locate the `peers.dat` file in your Bitcoin or DigiByte directory:

    **Bitcoin:**
    - Windows: `%APPDATA%\Bitcoin\peers.dat`
    - macOS: `~/Library/Application Support/Bitcoin/peers.dat`
    - Linux: `~/.bitcoin/peers.dat`

    **DigiByte:**
    - Windows: `%APPDATA%\DigiByte\peers.dat`
    - macOS: `~/Library/Application Support/DigiByte/peers.dat`
    - Linux: `~/.digibyte/peers.dat`

3. Update the `peers_dat_path` variable in the script with the path to your `peers.dat` file:
    ```python
    peers_dat_path = '/path/to/your/peers.dat'
    ```

4. Run the script:
    ```bash
    python parse_peers_dat.py
    ```

5. The script will display the unique IPv4 and IPv6 addresses of the peers, followed by the counts:
    ```plaintext
    IPv4 Addresses:
    192.168.0.1
    10.0.0.2
    ...

    IPv6 Addresses:
    2001:db8::1
    ...

    Total Unique DGB Peers Seen By This Node: 4760
    Total Unique IPv4 Peers: 4760
    Total Unique IPv6 Peers: 0
    ```

    The counts will reflect the actual numbers of unique peers found in your `peers.dat` file.

## How It Works

The script follows these steps to parse the `peers.dat` file:
- It opens the `peers.dat` file in binary mode and reads its contents.
- It initializes two sets, `ipv4_addresses` and `ipv6_addresses`, to store the unique IPv4 and IPv6 addresses respectively.
- It iterates over the file data, extracting the network address for each entry.
    - The network address is a 16-byte structure that contains either an IPv4 or IPv6 address.
        - If the first byte of the network address is `0`, it indicates an IPv4 address. The script extracts the 4-byte IP address using `socket.inet_ntop()` with `socket.AF_INET` and adds it to the `ipv4_addresses` set.
        - If the first byte of the network address is `1`, it indicates an IPv6 address. The script extracts the 16-byte IP address using `socket.inet_ntop()` with `socket.AF_INET6` and adds it to the `ipv6_addresses` set.
- The script moves to the next network address by skipping 30 bytes (16 bytes for the network address and 14 bytes for other metadata).
- Finally, the script displays the unique IPv4 and IPv6 addresses and prints the counts of total unique peers, unique IPv4 peers, and unique IPv6 peers.

**Note:** Make sure you have the necessary permissions to read the `peers.dat` file.

## License

This script is released under the MIT License.

