#!/bin/bash

# -----------------------------
# Configuration
# -----------------------------

# Define the name of the virtual environment directory
VENV_DIR="v_smICA_env"

# External third-party resource(s) fetched during installation
THIRD_PARTY_URL="https://raw.githubusercontent.com/TKmist/readPTU_FLIM/refs/heads/NIKON_correction/readPTU_FLIM.py"
THIRD_PARTY_LICENSE_HINT="Licensing information is typically provided in the upstream repository (e.g., LICENSE file and/or README). Please review it before accepting."

# -----------------------------
# Helper functions
# -----------------------------

abort_install() {
  # Abort installation with a clear message and non-zero exit code.
  echo
  echo "Installation aborted."
  exit 1
}

prompt_yes_no() {
  # Ask a yes/no question in English and require an explicit yes/no answer.
  # Usage: prompt_yes_no "Your question here"
  local prompt="$1"
  local reply=""

  while true; do
    read -r -p "${prompt} [y/N]: " reply
    case "${reply}" in
      [yY]|[yY][eE][sS]) return 0 ;;
      [nN]|[nN][oO]|"")  return 1 ;;
      *) echo "Please answer 'y' or 'n'." ;;
    esac
  done
}

show_license_and_require_acceptance() {
  # Display the LICENSE file and require user acceptance to continue.
  if [[ ! -f "LICENSE" ]]; then
    echo "ERROR: LICENSE file not found in the current directory."
    echo "Please ensure you run this installer from the project root (where LICENSE exists)."
    abort_install
  fi

  echo "========================================"
  echo "               LICENSE                  "
  echo "========================================"
  echo
  cat "LICENSE"
  echo
  echo "========================================"
  echo

  if ! prompt_yes_no "Do you accept the terms of the LICENSE agreement?"; then
    echo "You did not accept the LICENSE terms."
    abort_install
  fi
}

inform_third_party_and_require_acceptance() {
  # Inform the user about third-party downloads and require acceptance.
  echo
  echo "========================================"
  echo "         THIRD-PARTY COMPONENTS         "
  echo "========================================"
  echo
  echo "This installer will download and use third-party scripts/libraries from external sources."
  echo "Example resource:"
  echo "  - ${THIRD_PARTY_URL}"
  echo
  echo "${THIRD_PARTY_LICENSE_HINT}"
  echo "By continuing, you confirm you understand and accept that third-party components may have their own licenses and terms."
  echo

  if ! prompt_yes_no "Do you agree to proceed with installation including third-party components?"; then
    echo "You did not agree to install third-party components."
    abort_install
  fi
}

if ! command -v python3 &> /dev/null; then
  echo "Python3 is not installed. Please install Python 3.6 or higher and re-run this script."
  exit 1
fi


show_license_and_require_acceptance
inform_third_party_and_require_acceptance
# Check if pip is available or create a virtual environment first
echo "Checking for pip..."
if ! python3 -m pip --version &> /dev/null; then
    echo "Pip is not available. Creating a virtual environment to bootstrap pip."
    python3 -m venv $VENV_DIR
    if [ $? -ne 0 ]; then
        echo "Failed to create a virtual environment. Exiting."
        exit 1
    fi
    source "$VENV_DIR/bin/activate"
    python -m ensurepip --upgrade
    if [ $? -ne 0 ]; then
        echo "Failed to bootstrap pip in the virtual environment. Exiting."
        deactivate
        exit 1
    fi
else
    echo "Pip is available. Proceeding."
fi

# Create a virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment in $VENV_DIR..."
    python3 -m venv $VENV_DIR
    if [ $? -ne 0 ]; then
        echo "Failed to create a virtual environment. Exiting."
        exit 1
    fi
fi

# Activate the virtual environment
echo "Activating virtual environment..."
source "$VENV_DIR/bin/activate"
if [ $? -ne 0 ]; then
    echo "Failed to activate the virtual environment. Exiting."
    exit 1
fi

# Upgrade pip in the virtual environment
echo "Upgrading pip in the virtual environment..."
python -m pip install --upgrade pip

# Install the package and dependencies using pip
echo "Installing dependencies using pip..."
python -m pip install .
if [ $? -ne 0 ]; then
    echo "Failed to install dependencies. Exiting."
    deactivate
    exit 1
fi

# Ensure the icon directory exists and copy the icon
ICON_SRC="$PWD/src/smICA/res/icons/smICA.png"
ICON_DEST="$HOME/.local/share/icons/smICA.png"
echo "Preparing icon directory at $HOME/.local/share/icons/"
mkdir -p "$(dirname "$ICON_DEST")"
cp "$ICON_SRC" "$ICON_DEST"
if [ $? -ne 0 ]; then
    echo "Failed to copy icon to $ICON_DEST. Exiting."
    deactivate
    exit 1
fi

# Update the icon cache
echo "Updating icon cache..."
gtk-update-icon-cache "$HOME/.local/share/icons"

# Create run_app.sh script
echo "Creating run_smICA script..."
cat <<EOL > run_smICA
#!/bin/bash
# Activate the virtual environment and run the main script

source "$PWD/$VENV_DIR/bin/activate"
cd smICA/smICA
python "$PWD/smICA/smICA/smICA_tool.py"
deactivate
EOL

# Make run_smICA executable
chmod +x run_smICA
if [ $? -ne 0 ]; then
    echo "Failed to make run_FcsIT executable. Exiting."
    deactivate
    exit 1
fi
echo "run_FcsIT script created and made executable."

# Create a .desktop entry in KDE/GNOME menu
DESKTOP_ENTRY_DIR="$HOME/.local/share/applications"
DESKTOP_ENTRY="$DESKTOP_ENTRY_DIR/smICA.desktop"

# Ensure the directory exists
mkdir -p "$DESKTOP_ENTRY_DIR"

# Generate the .desktop file
cat <<EOL > "$DESKTOP_ENTRY"
[Desktop Entry]
Version=1.2.0
Type=Application
Name=smICA
Comment=Run smICA application
Exec=$PWD/run_smICA
Path=$PWD/smICA/smICA/
Icon=$HOME/.local/share/icons/smICA.png
Terminal=false
Categories=Utility;Application;
EOL

if [ $? -ne 0 ]; then
    echo "Failed to create desktop entry. Exiting."
    deactivate
    exit 1
fi
echo "Desktop entry created at $DESKTOP_ENTRY"

# Deactivate the virtual environment
echo "Deactivating virtual environment..."
deactivate

echo "Renaming src directory to smICA..."
mv src smICA
if [ $? -ne 0 ]; then
    echo "Failed to rename src directory to smICA. Exiting."
    exit 1
fi

# Step 2: Move all files in the main directory (except install.sh and setup.py) to the smICA directory
echo "Moving files to smICA directory..."
for file in *; do
    if [[ "$file" != "install.sh" && "$file" != "setup.py" && "$file" != "run_smICA" && "$file" != "smICA" && "$file" != "v_smICA_env" && "$file" != "python_embedded" && "$file" != "REWRITE_ROI"  && "$file" != "Docs" ]]; then
        mv "$file" smICA/
        if [ $? -ne 0 ]; then
            echo "Failed to move file $file to smICA directory. Exiting."
            exit 1
        fi
    fi
done

# Step 3: Remove setup.py and install.sh
echo "Removing setup.py and install.sh..."
rm -f -R setup.py install.sh python_embedded
if [ $? -ne 0 ]; then
    echo "Failed to remove setup.py or install.sh. Exiting."
    exit 1
fi


# Confirm completion
echo "All files successfully organized and cleaned up."
echo "Installation and reorganization completed successfully!"
