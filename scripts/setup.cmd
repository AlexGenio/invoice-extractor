@echo off

if defined SETUP_RUN (
   echo.
   echo Info: setup already run, skipping doing it again.
   echo.   
   exit /b 0
)

:ParseArgLoop

if "%1"=="" goto AfterProcessArgs
if "%1"=="-NoShell" set _NO_SHELL_REQ=1
if "%1"=="-NOSHELL" set _NO_SHELL_REQ=1
shift
goto ParseArgLoop

:AfterProcessArgs

set APP_NAME=InvoiceExtractor

echo.
echo ***************************************
echo *   Setting up %APP_NAME% env   *
echo ***************************************
echo.

:: Paths for general use
set SCRIPT_DIR=%CD%
set DEV_DIR=%CD%\..
set BUILD_DIR=%DEV_DIR%\build
set INSTALLER_SRC_DIR=%DEV_DIR%\installer
set SRC_DIR=%DEV_DIR%\src
set UI_SRC_DIR=%SRC_DIR%\ui
set TEST_DIR=%DEV_DIR%\tests
set UI_DIR=%DEV_DIR%\ui
set VIRTUAL_ENV_DIR=%DEV_DIR%\venv

:: Paths for pyinstaller
set INSTALLER_DEST_DIR=%BUILD_DIR%\installer
set DIST_DIR=%BUILD_DIR%\_dist
set WORK_DIR=%BUILD_DIR%\_temp

:: Paths for QT
set PYQTDESIGNERPATH=%SRC_DIR%

:: Environment variables
set APP_ICON=%UI_DIR%\resources\logo.ico

:: Check for Python Installation
python --version 3>NUL
if not errorlevel 0 goto NoPython

IF not exist "%VIRTUAL_ENV_DIR%" (
	echo ***************************************
	echo *     Creating Virtual Environment    *
	echo ***************************************
	echo.
	
	mkdir %VIRTUAL_ENV_DIR%
	virtualenv -p python %VIRTUAL_ENV_DIR%
	call %VIRTUAL_ENV_DIR%\Scripts\activate.bat
	pip install -r requirements.txt
	
	goto Success
	
) ELSE (
    echo INFO: Directory "%VIRTUAL_ENV_DIR%" already exists.
    echo INFO: Activating virtual environment.

    call %VIRTUAL_ENV_DIR%\Scripts\activate.bat
	goto Success
)

:NoPython

echo ERROR: Python version 3 is not installed.
goto Error

:Success

echo.
echo ***************************************
echo *           Setup Successful          *
echo ***************************************
echo.

echo Creating aliasses...
call %SCRIPT_DIR%\create_aliasses.cmd
echo.

set SETUP_RUN=1

goto End

:Error

echo.
echo ***************************************
echo *             Setup Failed            *
echo ***************************************
echo.
goto End

:End

REM Calling script requests not to have an open shell
if defined _NO_SHELL_REQ exit /b 0

REM Terminate successfully current script
%comspec% /k
exit /b 0