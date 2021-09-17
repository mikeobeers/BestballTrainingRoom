import cx_Freeze

executables = [cx_Freeze.Executable("draftgame2021.py", base = "Win32GUI")]

cx_Freeze.setup(
    name = "Bestball Training Room",
    options={"build_exe": {"packages":["pygame","sklearn","scipy"],
                           "include_files": ["background-red.png","colors.py","config.py","DLscoringdata2021.csv","ALLsite_model_2021.pkl","setupfunctions.py"]}},
    executables = executables)