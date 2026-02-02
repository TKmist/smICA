import sys
from setuptools import setup, find_packages
from setuptools.command.install import install
import os
import urllib.request

version_path='VERSION'

with open(version_path, 'r') as file:
    VERSION = file.read()

win_packages = ['pywin32']
basic_packages = [
"dearpygui==2.0.0",
        "pandas==2.2.3",
        "numpy==1.26.4",
        "decorator==5.2.1",
        "screeninfo==0.8.1",
        "opencv-python==4.11.0.86",
        "scikit-image==0.25.2",
        "requests==2.32.3",
        "matplotlib==3.9.2",
        "numba==0.60.0",
        "scipy==1.15.3",
]
req_pack = []
if os.name == 'nt':
    req_pack = basic_packages + win_packages
elif os.name == 'posix':
    req_pack = basic_packages


class runInstall(install):
    """Download `readPTU_FLIM.py` from GitHub."""

        
    def run(self):
        
        install.run(self)

        # Read installer decision from environment
        flag = os.environ.get("SMICA_DOWNLOAD_READPTU_FLIM", "").strip().lower()
        download_enabled = flag in ("1", "true", "yes", "y", "on")
        
        if not download_enabled:
            print("Skipping download of readPTU_FLIM.py (SMICA_DOWNLOAD_READPTU_FLIM=0).")
            return
        
        url = "https://raw.githubusercontent.com/TKmist/readPTU_FLIM/refs/heads/NIKON_correction/readPTU_FLIM.py"
        
        
        target_directory = os.path.join(os.path.dirname(__file__), "src/smICA/Required/Third_party")
        target_file = os.path.join(target_directory, "readPTU_FLIM.py")
        
        
        os.makedirs(target_directory, exist_ok=True)
        
        
        try:
            print(f"Downloading `readPTU_FLIM.py` from {url} to {target_file}...")
            urllib.request.urlretrieve(url, target_file)
            print("\nDownload complete.\n")
        except Exception as e:
            print(f"\nFailed to download `readPTU_FLIM.py`: {e}")
            print(f"Please manually download the file from: {url}")
            print(f"Once downloaded, place it in the following directory: {target_directory}\n")


setup(
    name='smICA',
    version=VERSION,
    packages=find_packages(),
    include_package_data=True,
    install_requires=req_pack,
    python_requires='>=3.11.5',
    cmdclass={
        'install': runInstall, 
    },
    author='TKmist',
    license='MIT',

)
