import os
import math
from functions import *

def create_patch_files(patch_folder, ratio_value, scaling_factor, visual_fixes):

    visual_fixesa = visual_fixes[0]
    scaling_factor = float(scaling_factor)
    ratio_value = float(ratio_value)
    print(f"The scaling factor is {scaling_factor}.")
    hex_value1, hex_value2= eow_hex23(ratio_value)
    version_variables = ["1.0.1"]
    for version_variable in version_variables:
        file_name = f"main-{version_variable}.pchtxt"
        file_path = os.path.join(patch_folder, file_name)

        if version_variable == "1.0.1":
            nsobidid = "09A15C8259828A41B91B036B12F0687973A4627A"
            replace1 = "0045fd90"
            replace2 = "0045fd94"
            visual_fix = visual_fixesa

        patch_content = f'''@nsobid-{nsobidid}

@flag print_values
@flag offset_shift 0x100

@enabled
00348b6c {hex_value1}
00348b70 {hex_value2}
@disabled

{visual_fix}

// Generated using EOW-AAR by Fayaz (github.com/fayaz12g/eow-aar)
// Made possible by Fl4sh_#9174'''
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as patch_file:
            patch_file.write(patch_content)
        print(f"Patch file created: {file_path}")
