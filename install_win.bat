@echo off
setlocal EnableExtensions

cd /d "%~dp0"
if errorlevel 1 (
    echo ERROR: Cannot enter the installer directory: "%~dp0"
    exit /b 1
)

:: ============================================================
:: smICA installer (Windows)
:: ============================================================


set "VENV_DIR=v_smICA_env"
set "LICENSE_FILE=LICENSE"

set "PYTHON_DIR=python_embedded"
set "PYTHON_EXE=%PYTHON_DIR%\python.exe"
set "PIP_EXE=%PYTHON_DIR%\Scripts\pip.exe"
set "GET_PIP=%PYTHON_DIR%\get-pip.py"

set "THIRD_PARTY_URL=https://raw.githubusercontent.com/TKmist/readPTU_FLIM/refs/heads/NIKON_correction/readPTU_FLIM.py"
set "THIRD_PARTY_TARGET_DIR=src\smICA\Required\Third_party"
set "THIRD_PARTY_TARGET=%THIRD_PARTY_TARGET_DIR%\readPTU_FLIM.py"

set "LAUNCHER_BAT=%~dp0smICA.bat"

if exist "%LAUNCHER_BAT%" (
    echo ERROR: An existing smICA installation was found in this directory.
    echo Extract the release archive into a new, empty directory and run install_win.bat there.
    exit /b 1
)
if exist "%~dp0smICA" (
    echo ERROR: An existing smICA application directory was found.
    echo Extract the release archive into a new, empty directory and run install_win.bat there.
    exit /b 1
)

echo ------------------------------------------------------------
echo smICA installer
echo ------------------------------------------------------------
echo.


if not exist "%LICENSE_FILE%" (
    echo ERROR: LICENSE file not found in the current directory.
    echo Expected: %CD%\%LICENSE_FILE%
    exit /b 1
)

echo This installer will set up smICA and its dependencies.
echo smICA is licensed under the MIT License.
echo.
echo Displaying LICENSE...
echo ------------------------------------------------------------
more "%LICENSE_FILE%"
echo ------------------------------------------------------------
echo.

:LICENSE_MENU
echo Choose an option:
echo   [a] I acknowledge that I have read the license and want to continue the installation
echo   [d] Abort the installation
echo Choosing 'Abort' will only terminate the installer.
echo The source code remains available to you under the terms of the MIT license.

choice /c AD /n /m "Your choice [a/d]: "
if errorlevel 2 goto ABORT_INSTALL
if errorlevel 1 goto LICENSE_ACCEPT
goto LICENSE_MENU

:LICENSE_ACCEPT
echo Continuing installation.


echo.
echo ------------------------------------------------------------
echo Checking prerequisites
echo ------------------------------------------------------------

if not exist "%PYTHON_EXE%" (
    echo Embedded Python not found at %PYTHON_EXE%. Exiting.
    exit /b 1
)

echo.
echo ------------------------------------------------------------
echo Optional legacy PTU reader: readPTU_FLIM.py
echo ------------------------------------------------------------
echo.
echo smICA uses phconvert for supported PicoHarp 300 T3 files.
echo The third-party readPTU_FLIM.py reader is only used as a fallback
echo for PTU record types that are not supported by the phconvert backend.
echo Source URL:
echo   %THIRD_PARTY_URL%
echo.

if exist "%THIRD_PARTY_TARGET%" (
    echo readPTU_FLIM.py is already present; no download is needed.
    goto AFTER_READPTU
)

:READPTU_PROMPT
choice /c YN /n /m "Install the optional legacy PTU fallback? [y/n]: "
if errorlevel 2 goto READPTU_NO
if errorlevel 1 goto READPTU_YES
goto READPTU_PROMPT

