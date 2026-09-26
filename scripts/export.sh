#!/usr/bin/env bash
# export.sh — export every variant of a part: STL (binary, print position), checks, renders, log.
# MSF "3D Printing for All". Works with any Customizer-ready .scad; bash (not sh).
#
# Usage:  scripts/export.sh <item.scad> <version> [variants.txt] [context_scene.scad]
#   variants.txt: one variant per line:   <name> | <-D overrides, space separated> | [xN = N identical copies]
#                 e.g.   holder      | part="holder"
#                        holder_wide | part="holder" dev_w=120
#                        rib         | part="rib" | x10        -> rib_1 ... rib_10 as separate STL files, ready to import
#                        coupon      | (empty = defaults of test_coupon.scad, see COUPON below)
#   Without a variants file, the defaults are exported as one variant named after the file.
# Environment:   OPENSCAD=/path/to/openscad   SECTIONS=5,20   ALLOW_BRIDGES=1   NO_RENDERS=1   COUPON=scad/test_coupon.scad
#
# Output (next to the .scad, in the package layout of the workflow):
#   stl/<item>_<variant>_v<version>.stl     img/<item>_<variant>_*.png + _sheet.png     stl/EXPORT_LOG.txt
# Exit code 1 if any check fails — fix the model, do not ship.
set -u
SCAD="${1:?item.scad}"; VERSION="${2:?version, e.g. 1.0}"; VARIANTS="${3:-}"; CONTEXT="${4:-}"
# STL export uses the Manifold build when it is installed (4-22x faster); PNG views always use the native openscad.
if [ -z "${OPENSCAD:-}" ]; then
  HERE0="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  if [ -x "$HERE0/openscad-fast" ] && [ -f "$HOME/.openscad-wasm/node_modules/openscad-wasm/openscad.js" ]; then OPENSCAD="$HERE0/openscad-fast"; else OPENSCAD=openscad; fi
fi
NATIVE_OPENSCAD="${NATIVE_OPENSCAD:-openscad}"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DIR="$(cd "$(dirname "$SCAD")" && pwd)"; ITEM="$(basename "${SCAD%.scad}")"
mkdir -p "$DIR/stl" "$DIR/img"
LOG="$DIR/stl/EXPORT_LOG.txt"
FAIL=0
{
  echo "=== export $(date -u +%FT%TZ)  $ITEM v$VERSION"
  echo "openscad: $($OPENSCAD --version 2>&1 | head -1)"
} >> "$LOG"

export_one() {   # name, defines, copies
  local name="$1"; local defs="$2"; local copies="${3:-1}"; local args=()
  for d in $defs; do args+=(-D "$d"); done
  local stl="$DIR/stl/${ITEM}_${name}_v${VERSION}.stl"
  echo "--- $name  [$defs]"
  if ! "$OPENSCAD" -o "$stl" --export-format binstl "${args[@]}" "$SCAD" > "$DIR/stl/${name}.log" 2>&1; then
    echo "FAIL render $name — see stl/${name}.log"; FAIL=1; echo "FAIL render $name" >> "$LOG"; return
  fi
  grep -E "^(WARNING|ECHO)" "$DIR/stl/${name}.log" | head -20
  local chk=(python3 "$HERE/check_stl.py" "$stl" --json "$DIR/stl/${name}.check.json")
  [ -n "${SECTIONS:-}" ] && chk+=(--sections "$SECTIONS")
  [ -n "${ALLOW_BRIDGES:-}" ] && chk+=(--allow-bridges)
  if ! "${chk[@]}"; then FAIL=1; echo "FAIL check $name" >> "$LOG"; else echo "ok    $name  $(basename "$stl")  [$defs]" >> "$LOG"; fi
  if [ "$copies" -gt 1 ] 2>/dev/null; then   # N identical items: one numbered STL per item, so the user just imports them all
    local k; for k in $(seq 1 "$copies"); do cp "$stl" "$DIR/stl/${ITEM}_${name}_${k}_v${VERSION}.stl"; done
    rm -f "$stl"; echo "      $copies copies: ${ITEM}_${name}_1..${copies}_v${VERSION}.stl" | tee -a "$LOG"
  fi
  if [ -z "${NO_RENDERS:-}" ]; then
    local rv=(python3 "$HERE/render_views.py" "$SCAD" --out "$DIR/img" --name "${ITEM}_${name}" --openscad "$NATIVE_OPENSCAD")
    for d in $defs; do rv+=(-D "$d"); done
    [ -n "$CONTEXT" ] && rv+=(--context "$CONTEXT")
    "${rv[@]}" || { echo "WARN renders incomplete for $name"; echo "WARN renders $name" >> "$LOG"; }
  fi
}

if [ -n "$VARIANTS" ] && [ -f "$VARIANTS" ]; then
  while IFS='|' read -r name defs copies; do
    name="$(echo "$name" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')"; defs="$(echo "${defs:-}" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')"
    copies="$(echo "${copies:-}" | sed 's/^[[:space:]]*x\?//;s/[[:space:]]*$//')"; [ -z "$copies" ] && copies=1
    [ -z "$name" ] && continue; case "$name" in \#*) continue;; esac
    export_one "$name" "$defs" "$copies"
  done < "$VARIANTS"
else
  export_one "default" ""
fi

if [ -n "${COUPON:-}" ] && [ -f "$COUPON" ]; then
  echo "--- coupon"
  "$OPENSCAD" -o "$DIR/stl/${ITEM}_coupon_v${VERSION}.stl" --export-format binstl "$COUPON" > "$DIR/stl/coupon.log" 2>&1 \
    && grep "^ECHO" "$DIR/stl/coupon.log" | sed 's/ECHO: //' | tee -a "$LOG" \
    || { echo "FAIL coupon"; FAIL=1; }
fi

echo "=== done, exit $FAIL  (exporter: $OPENSCAD)" | tee -a "$LOG"
exit $FAIL
