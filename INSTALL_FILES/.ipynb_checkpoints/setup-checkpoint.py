import sys
from setuptools import setup, find_packages
from setuptools.command.install import install
import os
import urllib.request

version_path='VERSION'#os.path.join('src',)

with open(version_path, 'r') as file:
    VERSION = file.read()

win_packages = ['pywin32']
basic_packages = [
'asteval',
'Bottleneck',
'contourpy',
'cycler',
'dearpygui==1.11.1',
'dill',
'EasyProcess',
'entrypoint2',
'fonttools',
'future',
'jeepney',
'kiwisolver',
'llvmlite',
'lmfit==1.3.2',
'matplotlib==3.8.4',
'mkl_fft',
'mkl_random',
'MouseInfo',
'mpmath',
'mss',
'multipletau==0.4.1',
'numba==0.59.1',
'numexpr',
'numpy==1.26.4',
'opencv',
'packaging',
'pandas==2.2.2',
'pillow',
'ply',
'PyMsgBox',
'pyparsing',
'pyperclip',
'PyQt5==5.15.10',
'PyQt5-sip',
'pyscreenshot',
'PyScreeze',
'python-dateutil',
'python-xlib',
'pytweening',
'pytz',
'pyautogui',
'rubicon-objc',
'scipy==1.14.1',
'screeninfo==0.8.1',
'setuptools==75.1.0',
'setuptools-scm',
'sip',
'six',
'sympy==1.12',
'tomli',
'tornado',
'typing_extensions',
'tzdata',
'uncertainties',
'unicodedata2',
'wheel==0.44.0',
]
req_pack = []
if os.name == 'nt':
    req_pack = basic_packages + win_packages
elif os.name == 'posix':
    req_pack = basic_packages


class runInstall(install):
    """Download `readPTU_FLIM.py` from GitHub."""

        
    def run(self):
        # Run the standard install first
        install.run(self)
        
        # Specify the URL of the file on GitHub
        url = "https://raw.githubusercontent.com/TKmist/readPTU_FLIM/refs/heads/NIKON_correction/readPTU_FLIM.py"
        
        # Specify the target directory (e.g., where your package installs files)
        target_directory = os.path.join(os.path.dirname(__file__), "src/Methods/PTU_Corr/include")
        target_file = os.path.join(target_directory, "readPTU_FLIM.py")
        
        # Ensure the target directory exists
        os.makedirs(target_directory, exist_ok=True)
        
        # Download the file
        try:
            print(f"Downloading `readPTU_FLIM.py` from {url} to {target_file}...")
            urllib.request.urlretrieve(url, target_file)
            print("\nDownload complete.\n")
        except Exception as e:
            print(f"\nFailed to download `readPTU_FLIM.py`: {e}")
            print(f"Please manually download the file from: {url}")
            print(f"Once downloaded, place it in the following directory: {target_directory}\n")


setup(
    name='FcsIT',
    version=VERSION,
    packages=find_packages(),
    include_package_data=True,
    install_requires=req_pack,
    python_requires='>=3.11.5',
    cmdclass={
        'install': runInstall,  # Replace the install command
    },
    author='TKmist',
    license='GPL-2.0',

)