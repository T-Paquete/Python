import math


# ==================== USER INPUT ====================
# Ask user for IP and subnet mask
input_ipv4_address = input("Enter IPv4 Address (e.g. 10.10.10.10): ")

try:
    original_mask = int(input("Enter the original subnet mask (0-32): /"))
    number_of_subnets = int(input("Enter the number of desired subnets: "))
except ValueError:
    print("Enter a valid number for the subnet mask.")
    exit(1)  # Stop execution if invalid


# ==================== SUBNET MASK CALCULATION ====================
def calculate_new_subnet_mask_for_subnets(base_mask, desired_subnets):
    """
    Take the original mask and desired_subnets.
    Calculate how many bits to borrow and what the new mask is.
    Return: new_mask, total_possible_subnets, bits_to_borrow.
    """
    if not (0 <= base_mask <= 32):
        raise ValueError("CIDR must be between 0 and 32.")
    if desired_subnets <= 0:
        raise ValueError("Number of subnets must be positive.")
    
    # Calculate: 2^bits_to_borrow >= desired_subnets
    # Round up to the nearest integer
    bits_to_borrow = math.ceil(math.log2(desired_subnets))
    new_mask = base_mask + bits_to_borrow
    
    if new_mask > 32:
        raise ValueError(
            f"Cannot create {desired_subnets} subnets from /{base_mask} because /{new_mask} is > /32."
        )
    
    # Calculate total subnets
    total_subnets = 2 ** bits_to_borrow

    return new_mask, total_subnets, bits_to_borrow


# ==================== IP VALIDATION & CONVERSION ====================
def get_ip_address(ip_string):
    """
    Validate the IP string.
    Return: dotted_decimal, binary.
    """
    # Clean whitespace and split by '.'
    parts = ip_string.strip().split('.')

    # Validate the number of octets
    if len(parts) != 4:
        raise ValueError("The IPv4 address must have exactly four octets.")
    
    octets_decimal = []
    octets_binary = []

    for part in parts:
        # Check if part is a number
        if not part.isdigit():
            raise ValueError(f"Octet '{part}' is not a valid number.")
        # Check if part is in the range 0-255
        octet_value = int(part)
        if octet_value < 0 or octet_value > 255:
            raise ValueError(f"Octet '{part}' is outside 0-255 range.")
        
        # Append to the lists as string for later joining
        octets_decimal.append(str(octet_value))
        octets_binary.append(format(octet_value, '08b'))

    # Join the octets to form the dotted-decimal and binary representations
    dotted_decimal_ip = '.'.join(octets_decimal)
    binary_format_ip = '.'.join(octets_binary)
    return dotted_decimal_ip, binary_format_ip


# ==================== CIDR TO MASK CONVERSION ====================
def cidr_to_subnet_mask(cidr_int):
    """
    Convert CIDR to:
        - dotted-decimal format (e.g., 255.255.255.0)
        - binary format (e.g., 11111111.11111111.11111111.00000000)
    """
    # Check if CIDR is valid
    if not (0 <= cidr_int <= 32):
        raise ValueError("CIDR must be in [0..32].")
    
    # Create binary mask
    # 1s for the network part, 0s for the host part
    # e.g., /24 => 11111111.11111111.11111111.00000000
    binary_mask = '1' * cidr_int + '0' * (32 - cidr_int)

    # Split into 4 octets of 8 bits each
    # Convert each octet from binary to decimal
    octets_binary = [binary_mask[i:i+8] for i in range(0, 32, 8)]
    octets_decimal = [str(int(bit, 2)) for bit in octets_binary]

    # Join the octets to form the dotted-decimal and binary representations
    dotted_decimal_mask = '.'.join(octets_decimal)
    binary_format_mask = '.'.join(octets_binary)

    return dotted_decimal_mask, binary_format_mask


