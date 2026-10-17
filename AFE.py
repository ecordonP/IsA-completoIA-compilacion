# ISA_STUB: solo importaciones de AFE.py. Generado por publicar_compilacion.py.
# PyInstaller necesita ver qué librerías usa el programa; el programa real está
# ofuscado en obf_win/, obf_mac/, obf_mac_intel/ y obf_linux/.
if __name__ == "__isa_stub__":
    from dataclasses import dataclass
    from factor_analyzer import FactorAnalyzer
    from factor_analyzer.factor_analyzer import calculate_bartlett_sphericity, calculate_kmo
    from factor_analyzer.polychoric import calculate_polychoric_correlation_matrix
    from factor_analyzer.utils import calculate_polychoric_correlation_matrix
    from importlib.metadata import version as _pytz_version
    from licencia import check_module_license
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    from matplotlib.figure import Figure
    from numpy.linalg import eigh
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as ReportLabImage, Table, TableStyle, PageBreak
    from tkinter import ttk, filedialog, messagebox
    from tkinter.scrolledtext import ScrolledText
    import ctypes
    import ia_config
    import ia_guias
    import inspect as _inspect
    import io
    import json
    import matplotlib.pyplot as plt
    import numpy as np
    import os
    import pandas as pd
    import prince
    import pyreadstat
    import pytz as _pytz
    import semopy
    import sklearn.utils as _sk_utils
    import sklearn.utils.validation as _sk_val
    import sys
    import tkinter as tk
    import warnings
