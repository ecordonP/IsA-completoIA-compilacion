# -*- mode: python ; coding: utf-8 -*-
#
# Spec único de IsA completo (menú + 21 módulos) para Windows, macOS y Linux.
#
#   Windows (x86_64): carpeta dist/IsA con Menu.exe y los 21 módulos .exe, que
#                     comparten la carpeta _internal (como en la distribución C:\IsA).
#   Linux (x86_64):   carpeta dist/IsA, igual que en Windows.
#   macOS:            dist/IsA.app con todos los ejecutables en Contents/MacOS, que
#                     comparten Contents/Frameworks. Apple Silicon (arm64, por
#                     defecto) o Intel (ISA_TARGET_ARCH=x86_64).
# Menu.py lanza los módulos desde la carpeta de su propio ejecutable.
#
# Ofuscación: los scripts se ofuscan en Windows con `python obfuscate.py` (pyarmor) en
# obf_win/, obf_mac/, obf_mac_intel/ y obf_linux/, y este spec sustituye en cada Analysis
# el código fuente por el ofuscado (equivale al parche que genera `pyarmor gen --pack`,
# que solo admite un Analysis).
#
# Las opciones de cada módulo son las de su <modulo>_onedir.spec de Windows.
#
# Variables de entorno opcionales:
#     ISA_TARGET_ARCH         macOS: arm64 (Apple Silicon, por defecto) o x86_64 (Intel)
#     ISA_OBF_DIR             carpeta con los scripts ofuscados (por defecto la de la plataforma)
#     ISA_REQUIRE_PYARMOR=1   falla si no hay scripts ofuscados (lo usa la CI)
#     ISA_CODESIGN_IDENTITY   macOS: identidad "Developer ID Application: ..." para firmar
import os
import sys

from PyInstaller.utils.hooks import (collect_all, collect_data_files, collect_dynamic_libs,
                                     collect_submodules, copy_metadata)

ROOT = SPECPATH
IS_WIN = sys.platform == 'win32'
IS_MAC = sys.platform == 'darwin'
IS_LINUX = sys.platform.startswith('linux')

TARGET_ARCH = os.environ.get('ISA_TARGET_ARCH', 'arm64') if IS_MAC else None
if IS_WIN:
    _default_obf = 'obf_win'
elif IS_MAC:
    _default_obf = 'obf_mac' if TARGET_ARCH == 'arm64' else 'obf_mac_intel'
else:
    _default_obf = 'obf_linux'
OBF = os.environ.get('ISA_OBF_DIR', os.path.join(ROOT, _default_obf))
RUNTIME_PKG = 'pyarmor_runtime_011681'
USE_PYARMOR = os.path.isdir(os.path.join(OBF, RUNTIME_PKG))
if os.environ.get('ISA_REQUIRE_PYARMOR') == '1' and not USE_PYARMOR:
    raise SystemExit(f'No se encuentran los scripts ofuscados en {OBF}')

CODESIGN_IDENTITY = (os.environ.get('ISA_CODESIGN_IDENTITY') or None) if IS_MAC else None
ENTITLEMENTS = os.path.join(ROOT, 'entitlements.plist') if CODESIGN_IDENTITY else None
ICON = os.path.join(ROOT, 'IsA.ico')  # en macOS PyInstaller lo convierte a .icns con Pillow

PYREADSTAT_IMPORTS = [
    'pyreadstat._readstat_writer',
    'pyreadstat._readstat_parser',
    'pyreadstat.worker',
    'scipy.special._cdflib',
]
# El arranque de PyInstaller (pyi_rth_pkgres) carga pkg_resources, que necesita jaraco y
# backports.tarfile. Se incluyen en cada programa: si no, rthook_block_foreign_packages los
# trata como paquetes ajenos de la carpeta compartida y el programa no arranca.
PKG_RESOURCES_IMPORTS = ['jaraco.text', 'jaraco.context', 'jaraco.functools', 'backports.tarfile']
if IS_LINUX:
    # PIL.ImageTk carga PIL._tkinter_finder de forma dinámica (PyInstaller no lo ve) y sin
    # él falla «invalid command name PyImagingPhoto» en los módulos con imágenes
    PKG_RESOURCES_IMPORTS += ['PIL._tkinter_finder']
