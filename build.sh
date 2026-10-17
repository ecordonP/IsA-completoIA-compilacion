#!/usr/bin/env bash
# Compila IsA completo (menú + 21 módulos) con PyInstaller a partir de los scripts
# ofuscados y genera el paquete de distribución de la plataforma en que se ejecuta:
#   Windows x86_64 (Git Bash)  dist/IsA-windows-x64.zip       (carpeta IsA con Menu.exe...)
#   macOS arm64                dist/IsA-macos-arm64.dmg      (IsA.app, Apple Silicon)
#   macOS x86_64               dist/IsA-macos-intel.dmg      (IsA.app, Intel)
#   Linux x86_64               dist/IsA-linux-x86_64.tar.gz  (carpeta IsA + instalar_isa.sh)
#
# Los scripts ofuscados se generan antes en Windows con `python obfuscate.py` (la
# licencia de pyarmor no admite CI) y se publican en obf_win/, obf_mac/, obf_mac_intel/
# y obf_linux/. Aquí solo se comprueba que están al día y se compila.
#
# Requisitos: Python 3.11 con requirements-ci.txt instalado.
# Variables de entorno opcionales:
#   ISA_CODESIGN_IDENTITY   macOS: "Developer ID Application: Nombre (TEAMID)"; sin ella
#                           se firma ad hoc (válido solo para pruebas internas)
#   ISA_SKIP_PYARMOR=1      compila sin ofuscar (solo para depurar)
set -euo pipefail
cd "$(dirname "$0")"

OS="$(uname -s)"
ARCH="$(uname -m)"
EXT=""
case "$OS" in
    MINGW*|MSYS*|CYGWIN*) PLATFORM=windows; OBF_TARGET=win; EXT=".exe"; PKG=IsA-windows-x64.zip ;;
    Darwin)
        PLATFORM=mac
        case "$ARCH" in
            arm64)  OBF_TARGET=mac;       PKG=IsA-macos-arm64.dmg ;;
            x86_64) OBF_TARGET=mac_intel; PKG=IsA-macos-intel.dmg ;;
            *) echo "Arquitectura no admitida: $ARCH" >&2; exit 1 ;;
        esac
        export ISA_TARGET_ARCH="$ARCH" ;;
    Linux)
        [[ "$ARCH" == "x86_64" ]] || { echo "Arquitectura no admitida: $ARCH" >&2; exit 1; }
        PLATFORM=linux; OBF_TARGET=linux; PKG=IsA-linux-x86_64.tar.gz ;;
    *) echo "Sistema no admitido: $OS" >&2; exit 1 ;;
esac
# macOS trae bash 3.2: sin arrays asociativos
case "$OBF_TARGET" in
    win) OBF_DIR=obf_win ;; mac) OBF_DIR=obf_mac ;; mac_intel) OBF_DIR=obf_mac_intel ;; linux) OBF_DIR=obf_linux ;;
esac

APPS=(Menu Datos Graficos Descriptivas Likert Tablas Comparar Fiabilidad Regresion Regcateg Series
      Muestra SimpleTest Bayesiano Moderacion Mediacion Process Panel AFE Cluster ClusteringSV MetaAnalisis)

# Ruta para Python: en Git Bash (Windows) $PWD es /d/... y Python necesita D:/...
HERE="$(pwd -W 2>/dev/null || pwd)"

rm -rf build dist

if [[ "${ISA_SKIP_PYARMOR:-0}" != "1" ]]; then
    # En el repositorio público de compilación no hay fuentes: la comprobación se hizo al publicar
    if [[ -f obfuscate.py ]]; then
        echo "==> Comprobando scripts ofuscados ($OBF_TARGET)"
        python obfuscate.py --check "$OBF_TARGET"
    fi
    export ISA_OBF_DIR="$HERE/$OBF_DIR"
    export ISA_REQUIRE_PYARMOR=1
else
    export ISA_OBF_DIR="$HERE/build/no-obf"
fi

echo "==> Compilando IsA con PyInstaller ($PLATFORM $ARCH)"
pyinstaller --noconfirm --clean IsA.spec

if [[ "$PLATFORM" == "mac" ]]; then BIN="dist/IsA.app/Contents/MacOS"; else BIN="dist/IsA"; fi
for name in "${APPS[@]}"; do
    test -f "$BIN/$name$EXT" || { echo "Falta el ejecutable $name$EXT" >&2; exit 1; }
done

case "$PLATFORM" in
windows)
    echo "==> Creando $PKG"
    cp LEEME_WINDOWS.txt dist/IsA/LEEME.txt
    (cd dist && 7z a -tzip -mx=7 "$PKG" IsA >/dev/null)
    ;;
mac)
    APP="dist/IsA.app"
    if [[ -n "${ISA_CODESIGN_IDENTITY:-}" ]]; then
        echo "==> Verificando firma"
        codesign --verify --deep --strict --verbose=2 "$APP"
    fi
    echo "==> Creando $PKG"
    STAGE="build/dmg"
    rm -rf "$STAGE" && mkdir -p "$STAGE"
    cp -R "$APP" "$STAGE/"
    ln -s /Applications "$STAGE/Applications"
    cp "mac/Instrucciones de instalación.html" "$STAGE/"
    hdiutil create -volname "IsA" -srcfolder "$STAGE" -ov -format UDZO "dist/$PKG"
    if [[ -n "${ISA_CODESIGN_IDENTITY:-}" ]]; then
        codesign --force --sign "$ISA_CODESIGN_IDENTITY" "dist/$PKG"
    fi
    ;;
linux)
    echo "==> Creando $PKG"
    python - "$HERE/IsA.ico" "$BIN/isa.png" <<'PY'
import sys
from PIL import Image
im = Image.open(sys.argv[1])
im.size = sorted(im.info.get("sizes", [im.size]))[-1]
im.convert("RGBA").resize((256, 256), Image.LANCZOS).save(sys.argv[2])
PY
    cp linux/instalar_isa.sh "$BIN/instalar_isa.sh"
    cp linux/LEEME_LINUX.txt "$BIN/LEEME.txt"
    chmod +x "$BIN/instalar_isa.sh"
    tar -C dist -czf "dist/$PKG" IsA
    ;;
esac
echo "==> Listo: dist/$PKG"