# ==================== NETWORK ADDRESS ====================
def get_network_address(ip_binary, mask_binary):
    """
    Performs a bitwise AND between the binary IP and subnet mask.
    Returns:
        - network address in dotted-decimal and binary format
    """
    # Remove dots to get raw binary strings
    ip_raw = ip_binary.replace('.', '')
    mask_raw = mask_binary.replace('.', '')

    # Convert binary strings to integers (base 2)
    ip_int = int(ip_raw, 2)
    mask_int = int(mask_raw, 2)

    # Perform bitwise AND to get the network address
    network_int = ip_int & mask_int
    network_binary = format(network_int, '032b')

    # Split the binary string into 4 octets of 8 bits each
    network_octets_binary = [network_binary[i:i+8] for i in range(0, 32, 8)]
    network_octets_decimal = [str(int(octet, 2)) for octet in network_octets_binary]

    # Join the octets to form the dotted-decimal and binary representations
    network_binary_format = '.'.join(network_octets_binary)
    network_dotted_format = '.'.join(network_octets_decimal)

    return network_dotted_format, network_binary_format


# ==================== HOST CALCULATION ====================
def calculate_possible_hosts(cidr_int):
    """
    Returns number of usable hosts based on CIDR mask.
    Special cases:
        /31 = 2 (used in point-to-point)
        /32 = 1 (single host)
    """
    if cidr_int == 32:
        return 1
    elif cidr_int == 31:
        return 2
    else:
        # 2^(host_bits) - 2
        return (2 ** (32 - cidr_int)) - 2


# ==================== CONVERT INT TO DOTTED IP ====================
def int_to_dotted(ip_int):
    """
    Converts a 32-bit integer to a dotted-decimal IPv4 address.
    Takes an integer and converts it to a string in the format "x.x.x.x".
    Example: 3232235777 → "192.168.1.1"
    """
    # List to hold the 4 octets
    octets = []

    # Extract each of the 4 bytes from the integer
    #We go from left to right (most significant byte to least), meaning:
        # i = 3 → first byte (bits 24–31)
        # i = 2 → second byte (bits 16–23)
        # i = 1 → third byte (bits 8–15)
        # i = 0 → fourth byte (bits 0–7)
    # Each octet is 8 bits, so we shift right by 8 * i bits
    # and mask with 0xFF to get the last 8 bits
    # The loop goes from 3 to 0 (4 octets)
    # 0xFF is 255 in decimal, which is the max value for an octet
    for i in range(3, -1, -1):                      # i = 3, 2, 1, 0
        shift_amount = 8 * i                        # Calculate how many bits to shift
        octet = (ip_int >> shift_amount) & 0xFF     # >>: Shifts the bits to the right
        octets.append(str(octet))                   # Convert to string

    # Join the 4 octet strings into a dotted IP address
    dotted_ip = '.'.join(octets)
    return dotted_ip


# ==================== ENUMERATE SUBNET RANGES ====================
def get_subnet_ranges(base_network_int, new_mask, total_subnets):
    """
    Enumerate each of the sub-subnets under the new_mask.
    Return a List of dicts containing: 
            - network
            - broadcast
            - first_host
            - last_host
    """
    # Each subnet's size in IP addresses (including network & broadcast):
    # The size of each subnet is 2^(32 - new_mask)
    subnet_size = 2 ** (32 - new_mask)
    
    # Placeholder for subnet information
    # Each subnet will be a dictionary with its details
    subnets_info = []

    # Loop through the number of subnets
    # Each subnet is an increment of the base network address
    # by the size of the subnet
    for i in range(total_subnets):
        # Calculate this subnet's network address (integer)
        subnet_network_int = base_network_int + (i * subnet_size)
        # Broadcast address is one less than the next subnet's network
        # or (subnet_network_int + subnet_size - 1)
        subnet_broadcast_int = subnet_network_int + subnet_size - 1

        # Convert them to dotted
        subnet_network_dotted = int_to_dotted(subnet_network_int)
        subnet_broadcast_dotted = int_to_dotted(subnet_broadcast_int)

        # Calculate first/last host
        if new_mask >= 31:
            first_host = "N/A"
            last_host = "N/A"
        else:
            first_host = int_to_dotted(subnet_network_int + 1)
            last_host = int_to_dotted(subnet_broadcast_int - 1)

        sub_dict = {
            "subnet_index": i + 1,
            "network": subnet_network_dotted,
            "broadcast": subnet_broadcast_dotted,
            "first_host": first_host,
            "last_host": last_host
        }
        subnets_info.append(sub_dict)

    return subnets_info


