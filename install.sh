#!/bin/bash
set -e

VENV_DIR="v_smICA_env"
LICENSE_FILE="LICENSE"

THIRD_PARTY_URL="https://raw.githubusercontent.com/TKmist/readPTU_FLIM/refs/heads/NIKON_correction/readPTU_FLIM.py"
THIRD_PARTY_TARGET_DIR="src/smICA/Required/Third_party"
THIRD_PARTY_TARGET="$THIRD_PARTY_TARGET_DIR/readPTU_FLIM.py"


PAGER_CMD=""
if command -v less >/dev/null 2>&1; then
    PAGER_CMD="less"
elif command -v more >/dev/null 2>&1; then
    PAGER_CMD="more"
fi

prompt_choice() {
    
    local question="$1"
    local valid="$2"
    while true; do
        echo
        read -r -p "$question " REPLY
        REPLY="$(echo "$REPLY" | tr '[:upper:]' '[:lower:]')"
        if [[ "$valid" == *"$REPLY"* ]]; then
            return 0
        fi
        echo "Invalid choice. Please enter one of: $valid"
    done
}

show_file() {
    local file_path="$1"
    if [ ! -f "$file_path" ]; then
        echo "File not found: $file_path"
        exit 1
    fi

    if [ -n "$PAGER_CMD" ]; then
        $PAGER_CMD "$file_path"
    else
        cat "$file_path"
    fi
}

abort_install() {
    echo
    echo "Installation aborted."
    exit 1
}


echo "------------------------------------------------------------"
echo "smICA installer"
echo "------------------------------------------------------------"
echo


if [ ! -f "$LICENSE_FILE" ]; then
    echo "ERROR: LICENSE file not found in the current directory."
    echo "Expected: $PWD/$LICENSE_FILE"
    exit 1
fi

echo "This installer will set up smICA and its dependencies."
echo "smICA is licensed under the MIT License."
echo
echo "Displaying LICENSE..."
echo "------------------------------------------------------------"
show_file "$LICENSE_FILE"
echo "------------------------------------------------------------"
echo

while true; do
    echo "Choose an option:"
    echo "  [a] I acknowledge that I have read the license and want to continue the installation"
    echo "  [d] Abort the installation"
    echo "Choosing 'Abort' will only terminate the installer."
    echo "The source code remains available to you under the terms of the MIT license."
    prompt_choice "Your choice [a/d]:" "ad"

    if [ "$REPLY" = "a" ]; then
        echo "Continuing installation."
        break
    elif [ "$REPLY" = "d" ]; then
        abort_install
    fi
done


echo
echo "------------------------------------------------------------"
echo "Checking prerequisites"
echo "------------------------------------------------------------"

if ! command -v python3 >/dev/null 2>&1; then
    echo "Python3 is not installed. Please install Python 3.6 or higher and re-run this script."
    exit 1
fi


echo
echo "------------------------------------------------------------"
echo "Optional legacy PTU reader: readPTU_FLIM.py"
echo "------------------------------------------------------------"
echo
echo "smICA uses phconvert for supported PicoHarp 300 T3 files."
echo "The third-party readPTU_FLIM.py reader is only used as a fallback"
echo "for PTU record types that are not supported by the phconvert backend."
echo "Source URL:"
echo "  $THIRD_PARTY_URL"
echo

if [ -f "$THIRD_PARTY_TARGET" ]; then
    echo "readPTU_FLIM.py is already present; no download is needed."
else
    prompt_choice "Install the optional legacy PTU fallback? [y/n]:" "yn"
    if [ "$REPLY" = "y" ]; then
        echo "Downloading readPTU_FLIM.py..."
        mkdir -p "$THIRD_PARTY_TARGET_DIR"
        download_succeeded=0

        if command -v curl >/dev/null 2>&1; then
            if curl -fsSL "$THIRD_PARTY_URL" -o "$THIRD_PARTY_TARGET"; then
                download_succeeded=1
            fi
        fi
        if [ "$download_succeeded" -eq 0 ] && command -v wget >/dev/null 2>&1; then
            if wget -q "$THIRD_PARTY_URL" -O "$THIRD_PARTY_TARGET"; then
                download_succeeded=1
            fi
        fi

        if [ "$download_succeeded" -eq 1 ]; then
            echo "Optional legacy PTU fallback installed successfully."
        else
            rm -f "$THIRD_PARTY_TARGET"
            echo "WARNING: readPTU_FLIM.py could not be downloaded."
            echo "Installation will continue with the phconvert backend."
            echo "Only unsupported legacy PTU record types will be unavailable."
        fi
    else
        echo "Optional legacy PTU fallback skipped."
        echo "Installation will continue with the phconvert backend."
        echo "Only unsupported legacy PTU record types will be unavailable."
    fi
fi


echo
echo "------------------------------------------------------------"
echo "Python environment setup"
echo "------------------------------------------------------------"

echo "Checking for pip..."
if ! python3 -m pip --version >/dev/null 2>&1; then
    echo "Pip is not available. Creating a virtual environment to bootstrap pip."
    python3 -m venv "$VENV_DIR"
    source "$VENV_DIR/bin/activate"
    python -m ensurepip --upgrade
