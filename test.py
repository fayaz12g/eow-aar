def asm_to_hex(instruction):
    """Converts an ARM64 assembly instruction to its hexadecimal representation."""

    parts = instruction.split()
    opcode = parts[0]
    operands = parts[1:]

    if opcode == "mov":
        rd = int(operands[0][1:].replace(",", ""))  # Remove comma if present
        immediate = int(operands[1].replace("#0x", ""), 16)

        if len(operands) == 2:  # mov w9, #immediate
            hex_value = (0x52 << 24) | (immediate << 5) | rd
        else: #should not be reached
            hex_value = 0

    elif opcode == "movk":
        rd = int(operands[0][1:].replace(",", ""))  # Remove comma if present
        immediate = int(operands[1].replace("#0x", "").replace(",", ""), 16) # Remove comma here as well 
        shift = int(operands[3].replace("#", ""))

        hex_value = (0x72 << 24) | (shift // 16 << 21) | (immediate << 5) | rd

    else:
        # Handle other instructions if needed
        hex_value = 0

    return format(hex_value, '08X')  # Convert to 8-digit uppercase hex string


# Test function with example instructions
test_cases = [
    (f"mov w9, #0xe38e", "C9719C52"),
    (f"movk w9, #0x4018, lsl #16", "0903A872"),
    (f"mov w9, #0x4018", "09038852"),
    (f"movk w9, #0xe38e, lsl #16", "C971BC72"),
    (f"mov w9, #0x2014", "89028452"),
    (f"movk w9, #0xe99a, lsl #16", "4933BD72")
]

# Test each case
for instruction, expected in test_cases:
    result = asm_to_hex(instruction)
    print(f"Input:    {instruction}")
    print(f"Result:   {result}")
    print(f"Expected: {expected}")
    print()