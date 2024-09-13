#!/usr/bin/env python
# coding: utf-8

# In[5]:


import sys
import os
import numpy as np
from dep.CLI_classes import CLI
# Check if an argument is provided
print(sys.argv[0])
if len(sys.argv) != 4:
    print(sys.argv[0])
    print("Usage: python "+sys.argv[0]+" <Path to JSON workspace file> <Path to output folder> <format of the output file>")
    sys.exit(1)
# Get the argument from the command line
workspace_info_path = sys.argv[1]
output_path = sys.argv[2]
output_format = sys.argv[3]
# workspace_info_path = 'samples/PTU/workspace_info.json'
# output_path = 'samples/'
# output_format = 'csv'
cli = CLI(workspace_info_path,output_path,output_format)

with open('../LICENSE', 'r') as file:
    Licence = file.read()
with open('../VERSION', 'r') as file:
    VERSION = file.read()
line='=============================================================================='



def execfile(filepath, globals=globals(), locals=None):
    '''Import module allowing execution of external python scripts as part of the main code. This part of the code is based on the following source: https://stackoverflow.com/a/41658338 '''
    globals.update({
        "__file__": filepath,
        "__name__": "__main__",
    })
    with open(filepath, 'rb') as file:
        exec(compile(file.read(), filepath, 'exec'), globals, locals)
import platform
import os
import datetime
import warnings
warnings.filterwarnings('ignore')
print(line)
print(line,end='\n\n')
print(Licence)
print('\n')
print('VERSION = ',VERSION,end='\n')
print(line)
print(line,end='\n\n')

cli.print_init()

# print(cli.workspace_path)
# print(cli.setts)

# print('\n\n\n====================================================\n\n')

# cli.print_pretty_dict(cli.setts)

# cli.ptu_files

for f in cli.ptu_files[:2]:
    cli.load_ptu_file(f,cli.PTU_directory_path)
    cli.calculate(cli.an_file)
#     print(cli.Current_image_1)
#     print(cli.Current_image_2)
    # print(cli.Sing_Results_DF)
    cli.export_results()


# In[8]:




