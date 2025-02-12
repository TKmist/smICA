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
'argon2-cffi',
'argon2-cffi-bindings',
'asteval',
'asttokens',
'async-lru',
'attrs',
'Babel',
'beautifulsoup4',
'bleach',
'Bottleneck',
'Brotli',
'build',
'CacheControl',
'certifi',
'cffi',
'charset-normalizer',
'cleo',
'comm',
'contourpy',
'crashtest',
'cryptography',
'cycler',
'dearpygui==2.0.0',
'debugpy',
'decorator',
'defusedxml',
'dill',
'distlib',
'dulwich',
'et-xmlfile',
'executing',
'fastjsonschema',
'filelock',
'fonttools',
'future',
'h11',
'httpcore',
'httpx',
'idna',
'importlib_metadata',
'importlib_resources',
'installer',
'ipykernel',
'ipython',
'ipywidgets',
'jaraco.classes',
'jaraco.context',
'jaraco.functools',
'jedi',
'jeepney',
'Jinja2',
'json5',
'jsonschema',
'jsonschema-specifications',
'keyring',
'kiwisolver',
'llvmlite==0.43.0',
'lmfit',
'MarkupSafe',
'matplotlib==3.9.2',
'matplotlib-inline',
'mistune',
'mkl-service==2.4.2',
'mkl_fft',
'mkl_random',
'more-itertools',
'MouseInfo',
'mpmath',
'msgpack',
'nbclient',
'nbconvert',
'nbformat',
'nest-asyncio',
'notebook',
'notebook_shim',
'numba==0.60.0',
'numexpr',
'numpy',
'opencv-python>=4.10.0',
'opencv-python-headless>=4.10.0',
'openpyxl',
'overrides',
'packaging',
'pandas',
'pandocfilters',
'parso',
'pexpect',
'pillow',
'pkginfo',
'platformdirs',
'ply',
'poetry',
'poetry-core',
'prometheus_client',
'prompt-toolkit',
'psutil',
'ptyprocess',
'pure-eval',
'PyAutoGUI',
'pycparser',
'Pygments',
'PyMsgBox',
'pyparsing',
'pyperclip',
'pyproject_hooks',
'PyQt5==5.15.10',
'PyQt5-sip',
'PyScreeze',
'PySocks',
'python-dateutil',
'python-json-logger',
'python-xlib',
'pytweening',
'pytz',
'PyYAML',
'pyzmq',
'qtconsole',
'QtPy',
'rapidfuzz',
'referencing',
'requests',
'requests-toolbelt',
'rfc3339-validator',
'rfc3986-validator',
'rpds-py',
'rubicon-objc',
'scipy',
'screeninfo',
'SecretStorage',
'Send2Trash',
'setuptools==72.1.0',
'setuptools-scm',
'shellingham',
'sip',
'six',
'sniffio',
'soupsieve',
'stack-data',
'sympy',
'terminado',
'tinycss2',
'tomli',
'tomlkit',
'tornado',
'tqdm',
'traitlets',
'trove-classifiers',
'typing_extensions',
'tzdata',
'uncertainties',
'unicodedata2',
'urllib3',
'virtualenv',
'wcwidth',
'webencodings',
'websocket-client',
'wheel==0.44.0',
'widgetsnbextension',
'zipp',

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
        
        
        url = "https://raw.githubusercontent.com/TKmist/readPTU_FLIM/refs/heads/NIKON_correction/readPTU_FLIM.py"
        
        
        target_directory = os.path.join(os.path.dirname(__file__), "src/smICA/Required")
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