# ISA_STUB: solo importaciones de Panel.py. Generado por publicar_compilacion.py.
# PyInstaller necesita ver qué librerías usa el programa; el programa real está
# ofuscado en obf_win/, obf_mac/, obf_mac_intel/ y obf_linux/.
if __name__ == "__isa_stub__":
    from importlib.metadata import version as _pytz_version
    from licencia import check_module_license
    from linearmodels.iv import IV2SLS
    from linearmodels.panel import PooledOLS, PanelOLS, RandomEffects, FirstDifferenceOLS, compare
    from linearmodels.panel.results import PanelEffectsResults, RandomEffectsResults
    from linearmodels.panel.unitroot import LevinLinChu, ImPesaranShin, ADF, Hadri
    from pathlib import Path
    from pydynpd import regression as pydynpd_reg
    from scipy.stats import chi2
    from scipy.stats import norm
    from statsmodels.stats.diagnostic import het_breuschpagan
    from tkinter import ttk, filedialog, messagebox
    from tkinter.scrolledtext import ScrolledText
    import ia_config
    import ia_guias
    import json
    import numpy as np
    import pandas as pd
    import pyreadstat
    import pytz as _pytz
    import statsmodels.api as sm
    import sys
    import tkinter as tk
    import warnings
