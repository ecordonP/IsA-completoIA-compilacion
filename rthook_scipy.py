"""
Runtime hook de diagnóstico para PyInstaller.
Activa console=True en el spec para ver esta salida.
"""
import os
import sys

print("[rthook] Iniciando runtime hook de scipy...")

if sys.platform == 'win32' and hasattr(sys, '_MEIPASS'):
    _base = sys._MEIPASS
    print(f"[rthook] _MEIPASS = {_base}")

    _scipy_special = os.path.join(_base, 'scipy', 'special')

    # Estado actual de los ficheros clave
    for _f in ['liblapack.dll']:
        for _d in [_base, _scipy_special]:
            _p = os.path.join(_d, _f)
            print(f"[rthook] {'EXISTS' if os.path.exists(_p) else 'MISSING'}: {_p}")

    # Añadir directorios con os.add_dll_directory
    _candidates = [
        _scipy_special,
        _base,
        os.path.join(_base, 'scipy', '.libs'),
        os.path.join(_base, 'scipy.libs'),
        os.path.join(_base, 'numpy', '.libs'),
        os.path.join(_base, 'numpy.libs'),
    ]
    for _path in _candidates:
        if os.path.isdir(_path):
            try:
                os.add_dll_directory(_path)
                print(f"[rthook] add_dll_directory OK: {_path}")
            except Exception as e:
                print(f"[rthook] add_dll_directory FAIL: {_path} → {e}")

    # También añadir al PATH como método alternativo
    _path_extra = os.pathsep.join([p for p in [_scipy_special, _base] if os.path.isdir(p)])
    os.environ['PATH'] = _path_extra + os.pathsep + os.environ.get('PATH', '')
    print(f"[rthook] PATH prepend: {_path_extra}")

    # Intentar cargar liblapack.dll directamente con ctypes para ver el error exacto
    try:
        import ctypes

        _lapack_path = os.path.join(_scipy_special, 'liblapack.dll')
        if os.path.exists(_lapack_path):
            ctypes.WinDLL(_lapack_path)
            print(f"[rthook] ctypes.WinDLL(liblapack.dll): OK")
        else:
            print(f"[rthook] ctypes.WinDLL(liblapack.dll): fichero no encontrado")
    except Exception as e:
        print(f"[rthook] ctypes.WinDLL(liblapack.dll): FALLO → {e}")

else:
    print("[rthook] No estamos en un bundle PyInstaller de Windows.")

print("[rthook] Runtime hook completado.")
pass