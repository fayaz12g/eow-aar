
def create_visuals(do_DOF, do_lod, do_2k, bloom, resolution):

    dof = "disabled"
    lod = "disabled"
    shadow2k = "disabled"
    res1920 = "disabled"
    res2560 = "disabled"
    bloom1 = "disabled"
    bloom0 = "disabled"
    
    visual_fixes = []

    if do_DOF:
        dof = "enabled"
    if do_lod:
        lod = "enabled"
    if do_2k:
        shadow2k = "enabled"

    if resolution == "1920":
        res1920 = "enabled"
    if resolution == "2560":
        res2560 = "enabled"

    if bloom == "1":
        bloom1 = "enabled"
    if bloom == "0":
        bloom0 = "enabled"


    visuals1_0_1 = f'''// Disable DOF
@{dof}
0276a66c 1F7C0329
@stop

// Max LOD
@{lod}
0032cfd0 00D0351E
@disabled

// 2K Shadow Resolution
@{shadow2k}
0277C510 00008152
0277C514 01008152
0277C518 03008152
0277C51C 04008152
0277C6A8 08A0A8D2
0277C6B4 08A0E8F2
0277C6AC E90315B2
@disabled


// Reduce Bloom
@{bloom1}
032f5f59 00000000
@disabled

// Remove Bloom
@{bloom0}
02761be0 E003271E
02761be8 E003271E
02761bf0 E003271E
02761bfc E003271E
@disabled

// Resolutions

// 1920 x 1080 Docked
@{res1920}
02720994 09008052
@disabled

// 2560 x 1440 Docked
@{res2560}
0247deb0 08F08052
0247dec0 08878052
02700d9c 1B4081D2
02700da4 1BB4C0F2
02701b30 C8018052
02701b58 08B48052
02701b64 09408152
0271c718 08F08052
0271c71c 09878052
0271c740 09408152
0271c764 0AB48052
0272069c 1CB48052
027206a0 1B408152
027207a4 08B48052
027207ac 08408152
02720994 A9058052
02785494 09878052
@disabled

'''

    visuals1_0_2 = f'''// Disable DOF
@{dof}
0276C54C 1F7C0329
@stop

// Max LOD
@{lod}
0032cfd0 00D0351E
@disabled

// 2K Shadow Resolution
@{shadow2k}
0277E3F0 00008152
0277E3F4 01008152
0277E3F8 03008152
0277E3FC 04008152
0277E588 08A0A8D2
0277E594 08A0E8F2
0277E58C E90315B2
@disabled


// Reduce Bloom
@{bloom1}
032f81bc 00000000
@disabled

// Remove Bloom
@{bloom0}
02763AC0 E003271E
02763AC8 E003271E
02763AD0 E003271E
02763ADC E003271E
@disabled

// Resolutions

// 1920 x 1080 Docked
@{res1920}
02722874 09008052
@disabled

// 2560 x 1440 Docked
@{res2560}
0247FCE0 08F08052
0247FCF0 08878052
02702C7C 1B4081D2
02702C84 1BB4C0F2
02703A10 C8018052
02703A38 08B48052
02703A44 09408152
0271E5F8 08F08052
0271E5FC 09878052
0271E620 09408152
0271E644 0AB48052
0272257C 1CB48052
02722580 1B408152
02722684 08B48052 
0272268C 08408152
02722874 A9058052
02787374 09878052
@disabled

'''
    
    visual_fixes.append(visuals1_0_1)
    visual_fixes.append(visuals1_0_2)
    
    return visual_fixes