# ISA_STUB: solo importaciones de Series.py. Generado por publicar_compilacion.py.
# PyInstaller necesita ver qué librerías usa el programa; el programa real está
# ofuscado en obf_win/, obf_mac/, obf_mac_intel/ y obf_linux/.
if __name__ == "__isa_stub__":
    from arch import arch_model
    from dataclasses import dataclass
    from importlib.metadata import version as _pytz_version
    from licencia import check_module_license
    from lightgbm import LGBMRegressor
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
    from matplotlib.figure import Figure
    from prophet import Prophet
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import Image as RLImage
    from reportlab.platypus import SimpleDocTemplate, Spacer, Preformatted, Paragraph
    from scipy.sparse import SparseEfficiencyWarning
    from scipy.stats import yeojohnson
    from sklearn.ensemble import GradientBoostingRegressor
    from sklearn.ensemble import RandomForestRegressor
    from statsmodels.stats.diagnostic import acorr_ljungbox, het_arch
    from statsmodels.stats.stattools import durbin_watson, jarque_bera
    from statsmodels.tools.sm_exceptions import ConvergenceWarning, InterpolationWarning, SpecificationWarning
    from statsmodels.tsa.ar_model import AutoReg
    from statsmodels.tsa.ardl import ARDL
    from statsmodels.tsa.forecasting.theta import ThetaModel
    from statsmodels.tsa.holtwinters import ExponentialSmoothing
    from statsmodels.tsa.seasonal import STL
    from statsmodels.tsa.statespace.sarimax import SARIMAX
    from statsmodels.tsa.statespace.structural import UnobservedComponents
    from statsmodels.tsa.stattools import acf, adfuller, kpss, pacf, zivot_andrews
    from statsmodels.tsa.vector_ar.var_model import VAR
    from statsmodels.tsa.vector_ar.vecm import VECM
    from tkinter import filedialog, messagebox, ttk
    from typing import Any, Optional
    from ui_adapt import apply_tk_scaling, maximize_window, set_dpi_awareness
    from xgboost import XGBRegressor
    import csv
    import html
    import ia_config
    import ia_guias
    import io
    import json
    import logging
    import math
    import numpy as np
    import os
    import pandas as pd
    import pyreadstat
    import pytz as _pytz
    import threading
    import tkinter as tk
    import warnings