else
    echo "Pip is available. Proceeding."
fi

if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment in $VENV_DIR..."
    python3 -m venv "$VENV_DIR"
fi

echo "Activating virtual environment..."
source "$VENV_DIR/bin/activate"

echo "Upgrading pip in the virtual environment..."
python -m pip install --upgrade pip


echo "Installing dependencies using pip..."
python -m pip install .
if [ $? -ne 0 ]; then
    echo "Failed to install dependencies. Exiting."
    deactivate || true
    exit 1
fi

echo "Creating text-based automation client scripts..."
SMICA_CALL_SCRIPT="$PWD/$VENV_DIR/bin/smica-call"
SMICA_CALL_ALIAS="$PWD/$VENV_DIR/bin/smica_call"
cat <<'EOL' > "$SMICA_CALL_SCRIPT"
#!/usr/bin/env bash
# Text launcher for the smICA TCP client. No compiled launcher is used.
SCRIPT_DIRECTORY="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
exec "$SCRIPT_DIRECTORY/python" -m smICA.Required.automation_client "$@"
EOL
cp "$SMICA_CALL_SCRIPT" "$SMICA_CALL_ALIAS"
chmod +x "$SMICA_CALL_SCRIPT" "$SMICA_CALL_ALIAS"
if [ ! -x "$SMICA_CALL_SCRIPT" ] || [ ! -x "$SMICA_CALL_ALIAS" ]; then
    echo "Failed to create the automation client scripts. Exiting."
    deactivate || true
    exit 1
fi

echo "Building bundled documentation..."
if ! python src/smICA/Required/documentation_builder.py \
    --source docs \
    --target src/smICA/doc/assets/help_html; then
    echo "Failed to build the documentation. Exiting."
    deactivate || true
    exit 1
fi
echo "Documentation built successfully."


echo
echo "------------------------------------------------------------"
echo "Desktop integration"
echo "------------------------------------------------------------"

ICON_SRC="$PWD/src/smICA/res/icons/smICA.png"
ICON_DEST="$HOME/.local/share/icons/smICA.png"

echo "Preparing icon directory at $HOME/.local/share/icons/"
mkdir -p "$(dirname "$ICON_DEST")"
cp "$ICON_SRC" "$ICON_DEST"

echo "Updating icon cache..."
if command -v gtk-update-icon-cache >/dev/null 2>&1; then
    gtk-update-icon-cache "$HOME/.local/share/icons" || true
else
    echo "gtk-update-icon-cache not found; skipping icon cache update."
fi

echo "Creating run_smICA script..."
cat <<EOL > run_smICA
#!/bin/bash
source "$PWD/$VENV_DIR/bin/activate"
if [ "\${1:-}" = "--test" ]; then
    python "$PWD/smICA/calc_tests/unit_test/run_all.py"
    TEST_STATUS=\$?
    deactivate
    exit \$TEST_STATUS
fi
if [ "\${1:-}" = "--demo" ]; then
    python "$PWD/smICA/calc_tests/demo_data/run_demo.py"
    DEMO_STATUS=\$?
    deactivate
    exit \$DEMO_STATUS
fi
cd smICA/smICA
python "$PWD/smICA/smICA/smICA_tool.py" "\$@"
deactivate
EOL

chmod +x run_smICA
echo "run_smICA script created and made executable."
echo "Use 'run_smICA --test' to run the standalone unit tests."
echo "Use 'run_smICA --demo' to run the bundled end-to-end demonstration."
echo "Use 'run_smICA --automation-server' to start the local automation server."
echo "The text-based smica-call and smica_call Bash clients are installed in $PWD/$VENV_DIR/bin/."

DESKTOP_ENTRY_DIR="$HOME/.local/share/applications"
DESKTOP_ENTRY="$DESKTOP_ENTRY_DIR/smICA.desktop"
mkdir -p "$DESKTOP_ENTRY_DIR"

cat <<EOL > "$DESKTOP_ENTRY"
[Desktop Entry]
Version=1.0
Type=Application
Name=smICA
Comment=Run smICA application
Exec=$PWD/run_smICA
Path=$PWD/smICA/smICA/
Icon=$HOME/.local/share/icons/smICA.png
Terminal=false
Categories=Utility;Application;
EOL

echo "Desktop entry created at $DESKTOP_ENTRY"


echo
echo "------------------------------------------------------------"
echo "Reorganizing project files"
echo "------------------------------------------------------------"

echo "Deactivating virtual environment..."
deactivate

echo "Renaming src directory to smICA..."
mv src smICA

echo "Moving files to smICA directory..."
for file in *; do
    if [[ "$file" != "install.sh" && "$file" != "setup.py" && "$file" != "run_smICA" && "$file" != "smICA" && "$file" != "v_smICA_env" && "$file" != "python_embedded" && "$file" != "REWRITE_ROI" && "$file" != "Docs" ]]; then
        mv "$file" smICA/
    fi
done

echo "Removing setup.py and install.sh..."
rm -rf setup.py install.sh python_embedded

echo
echo "All files successfully organized and cleaned up."
echo "Installation and reorganization completed successfully!"
