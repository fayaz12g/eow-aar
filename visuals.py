
def create_visuals(do_DOF, do_lod, do_2k):

    dof = "disabled"
    lod = "disabled"
    shadow2k = "disabled"

    
    visual_fixes = []

    if do_DOF:
        dof = "enabled"
    if do_lod:
        lod = "enabled"
    if do_2k:
        shadow2k = "enabled"


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
'''

    visual_fixes.append(visuals1_0_1)
    
    return visual_fixes