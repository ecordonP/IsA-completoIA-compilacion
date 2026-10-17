# ISA_STUB: solo importaciones de Cluster.py. Generado por publicar_compilacion.py.
# PyInstaller necesita ver qué librerías usa el programa; el programa real está
# ofuscado en obf_win/, obf_mac/, obf_mac_intel/ y obf_linux/.
if __name__ == "__isa_stub__":
    from datetime import datetime
    from importlib.metadata import version as _pytz_version
    from licencia import check_module_license
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
    from matplotlib.figure import Figure
    from pathlib import Path
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as ReportLabImage, Table, TableStyle, PageBreak
    from scipy.cluster.hierarchy import dendrogram, linkage
    from scipy.optimize import minimize_scalar
    from scipy.spatial.distance import squareform
    from scipy.stats import chi2_contingency, f_oneway, kruskal
    from scipy.stats import multivariate_normal, norm
    from sklearn.base import clone
    from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
    from sklearn.decomposition import PCA
    from sklearn.ensemble import IsolationForest
    from sklearn.impute import SimpleImputer
    from sklearn.metrics import adjusted_rand_score, calinski_harabasz_score, davies_bouldin_score, silhouette_score
    from sklearn.neighbors import NearestNeighbors
    from sklearn.preprocessing import RobustScaler, StandardScaler
    from sklearn_extra.cluster import KMedoids
    from statsmodels.stats.correlation_tools import corr_nearest
    from tkinter import filedialog, messagebox, ttk
    from tkinter.scrolledtext import ScrolledText
    import ctypes
    import ia_config
    import ia_guias
    import io
    import json
    import matplotlib
    import matplotlib.pyplot as plt
    import multiprocessing
    import numpy as np
    import os
    import pandas as pd
    import platform
    import pyreadstat
    import pytz as _pytz
    import queue
    import reportlab
    import scipy
    import sklearn
    import statsmodels
    import sys
    import tempfile
    import threading
    import tkinter as tk
    import traceback
