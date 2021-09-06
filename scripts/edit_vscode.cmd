@echo off

REM Setup FlightDisplay environment
call setup.cmd -NoShell

set VS_CODE_DIR=C:\Users\Vanessa\AppData\Local\Programs\Microsoft VS Code

:: Open root folder in visual studio code
"%VS_CODE_DIR%\Code.exe" %DEV_DIR%

exit /b 0