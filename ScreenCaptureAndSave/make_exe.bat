@echo off
pyinstaller main.py --onefile
move /Y .\dist\main.exe .\main.exe
del .\main.spec
rmdir .\dist
rmdir .\build /s /q
rmdir .\__pycache__ /s /q
