#!/usr/bin/env bash
# export.sh — export every variant of a part: STL (binary, print position), checks, renders, log.
# MSF "3D Printing for All". Works with any Customizer-ready .scad.
#
# Usage:  bash scripts/export.sh <item.scad> <version> [variants.txt] [context_scene.scad]
#   variants.txt: one variant per line:   <name> | <-D overrides, space separated> | [xN = N identical copies]
#                 e.g.   holder      | part="holder"
#                        holder_wide | part="holder" dev_w=120
#                        rib         | part="rib" | x10          -> rib_1 ... rib_10 as separate STL files
#                        plate       | part="all"                -> all parts on one print plate
#                        assembly    | part="assembly"           -> assembled view, goes to stl/view_only/
#                 Values may contain spaces inside double quotes: label | label_text="BED 12"
#                 Lines starting with # and blank lines are ignored.
#   Without a variants file, the defaults are exported as one variant named "default".
#   The tolerance coupon is not a variant: set COUPON=<coupon.scad> (e.g. COUPON=test_coupon.scad).
# A model announces multi-body STLs with echo("CHECK expect_bodies=N") (print plate) or
# echo("CHECK view_only expect_bodies=N") (assembled view: checked for watertightness only, not for printing).
# Every STL is cleaned of zero-area specks (stl_clean.py, logged) before the checks.
# The one-file Customizer version <item>_customizer.scad is regenerated (flatten_scad.py --verify, which reuses
# its five-line header) and checked (lint_customizer.py) together with the working file. The first time, give
# the header values: CZ_NAME="..." CZ_DESCRIPTION="..." CZ_CATEGORY="..." CZ_CREDIT="..." [CZ_LICENSE=MIT].
# Environment:   OPENSCAD=/path/to/openscad   SECTIONS=auto (default) | 5,20 | "" (none)   ALLOW_BRIDGES=1
#                NO_RENDERS=1   NO_CUSTOMIZER=1 (coupon-only or scratch runs)
#                COUPON=test_coupon.scad   COUPON_D='preset="rusty" nominal=25'
#
# Output (next to the .scad):
#   stl/<item>_<variant>_v<version>.stl   stl/<item>_<variant>_<k>_v<version>.stl (xN)   stl/<item>_coupon_v<version>.stl
#   stl/view_only/<item>_<variant>_v<version>.stl   img/<item>_<variant>_<view>.png + _sheet.png   img/<item>_coupon.png
#   stl/EXPORT_LOG.txt (exporter version, date, parameter set and check result per STL, coupon step table)
# Exit code 1 if any render or check fails or an expected file is missing — fix the model, do not ship.
[ -z "${BASH_VERSION:-}" ] && exec bash "$0" "$@"
set -u
SCAD="${1:?item.scad}"; VERSION="${2:?version, e.g. 1.0}"; VARIANTS="${3:-}"; CONTEXT="${4:-}"
HERE="$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")" && pwd)"
[ -f "$SCAD" ] || { echo "FAIL: $SCAD not found"; exit 1; }
# STL export uses the Manifold build when it works (several times faster); PNG views always use the native openscad.
if [ -z "${OPENSCAD:-}" ]; then
  OPENSCAD=openscad
  if [ -f "$HERE/openscad-fast" ]; then
    chmod +x "$HERE/openscad-fast" "$HERE/openscad_manifold.mjs" 2>/dev/null   # git may drop the executable bit
    "$HERE/openscad-fast" --version >/dev/null 2>&1 && OPENSCAD="$HERE/openscad-fast"
  fi
fi
NATIVE_OPENSCAD="${NATIVE_OPENSCAD:-openscad}"
SECTIONS="${SECTIONS-auto}"
DIR="$(cd "$(dirname "$SCAD")" && pwd)"; ITEM="$(basename "${SCAD%.scad}")"
mkdir -p "$DIR/stl" "$DIR/img"
LOG="$DIR/stl/EXPORT_LOG.txt"
FAIL=0
EXPECTED=()      # every STL this run must leave behind
strip() { sed -E 's/^\[OpenSCAD[^]]*\]: //'; }   # tolerate an older wrapper that prefixed every line
{
  echo "=== export $(date -u +%FT%TZ)  $ITEM v$VERSION"
  echo "exporter: $("$OPENSCAD" --version 2>&1 | strip | head -1)  ($OPENSCAD)"
} >> "$LOG"