BOKEH_IMPORTS = [
    'bokeh.resources',
    'bokeh.util',
    'bokeh._version',
    'bokeh.settings',
    'bokeh.core.templates',
    'bokeh.core.property.bases',
    'bokeh.core.property.container',
    'bokeh.core.property.singletons',
    'bokeh.core.property.descriptors',
    'bokeh.core.property.struct',
]
TKAGG_IMPORTS = ['matplotlib.backends.backend_tkagg', 'matplotlib.backends._backend_tk']

# Informe IA (ia_config.py): SDK de Claude (importado solo al usarlo) y exportación a Word
AI_IMPORTS = collect_submodules('anthropic') + ['docx']
AI_DATAS = collect_data_files('docx') + copy_metadata('anthropic')

# Con todos los módulos en una misma carpeta, evita que un módulo importe como
# namespace package vacío una librería que solo incluye otro (ver el propio hook).
COMMON_RTHOOKS = [os.path.join(ROOT, 'rthook_block_foreign_packages.py')]
if IS_MAC:
    # En macOS Tk no aplica `tk scaling` a la letra; el hook la escala como en Windows
    COMMON_RTHOOKS.append(os.path.join(ROOT, 'rthook_mac_tk_fonts.py'))
if IS_LINUX:
    # Los programas del sistema que se lanzan no heredan _internal
    COMMON_RTHOOKS.append(os.path.join(ROOT, 'rthook_linux_env.py'))
BOKEH_RTHOOK = [os.path.join(ROOT, 'rthook_bokeh_no_notebook.py')]

PYREADSTAT_LIBS = collect_dynamic_libs('pyreadstat')
BOKEH_IPYTHON_DATAS = (copy_metadata('bokeh') + copy_metadata('IPython') + copy_metadata('pyreadstat')
                       + collect_data_files('bokeh') + collect_data_files('IPython'))

# --- Regresion y Regcateg: diagnostic.py de statsmodels como dato ---
import statsmodels.stats.diagnostic as _sm_diagnostic
_diagnostic_datas = BOKEH_IPYTHON_DATAS + [(os.path.abspath(_sm_diagnostic.__file__), 'statsmodels/stats')]

# --- Series: prophet, cmdstanpy, xgboost, lightgbm y arch completos ---
_series_datas = collect_data_files('matplotlib') + collect_data_files('pyreadstat') + copy_metadata('pytz')
_series_binaries = list(PYREADSTAT_LIBS)
_series_hidden = [
    'pyreadstat', 'prophet', 'cmdstanpy', 'arch', 'xgboost', 'lightgbm', 'matplotlib', 'statsmodels',
    'statsmodels.tsa.statespace.sarimax', 'statsmodels.tsa.statespace.structural',
    'statsmodels.tsa.holtwinters', 'statsmodels.tsa.forecasting.theta', 'statsmodels.tsa.ar_model',
    'statsmodels.tsa.ardl', 'statsmodels.tsa.vector_ar.var_model', 'statsmodels.tsa.vector_ar.vecm',
] + TKAGG_IMPORTS
for _pkg in ('prophet', 'cmdstanpy', 'xgboost', 'lightgbm', 'arch'):
    try:
        _d, _b, _h = collect_all(_pkg)
        _series_datas += _d
        _series_binaries += _b
        _series_hidden += _h
    except Exception:
        pass

# --- Bayesiano: pymc/pytensor/arviz completos; pytensor con backend Python (rthook_pytensor) ---
_bayes_hidden = ['tkinter', 'tkinter.ttk', 'tkinter.filedialog', 'tkinter.messagebox', 'tkinter.scrolledtext']
for _pkg in ('numpy', 'pandas', 'matplotlib', 'seaborn', 'pymc', 'pytensor', 'statsmodels',
             'sklearn', 'arviz', 'arviz_base', 'xarray', 'pyreadstat'):
    try:
        _bayes_hidden += collect_submodules(_pkg)
    except Exception:
        pass
