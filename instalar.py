import sys
from cx_Freeze import setup, Executable

if sys.platform == "win32":
    executable = Executable(
        "app.py",
        base="Win32GUI",
        icon="Equibris.ico",
    )
else:
    executable = Executable(
        "app.py",
    )

setup(
    name="Equibris",
    version="1.0",
    executables=[executable],
)