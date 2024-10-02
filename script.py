import os
import struct
from functions import *

def patch_blarc(aspect_ratio, HUD_pos, unpacked_folder, cutscene_zoomed):
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
    
    do_not_scale_rootpane = ["Fade", "ScreenCapture", "FrontBlindScreen", "ScreenMainMenu", "ScreenSubMenu", "StaffRoll", "SmoothieBg", "BlindScreen"]
   
    rootpane_by_y = []

    if cutscene_zoomed:
        rootpane_by_y = rootpane_by_y + ["Movie"]
        do_not_scale_rootpane = do_not_scale_rootpane + ["Movie"]

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

        patch_blyt('SmoothieBgFront', 'W_FootSdw_00', 'scale_x', 1/s1)

        patch_blyt('MapMenu', 'L_SubHeaderLine_00', 'scale_x', 1/s1)

        patch_blyt('ScreenMainMenu', 'RootPane', 'scale_x', 1/s1)


        if HUD_pos == 'corner':
            print("Shifitng elements for corner HUD")
            patch_blyt('Throbber', 'A_Save_00', 'shift_x', adjust_x(-900, s1))           
            patch_blyt('Counter', 'L_Cost_00', 'shift_x', adjust_x(711, s1))
            patch_blyt('CountCost', 'P_Base_00', 'shift_x', adjust_x(1002, s1))
            patch_blyt('CountCost', 'L_Cost_00', 'shift_x', adjust_x(711, s1))
            patch_blyt('HeartGaugeList', 'N_Life_00', 'shift_x', adjust_x(-903, s1))
            patch_blyt('SetSlotUseItem', 'L_SetItem_00', 'shift_x', adjust_x(866, s1))
            patch_blyt('SystemMenu', 'N_List_00', 'shift_x', adjust_x(-652, s1))
            patch_blyt('SystemMenu', 'L_ControllerKeyConfig_00', 'shift_x', adjust_x(355.79, s1))

            patch_blyt('MapMenu', 'L_Item_00', 'shift_x', adjust_x(693, s1))

            patch_blyt('KeyItem', 'N_Key_00', 'shift_x', adjust_x(915, s1))       

            patch_blyt('BuffTimer', 'L_BuffDescription_00', 'shift_x', adjust_x(-519, s1))  

            patch_blyt('SetSlotPasteActor', 'L_CopySetItem_00', 'shift_x', adjust_x(724, s1))

            patch_blyt('LinkGauge', 'N_InOut_00', 'shift_x', adjust_x(-918, s1)) 
            patch_blyt('PartnerGauge', 'N_Offset_00', 'shift_x', adjust_x(838, s1)) 
            patch_blyt('PartnerGauge', 'W_window_02', 'shift_x', adjust_x(938, s1)) 

            patch_blyt('L_PasteActorSelectList', 'P_pict_01', 'shift_x', adjust_x(911, s1)) 
            patch_blyt('L_PasteActorSelectList', 'P_pict_00', 'shift_x', adjust_x(-911, s1)) 

            patch_blyt('LocationInfoField', 'N_InOut_00', 'shift_x', adjust_x(-960, s1)) 

            patch_blyt('L_MachineSelectList', 'P_pict_01', 'shift_x', adjust_x(911, s1)) 
            patch_blyt('L_MachineSelectList', 'P_pict_00', 'shift_x', adjust_x(-911, s1)) 

            patch_blyt('WorldGlobePieceSensor', 'N_Sensor_00', 'shift_x', adjust_x(597, s1)) 

            patch_blyt('MiniGameQuitHelp', 'N_Interact_00', 'shift_x', adjust_x(900, s1)) 
            patch_blyt('MiniGameQuitHelp', 'L_Interact_00', 'shift_x', adjust_x(-1760, s1)) 

            patch_blyt('CollectMenu', 'N_ZeldaLinkItem_00', 'shift_x', adjust_x(-346, s1)) 
            patch_blyt('CollectMenu', 'L_Item_21', 'shift_x', adjust_x(-716, s1))
            patch_blyt('CollectMenu', 'N_Proof_00', 'shift_x', adjust_x(332, s1)) 
            patch_blyt('CollectMenu', 'N_StampCard_00', 'shift_x', adjust_x(122, s1))
            patch_blyt('CollectMenu', 'N_Bottle_00', 'shift_x', adjust_x(112, s1)) 
            patch_blyt('CollectMenu', 'N_PartnerLevel_00', 'shift_x', adjust_x(-352, s1))
            patch_blyt('CollectMenu', 'L_BtnChoice_00', 'shift_x', adjust_x(232, s1))

            patch_blyt('MapFilter', 'N_InOut_00', 'shift_x', adjust_x(-622, s1))
        
            patch_blyt('SetSlotLink', 'L_SetItem_00', 'shift_x', adjust_x(638, s1)) 
            patch_blyt('SetSlotLink', 'L_SetItem_01', 'shift_x', adjust_x(757, s1))
            patch_blyt('SetSlotLink', 'L_SetItem_02', 'shift_x', adjust_x(876, s1))

            patch_blyt('FooterHelp', 'N_Interact_00', 'shift_x', adjust_x(900, s1))

            patch_blyt('QuestUpdate', 'N_InOut_00', 'shift_x', adjust_x(490, s1))

            
            patch_blyt('DressUp', 'N_PageInOut_00', 'shift_x', adjust_x(100, s1))
            patch_blyt('DressUp', 'N_null_00', 'shift_x', adjust_x(-5, s1))

            patch_blyt('SmoothieBgFront', 'SmoothieFruitsSide_00', 'shift_x', adjust_x(-789, s1)) 
            patch_blyt('SmoothieBgFront', 'SmoothieFruitsSide_01', 'shift_x', adjust_x(789, s1))
            patch_blyt('SmoothieBgFront', 'SmoothieFruits_00', 'shift_x', adjust_x(-629, s1))
            patch_blyt('SmoothieBgFront', 'SmoothieFruits_01', 'shift_x', adjust_x(629, s1))
        
            patch_blyt('SubQuestInformation', 'N_QuestComplete_00', 'shift_x', adjust_x(346, s1))
            
            patch_blyt('QuestInformation', 'N_QuestComplete_00', 'shift_x', adjust_x(346, s1))
            
            patch_blyt('SmoothieChoose', 'N_Preview_01', 'shift_x', adjust_x(390, s1))
            patch_blyt('SmoothieChoose', 'N_Title_00', 'shift_x', adjust_x(-450, s1))
            patch_blyt('SmoothieChoose', 'N_ListPosition_00', 'shift_x', adjust_x(-450, s1))

            patch_blyt('SmoothieMenu', 'N_List_00', 'shift_x', adjust_x(-516, s1))
            patch_blyt('SmoothieMenu', 'N_Select_00', 'shift_x', adjust_x(-78, s1))

            patch_blyt('Operate', 'N_InOut_00', 'shift_x', adjust_x(-853, s1))

            patch_blyt('MessageWindowGuide', 'N_DecideOut_00', 'shift_x', adjust_x(496, s1))

            patch_blyt('MessageWindow', 'A_Choice_00', 'shift_x', adjust_x(725, s1))
            patch_blyt('MessageWindowShop', 'A_Choice_00', 'shift_x', adjust_x(725, s1))

            patch_blyt('RecipeMenu', 'N_Title_00', 'shift_x', adjust_x(-450, s1))
            patch_blyt('RecipeMenu', 'N_ListPosition_00', 'shift_x', adjust_x(-450, s1))
            patch_blyt('RecipeMenu', 'N_Preview_00', 'shift_x', adjust_x(390, s1))

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