_bayes_datas = []
for _pkg in ('matplotlib', 'seaborn', 'statsmodels', 'arviz', 'arviz_base', 'pymc', 'pytensor',
             'xarray', 'pyreadstat'):
    try:
        _bayes_datas += collect_data_files(_pkg)
    except Exception:
        pass
_bayes_binaries = []
for _pkg in ('pytensor', 'pyreadstat', 'numpy', 'pandas'):
    _bayes_binaries += collect_dynamic_libs(_pkg)
_bayes_excludes = [
    'aesara', 'numba', 'llvmlite', 'pytest', 'torch', 'numpy.f2py.tests', 'numpy.tests',
    'scipy.tests', 'scipy._lib.array_api_compat.torch', 'matplotlib.tests', 'matplotlib.testing',
    'sklearn.externals.array_api_compat.torch',
]

# --- Cluster ---
_cluster_hidden = ['matplotlib.backends.backend_tkagg', 'sklearn.utils._cython_blas',
                   'sklearn.neighbors._partition_nodes', 'sklearn.manifold', 'sklearn.manifold._mds']
for _mod in ('factor_analyzer.polychoric', 'factor_analyzer.utils', 'sklearn_extra.cluster'):
    try:
        __import__(_mod)
        _cluster_hidden.append(_mod)
    except Exception:
        pass
_cluster_datas, _cluster_binaries = [], []
for _pkg in ('matplotlib', 'reportlab', 'sklearn', 'numpy', 'scipy', 'pandas', 'statsmodels', 'pyreadstat'):
    try:
        _cluster_datas += collect_data_files(_pkg)
    except Exception:
        pass
for _pkg in ('numpy', 'scipy', 'sklearn', 'matplotlib', 'pyreadstat'):
    try:
        _cluster_binaries += collect_dynamic_libs(_pkg)
    except Exception:
        pass
for _pkg in ('matplotlib', 'numpy', 'pandas', 'pyreadstat', 'reportlab', 'scikit-learn', 'scipy', 'statsmodels'):
    try:
        _cluster_datas += copy_metadata(_pkg)
    except Exception:
        pass

_menu_files = ['LogoOE2.png', 'logoIsA.png', 'logoIA.png', 'licencia.md'] + (['IsA.ico'] if IS_LINUX else [])