:READPTU_YES
if not exist "%THIRD_PARTY_TARGET_DIR%" mkdir "%THIRD_PARTY_TARGET_DIR%"
echo Downloading readPTU_FLIM.py...
"%PYTHON_EXE%" -c "import urllib.request; urllib.request.urlretrieve(r'%THIRD_PARTY_URL%', r'%THIRD_PARTY_TARGET%')"
if errorlevel 1 (
    if exist "%THIRD_PARTY_TARGET%" del /f /q "%THIRD_PARTY_TARGET%"
    echo WARNING: readPTU_FLIM.py could not be downloaded.
    echo Installation will continue with the phconvert backend.
    echo Only unsupported legacy PTU record types will be unavailable.
) else (
    echo Optional legacy PTU fallback installed successfully.
)
goto AFTER_READPTU

:READPTU_NO
echo Optional legacy PTU fallback skipped.
echo Installation will continue with the phconvert backend.
echo Only unsupported legacy PTU record types will be unavailable.

:AFTER_READPTU

:: ----------------------------
:: 4) Virtual environment setup
:: ----------------------------
echo.
echo ------------------------------------------------------------
echo Python environment setup
echo ------------------------------------------------------------

echo Checking for pip...
if not exist "%PIP_EXE%" (
    echo Pip not found. Installing pip...
    "%PYTHON_EXE%" "%GET_PIP%" --no-warn-script-location
    if errorlevel 1 (
        echo Failed to install pip. Exiting.
        exit /b 1
    )
) else (
    echo Pip is available. Proceeding.
)

echo Installing virtualenv...
"%PYTHON_EXE%" -m pip install virtualenv --no-warn-script-location
if errorlevel 1 (
    echo Failed to install virtualenv. Exiting.
    exit /b 1
)

if exist "%VENV_DIR%" (
    echo Removing old virtual environment...
    rmdir /s /q "%VENV_DIR%"
    if exist "%VENV_DIR%" (
        echo Failed to remove old virtual environment. Exiting.
        exit /b 1
    )
    echo Old virtual environment removed.
)

echo Creating virtual environment in %VENV_DIR%...
"%PYTHON_EXE%" -m virtualenv --copies "%~dp0%VENV_DIR%"
if errorlevel 1 (
    echo Failed to create virtual environment. Exiting.
    exit /b 1
)

echo Activating virtual environment...
call "%~dp0%VENV_DIR%\Scripts\activate.bat"
if errorlevel 1 (
    echo Failed to activate the virtual environment. Exiting.
    exit /b 1
)

echo Upgrading pip in the virtual environment...
"%~dp0%VENV_DIR%\Scripts\python.exe" -m pip install --upgrade pip

:: ----------------------------
:: 5) Install package
:: ----------------------------
echo Installing dependencies using pip...

"%~dp0%VENV_DIR%\Scripts\pip.exe" install . --no-warn-script-location --disable-pip-version-check --verbose >install.log 2>&1
if errorlevel 1 (
    echo Failed to install dependencies. Exiting.
    exit /b 1
)

echo Creating text-based automation client scripts...
set "SMICA_CALL_BAT=%~dp0%VENV_DIR%\Scripts\smica-call.bat"
set "SMICA_CALL_ALIAS_BAT=%~dp0%VENV_DIR%\Scripts\smica_call.bat"
> "%SMICA_CALL_BAT%" echo @echo off
>> "%SMICA_CALL_BAT%" echo rem Text launcher for the smICA TCP client. No compiled launcher is used.
>> "%SMICA_CALL_BAT%" echo "%%~dp0python.exe" -m smICA.Required.automation_client %%*
copy /y "%SMICA_CALL_BAT%" "%SMICA_CALL_ALIAS_BAT%" >nul
if errorlevel 1 (
    echo Failed to create the automation client scripts. Exiting.
    exit /b 1
)

echo Building bundled documentation...
"%~dp0%VENV_DIR%\Scripts\python.exe" "src\smICA\Required\documentation_builder.py" --source "docs" --target "src\smICA\doc\assets\help_html"
if errorlevel 1 (
    echo Failed to build the documentation. Exiting.
    exit /b 1
)
echo Documentation built successfully.

:: ----------------------------
:: 6) Desktop integration (Windows analogue)
:: - create launcher .bat + desktop shortcut
:: ----------------------------
echo.
echo ------------------------------------------------------------
echo Desktop integration
echo ------------------------------------------------------------

