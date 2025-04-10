# 🧮 Python Subnet Calculator

A command-line subnet calculator written in Python that helps you:
- Validate and parse IPv4 addresses
- Calculate subnet masks based on the number of required subnets
- Determine broadcast addresses, first/last hosts, and total hosts
- Enumerate all subnet ranges from a base network

Useful for **students**, **network engineers**, and **anyone learning subnetting and IP math**.

---

## 📌 Features

- CIDR input (`/mask`) with subnet split calculation
- IPv4 validation (format, range)
- Binary and dotted-decimal format conversion
- Broadcast address calculation
- Subnet enumeration: network address, broadcast, first/last usable host
- Supports subnetting down to `/31` and `/32`

---

## 🧪 Sample Usage

```bash
$ python subnet_calculator.py
Enter IPv4 Address (e.g. 10.10.10.10): 192.168.1.0
Enter the original subnet mask (0-32): /24
Enter the number of desired subnets: 4


========================== RESULTS ==========================
Original IP:                192.168.1.0
Original CIDR:              /24 (255.255.255.0)
Base Network (Dotted):      192.168.1.0
Base Network (Binary):      11000000.10101000.00000001.00000000

Desired Subnets:            4
New Mask (CIDR):            /26 (255.255.255.192)
Bits Borrowed:              2
Total Subnets Created:      4
Hosts per Subnet:           62  (with /26)
=============================================================

------- Subnet Ranges -------
Subnet #1 => Network: 192.168.1.0/26
  Broadcast: 192.168.1.63
  First Host: 192.168.1.1   Last Host: 192.168.1.62
-------------------------------------------------------------
...
