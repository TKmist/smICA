@echo off
setlocal EnableExtensions EnableDelayedExpansion

:: ------------------------------------------------------------
:: Configuration
:: ------------------------------------------------------------

:: Define paths
set "PYTHON_DIR=python_embedded"
set "PYTHON_EXE=%PYTHON_DIR%\python.exe"
set "PIP_EXE=%PYTHON_DIR%\Scripts\pip.exe"
set "GET_PIP=%PYTHON_DIR%\get-pip.py"
set "VENV_DIR=v_smICA_env"
set "LAUNCHER_BAT=%~dp0smICA.bat"

:: External third-party resource(s) fetched during installation
set "THIRD_PARTY_URL=https://raw.githubusercontent.com/TKmist/readPTU_FLIM/refs/heads/NIKON_correction/readPTU_FLIM.py"
set "THIRD_PARTY_LICENSE_HINT=Licensing information is typically provided in the upstream repository (e.g., LICENSE file and/or README). Please review it before accepting."

:: ------------------------------------------------------------
:: Helper labels (functions)
:: ------------------------------------------------------------

:AbortInstall
echo.
echo Installation aborted.
exit /b 1

:RequireYesNo
:: Usage:
::   call :RequireYesNo "Question text here" VAR_NAME
:: On return:
::   VAR_NAME will be set to YES or NO
set "Q_TEXT=%~1"
set "OUTVAR=%~2"
set "REPLY="

:RequireYesNoLoop
set "REPLY="
set /p "REPLY=%Q_TEXT% [y/N]: "
if /I "%REPLY%"=="Y"  set "REPLY=YES"
if /I "%REPLY%"=="YES" set "REPLY=YES"
if /I "%REPLY%"=="N"  set "REPLY=NO"
if /I "%REPLY%"=="NO" set "REPLY=NO"
if "%REPLY%"=="" set "REPLY=NO"

if /I "%REPLY%"=="YES" (
  set "%OUTVAR%=YES"
  exit /b 0
) else if /I "%REPLY%"=="NO" (
  set "%OUTVAR%=NO"
  exit /b 0
) else (
  echo Please answer 'y' or 'n'.
  goto :RequireYesNoLoop
)

:ShowLicenseAndRequireAcceptance
:: Display the LICENSE file and require user acceptance.
if not exist "LICENSE" (
  echo ERROR: LICENSE file not found in the current directory.
  echo Please run this installer from the project root where LICENSE exists.
  call :AbortInstall
)

echo ========================================
echo               LICENSE
echo ========================================
echo.

:: Prefer paging through MORE so the user can scroll.
:: If MORE is unavailable, fall back to TYPE.
where more >nul 2>&1
if %errorlevel%==0 (
  type "LICENSE" | more
) else (
  type "LICENSE"
)

echo.
echo ========================================
echo.

call :RequireYesNo "Do you accept the terms of the LICENSE agreement?" LICENSE_ACCEPTED
if /I not "%LICENSE_ACCEPTED%"=="YES" (
  echo You did not accept the LICENSE terms.
  call :AbortInstall
)
exit /b 0

:InformThirdPartyAndRequireAcceptance
:: Inform the user about third-party downloads and require acceptance.
echo.
echo ========================================
echo         THIRD-PARTY COMPONENTS
echo ========================================
echo.
echo This installer will download and use third-party scripts/libraries from external sources.
echo Example resource:
echo   - %THIRD_PARTY_URL%
echo.
echo %THIRD_PARTY_LICENSE_HINT%
echo By continuing, you confirm you understand and accept that third-party components may have their own licenses and terms.
echo.

call :RequireYesNo "Do you agree to proceed with installation including third-party components?" THIRD_PARTY_ACCEPTED
if /I not "%THIRD_PARTY_ACCEPTED%"=="YES" (
  echo You did not agree to install third-party components.
  call :AbortInstall
)
exit /b 0

:: ------------------------------------------------------------
:: Pre-flight checks
:: ------------------------------------------------------------

:: Ensure the embedded Python exists
if not exist "%PYTHON_EXE%" (
  echo Embedded Python not found at "%PYTHON_EXE%". Exiting.
  exit /b 1
)

:: ------------------------------------------------------------
:: Required user consents (must happen BEFORE installation steps)
:: ------------------------------------------------------------

call :ShowLicenseAndRequireAcceptance
call :InformThirdPartyAndRequireAcceptance


