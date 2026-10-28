from setuptools import setup, find_packages
import os

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
        "seaborn==0.13.2",
        "scikit-learn==1.5.2",
        "numba==0.60.0",
        "scipy==1.15.3",
        "phconvert==0.10.1",
        "jupyter-book==2.1.2",
]
req_pack = []
if os.name == 'nt':
    req_pack = basic_packages + win_packages
elif os.name == 'posix':
    req_pack = basic_packages


setup(
    name='smICA',
    version=VERSION,
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=req_pack,
    python_requires='>=3.11.5',
    author='TKmist',
    license='MIT',

)
