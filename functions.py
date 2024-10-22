import struct
# from keystone import *

import binascii
import math
import os
# from keystone.keystone_const import *

# from keystone import Ks, KS_ARCH_ARM64, KS_MODE_LITTLE_ENDIAN


def make_movz_hex(immediate, reg):
    # MOVZ (1101 0101 op 1 hw Rd)
    opcode = 0b1101010101000000
    imm = (immediate & 0xFFFF) << 5
    reg_code = reg & 0b11111  # lower 5 bits for the register
    instruction = opcode | imm | reg_code
    hex_value = '{:08x}'.format(instruction).upper()
    return hex_value

def make_movk_hex(immediate, reg, shift):
    # MOVK (1111 0101 op 1 hw Rd)
    opcode = 0b1111010101000000
    imm = (immediate & 0xFFFF) << 5
    shift_code = (shift // 16) << 21  # Determine hw field from shift
    reg_code = reg & 0b11111  # lower 5 bits for the register
    instruction = opcode | shift_code | imm | reg_code
    hex_value = '{:08x}'.format(instruction).upper()
    return hex_value



def make_hex(x, r):
    p = math.floor(math.log(x, 2))
    a = round(16*(p-2) + x / 2**(p-4))
    if a<0: a += 128
    a = 2*a + 1
    h = hex(a).lstrip('0x').rjust(2,'0').upper()
    hex_value = f'0{r}' + h[1] + '02' + h[0] + '1E' 
    print(hex_value)
    return hex_value

def hex2float(h):
    return struct.unpack('<f', struct.pack('>I', int(h, 16)))[0]

# def asm_to_hex(asm_code):
#     ks = Ks(KS_ARCH_ARM64, KS_MODE_LITTLE_ENDIAN)
#     encoding, count = ks.asm(asm_code)
#     return ''.join('{:02x}'.format(x) for x in encoding)

def eow_hex23(num):
    num = round(num, 15)
    packed = struct.pack('!f', num)
    full_hex = ''.join('{:02x}'.format(b) for b in packed)
    hex_1 = full_hex[:4]  # Upper 16 bits
    hex_2 = full_hex[4:]  # Lower 16 bits
    
    # Convert to decimal for MOVZ/MOVK functions
    imm_1 = int(hex_1, 16)
    imm_2 = int(hex_2, 16)
    
    # Register 9 for w9
    reg = 9
    
    # Use manual conversion functions
    hex_value1 = make_movz_hex(imm_2, reg)
    hex_value2 = make_movk_hex(imm_1, reg, shift=16)
    
    return hex_value1, hex_value2


def float2hex(f):
        return hex(struct.unpack('>I', struct.pack('<f', f))[0]).lstrip('0x').rjust(8,'0').upper()

# This one finds the correct translation in correleation to the aspect ratio
def do_some_math(num, ratio):
    num = int(num)
    ratio = int(ratio)
    return ((num/(16/9))*ratio)

# This one finds the inverse value from the middle of the pane
def do_special_math(num, ratio):
    num = int(num)
    ratio = int(ratio)
    newnum = do_some_math(num, ratio)
    return ((newnum*-1)+num)

# This one is weird, and halfs the translation
def do_weirder_math(num, ratio):
    num = int(num)
    ratio = int(ratio)
    newnum = do_some_math(num, ratio)
    newernum = (abs(newnum) - abs(num))/2
    return (newernum+newnum)

# This one moves the element the same amount Mario Lives is moved
def do_specific_math(num, ratio):
    num = int(num)
    ratio = int(ratio)
    lives = int(651)
    newnum = do_some_math(lives, ratio)
    newernum = (abs(newnum) - lives)
    return (newernum+num)

def add_aar_tag(file_path):
    old_hex_str = '4E 00 69 00 6E 00 74 00 65 00 6E 00 64 00 6F 00'
    new_hex_str = '4E 00 69 00 6E 00 74 00 65 00 6E 00 64 00 6F 00 20 00 7C 00 20 00 41 00 6E 00 79 00 41 00 73 00 70 00 65 00 63 00 74 00 52 00 61 00 74 00 69 00 6F 00 20 00 62 00 79 00 20 00 46 00 61 00 79 00 61 00 00'

    old_hex = bytes.fromhex(old_hex_str)
    new_hex = bytes.fromhex(new_hex_str)

    with open(file_path, 'rb') as file:
        file_data = file.read()
    
    new_data = file_data.replace(old_hex, new_hex)
    
    with open(file_path, 'wb') as file:
        file.write(new_data)
    print("Added AAR Splash")