echo Creating run_smICA script...
echo @echo off > "%LAUNCHER_BAT%"
echo setlocal EnableExtensions >> "%LAUNCHER_BAT%"
echo set "SMICA_INSTALLATION=%%~dp0" >> "%LAUNCHER_BAT%"
echo set "SMICA_PYTHON=%%SMICA_INSTALLATION%%v_smICA_env\Scripts\python.exe" >> "%LAUNCHER_BAT%"
echo if exist "%%SMICA_PYTHON%%" goto PARSE_ARGUMENTS >> "%LAUNCHER_BAT%"
echo echo ERROR: The smICA Python environment was not found. >> "%LAUNCHER_BAT%"
echo echo Expected: "%%SMICA_PYTHON%%" >> "%LAUNCHER_BAT%"
echo exit /b 1 >> "%LAUNCHER_BAT%"
echo :PARSE_ARGUMENTS >> "%LAUNCHER_BAT%"
echo if "%%~1"=="--demo" goto RUN_DEMO >> "%LAUNCHER_BAT%"
echo if not "%%~1"=="--test" goto RUN_GUI >> "%LAUNCHER_BAT%"
echo set "SMICA_TEST_RUNNER=%%SMICA_INSTALLATION%%smICA\calc_tests\unit_test\run_all.py" >> "%LAUNCHER_BAT%"
echo if exist "%%SMICA_TEST_RUNNER%%" goto RUN_TESTS >> "%LAUNCHER_BAT%"
echo echo ERROR: Unit test runner was not found. >> "%LAUNCHER_BAT%"
echo echo Checked: "%%SMICA_INSTALLATION%%smICA\calc_tests\unit_test\run_all.py" >> "%LAUNCHER_BAT%"
echo exit /b 1 >> "%LAUNCHER_BAT%"
echo :RUN_TESTS >> "%LAUNCHER_BAT%"
echo "%%SMICA_PYTHON%%" "%%SMICA_TEST_RUNNER%%" >> "%LAUNCHER_BAT%"
echo set "TEST_STATUS=%%ERRORLEVEL%%" >> "%LAUNCHER_BAT%"
echo exit /b %%TEST_STATUS%% >> "%LAUNCHER_BAT%"
echo :RUN_DEMO >> "%LAUNCHER_BAT%"
echo set "SMICA_DEMO=%%SMICA_INSTALLATION%%smICA\calc_tests\demo_data\run_demo.py" >> "%LAUNCHER_BAT%"
echo if exist "%%SMICA_DEMO%%" goto START_DEMO >> "%LAUNCHER_BAT%"
echo echo ERROR: The bundled smICA demo was not found. >> "%LAUNCHER_BAT%"
echo echo Expected: "%%SMICA_DEMO%%" >> "%LAUNCHER_BAT%"
echo exit /b 1 >> "%LAUNCHER_BAT%"
echo :START_DEMO >> "%LAUNCHER_BAT%"
echo "%%SMICA_PYTHON%%" "%%SMICA_DEMO%%" >> "%LAUNCHER_BAT%"
echo set "DEMO_STATUS=%%ERRORLEVEL%%" >> "%LAUNCHER_BAT%"
echo exit /b %%DEMO_STATUS%% >> "%LAUNCHER_BAT%"
echo :RUN_GUI >> "%LAUNCHER_BAT%"
echo set "SMICA_APP=%%SMICA_INSTALLATION%%smICA\smICA\smICA_tool.py" >> "%LAUNCHER_BAT%"
echo if exist "%%SMICA_APP%%" goto START_GUI >> "%LAUNCHER_BAT%"
echo echo ERROR: The smICA application entry point was not found. >> "%LAUNCHER_BAT%"
echo echo Expected: "%%SMICA_APP%%" >> "%LAUNCHER_BAT%"
echo exit /b 1 >> "%LAUNCHER_BAT%"
echo :START_GUI >> "%LAUNCHER_BAT%"
echo cd /d "%%SMICA_INSTALLATION%%smICA\smICA" >> "%LAUNCHER_BAT%"
echo "%%SMICA_PYTHON%%" "%%SMICA_APP%%" %%* >> "%LAUNCHER_BAT%"
echo exit /b %%ERRORLEVEL%% >> "%LAUNCHER_BAT%"

