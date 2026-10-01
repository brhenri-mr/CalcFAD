import sys
from cx_Freeze import setup, Executable

base = "Win32GUI" if sys.platform == "win32" else None

executables = [
    Executable(
        "app.py",
        base=base,
        icon="Equibris.ico",
    )
]

setup(
    name="Equibris",
    version="1.0",
    executables=executables,
)