# ============================================================
# IPv4 SUBNET CALCULATOR — CASIO VERSION (same variables)
# ============================================================
# Same logic + same variable names as the PC version,
# but with short prompts and small-screen-friendly output.
# Includes two input modes:
#   1) Enter IP as A.B.C.D
#   2) Enter IP as 4 numbers (octets)
# ============================================================


def ipToInt(ip):
    octets = ip.strip().split(".")
    if len(octets) != 4:
        raise ValueError("IPv4 must have 4 octets")

    value = 0
    for part in octets:
        if part == "":
            raise ValueError("Empty octet")
        octet = int(part)
        if octet < 0 or octet > 255:
            raise ValueError("Octet must be 0-255")
        value = (value << 8) | octet

    return value & 0xFFFFFFFF


def intToIp(num):
    num = num & 0xFFFFFFFF
    first  = (num >> 24) & 255
    second = (num >> 16) & 255
    third  = (num >> 8)  & 255
    fourth = num & 255
    return str(first) + "." + str(second) + "." + str(third) + "." + str(fourth)


def subnetMaskFromCidr(cidr):
    if cidr < 0 or cidr > 32:
        raise ValueError("CIDR must be 0-32")
    if cidr == 0:
        return 0

    mask = ((1 << cidr) - 1) << (32 - cidr)
    return mask & 0xFFFFFFFF


def subnetInfo(ipInt, cidr):
    mask = subnetMaskFromCidr(cidr)

    network = (ipInt & mask) & 0xFFFFFFFF
    wildcard = (~mask) & 0xFFFFFFFF
    broadcast = (network | wildcard) & 0xFFFFFFFF

    hostBits = 32 - cidr

    if cidr == 32:
        usableHosts = 1
        first = network
        last = network
        note = "/32 single"

    elif cidr == 31:
        usableHosts = 2
        first = network
        last = broadcast
        note = "/31 p2p"

    else:
        usableHosts = (1 << hostBits) - 2
        first = (network + 1) & 0xFFFFFFFF
        last = (broadcast - 1) & 0xFFFFFFFF
        note = ""

    return mask, network, broadcast, first, last, usableHosts, note


def main():
    print("SubnetCalc Casio")
    print("1: A.B.C.D")
    print("2: 4 octets")
    mode = input("Mode(1/2): ").strip()

    try:
        if mode == "2":
            a = int(input("Oct1: "))
            b = int(input("Oct2: "))
            c = int(input("Oct3: "))
            d = int(input("Oct4: "))

            # Build the IP string using same variable name style
            ip = str(a) + "." + str(b) + "." + str(c) + "." + str(d)
            ipInt = ipToInt(ip)
        else:
            ip = input("IPv4: ").strip()
            ipInt = ipToInt(ip)

        cidr = int(input("CIDR(0-32): ").strip())

        mask, network, broadcast, first, last, hosts, note = subnetInfo(ipInt, cidr)

        print("IP:", ip + "/" + str(cidr))
        print("M :", intToIp(mask))
        print("N :", intToIp(network))
        print("B :", intToIp(broadcast))
        print("1 :", intToIp(first))
        print("L :", intToIp(last))
        print("H :", hosts)
        if note:
            print(note)

    except ValueError as e:
        print("Error:", e)


main()