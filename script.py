import os
import struct
from functions import *

def patch_blarc(aspect_ratio, HUD_pos, unpacked_folder, cutscene_zoomed):
    unpacked_folder = str(unpacked_folder)
    aspect_ratio = float(aspect_ratio)
    print(f"Aspect ratio is {aspect_ratio}")
    HUD_pos = str(HUD_pos)

    file_paths = {}

    layout_map = {
                    'Throbber': ['A_Save_00'],
                    'Counter': ['L_Cost_00'],
                    'CountCost': ['P_Base_00', 'L_Cost_00'],
                    'HeartGaugeList': ['N_Life_00'],
                    'SetSlotUseItem': ['L_SetItem_00'],
                    'SystemMenu': ['N_List_00', 'L_ControllerKeyConfig_00'],
                    'MapMenu': ['L_Item_00'],
                    'KeyItem': ['N_Key_00'],
                    'BuffTimer': ['L_BuffDescription_00'],
                    'SetSlotPasteActor': ['L_CopySetItem_00'],
                    'LinkGauge': ['N_InOut_00'],
                    'PartnerGauge': ['N_Offset_00', 'W_window_02'],
                    'L_PasteActorSelectList': ['P_pict_01', 'P_pict_00'],
                    'LocationInfoField': ['N_InOut_00'],
                    'L_MachineSelectList': ['P_pict_01', 'P_pict_00'],
                    'WorldGlobePieceSensor': ['N_Sensor_00'],
                    'MiniGameQuitHelp': ['N_Interact_00', 'L_Interact_00'],
                    'CollectMenu': ['N_ZeldaLinkItem_00', 'L_Item_21', 'N_Proof_00', 'N_StampCard_00', 'N_Bottle_00', 'N_PartnerLevel_00', 'L_BtnChoice_00'],
                    'MapFilter': ['N_InOut_00'],
                    'SetSlotLink': ['L_SetItem_00', 'L_SetItem_01', 'L_SetItem_02'],
                    'FooterHelp': ['N_Interact_00'],
                    'QuestUpdate': ['N_InOut_00'],
                    'DressUp': ['N_PageInOut_00', 'N_null_00'],
                    'SmoothieBgFront': ['SmoothieFruitsSide_00', 'SmoothieFruitsSide_01', 'SmoothieFruits_00', 'SmoothieFruits_01'],
                    'SubQuestInformation': ['N_QuestComplete_00'],
                    'QuestInformation': ['N_QuestComplete_00'],
                    'SmoothieChoose': ['N_Preview_01', 'N_Title_00', 'N_ListPosition_00'],
                    'SmoothieMenu': ['N_List_00', 'N_Select_00'],
                    'Operate': ['N_InOut_00'],
                    'MessageWindowGuide': ['N_DecideOut_00'],
                    'MessageWindow': ['A_Choice_00'],
                    'MessageWindowShop': ['A_Choice_00'],
                    'RecipeMenu': ['N_Title_00', 'N_ListPosition_00', 'N_Preview_00'],
                    'LinkItemMenu': ['A_Rupee_00'],
                    'Title': ['N_InOut_00'],
                    'SubMenuHeader': ['N_Header_00', 'N_Footer_00', 'N_CategoryList_00'],
                    'MenuHeader':['N_Header_00', 'N_Footer_00', 'N_CategoryList_00'],
                    'MapPopUp':['N_Offset_00'],
                    'Option':['N_Description_00', 'A_List_00'],
                    'DictionaryList':['N_PageInOut_00', 'L_Scrollbar_00', 'L_Scrollbar_00', 'L_SortInfo_00'],
                    'GameOver':['N_DlgSel_00', 'A_alignment_00', 'T_GameOver_00'],
                }

    def patch_ui_layouts(direction):
        if direction == "x":
            offset = 0x40
        if direction == 'y':
            offset = 0x48

        for filename, panes in layout_map.items():
            modified_name = filename + "_name"
            paths = file_paths.get(modified_name, [])
            
            if not paths:
                default_path = os.path.join(unpacked_folder, "region_common", "ui", "GameMain", "blyt", f"{filename}.bflyt")
                paths.append(default_path)
            
            for full_path_of_file in paths:
                with open(full_path_of_file, 'rb') as f:
                    content = f.read().hex()
                
                start_rootpane = content.index(b'RootPane'.hex())
                
                for pane in panes:
                    pane_hex = pane.encode('utf-8').hex()
                    start_pane = content.index(pane_hex, start_rootpane)
                    idx = start_pane + offset 
                    
                    current_value_hex = content[idx:idx+8]
                    current_value = hex2float(current_value_hex)
                    
                    new_value = (current_value * s1**-1)
                    new_value_hex = float2hex(new_value)

                    if pane == "L_SetItem_00" or pane == "L_SetItem_01" or pane == "L_SetItem_02" :
                        print(pane, current_value, new_value)
                    
                    content = content[:idx] + new_value_hex + content[idx+8:]
                
                with open(full_path_of_file, 'wb') as f:
                    f.write(bytes.fromhex(content))

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

        patch_blyt('GameOver', 'P_DisplaySub_00', 'scale_x', 1/s1)
        patch_blyt('GameOver', 'P_DisplayAdd_01', 'scale_x', 1/s1)


        patch_blyt('ActorCostDown', 'N_Blur_00', 'scale_x', 1/s1)
        patch_blyt('ActorCostDown', 'P_DisplyMask_00', 'scale_x', 1/s1)
        patch_blyt('ActorCostDown', 'N_Loop_00', 'scale_x', 1/s1)

        patch_blyt('ActorSelect', 'P_Pattern_02', 'scale_x', 1/s1)    
        patch_blyt('ActorSelect', 'P_Pattern_03', 'scale_x', 1/s1)

        if HUD_pos == 'corner':
            print("Shifitng elements for corner HUD")
    
            patch_ui_layouts("x")

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
             
        patch_blyt('SubMenuHeader', 'N_Header_00', 'scale_y', 1/s1)
        patch_blyt('SubMenuHeader', 'N_Footer_00', 'scale_y', 1/s1)
        patch_blyt('MenuHeader', 'P_pict_04', 'scale_y', 1/s1)
        patch_blyt('MenuHeader', 'N_Header_00', 'scale_y', 1/s1)
        patch_blyt('MenuHeader', 'N_Footer_00', 'scale_y', 1/s1)
        patch_blyt('ScreenCapture', 'RootPane', 'scale_y', 1/s1)

        patch_blyt('L_CommonModal', 'P_footer_00', 'scale_y', 1/s1)
        patch_blyt('L_CommonModal', 'N_Win_00', 'scale_y', 1/s1)
        patch_blyt('L_CommonModal', 'S_Graphic_00', 'scale_y', 1/s1)

        patch_blyt('SmoothieBgFront', 'W_FootSdw_00', 'scale_y', 1/s1)

        patch_blyt('MapMenu', 'L_SubHeaderLine_00', 'scale_y', 1/s1)

        patch_blyt('ScreenMainMenu', 'RootPane', 'scale_y', 1/s1)

        patch_blyt('GameOver', 'P_DisplaySub_00', 'scale_y', 1/s1)
        patch_blyt('GameOver', 'P_DisplayAdd_01', 'scale_y', 1/s1)

        if HUD_pos == 'corner':
            print("Shifitng elements for corner HUD")
            
            patch_ui_layouts("y")
