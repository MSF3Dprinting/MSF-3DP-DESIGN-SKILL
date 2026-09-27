#!/usr/bin/env bash
# install_openscad.sh — set up OpenSCAD and the check tooling in a fresh sandbox (MSF "3D Printing for All").
# Tested on Ubuntu 24.04 in the claude.ai sandbox and in a Claude Code cloud container. Installs:
#   native OpenSCAD 2021.01 (apt) + xvfb + fonts-liberation — PNG views only (render_views.py)
#   openscad-fast = OpenSCAD 2025.07.18 with the Manifold engine (npm openscad-wasm) — every geometry export
#   Python: trimesh numpy scipy shapely rtree networkx pillow matplotlib — the checks (networkx: section walls,
#           T19; matplotlib: section drawings)
# The snapshot host files.openscad.org is usually unreachable (403); pass --snapshot URL to try one.
# Safe to run again: installed parts are skipped, the readiness test always runs.
# Usage:  bash scripts/install_openscad.sh [--snapshot https://files.openscad.org/snapshots/OpenSCAD-<date>-x86_64.AppImage]
set -u
SNAP=""
[ "${1:-}" = "--snapshot" ] && SNAP="${2:-}"
SUDO=""; command -v sudo >/dev/null 2>&1 && [ "$(id -u)" != "0" ] && SUDO="sudo"
export DEBIAN_FRONTEND=noninteractive

# 1. a broken third-party apt list breaks apt-get update in some images
$SUDO rm -f /etc/apt/sources.list.d/nodesource* 2>/dev/null || true

# 2. foreground install with a timeout — background installs die when a tool call returns
if ! command -v openscad >/dev/null 2>&1; then
  timeout 600 bash -c "$SUDO apt-get update -qq && $SUDO apt-get install -y -qq --no-install-recommends openscad xvfb fonts-liberation" \
    || echo "apt install failed — check the network settings"
fi

# 3. optional snapshot AppImage (Manifold backend, fast renders, native headless PNG)
if [ -n "$SNAP" ]; then
  $SUDO apt-get install -y -qq --no-install-recommends libegl1 libgl1 libopengl0 libgbm1 libwayland-client0 libfontconfig1 libharfbuzz0b libgmp10 >/dev/null 2>&1 || true
  if curl -fsSL --max-time 120 -o /tmp/openscad.AppImage "$SNAP"; then
    chmod +x /tmp/openscad.AppImage && (cd /tmp && ./openscad.AppImage --appimage-extract >/dev/null 2>&1) \
      && $SUDO ln -sf /tmp/squashfs-root/AppRun /usr/local/bin/openscad && echo "snapshot installed"
  else
    echo "snapshot host not reachable — staying with the apt version"
  fi
fi

# 4. python tooling for the checks (shapely + rtree + networkx for sections, scipy for the footprint)
PY_PKGS="trimesh numpy scipy shapely rtree networkx pillow matplotlib"
timeout 300 pip install -q $PY_PKGS --break-system-packages 2>/dev/null \
  || timeout 300 pip install -q $PY_PKGS 2>&1 | tail -1      # older pip has no --break-system-packages

# 5. FAST GEOMETRY EXPORT: OpenSCAD 2025.07 with the Manifold engine, from the npm package openscad-wasm
#    (npmjs.org is on the sandbox allow-list; files.openscad.org is not). 4-22x faster than 2021.01 CGAL on
#    typical MSF parts. Used automatically by export.sh and sweep.py through the `openscad-fast` wrapper.
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if command -v node >/dev/null 2>&1; then
  if [ ! -f "$HOME/.openscad-wasm/node_modules/openscad-wasm/openscad.js" ]; then
    mkdir -p "$HOME/.openscad-wasm"
    timeout 280 npm install --prefix "$HOME/.openscad-wasm" --no-audit --no-fund --silent openscad-wasm@0.0.4 2>&1 | tail -1
  fi
  chmod +x "$HERE"/*.sh "$HERE"/*.py "$HERE/openscad-fast" "$HERE/openscad_manifold.mjs" 2>/dev/null   # git may drop the bits
  $SUDO ln -sf "$HERE/openscad-fast" /usr/local/bin/openscad-fast 2>/dev/null || true
  # readiness test = a real export through the PATH symlink (catches a broken symlink, a missing wasm, missing fonts)
  FAST_BIN="$(command -v openscad-fast 2>/dev/null || echo "$HERE/openscad-fast")"
  printf 'echo(v=version()); linear_extrude(1) text("1", font="Liberation Sans:style=Bold");\n' > /tmp/_osf_test.scad
  if timeout 120 "$FAST_BIN" -o /tmp/_osf_test.stl --export-format binstl /tmp/_osf_test.scad > /tmp/_osf_test.log 2>&1 \
     && [ -s /tmp/_osf_test.stl ] && ! grep -q "Can't get font" /tmp/_osf_test.log; then
    echo "openscad-fast: $("$FAST_BIN" --version 2>&1 | sed 's/^\[OpenSCAD\]: //' | head -1) (Manifold) via node, fonts OK — ready"
  else
    echo "openscad-fast NOT working — see /tmp/_osf_test.log; export.sh falls back to the native openscad"; tail -3 /tmp/_osf_test.log
  fi
  rm -f /tmp/_osf_test.scad /tmp/_osf_test.stl
else
  echo "node not found — openscad-fast (Manifold) unavailable; native 2021.01 will be used"
fi

echo "openscad: $(openscad --version 2>&1 | head -1)"
python3 -c "import trimesh, shapely, scipy, rtree, networkx, PIL, matplotlib; print('python tooling ok')" 2>&1 | tail -1
echo "STL export: openscad-fast (Manifold, seconds)  ·  PNG views: native openscad via render_views.py (xvfb-run)"
