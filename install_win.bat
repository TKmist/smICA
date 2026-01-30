@echo off
setlocal EnableExtensions

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

set "LAUNCHER_BAT=%~dp0smICA.bat"

:: Default: do not download unless explicitly agreed (setup.py reads this)
set "SMICA_DOWNLOAD_READPTU_FLIM=0"


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
echo Optional component: PTU_Corr / readPTU_FLIM.py
echo ------------------------------------------------------------
echo.
echo Some smICA functionalities rely on a third-party script:
echo   - readPTU_FLIM.py
echo   - Source URL:
echo       %THIRD_PARTY_URL%
echo.
echo If you choose YES, the installer will attempt to download this file
echo and place it in:
echo   %THIRD_PARTY_TARGET_DIR%
echo.
echo If you choose NO, smICA will still be installed,
echo BUT readPTU_FLIM.py-related functionality (EXTRACT from PTU and FILTER) WILL NOT work correctly and may raise errors.
echo.

:READPTU_PROMPT
choice /c YN /n /m "Download readPTU_FLIM.py automatically now? [y/n]: "
if errorlevel 2 goto READPTU_NO
if errorlevel 1 goto READPTU_YES
goto READPTU_PROMPT

:READPTU_YES
set "SMICA_DOWNLOAD_READPTU_FLIM=1"
echo Accepted. readPTU_FLIM.py will be downloaded during installation.
goto AFTER_READPTU

:READPTU_NO
set "SMICA_DOWNLOAD_READPTU_FLIM=0"
echo Declined.
echo WARNING:
echo   smICA will be installed, but EXTRACT from PTU and FILTER features depending on readPTU_FLIM.py
echo   WILL NOT work correctly.
echo   You can install the missing component later manually.
goto AFTER_READPTU

:AFTER_READPTU


echo.
echo ------------------------------------------------------------
echo Checking prerequisites
echo ------------------------------------------------------------

if not exist "%PYTHON_EXE%" (
    echo Embedded Python not found at %PYTHON_EXE%. Exiting.
    exit /b 1
)

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
"%PYTHON_EXE%" -m virtualenv "%~dp0%VENV_DIR%"
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

:: Make sure setup.py sees the flag (child processes inherit environment)
set "SMICA_DOWNLOAD_READPTU_FLIM=%SMICA_DOWNLOAD_READPTU_FLIM%"

"%~dp0%VENV_DIR%\Scripts\pip.exe" install . --no-warn-script-location --disable-pip-version-check --verbose >install.log 2>&1
if errorlevel 1 (
    echo Failed to install dependencies. Exiting.
    exit /b 1
)

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
echo call "%~dp0%VENV_DIR%\Scripts\activate.bat" >> "%LAUNCHER_BAT%"
echo cd /d "%~dp0smICA\smICA" >> "%LAUNCHER_BAT%"
echo python "%~dp0smICA\smICA\smICA_tool.py" >> "%LAUNCHER_BAT%"
echo call "%~dp0%VENV_DIR%\Scripts\deactivate.bat" >> "%LAUNCHER_BAT%"

echo run_smICA script created and made executable.

echo Creating the Windows shortcut on the Desktop...
set "SHORTCUT_NAME=smICA.lnk"
set "SHORTCUT_PATH=%USERPROFILE%\Desktop\%SHORTCUT_NAME%"
set "ICON_PATH=%~dp0src\smICA\res\icons\smICA.ico"
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

:: Move files to the smICA directory
echo Moving files to smICA directory...
for %%f in (*) do (
    if not "%%f" == "install_win.bat" if not "%%f" == "setup.py" if not "%%f" == "smICA.bat" if not "%%f" == "smICA" if not "%%f" == "%VENV_DIR%" if not "%%f" == "%PYTHON_DIR%" if not "%%f" == "REWRITE_ROI" if not "%%f" == "Docs" (
        move "%%f" smICA\
        if %errorlevel% neq 0 (
            echo Failed to move file %%f to FcsIT directory. Exiting.
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
    rmdir /s /q python_embedded
)

echo.
echo All files successfully organized and cleaned up.
echo Installation and reorganization completed successfully!
pause

endlocal
