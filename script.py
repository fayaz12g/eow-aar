import os
import struct
from functions import *

def patch_blarc(aspect_ratio, HUD_pos, unpacked_folder):
    unpacked_folder = str(unpacked_folder)
    aspect_ratio = float(aspect_ratio)
    print(f"Aspect ratio is {aspect_ratio}")
    HUD_pos = str(HUD_pos)

    file_paths = {}

    def patch_blyt(filename, pane, operation, value):
        if operation in ["scale_x", "scale_y"]:
            if value < 1:
                command = "Squishing"
            elif value > 1:
                command = "Stretching"
            else:
                command = "Ignoring"
        elif operation in ["shift_x", "shift_y"]:
            command = "Shifting"
        
        print(f"{command} {pane} of {filename}")
        
        offset_dict = {'shift_x': 0x40, 'shift_y': 0x48, 'scale_x': 0x70, 'scale_y': 0x78}
        modified_name = filename + "_name"
        
        # Get all paths for the given filename
        paths = file_paths.get(modified_name, [])
        if not paths:
            # If no paths are found, create a default path and add it to the list
            default_path = os.path.join(unpacked_folder, "region_common", "ui", "GameMain", "blyt", f"{filename}.bflyt")
            paths.append(default_path)
        
        for full_path_of_file in paths:
            with open(full_path_of_file, 'rb') as f:
                content = f.read().hex()
            
            start_rootpane = content.index(b'RootPane'.hex())
            pane_hex = str(pane).encode('utf-8').hex()
            start_pane = content.index(pane_hex, start_rootpane)
            idx = start_pane + offset_dict[operation]
            content_new = content[:idx] + float2hex(value) + content[idx+8:]
            
            with open(full_path_of_file, 'wb') as f:
                f.write(bytes.fromhex(content_new))


    def patch_anim(source, filename, offset, value):
        modified_name = filename + "_name"
        
        # Get all paths for the given filename
        paths = anim_file_paths.get(modified_name, [])
        if not paths:
            # If no paths are found, create a default path and add it to the list
            default_path = os.path.join(unpacked_folder, "Layout", f"{source}.Nin_NX_NVN", "anim", f"{filename}.bflan")
            paths.append(default_path)
        
        # Iterate over each path and patch the corresponding file
        for anim_path in paths:
            with open(anim_path, 'rb') as f:
                content = f.read().hex()
            
            idx = offset
            content_new = content[:idx] + float2hex(value) + content[idx+8:]
            
            with open(anim_path, 'wb') as f:
                f.write(bytes.fromhex(content_new))

            
    blyt_folder = os.path.abspath(os.path.join(unpacked_folder))
    
    do_not_scale_rootpane = ["Fade", "ScreenCapture", "FrontBlindScreen", "ScreenMainMenu", "ScreenSubMenu", "StaffRoll"]
   
    rootpane_by_y = []

    # Initialize a dictionary to store lists of paths
    file_paths = {}
    file_names_stripped = []

    for root, dirs, files in os.walk(blyt_folder):
        for file_name in files:
            if file_name.endswith(".bflyt"):
                stripped_name = file_name.strip(".bflyt")
                file_names_stripped.append(stripped_name)
                full_path = os.path.join(root, file_name)
                modified_name = stripped_name + "_name"
                if modified_name not in file_paths:
                    file_paths[modified_name] = []
                file_paths[modified_name].append(full_path)

        # Initialize a dictionary to store lists of paths
    anim_file_paths = {}
    anim_file_names_stripped = []

    for root, dirs, files in os.walk(blyt_folder):
        for file_name in files:
            if file_name.endswith(".bflan"):
                stripped_name = file_name.strip(".bflan")
                anim_file_names_stripped.append(stripped_name)
                full_path = os.path.join(root, file_name)
                modified_name = stripped_name + "_name"
                if modified_name not in anim_file_paths:
                    anim_file_paths[modified_name] = []
                anim_file_paths[modified_name].append(full_path)

    
    if aspect_ratio >= 16/9:
        s1 = (16/9)  / aspect_ratio
        print(f"Scaling factor is set to {s1}")
        s2 = 1-s1
        s3 = s2/s1
        s4 = (16/10) / aspect_ratio
        
        for name in file_names_stripped:
            if name in do_not_scale_rootpane:
                    print(f"Skipping RootPane scaling of {name}")
            if name not in do_not_scale_rootpane:
                patch_blyt(name, 'RootPane', 'scale_x', s1)
            if name in rootpane_by_y:
                patch_blyt(name, 'RootPane', 'scale_y', 1/s1)
                patch_blyt(name, 'RootPane', 'scale_x', 1)

        patch_blyt('SubMenuHeader', 'N_Header_00', 'scale_x', 1/s1)
        patch_blyt('SubMenuHeader', 'N_Footer_00', 'scale_x', 1/s1)
        patch_blyt('MenuHeader', 'P_pict_04', 'scale_x', 1/s1)
        patch_blyt('MenuHeader', 'N_Header_00', 'scale_x', 1/s1)
        patch_blyt('MenuHeader', 'N_Footer_00', 'scale_x', 1/s1)
        patch_blyt('ScreenCapture', 'RootPane', 'scale_x', 1/s1)

        patch_blyt('L_CommonModal', 'P_footer_00', 'scale_x', 1/s1)
        patch_blyt('L_CommonModal', 'N_Win_00', 'scale_x', 1/s1)
        patch_blyt('L_CommonModal', 'S_Graphic_00', 'scale_x', 1/s1)


        if HUD_pos == 'corner':
            print("Shifitng elements for corner HUD")
            patch_blyt('Throbber', 'A_Save_00', 'shift_x', adjust_x(-900, s1))           
            patch_blyt('Counter', 'L_Cost_00', 'shift_x', adjust_x(711, s1))
            patch_blyt('HeartGaugeList', 'N_Life_00', 'shift_x', adjust_x(-903, s1))
            patch_blyt('SetSlotUseItem', 'L_SetItem_00', 'shift_x', adjust_x(866, s1))
            patch_blyt('SystemMenu', 'N_List_00', 'shift_x', adjust_x(-652, s1))
            patch_blyt('SystemMenu', 'L_ControllerKeyConfig_00', 'shift_x', adjust_x(355.79, s1))

            patch_blyt('LinkGauge', 'N_InOut_00', 'shift_x', adjust_x(-918, s1)) 
            patch_blyt('PartnerGauge', 'N_Offset_00', 'shift_x', adjust_x(838, s1)) 
            patch_blyt('PartnerGauge', 'W_window_02', 'shift_x', adjust_x(938, s1)) 

            patch_blyt('CollectMenu', 'N_ZeldaLinkItem_00', 'shift_x', adjust_x(-346, s1)) 
            patch_blyt('CollectMenu', 'L_Item_21', 'shift_x', adjust_x(-716, s1))
            patch_blyt('CollectMenu', 'N_Proof_00', 'shift_x', adjust_x(332, s1)) 
            patch_blyt('CollectMenu', 'N_StampCard_00', 'shift_x', adjust_x(122, s1))
            patch_blyt('CollectMenu', 'N_Bottle_00', 'shift_x', adjust_x(112, s1)) 
            patch_blyt('CollectMenu', 'N_PartnerLevel_00', 'shift_x', adjust_x(-352, s1))
            patch_blyt('CollectMenu', 'L_BtnChoice_00', 'shift_x', adjust_x(232, s1))

            patch_blyt('LinkItemMenu', 'A_Rupee_00', 'shift_x', adjust_x(766, s1))

            # Adjust the title in the title scene animation
            patch_blyt('Title', 'N_InOut_00', 'shift_x', adjust_x(-478, s1))


        # To mirror an object, do -x scale, and 180 roate y. For example, if we want to mirror something that is 

    else:
        s1 = aspect_ratio / (16/9)
        s2 = 1-s1
        s3 = s2/s1
        
        for name in file_names_stripped:
            if name in do_not_scale_rootpane:
                print(f"Skipping root pane scaling of {name}")
            if name not in do_not_scale_rootpane:
                print(f"Scaling root pane vertically for {name}")
                patch_blyt(name, 'RootPane', 'scale_y', s1)
             
    

        # if HUD_pos == 'corner':
        #     print("Shifitng elements for corner HUD")
