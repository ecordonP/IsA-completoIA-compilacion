#!/usr/bin/env bash
# Prueba de arranque: abre el menú y cada módulo compilado y comprueba que siguen en
# marcha pasados unos segundos (si falta una librería o hay un error al importar, el
# programa termina enseguida). Necesita una licencia (ci/licencia_prueba.py) y, en
# Linux, una pantalla (Xvfb). En Windows se ejecuta con Git Bash.
#
# Uso:  bash ci/probar_modulos.sh <carpeta_con_los_ejecutables> <config.MENU>
set -uo pipefail
DIR="$1"
export ISA_MENU_CONFIG="$2"
case "$(uname -s)" in MINGW*|MSYS*|CYGWIN*) EXT=".exe" ;; *) EXT="" ;; esac
APPS=(Menu Datos Graficos Descriptivas Likert Tablas Comparar Fiabilidad Regresion Regcateg Series
      Muestra SimpleTest Bayesiano Moderacion Mediacion Process Panel AFE Cluster ClusteringSV MetaAnalisis)
WAIT=${ISA_TEST_WAIT:-30}
failed=()
for app in "${APPS[@]}"; do
    log="$(mktemp)"
    "$DIR/$app$EXT" --launched-from-menu > "$log" 2>&1 &
    pid=$!
    for _ in $(seq "$WAIT"); do
        sleep 1
        kill -0 "$pid" 2>/dev/null || break
    done
    title=""
    if [[ -n "$EXT" ]] && kill -0 "$pid" 2>/dev/null; then
        # Windows: un error al arrancar abre un diálogo («Unhandled exception», «Error fatal»,
        # licencia...) y el proceso sigue vivo; se mira el título de su ventana principal
        winpid="$(cat "/proc/$pid/winpid" 2>/dev/null || echo "$pid")"
        title="$(powershell.exe -NoProfile -Command "(Get-Process -Id $winpid -ErrorAction SilentlyContinue).MainWindowTitle" 2>/dev/null | tr -d '\r')"
    fi
    if kill -0 "$pid" 2>/dev/null && echo "$title" | grep -q -i -E "unhandled|error|fatal|licencia"; then
        echo "FALLO  $app (ventana de error: $title)"
        kill -9 "$pid" 2>/dev/null
        failed+=("$app")
    elif kill -0 "$pid" 2>/dev/null; then
        echo "OK     $app${title:+  [$title]}"
        kill "$pid" 2>/dev/null; sleep 1; kill -9 "$pid" 2>/dev/null
    else
        wait "$pid"; rc=$?
        echo "FALLO  $app (terminó con código $rc)"
        tail -n 40 "$log"
        failed+=("$app")
    fi
    rm -f "$log"
done
# El menú anota el último uso en config.MENU solo si la licencia es válida: si no se ha
# anotado, el menú se quedó en la ventana de error de licencia (no es un arranque correcto)
if ! grep -q '"estado"' "$ISA_MENU_CONFIG"; then
    echo "FALLO  Menu: la licencia de prueba no se ha aceptado (sin «estado» en config.MENU)"
    failed+=("licencia")
fi
if [ ${#failed[@]} -gt 0 ]; then
    echo "No arrancan: ${failed[*]}"
    exit 1
fi
echo "Todos los programas arrancan correctamente."