# (nombre del ejecutable = nombre en APPS de Menu.py, script, opciones de Analysis)
TARGETS = [
    ('Menu', 'Menu.py', dict(
        datas=[(os.path.join(ROOT, f), '.') for f in _menu_files],
    )),
    ('Datos', 'Datos.py', dict(
        excludes=[
            'torch', 'torchvision', 'torchaudio', 'transformers', 'tokenizers',
            'safetensors', 'onnxruntime', 'tensorflow', 'keras', 'jax', 'jaxlib',
            'numba', 'llvmlite',
            'av', 'cv2', 'yt_dlp', 'mutagen', 'brotli', 'curl_cffi', 'websockets',
            'pyarrow', 'dask', 'polars',
            'IPython', 'jupyter', 'jupyter_client', 'jupyter_core', 'notebook',
            'ipykernel', 'sphinx', 'pytest',
            'bokeh', 'plotly', 'sympy',
        ],
    )),
    ('Graficos', 'Graficos.py', dict()),
    ('Descriptivas', 'Descriptivas.py', dict()),
    ('Likert', 'Likert.py', dict(hiddenimports=BOKEH_IMPORTS)),
    ('Tablas', 'Tablas.py', dict(ai=True)),
    ('Comparar', 'Comparar.py', dict(hiddenimports=BOKEH_IMPORTS, ai=True)),
    ('Fiabilidad', 'Fiabilidad.py', dict(hiddenimports=BOKEH_IMPORTS, binaries=PYREADSTAT_LIBS, ai=True)),
    ('Regresion', 'Regresion.py', dict(
        datas=_diagnostic_datas, binaries=PYREADSTAT_LIBS, hiddenimports=collect_submodules('pyreadstat'),
        runtime_hooks=BOKEH_RTHOOK, excludes=['statsmodels.stats.diagnostic'], ai=True,
    )),
    ('Regcateg', 'Regcateg.py', dict(
        datas=_diagnostic_datas, binaries=PYREADSTAT_LIBS, hiddenimports=collect_submodules('pyreadstat'),
        runtime_hooks=BOKEH_RTHOOK, excludes=['statsmodels.stats.diagnostic'], ai=True,
    )),
    ('Series', 'Series.py', dict(
        datas=_series_datas, binaries=_series_binaries, hiddenimports=_series_hidden, ai=True,
    )),
    ('Muestra', 'Muestra.py', dict(hiddenimports=BOKEH_IMPORTS, binaries=PYREADSTAT_LIBS)),
    ('SimpleTest', 'SimpleTest.py', dict(ai=True)),
    ('Bayesiano', 'Bayesiano.py', dict(
        datas=_bayes_datas, binaries=_bayes_binaries, hiddenimports=_bayes_hidden,
        runtime_hooks=[os.path.join(ROOT, 'rthook_pytensor.py')], excludes=_bayes_excludes, ai=True,
    )),
    ('Moderacion', 'Moderacion.py', dict(
        datas=BOKEH_IPYTHON_DATAS, binaries=PYREADSTAT_LIBS, hiddenimports=collect_submodules('pyreadstat'),
        runtime_hooks=BOKEH_RTHOOK, ai=True,
    )),
    ('Mediacion', 'Mediacion.py', dict(
        datas=copy_metadata('pyreadstat') + copy_metadata('pytz') + collect_data_files('statsmodels'),
        binaries=PYREADSTAT_LIBS,
        hiddenimports=collect_submodules('pyreadstat') + collect_submodules('statsmodels') + TKAGG_IMPORTS,
        ai=True,
    )),
    ('Process', 'Process.py', dict(
        datas=BOKEH_IPYTHON_DATAS, binaries=PYREADSTAT_LIBS, hiddenimports=collect_submodules('pyreadstat'),
        runtime_hooks=BOKEH_RTHOOK, ai=True,
    )),
    ('Panel', 'Panel.py', dict(datas=copy_metadata('pytz'), ai=True)),
    ('AFE', 'AFE.py', dict(
        datas=BOKEH_IPYTHON_DATAS + copy_metadata('pytz'), binaries=PYREADSTAT_LIBS,
        hiddenimports=collect_submodules('pyreadstat'), runtime_hooks=BOKEH_RTHOOK, ai=True,
    )),
    ('Cluster', 'Cluster.py', dict(
        datas=_cluster_datas, binaries=_cluster_binaries, hiddenimports=_cluster_hidden,
        runtime_hooks=[os.path.join(ROOT, 'rthook_scipy.py')],
        excludes=['IPython', 'jupyter_client', 'jupyter_core', 'matplotlib.tests', 'numpy.tests',
                  'pandas.tests', 'pytest', 'setuptools.tests', 'tkinter.test'],
        ai=True,
    )),
    ('ClusteringSV', 'ClusteringSV.py', dict(ai=True)),
    ('MetaAnalisis', 'MetaAnalisis.py', dict(
        datas=(copy_metadata('IPython') + copy_metadata('pyreadstat') + collect_data_files('IPython')
               + collect_data_files('matplotlib') + collect_data_files('seaborn')),
        binaries=PYREADSTAT_LIBS,
        hiddenimports=(collect_submodules('pyreadstat') + ['meta_stats', 'IPython', 'scipy.special.cython_special']
                       + TKAGG_IMPORTS),
        excludes=['notebook', 'jupyter', 'nbformat'],
        ai=True,
    )),
]


