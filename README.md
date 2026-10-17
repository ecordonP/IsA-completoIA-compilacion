# IsA completo (con informe IA): compilación para Windows, macOS y Linux

Este repositorio **no contiene el código fuente** de IsA – Intelligent Statistical
Assistant (versión completa: menú y 21 módulos, con informe de resultados mediante IA).
Solo contiene lo necesario para compilarlo en GitHub Actions:

- `obf_win/`, `obf_mac/`, `obf_mac_intel/`, `obf_linux/`: el programa **ofuscado con
  pyarmor** para Windows x64, macOS Apple Silicon, macOS Intel y Linux x86_64.
- Un archivo por programa (`Menu.py`, `Datos.py`...) con **solo sus líneas `import`**,
  que PyInstaller necesita para saber qué librerías incluir. No contienen el programa.
- `IsA.spec` (PyInstaller), `build.sh`, *runtime hooks* y el flujo de Actions.

El código fuente está en un repositorio privado; este se actualiza desde allí con
`publicar_compilacion.py`. **No edite este repositorio a mano.**

## Compilaciones

El flujo **Compilar IsA completo** compila las cuatro plataformas (o la elegida):

| Plataforma | Máquina | Resultado |
|---|---|---|
| Windows 10/11 de 64 bits | `windows-2025` | `IsA-windows-x64.zip` |
| macOS Apple Silicon (M1–M5) | `macos-15` | `IsA-macos-arm64.dmg` |
| macOS Intel | `macos-15-intel` | `IsA-macos-intel.dmg` |
| Linux x86_64 (Ubuntu 24.04 o posterior) | `ubuntu-24.04` | `IsA-linux-x86_64.tar.gz` |

Se lanza desde Actions → **Compilar IsA completo** → **Run workflow**, o con una etiqueta
`v*`. Cada compilación comprueba que el menú y los 21 módulos arrancan, con una licencia
de prueba que se guarda como secreto cifrado del repositorio (`ISA_CI_LICENSE`); en Linux
se prueba además en un Ubuntu 24.04 limpio.

## Licencia

IsA es software con licencia de uso (ver `licencia.md`). Las licencias van firmadas
digitalmente: el programa solo contiene la clave pública, que permite comprobarlas pero
no crearlas. © 2026 Eulogio Cordón Pozo, Universidad de Granada.
