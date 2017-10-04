from cx_Freeze import setup, Executable

addtional_mods = ['numpy.core._methods', 'numpy.lib.format']

options = {
    'build_exe': {

        # Sometimes a little fine-tuning is needed
        # exclude all backends except wx
        'includes': addtional_mods
    }
}

setup(
    name = "PSUPozyx",
    version = "0.1",
    description = "A script used for the PSU Pozyx system",
    options = options,
    executables = [Executable("1D_ranging.py"), Executable("3D_positioning.py"), Executable("motion_data.py")]
)