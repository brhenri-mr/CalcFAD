from cx_Freeze import setup, Executable

setup(
    name="Calculadora fadiga",
    version="0.1",
    description="Descrição do meu programa",
    options={"build_exe": {"include_files": ["T.png"]}},
    executables=[Executable("app.py", base="Win32GUI", icon='Equibris.ico')]
)