echo run_smICA script created and made executable.
echo Use smICA.bat --test to run the standalone unit tests.
echo Use smICA.bat --demo to run the bundled end-to-end demonstration.
echo Use smICA.bat --automation-server to start the local automation server.
echo The text-based smica-call.bat and smica_call.bat clients are installed in %~dp0%VENV_DIR%\Scripts\.

echo Creating the Windows shortcut on the Desktop...
set "SHORTCUT_NAME=smICA.lnk"
set "SHORTCUT_PATH=%USERPROFILE%\Desktop\%SHORTCUT_NAME%"
set "ICON_PATH=%~dp0smICA\smICA\res\icons\smICA.ico"
set "TEMP_VBS=%TEMP%\%RANDOM%-%RANDOM%-%RANDOM%-%RANDOM%.vbs"

echo Set oWS = WScript.CreateObject("WScript.Shell") > "%TEMP_VBS%"
echo Set oLink = oWS.CreateShortcut("%SHORTCUT_PATH%") >> "%TEMP_VBS%"
echo oLink.TargetPath = "%LAUNCHER_BAT%" >> "%TEMP_VBS%"
echo oLink.IconLocation = "%ICON_PATH%" >> "%TEMP_VBS%"
echo oLink.Description = "Run smICA application" >> "%TEMP_VBS%"
echo oLink.Save >> "%TEMP_VBS%"

cscript /nologo "%TEMP_VBS%"
if errorlevel 1 (
    echo Failed to create shortcut. Exiting.
    del "%TEMP_VBS%"
    exit /b 1
)
del "%TEMP_VBS%"

echo Shortcut created successfully at "%SHORTCUT_PATH%".


echo.
echo ------------------------------------------------------------
echo Reorganizing project files
echo ------------------------------------------------------------

echo Deactivating virtual environment...
call "%~dp0%VENV_DIR%\Scripts\deactivate.bat"

echo Renaming src directory to smICA...
rename src smICA
if errorlevel 1 (
    echo Failed to rename src directory to smICA. Exiting.
    exit /b 1
)

:: Move payload directories and files to the smICA directory.
echo Moving directories to smICA directory...
for /d %%d in (*) do (
    if /i not "%%d" == "smICA" if /i not "%%d" == "%VENV_DIR%" if /i not "%%d" == "%PYTHON_DIR%" (
        move "%%d" smICA\
        if errorlevel 1 (
            echo Failed to move directory %%d to smICA. Exiting.
            exit /b 1
        )
    )
)

echo Moving files to smICA directory...
for /f "delims=" %%f in ('dir /b /a-d') do (
    if /i not "%%f" == "install_win.bat" if /i not "%%f" == "setup.py" if /i not "%%f" == "smICA.bat" (
        move "%%f" smICA\
        if errorlevel 1 (
            echo Failed to move file %%f to smICA. Exiting.
            exit /b 1
        )
    )
)


echo Removing setup.py and install_win.bat...
del /f /q setup.py install_win.bat
if errorlevel 1 (
    echo Failed to remove setup.py or install_win.bat. Exiting.
    exit /b 1
)

if exist "python_embedded" (
    attrib -r -s -h "python_embedded\*" /s /d >nul 2>&1
    rmdir /s /q python_embedded
    if exist "python_embedded" (
        echo Failed to remove the embedded Python bootstrap directory. Exiting.
        exit /b 1
    )
)

"%~dp0%VENV_DIR%\Scripts\python.exe" -c "import sys; print('smICA Python environment verified:', sys.executable)"
if errorlevel 1 (
    echo The installed Python environment is not usable after cleanup. Exiting.
    exit /b 1
)

echo.
echo All files successfully organized and cleaned up.
echo Installation and reorganization completed successfully!
pause

endlocal
