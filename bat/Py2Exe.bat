@echo off

set PY_DIR=%~dp1
echo %PY_DIR%
set PY_NAME=%~1
echo %PY_NAME%
set SPEC_NAME=%PY_DIR%%~n1%.spec
echo %SPEC_NAME%
set EXE_NAME_1=%PY_DIR%dist\%~n1%.exe
set EXE_NAME_2=%PY_DIR%%~n1%.exe
echo %EXE_NAME_1%
echo %EXE_NAME_2%

pyinstaller %1 --onefile
move /Y %EXE_NAME_1% %EXE_NAME_2%
del %SPEC_NAME%
rmdir %PY_DIR%dist
rmdir %PY_DIR%build /s /q
rmdir %PY_DIR%__pycache__ /s /q