:: Ensure pip is installed
if not exist "%PIP_EXE%" (
    echo Pip not found. Installing pip...
    "%PYTHON_EXE%" "%GET_PIP%"
    if %errorlevel% neq 0 (
        echo Failed to install pip. Exiting.
        exit /b 1
    )
)

:: Install virtualenv
echo Installing virtualenv...
"%PYTHON_EXE%" -m pip install virtualenv --no-warn-script-location
if %errorlevel% neq 0 (
    echo Failed to install virtualenv. Exiting.
    exit /b 1
)

:: Remove the existing virtual environment if it exists
if exist "%VENV_DIR%" (
    echo Removing old virtual environment...
    rmdir /s /q "%VENV_DIR%"
    if exist "%VENV_DIR%" (
        echo Failed to remove old virtual environment. Exiting.
        exit /b 1
    )
    echo Old virtual environment removed.
)

:: Create virtual environment using virtualenv
echo Creating virtual environment in %VENV_DIR%...
"%PYTHON_EXE%" -m virtualenv "%~dp0%VENV_DIR%"
if %errorlevel% neq 0 (
    echo Failed to create virtual environment. Exiting.
    exit /b 1
)

:: Activate the virtual environment
echo Activating virtual environment...
call "%~dp0%VENV_DIR%\Scripts\activate.bat"
if %errorlevel% neq 0 (
    echo Failed to activate virtual environment. Exiting.
    exit /b 1
)

:: Install dependencies
echo Installing dependencies...
"%PIP_EXE%" cache purge
"%PYTHON_EXE%" -m pip install --upgrade pip 

"%~dp0%VENV_DIR%\Scripts\pip.exe" install . --no-warn-script-location --disable-pip-version-check --verbose >install.log 2>&1
if %errorlevel% neq 0 (
    echo Failed to install dependencies. Exiting.
    exit /b 1
)

:: Create the launcher .bat file
echo Creating the smICA.bat file...
echo @echo off > %LAUNCHER_BAT%

echo call "%~dp0%VENV_DIR%\Scripts\activate.bat" >> %LAUNCHER_BAT%
echo cd /d "%~dp0smICA\smICA" >> %LAUNCHER_BAT%
echo python smICA_tool.py >> %LAUNCHER_BAT%
echo call "%~dp0%VENV_DIR%\Scripts\deactivate.bat" >> %LAUNCHER_BAT%
echo cd /d "%~dp0smICA" >> %LAUNCHER_BAT%
if %errorlevel% neq 0 (
    echo Failed to create launcher .bat file. Exiting.
    exit /b 1
)

:: Create a Windows shortcut on the Desktop using VBScript
echo Creating the Windows shortcut on the Desktop...
set SHORTCUT_NAME=smICA.lnk
set SHORTCUT_PATH="%USERPROFILE%\Desktop\%SHORTCUT_NAME%"
set ICON_PATH="%~dp0smICA\smICA\res\icons\smICA.ico"
set TEMP_VBS="%TEMP%\%RANDOM%-%RANDOM%-%RANDOM%-%RANDOM%.vbs"

:: Generate VBScript for shortcut creation
echo Set oWS = WScript.CreateObject("WScript.Shell") >> %TEMP_VBS%
echo Set oLink = oWS.CreateShortcut(%SHORTCUT_PATH%) >> %TEMP_VBS%
echo oLink.TargetPath = %LAUNCHER_BAT% >> %TEMP_VBS%
echo oLink.IconLocation = %ICON_PATH% >> %TEMP_VBS%
echo oLink.Description = "Launch smICA Application" >> %TEMP_VBS%
echo oLink.Save >> %TEMP_VBS%

:: Execute VBScript to create the shortcut
echo Creating shortcut on Desktop...
cscript /nologo %TEMP_VBS%
if %errorlevel% neq 0 (
    echo Failed to create shortcut. Exiting.
    del %TEMP_VBS%
    exit /b 1
)

:: Clean up VBScript file
del %TEMP_VBS%

:: Check if the shortcut was created
if exist %SHORTCUT_PATH% (
    echo Shortcut created successfully at %SHORTCUT_PATH%.
) else (
    echo Failed to create shortcut. Please check the script.
)

:: Deactivate the virtual environment
echo Deactivating virtual environment...
call "%~dp0%VENV_DIR%\Scripts\deactivate.bat"

:: Rename src directory to smICA
echo Renaming src directory to smICA...
rename src smICA
if %errorlevel% neq 0 (
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

:: Remove setup.py and install_win.bat
echo Removing setup.py and install_win.bat...
del setup.py



echo Installation completed successfully!
@echo off
del install_win.bat