split_defs() {   # "a=1 b=\"x y\"" -> one -D argument per line, quotes kept (never eval)
  python3 -c 'import shlex,sys; [print(t) for t in shlex.split(sys.argv[1], posix=False)]' "$1"
}

export_one() {   # name, defines, copies
  local name="$1" defs="$2" copies="${3:-1}" args=() d
  while IFS= read -r d; do [ -n "$d" ] && args+=(-D "$d"); done < <(split_defs "$defs")
  local stl="$DIR/stl/${ITEM}_${name}_v${VERSION}.stl" log="$DIR/stl/${name}.log"
  echo "--- $name  [$defs]"
  if ! "$OPENSCAD" -o "$stl" --export-format binstl "${args[@]}" "$SCAD" > "$log" 2>&1; then
    local why; why="$(strip < "$log" | grep -E "^(ERROR|WARNING)|Assertion" | head -1 | tr '\n' ' ')"
    echo "FAIL render $name — ${why:-see stl/${name}.log}"; FAIL=1; echo "FAIL render $name  [$defs]  ${why}" >> "$LOG"; return
  fi
  strip < "$log" | grep -E "^(WARNING|ECHO)" | head -20
  python3 "$HERE/stl_clean.py" "$stl" --quiet | tee -a "$LOG"
  local chk=(python3 "$HERE/check_stl.py" "$stl" --json "$DIR/stl/${name}.check.json") ce view=""
  ce="$(strip < "$log" | grep -oE 'CHECK( +[a-z_]+(=[0-9.]+)?)+' | head -1)"
  if [ -n "$ce" ]; then
    local nb ms; nb="$(echo "$ce" | grep -oE 'expect_bodies=[0-9]+' | cut -d= -f2)"; ms="$(echo "$ce" | grep -oE 'max_size=[0-9.]+' | cut -d= -f2)"
    [ -n "$nb" ] && chk+=(--expect-bodies "$nb"); [ -n "$ms" ] && chk+=(--max-size "$ms")
    echo "$ce" | grep -qw view_only && { view=1; chk+=(--view-only); }
  fi
  [ -z "$view" ] && [ -n "$SECTIONS" ] && chk+=(--sections "$SECTIONS")
  [ -n "${ALLOW_BRIDGES:-}" ] && chk+=(--allow-bridges)
  local verdict="ok   "
  if ! "${chk[@]}"; then FAIL=1; verdict="FAIL "; fi
  if [ -n "$view" ]; then   # assembled view: never in the print set
    mkdir -p "$DIR/stl/view_only"; mv "$stl" "$DIR/stl/view_only/"; stl="$DIR/stl/view_only/$(basename "$stl")"
    EXPECTED+=("$stl"); echo "$verdict $name  view only, not for printing: stl/view_only/$(basename "$stl")  [$defs]" >> "$LOG"
  elif [ "$copies" -gt 1 ] 2>/dev/null; then   # N identical items: one numbered STL per item, so the user just imports them all
    local k; for k in $(seq 1 "$copies"); do cp "$stl" "$DIR/stl/${ITEM}_${name}_${k}_v${VERSION}.stl"; EXPECTED+=("$DIR/stl/${ITEM}_${name}_${k}_v${VERSION}.stl"); done
    rm -f "$stl"; echo "$verdict $name  $copies copies: ${ITEM}_${name}_1..${copies}_v${VERSION}.stl  [$defs]" | tee -a "$LOG"
  else
    EXPECTED+=("$stl"); echo "$verdict $name  $(basename "$stl")  [$defs]" >> "$LOG"
  fi
  if [ -z "${NO_RENDERS:-}" ]; then
    local rv=(python3 "$HERE/render_views.py" "$SCAD" --out "$DIR/img" --name "${ITEM}_${name}" --openscad "$NATIVE_OPENSCAD")
    for d in "${args[@]}"; do [ "$d" != "-D" ] && rv+=(-D "$d"); done
    [ -n "$CONTEXT" ] && [ -z "$view" ] && rv+=(--context "$CONTEXT")
    "${rv[@]}" || { echo "FAIL renders for $name"; FAIL=1; echo "FAIL renders $name" >> "$LOG"; }
  fi
}

