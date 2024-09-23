
def create_visuals(do_DOF, do_120, do_docked):

    fps120 = "disabled"
    docked = "disabled"
    dof = "disabled"

    
    visual_fixes = []

    if do_DOF:
        dof = "enabled"
    if do_120:
        fps120 = "enabled"
    if do_docked:
        docked = "enabled"
        
    visuals1_0_0 = f'''// 2880x1620 Docked
@{docked}
002F9D68 02688152
002F9D58 83CA8052
00E73C5C 086881D2
00E73C60 88CAC0F2
00E73C68 08F080D2
00E73C6C 0887C0F2
00E74064 086881D2
00E7406C 88CAC0F2
00E74A00 086881D2
00E74A10 88CAC0F2
00E75DA4 086881D2
00E75DA8 88CAC0F2
003A8A60 0868C1F2
003A8A34 8ACA8052
@disabled


// Disable DOF
@{dof}
012AE28D 1F2003D5
@stop
'''


    visuals1_0_1 = f'''// 2880x1620 Docked
@{docked}
002f9d78 02688152
002f9d68 83CA8052
00e73c6c 086881D2
00e73c70 88CAC0F2
00E73C78 08F080D2
00E73C7C 0887C0F2
00e74074 086881D2
00e7407c 88CAC0F2
00e74a10 086881D2
00e74a20 88CAC0F2
00e75db4 086881D2
00e75db8 88CAC0F2
003a8a70 0868C1F2
003a8a44 8ACA8052
@disabled

// 120 FPS
@{fps120}
008193B0 C0035FD6
@disabled

// Disable DOF
@{dof}
012AE28D 1F2003D5
@stop
'''

    visual_fixes.append(visuals1_0_0)
    visual_fixes.append(visuals1_0_1)
    
    return visual_fixes