# IPv4 Subnet Calculator (PC + Casio)

While preparing for CompTIA Network+, I wanted to truly understand subnetting instead of memorizing subnet tables.

So I built an IPv4 Subnet Calculator in Python from scratch and deployed the same logic onto a Casio fx-9750GIII graphing calculator.

This project demonstrates how routers compute network boundaries using bitwise operations.

------------------------------------------------------------

WHAT THIS PROJECT DEMONSTRATES

- Packing IPv4 addresses into 32-bit integers
- Generating subnet masks from CIDR prefixes
- Calculating:
  - Network address
  - Broadcast address
  - First usable host
  - Last usable host
  - Total usable hosts
- Using bitwise operations:
  - << (left shift)
  - >> (right shift)
  - &  (AND)
  - |  (OR)
  - ~  (NOT)
- Handling special cases:
  - /31 point-to-point networks
  - /32 single host networks

Core networking logic implemented:

network   = ip & mask  
broadcast = network | wildcard  
usable    = 2^(host_bits) - 2  

------------------------------------------------------------

PC VERSION

File:
pc-version/subnet-calculator_pc.py

Run:
python pc-version/subnet-calculator_pc.py

Example Input:
192.168.1.10
24

Example Output:
Subnet Mask:     255.255.255.0
Network:         192.168.1.0
Broadcast:       192.168.1.255
First Usable:    192.168.1.1
Last Usable:     192.168.1.254
Usable Hosts:    254

------------------------------------------------------------

CASIO VERSION (fx-9750GIII Python)

File:
casio-version/subnet_calculator_casio.py

INSTALLATION STEPS

1. Connect calculator to PC via USB.
2. Select "USB Flash / Mass Storage" mode.
3. Open the calculator drive in File Explorer.
4. Copy the .py file into the root or PYTHON folder.
5. Safely eject the drive.
6. Open the Python app on the calculator.
7. Run the program.

Example Casio Input:
192.168.2.0/25

Example Casio Output:
M : 255.255.255.128
N : 192.168.2.0
B : 192.168.2.127
1 : 192.168.2.1
L : 192.168.2.126
H : 126

------------------------------------------------------------

SCREENSHOTS

File transferred to calculator:
casio-version/docs/screenshots/casio_plugged_on_pc.png

Python app open:
casio-version/docs/screenshots/casio_python_app.png

Program selected:
casio-version/docs/screenshots/casio_program_menu.png

Example output:
casio-version/docs/screenshots/casio_output_example.png

------------------------------------------------------------

WHY I BUILT THIS

Subnetting is often taught through memorization.
Building the logic forced me to understand:

- Binary representation of IP addresses
- Network vs host bit boundaries
- CIDR block sizing
- How routers perform masking internally

This project strengthened my networking fundamentals while preparing for CompTIA Network+.

------------------------------------------------------------

FUTURE IMPROVEMENTS

- Binary visualization mode
- Subnet quiz mode
- Block size calculator
- IPv6 version
