import os
import struct
from functions import *

def patch_blarc(aspect_ratio, HUD_pos, unpacked_folder, expiremental_menu):
    unpacked_folder = str(unpacked_folder)
    aspect_ratio = float(aspect_ratio)
    print(f"Aspect ratio is {aspect_ratio}")
    HUD_pos = str(HUD_pos)
    # expiremental_menu = eval(expiremental_menu)

    file_paths = {}

    broken_names = ["PaMenu_Btn_Level", "PaMenu_Btn_Slot"]
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
            default_path = os.path.join(unpacked_folder, "Layout", f"{filename}.Nin_NX_NVN", "blyt", f"{filename}.bflyt")
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
    
    do_not_scale_rootpane = []
   
    rootpane_by_y = []

    # # Add the AAR Tag on the splash before scaling
    # splash1 = os.path.join(unpacked_folder, "Layout", f"GameSplashScreen_00.Nin_NX_NVN", "blyt", f"GameSplashScreen_00.bflyt")
    # splash2 = os.path.join(unpacked_folder, "UI", "LayoutArchive", f"Menu.Product.100.Nin_NX_NVN", "blyt", f"GameSplashScreen_00.bflyt")
    # add_aar_tag(splash1)
    # add_aar_tag(splash2)

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

# TODO
# fix game confimration (controller, exit)

        # Fix indicators!!! Mini mario, player 1 and 2

        # patch_blyt('PlayerIndicator_00', 'RootPane', 'scale_x', s1/2) #Mario Bubble
        # patch_blyt('PlayerIndicator_01', 'RootPane', 'scale_x', s1/2) #Toad Bubble
        # patch_blyt('MiniMarioIndicator', 'RootPane', 'scale_x', s1/2)
        # patch_blyt('BarrelIndicator', 'RootPane', 'scale_x', s1/2)

        if expiremental_menu:
            print("Doing Expirements!")
            # Expiremental Changes, Expands the Level Select Window to be wider so the UI on the sides doesn't look empty (space to L+R)!
            patch_blyt('GameLevelSelect_00', 'T_ArrowR_00', 'shift_x', do_specific_math(805, aspect_ratio))
            patch_blyt('GameLevelSelect_00', 'P_ArrowR_00', 'shift_x', do_specific_math(840, aspect_ratio))
            patch_blyt('GameLevelSelect_00', 'T_ArrowL_00', 'shift_x', do_specific_math(-805, aspect_ratio))
            patch_blyt('GameLevelSelect_00', 'P_ArrowL_00', 'shift_x', do_specific_math(-840, aspect_ratio))
            patch_blyt('GameLevelSelect_00', 'L_Levels_P0', 'shift_x', do_specific_math(-3266, aspect_ratio))
            patch_blyt('GameLevelSelect_00', 'L_Levels_P1', 'shift_x', do_specific_math(-1648, aspect_ratio))
            patch_blyt('GameLevelSelect_00', 'L_Levels', 'scale_x', 1/s1)
            patch_blyt('GameLevelSelect_00', 'L_Levels_N1', 'shift_x', do_specific_math(3266, aspect_ratio))
            patch_blyt('GameLevelSelect_00', 'L_Levels_N0', 'shift_x', do_specific_math(1648, aspect_ratio))
            patch_blyt('PaMenu_Btn_Level', 'RootPane', 'scale_x', 1/s1)



        if HUD_pos == 'corner':
            print("Shifitng elements for corner HUD")
            patch_blyt('PaFooter_00', 'L_Select_01', 'shift_x', do_some_math(223.96, aspect_ratio))
            patch_blyt('PaFooter_00', 'L_ButtonB_01', 'shift_x', do_some_math(409.02, aspect_ratio))
            patch_blyt('PaFooter_00', 'L_ButtonX_01', 'shift_x', do_some_math(-645.74, aspect_ratio))
            patch_blyt('PaFooter_00', 'L_ButtonA_01', 'shift_x', do_some_math(779.14, aspect_ratio))
            patch_blyt('PaFooter_00', 'L_Special_00', 'shift_x', do_some_math(-830.79, aspect_ratio))
            patch_blyt('PaFooter_00', 'L_ButtonX_00', 'shift_x', do_some_math(-645.74, aspect_ratio))

            patch_blyt('GameSplashScreen_00', 'P_pict_Mario', 'shift_x', do_some_math(-542, aspect_ratio))
            patch_blyt('GameSplashScreen_00', 'P_pict_Mario', 'shift_y', do_some_math(80, aspect_ratio))
            patch_blyt('GameSplashScreen_00', 'P_pict_DK', 'shift_x', do_some_math(450, aspect_ratio))
            # patch_blyt('GameSplashScreen_00', 'P_pict_Mario', 'shift_y', do_some_math(200, aspect_ratio))
            # patch_blyt('GameSplashScreen_00', 'P_pict_DK', 'shift_x', do_some_math(-200, aspect_ratio))


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
             
        patch_blyt('Pa_CongratsWorldClearBanner', 'P_Banner', 'scale_y', 1/s1)
        patch_blyt('GameLevelWin_00', 'L_World', 'scale_y', 1/s1)
        patch_blyt('GameLevelWin_00', 'N_null_00', 'scale_y', do_some_math(-495, aspect_ratio))
        patch_blyt('GameOver_00', 'P_BG', 'scale_y', 1/s1)
        patch_blyt('GameModeChoice_00', 'P_BG', 'scale_y', 1/s1)
        patch_blyt('GameModeChoice_00', 'P_Background', 'scale_y', 1/s1)
        patch_blyt('GameModeChoice_00', 'L_Blur', 'scale_y', 1/s1)
        patch_blyt('GameLevelSelect_00', 'N_Background', 'scale_y', 1/s1)
        patch_blyt('GameLevelSelect_00', 'P_Cutout', 'scale_y', 1/s1)
        patch_blyt('GameLevelSelect_00', 'P_Cutout', 'scale_y', 1/s1)
        patch_blyt('GameLevelSelect_00', 'P_HeaderBG_01', 'scale_y', do_some_math(433, aspect_ratio))
        patch_blyt('GameLevelSelect_00', 'P_HeaderBG_02', 'scale_y', do_some_math(431, aspect_ratio))
        patch_blyt('GameLevelSelect_00', 'P_HeaderBGShadow_00', 'scale_y', do_some_math(433, aspect_ratio))
        patch_blyt('GameLevelSelect_00', 'L_GameMode', 'shift_y', do_some_math(-130, aspect_ratio))
        patch_blyt('GameLevelSelect_00', 'L_StarScore', 'shift_y', do_some_math(440, aspect_ratio))
        patch_blyt('GameLevelSelect_00', 'L_Lives', 'shift_y', do_some_math(440, aspect_ratio))
        # patch_blyt('GameLevelSelect_00', 'L_2P_Header', 'shift_y', do_some_math(710, aspect_ratio))
        patch_blyt('GameLevelSelect_00', 'P_Icon', 'shift_y', do_some_math(425, aspect_ratio))
        patch_blyt('GameLevelSelect_00', 'T_WorldName_00', 'shift_y', do_some_math(415, aspect_ratio))
        patch_blyt('GameLevelHUD_00', 'P_BorderL', 'shift_y', -2500)
        patch_blyt('GameLevelHUD_00', 'P_BorderR', 'shift_y', 2500)
        patch_blyt('GameLevelHUD_00', 'L_Lives', 'shift_y', do_some_math(-60, aspect_ratio))
        patch_blyt('GameLevelHUD_00', 'N_Blocks', 'shift_y', do_some_math(-64, aspect_ratio))
        patch_blyt('GameLevelHUD_00', 'N_DK', 'shift_y', do_some_math(-130, aspect_ratio))
        patch_blyt('GameLevelHUD_00', 'N_TimeAttack', 'scale_y', 1/s1)
        patch_blyt('GameLevelHUD_00', 'N_TA_Timer', 'scale_y', s1)
        patch_blyt('GameLevelHUD_00', 'N_TA_Timer', 'shift_y', do_some_math(305, aspect_ratio))
        patch_blyt('GameLevelHUD_00', 'N_Time', 'shift_y', do_some_math(-60, aspect_ratio))
        patch_blyt('GameLevelHUD_00', 'N_Collectable', 'shift_y', do_some_math(-130, aspect_ratio))
        patch_blyt('GameLevelPauseMenu_00', 'L_Blur', 'scale_y', 1/s1)
        patch_blyt('Cutscene_Skip', 'L_Skip_00', 'shift_y', do_some_math(-480, aspect_ratio))
        patch_blyt('CongratsScreen', 'P_Logo', 'shift_y', do_some_math(-480, aspect_ratio))
        patch_blyt('GameMainMenu_00', 'P_BlackPanel', 'scale_y', 1/s1)
        patch_blyt('GameSplashScreen_00', 'P_BG_Gray', 'scale_y', 1/s1)
        patch_blyt('GameSplashScreen_00', 'P_pict_Mario', 'shift_y', do_some_math(-480, aspect_ratio))
        patch_blyt('GameSplashScreen_00', 'P_pict_DK', 'shift_y', do_some_math(480, aspect_ratio))
        patch_blyt('GameSplashScreen_00', 'T_Notes', 'shift_y', do_some_math(-490, aspect_ratio))
        patch_blyt('GameSplashScreen_00', 'A_Align', 'shift_y', do_some_math(-320, aspect_ratio))
        patch_blyt('PaFooter_00', 'P_Backing', 'scale_y', 1/s1)
        patch_blyt('PaFooter_00', 'P_Shadow', 'scale_y', 1/s1)
        patch_blyt('WorldIntro', 'P_Fade', 'scale_y', 1/s1)
        patch_blyt('WorldIntro', 'S_Graphics', 'scale_y', 1/s1)
        patch_blyt('WorldIntro', 'P_BorderBot', 'scale_y', do_some_math(-445, aspect_ratio))
        patch_blyt('WorldIntro', 'N_TopArea', 'scale_y', do_some_math(20, aspect_ratio))
        patch_blyt('WorldIntro', 'L_Zipper_00', 'scale_y', do_some_math(-420, aspect_ratio))
        patch_blyt('WorldIntro', 'P_Icon_00', 'shift_y', do_some_math(-802, aspect_ratio))
        patch_blyt('PaFooter_00', 'N_null_00', 'shift_y', do_some_math(-495, aspect_ratio))
        # patch_blyt('PaMenu_Btn_Slot', 'P_Highlight', 'scale_y', 1/s1)

        # if HUD_pos == 'corner':
        #     print("Shifitng elements for corner HUD")
