from cx_Freeze import setup, Executable

setup(
    name = "HHConverter",
    version = "0.2",
    description = "Converts Seals with Clubs Hand Histories to Full Tilt format.",
    executables = [Executable("test.py")])

