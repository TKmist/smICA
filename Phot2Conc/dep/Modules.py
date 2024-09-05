
log_it('Modules - loaded on '+str(datetime.datetime.now()),'a')
import numpy as np
import pandas as pd
import time
from numpy import log10, sqrt, exp, log, pi
import json
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.gridspec as gridspec
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib as mpl
from sympy.parsing.sympy_parser import parse_expr
from sympy import latex
from PIL import Image
import pyautogui
from io import BytesIO
import matplotlib.pyplot as plt
from matplotlib.transforms import Bbox
from lmfit import Model, Parameters
import ast
import webbrowser
import sys
np.seterr(divide='ignore')
from scipy.stats import median_abs_deviation
mpl.use('Agg')




