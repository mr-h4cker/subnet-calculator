
# ============================================================
# IPv4 SUBNET CALCULATOR — LOGIC EXPLAINED IN COMMENTS
# ============================================================
# This program shows how subnetting works internally using
# bit operations. Every step explains what happens so the
# logic is easy to follow even if you are learning.
#
# Concepts demonstrated:
# - Packing IPv4 into 32 bits
# - Building subnet masks from CIDR
# - Finding network address
# - Finding broadcast address
# - Determining usable host range
# ============================================================


def ipToInt(ip):
    # --------------------------------------------------------
    # Convert a dotted IPv4 string like "192.168.1.10"
    # into one 32-bit number.
    #
    # Each octet is 8 bits:
    #   192 | 168 | 1 | 10
    #
    # We repeatedly:
    #   shift left by 8 bits (make space)
    #   insert next octet
    #
    # This is like stacking bytes together.
    # --------------------------------------------------------

    octets = ip.strip().split(".")

    if len(octets) != 4:
        raise ValueError("IPv4 must have 4 octets")

    value = 0

    for part in octets:
        octet = int(part)

        if octet < 0 or octet > 255:
            raise ValueError("Octet must be 0–255")

        # Shift existing bits left by 8.
        # This moves previous bytes to higher positions.
        #
        # Example:
        #   11000000 becomes
        #   11000000 00000000
        value = value << 8

        # Insert new octet into the empty space.
        value = value | octet

    return value


def intToIp(num):
    # --------------------------------------------------------
    # Convert a 32-bit number back to dotted format.
    #
    # We extract each byte by:
    #   shifting right to bring desired byte down
    #   masking with 255 (11111111) to keep only 8 bits
    # --------------------------------------------------------

    first  = (num >> 24) & 255
    second = (num >> 16) & 255
    third  = (num >> 8)  & 255
    fourth = num & 255

    return f"{first}.{second}.{third}.{fourth}"


def subnetMaskFromCidr(cidr):
    # --------------------------------------------------------
    # Build a subnet mask from CIDR prefix length.
    #
    # Example: /24 means
    #   first 24 bits = network (1s)
    #   last 8 bits  = hosts (0s)
    #
    # Steps:
    # 1. Create number with cidr ones
    # 2. Shift into left side of 32 bits
    #
    # (1 << cidr) creates a 1 followed by zeros.
    # Subtracting 1 turns it into all ones.
    # --------------------------------------------------------

    if cidr < 0 or cidr > 32:
        raise ValueError("CIDR must be between 0 and 32")

    if cidr == 0:
        return 0

    mask = ((1 << cidr) - 1) << (32 - cidr)
    return mask


def subnetInfo(ipInt, cidr):
    # --------------------------------------------------------
    # Compute subnet details using bit logic.
    # --------------------------------------------------------

    mask = subnetMaskFromCidr(cidr)

    # NETWORK ADDRESS:
    # AND operation keeps network bits and clears host bits.
    #
    # Wherever mask has 1 → keep IP bit
    # Wherever mask has 0 → result becomes 0
    network = ipInt & mask

    # WILDCARD MASK:
    # Flip bits of mask so host bits become 1.
    # Limit to 32 bits because integers are unlimited.
    wildcard = (~mask) & 0xFFFFFFFF

    # BROADCAST ADDRESS:
    # OR operation fills host bits with 1s.
    broadcast = network | wildcard

    hostBits = 32 - cidr

    if cidr == 32:
        usableHosts = 1
        first = network
        last = network
        note = "/32 — single address"

    elif cidr == 31:
        usableHosts = 2
        first = network
        last = broadcast
        note = "/31 — point-to-point"

    else:
        # Total combinations minus network and broadcast.
        usableHosts = (1 << hostBits) - 2

        # First usable is one above network.
        first = network + 1

        # Last usable is one below broadcast.
        last = broadcast - 1

        note = ""

    return mask, network, broadcast, first, last, usableHosts, note


def main():
    print("=== IPv4 Subnet Calculator ===")

    ip = input("Enter IPv4 (e.g., 192.168.1.10): ").strip()
    cidr = int(input("Enter CIDR prefix (0–32): ").strip())

    ipInt = ipToInt(ip)

    mask, network, broadcast, first, last, hosts, note = subnetInfo(ipInt, cidr)

    print("\n--- Results ---")
    print("IP:            ", ip, f"/{cidr}")
    print("Subnet Mask:   ", intToIp(mask))
    print("Network:       ", intToIp(network))
    print("Broadcast:     ", intToIp(broadcast))
    print("First Usable:  ", intToIp(first))
    print("Last Usable:   ", intToIp(last))
    print("Usable Hosts:  ", hosts)

    if note:
        print("Note:          ", note)


main()

