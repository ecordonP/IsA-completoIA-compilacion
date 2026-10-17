"""
Runtime hook para PyInstaller: configura PyTensor antes de que se importe
para evitar el error [WinError 3] al buscar compiladores C en rutas inexistentes.

En una aplicación empaquetada no hay compilador C disponible, así que se
desactiva la compilación C de PyTensor (cxx='') y se redirige el directorio
de compilación a una carpeta temporal escribible del sistema.
"""
import os
import tempfile

# Directorio temporal escribible para que PyTensor no intente escribir
# dentro de _internal (que es de solo lectura en el .exe empaquetado)
compiledir = os.path.join(tempfile.gettempdir(), "pytensor_compiledir")
os.makedirs(compiledir, exist_ok=True)

flags_extra = f"cxx=,base_compiledir={compiledir}"

existing = os.environ.get("PYTENSOR_FLAGS", "")
if existing:
    os.environ["PYTENSOR_FLAGS"] = existing + "," + flags_extra
else:
    os.environ["PYTENSOR_FLAGS"] = flags_extra