# ==================== BROADCAST ADDRESS ====================
def get_broadcast_address(ip_binary, mask_binary):
    """
    broadcast = IP | (~mask)
    Return: broadcast_binary, broadcast_dotted.
    """
    # Remove dots to get raw binary strings
    ip_raw = ip_binary.replace('.', '')
    mask_raw = mask_binary.replace('.', '')

    # Convert binary strings to integers (base 2)
    ip_int = int(ip_raw, 2)
    mask_int = int(mask_raw, 2)

    # Perform bitwise NOT on the mask and then OR with the IP
    # ~mask gives us the inverted mask
    # ~mask is a bitwise NOT operation, which flips all bits
    inverted_mask = ~mask_int & 0xFFFFFFFF
    broadcast_int = ip_int | inverted_mask

    # Convert the broadcast address back to binary
    # Format the integer as a 32-bit binary string
    # '032b' means 32 bits, padded with zeros if necessary
    broadcast_binary = format(broadcast_int, '032b')
    broadcast_octets_binary = [broadcast_binary[i:i+8] for i in range(0, 32, 8)]
    broadcast_octets_decimal = [str(int(octet, 2)) for octet in broadcast_octets_binary]

    # Join the octets to form the dotted-decimal and binary representations
    broadcast_binary_format = '.'.join(broadcast_octets_binary)
    broadcast_dotted_format = '.'.join(broadcast_octets_decimal)
    return broadcast_binary_format, broadcast_dotted_format


# ==================== MAIN EXECUTION ====================
# 1) Calculate the new mask and total subnets

try:
    # Validate the original mask
    new_mask, total_subnets, bits_borrowed = calculate_new_subnet_mask_for_subnets(original_mask, number_of_subnets)
except ValueError as e:
    print("Error:", e)
    exit(1)

# 2) Convert user IP to dotted & binary
try:
    dotted_decimal_ip, binary_format_ip = get_ip_address(input_ipv4_address)
except ValueError as e:
    print("Error:", e)
    exit(1)

# 3) Convert original_mask to dotted/binary 
# We want the *original* mask to find the base network.
orig_mask_dotted, orig_mask_binary = cidr_to_subnet_mask(original_mask)

# 4) Base Network Address with *original* mask
base_network_dotted, base_network_binary = get_network_address(binary_format_ip, orig_mask_binary)

# 5) Convert base_network_address to integer
base_network_int = int(base_network_binary.replace('.', ''), 2)

# 6) Summarize new_mask info
new_mask_dotted, new_mask_binary = cidr_to_subnet_mask(new_mask)
hosts_per_subnet = calculate_possible_hosts(new_mask)

# 7) Enumerate each new subnet
all_subnets = get_subnet_ranges(base_network_int, new_mask, total_subnets)


# ==================== OUTPUT RESULTS ====================
print("\n========================== RESULTS ==========================")
print(f"Original IP:                {dotted_decimal_ip}")
print(f"Original CIDR:              /{original_mask} ({orig_mask_dotted})")
print(f"Base Network (Dotted):      {base_network_dotted}")
print(f"Base Network (Binary):      {base_network_binary}")
print(f"\nDesired Subnets:            {number_of_subnets}")
print(f"New Mask (CIDR):            /{new_mask} ({new_mask_dotted})")
print(f"Bits Borrowed:              {bits_borrowed}")
print(f"Total Subnets Created:      {total_subnets}")
print(f"Hosts per Subnet:           {hosts_per_subnet}  (with /{new_mask})")
print("=============================================================\n")

print("------- Subnet Ranges -------")
for subnet in all_subnets:
    print(f"Subnet #{subnet['subnet_index']} => Network: {subnet['network']}/{new_mask}")
    print(f"  Broadcast: {subnet['broadcast']}")
    print(f"  First Host: {subnet['first_host']}   Last Host: {subnet['last_host']}")
    print("-------------------------------------------------------------")
