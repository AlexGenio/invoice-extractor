@echo off

REM Setup environment
call setup.cmd -NoShell

cd %SRC_DIR%

echo.
echo ***************************************
echo *  Build installation for application *
echo ***************************************
echo.
  
:: launch installer to convert python code to EXE
pyinstaller --clean ^
			--onedir ^
			--windowed ^
			--noconfirm ^
            --name %APP_NAME% ^
			--icon %APP_ICON% ^
			--paths %SRC_DIR% ^
			--distpath %DIST_DIR% ^
			--workpath %WORK_DIR% ^
			--specpath %DEV_DIR% ^
			main.py

echo.
echo ***************************************
echo *  Compile installer for application  *
echo ***************************************
echo.

:: Need to have Inno Setup installed and in the PATH	
iscc %INSTALLER_SRC_DIR%\%APP_NAME%.iss

:: Build error reporting
if %ERRORLEVEL%==1 goto CompilationError

pause

exit /b 0

:CompilationError
popd
echo ***************************************************************
echo ERROR: Compilation of installer failed.
echo ***************************************************************

pause

exit /b 1