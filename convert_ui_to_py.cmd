@echo off

REM Setup FlightDisplay environment
call setup.cmd -NoShell

echo.
echo ***************************************
echo *         CONVERTING UI TO PY         *
echo ***************************************
echo.

echo Generating .py files in %UI_SRC_DIR%
echo.

:: Loop over ui files
for /R %UI_DIR% %%K in (*.ui) DO (

	:: Generate .py code for the ui files
	echo Converting %%~nxK ...
	pyuic5 -x "%%K" -o "%UI_SRC_DIR%\%%~nK.py"
	
)

:: Loop over qrc files
for /R %UI_DIR% %%K in (*.qrc) DO (

	:: Generate .py code for the qrc files
	echo RCC'ing %%~nxK ...
	pyrcc5 "%%K" -o "%SRC_DIR%\%%~nK_rc.py"
	
)

echo.
pause
exit /b 0