@echo off

:: Define paths
set PYTHON_DIR=python_embedded
set PYTHON_EXE=%PYTHON_DIR%\pythonw.exe
set PIP_EXE=%PYTHON_DIR%\Scripts\pip.exe
set GET_PIP=%PYTHON_DIR%\get-pip.py
set VENV_DIR=v_smICA_env
set LAUNCHER_BAT="%~dp0smICA.bat"

:: Ensure the embedded Python exists
if not exist "%PYTHON_EXE%" (
    echo Embedded Python not found at %PYTHON_EXE%. Exiting.
    exit /b 1
)

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
echo cd /d "%~dp0smICA" >> %LAUNCHER_BAT%
echo python smICA_tool.py >> "%LAUNCHER_BAT%"
echo call "%~dp0%VENV_DIR%\Scripts\deactivate.bat" >> %LAUNCHER_BAT%
if %errorlevel% neq 0 (
    echo Failed to create launcher .bat file. Exiting.
    exit /b 1
)

:: Create a Windows shortcut on the Desktop using VBScript
echo Creating the Windows shortcut on the Desktop...
set SHORTCUT_NAME=smICA.lnk
set SHORTCUT_PATH="%USERPROFILE%\Desktop\%SHORTCUT_NAME%"
set ICON_PATH="%~dp0smICA\res\icons\smICA.ico"
set TEMP_VBS="%TEMP%\%RANDOM%-%RANDOM%-%RANDOM%-%RANDOM%.vbs"

:: Generate VBScript for shortcut creation
echo Set oWS = WScript.CreateObject("WScript.Shell") >> %TEMP_VBS%
echo Set oLink = oWS.CreateShortcut(%SHORTCUT_PATH%) >> %TEMP_VBS%
echo oLink.TargetPath = %LAUNCHER_BAT% >> %TEMP_VBS%
echo oLink.IconLocation = %ICON_PATH% >> %TEMP_VBS%
echo oLink.Description = "Launch FcsIT Application" >> %TEMP_VBS%
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

:: Move files to the FcsIT directory
echo Moving files to FcsIT directory...
for %%f in (*) do (
    if not "%%f" == "install_win.bat" if not "%%f" == "setup.py" if not "%%f" == "run_smICA.bat" if not "%%f" == "smICA" if not "%%f" == "%VENV_DIR%" if not "%%f" == "%PYTHON_DIR%" if not "%%f" == "REWRITE_ROI"(
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
del install_win.bat


echo Installation completed successfully!
pause