def apply_pyarmor_patch(a):
    """Sustituye scripts y módulos locales del Analysis por su versión ofuscada."""
    if not USE_PYARMOR:
        return

    if hasattr(a.pure, '_code_cache'):
        code_cache = a.pure._code_cache
    else:
        from PyInstaller.config import CONF
        code_cache = CONF['code_cache'].get(id(a.pure))

    src = os.path.normcase(ROOT)

    def obfuscated(path):
        if path and os.path.normcase(path).startswith(src + os.sep):
            candidate = os.path.join(OBF, path[len(src) + 1:])
            if os.path.exists(candidate):
                return candidate
        return None

    count = 0
    for i, (name, path, typecode) in enumerate(a.scripts):
        x = obfuscated(path)
        if x:
            a.scripts[i] = (name, x, typecode)
            count += 1
    if count == 0:
        raise RuntimeError('No se encontró ningún script ofuscado para ' + a.scripts[-1][0])

    for i, (name, path, typecode) in enumerate(a.pure):
        x = obfuscated(path)
        if x:
            if code_cache is not None:
                code_cache.pop(name, None)
            a.pure[i] = (name, x, typecode)

    a.pure.append((RUNTIME_PKG, os.path.join(OBF, RUNTIME_PKG, '__init__.py'), 'PYMODULE'))
    # Extensión del runtime: pyarmor_runtime.pyd (Windows) o pyarmor_runtime.so (macOS, Linux)
    runtime_dir = os.path.join(OBF, RUNTIME_PKG)
    for fname in os.listdir(runtime_dir):
        if fname.startswith('pyarmor_runtime.') and fname.endswith(('.pyd', '.so')):
            ext = os.path.join(RUNTIME_PKG, fname)
            a.binaries.append((ext, os.path.join(OBF, ext), 'EXTENSION'))


analyses = []
exes = []
for name, script, opts in TARGETS:
    ai = opts.get('ai', False)
    a = Analysis(
        [os.path.join(ROOT, script)],
        pathex=[ROOT],
        binaries=opts.get('binaries', []),
        datas=opts.get('datas', []) + (AI_DATAS if ai else []),
        hiddenimports=(PYREADSTAT_IMPORTS + PKG_RESOURCES_IMPORTS + opts.get('hiddenimports', [])
                       + (AI_IMPORTS if ai else [])),
        hookspath=[],
        hooksconfig={},
        runtime_hooks=COMMON_RTHOOKS + opts.get('runtime_hooks', []),
        excludes=opts.get('excludes', []),
        noarchive=False,
        optimize=0,
    )
    apply_pyarmor_patch(a)
    pyz = PYZ(a.pure)
    exe_opts = dict(icon=ICON) if not IS_LINUX else {}
    if IS_MAC:
        exe_opts.update(argv_emulation=False, target_arch=TARGET_ARCH,
                        codesign_identity=CODESIGN_IDENTITY, entitlements_file=ENTITLEMENTS)
    exe = EXE(
        pyz,
        a.scripts,
        [],
        exclude_binaries=True,
        name=name,
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=False,   # UPX corrompe las .pyd de pandas/_libs (pandas_datetime)
        console=False,
        disable_windowed_traceback=False,
        **exe_opts,
    )
    analyses.append(a)
    exes.append(exe)

# El primer EXECUTABLE (Menu) es el CFBundleExecutable del .app
coll = COLLECT(
    *exes,
    *[a.binaries for a in analyses],
    *[a.datas for a in analyses],
    strip=False,
    upx=False,
    name='IsA',
)

if IS_MAC:
    app = BUNDLE(
        coll,
        name='IsA.app',
        icon=ICON,
        bundle_identifier='es.ugr.isa.completo',
        version='1.5',
        codesign_identity=CODESIGN_IDENTITY,
        entitlements_file=ENTITLEMENTS,
        info_plist={
            'CFBundleName': 'IsA',
            'CFBundleDisplayName': 'IsA - Intelligent Statistical Assistant',
            'CFBundleShortVersionString': '1.5',
            'LSMinimumSystemVersion': '12.0',
            'NSHighResolutionCapable': True,
            # La interfaz usa fondos blancos fijos: forzar modo claro
            'NSRequiresAquaSystemAppearance': True,
        },
    )