if [ -n "$VARIANTS" ]; then
  [ -f "$VARIANTS" ] || { echo "FAIL: variants file $VARIANTS not found"; echo "FAIL variants file $VARIANTS not found" >> "$LOG"; exit 1; }
  while IFS='|' read -r name defs copies; do
    name="$(echo "$name" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')"; defs="$(echo "${defs:-}" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')"
    copies="$(echo "${copies:-}" | sed 's/^[[:space:]]*x\?//;s/[[:space:]]*$//')"; [ -z "$copies" ] && copies=1
    [ -z "$name" ] && continue; case "$name" in \#*) continue;; esac
    export_one "$name" "$defs" "$copies"
  done < "$VARIANTS"
else
  export_one "default" ""
fi

if [ -n "${COUPON:-}" ]; then
  CP="$COUPON"; [ -f "$CP" ] || CP="$DIR/$COUPON"
  if [ ! -f "$CP" ]; then
    echo "FAIL coupon: $COUPON not found (relative paths are tried from the current folder and from $DIR)"; FAIL=1; echo "FAIL coupon not found: $COUPON" >> "$LOG"
  else
    echo "--- coupon  [${COUPON_D:-defaults}]"
    CARGS=(); while IFS= read -r d; do [ -n "$d" ] && CARGS+=(-D "$d"); done < <(split_defs "${COUPON_D:-}")
    CSTL="$DIR/stl/${ITEM}_coupon_v${VERSION}.stl"
    if "$OPENSCAD" -o "$CSTL" --export-format binstl "${CARGS[@]}" "$CP" > "$DIR/stl/coupon.log" 2>&1; then
      EXPECTED+=("$CSTL")
      python3 "$HERE/stl_clean.py" "$CSTL" --quiet | tee -a "$LOG"
      echo "coupon  $(basename "$CSTL")  [${COUPON_D:-defaults}]" >> "$LOG"
      strip < "$DIR/stl/coupon.log" | grep "^ECHO" | sed 's/^ECHO: //' | tee -a "$LOG"
      python3 "$HERE/check_stl.py" "$CSTL" --quiet || { FAIL=1; echo "FAIL check coupon" >> "$LOG"; }
      if [ -z "${NO_RENDERS:-}" ]; then
        RV=(python3 "$HERE/render_views.py" "$CP" --out "$DIR/img" --name "${ITEM}_coupon" --views top --no-sheet --openscad "$NATIVE_OPENSCAD")
        for d in "${CARGS[@]}"; do [ "$d" != "-D" ] && RV+=(-D "$d"); done
        "${RV[@]}" >/dev/null && mv -f "$DIR/img/${ITEM}_coupon_top.png" "$DIR/img/${ITEM}_coupon.png" \
          || { echo "FAIL coupon render"; FAIL=1; }
      fi
    else
      echo "FAIL coupon — $(strip < "$DIR/stl/coupon.log" | grep -E "^ERROR|Assertion" | head -1)"; FAIL=1; echo "FAIL coupon render" >> "$LOG"
    fi
  fi
fi

if [ -z "${NO_CUSTOMIZER:-}" ]; then
  echo "--- customizer"
  CZ="$DIR/${ITEM}_customizer.scad"; FL=(python3 "$HERE/flatten_scad.py" "$SCAD" --out "$CZ" --verify)
  [ -n "${CZ_NAME:-}" ] && FL+=(--name "$CZ_NAME"); [ -n "${CZ_DESCRIPTION:-}" ] && FL+=(--description "$CZ_DESCRIPTION")
  [ -n "${CZ_CATEGORY:-}" ] && FL+=(--category "$CZ_CATEGORY"); [ -n "${CZ_CREDIT:-}" ] && FL+=(--credit "$CZ_CREDIT")
  [ -n "${CZ_LICENSE:-}" ] && FL+=(--license "$CZ_LICENSE")
  if "${FL[@]}" && python3 "$HERE/lint_customizer.py" "$SCAD" && python3 "$HERE/lint_customizer.py" "$CZ"; then
    echo "customizer  $(basename "$CZ")  header, widgets and geometry checked" >> "$LOG"
  else
    FAIL=1; echo "FAIL customizer $(basename "$CZ") — see the messages above (no Customizer file ships without its header)" | tee -a "$LOG"
  fi
fi

echo "=== files"
for f in "${EXPECTED[@]}"; do
  if [ -s "$f" ]; then printf '  %8d bytes  %s\n' "$(stat -c %s "$f")" "${f#$DIR/}"
  else echo "  MISSING  ${f#$DIR/}"; FAIL=1; echo "MISSING ${f#$DIR/}" >> "$LOG"; fi
done
echo "=== done, exit $FAIL  (exporter: $OPENSCAD)" | tee -a "$LOG"
exit $FAIL
