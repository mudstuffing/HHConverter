from cx_Freeze import setup, Executable
#thsi si acomment
setup(
    name = "HHConverter",
    version = "0.2",
    description = "Converts Seals with Clubs Hand Histories to Full Tilt format.",
    executables = [Executable("test.py")])

