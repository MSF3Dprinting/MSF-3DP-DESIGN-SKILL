#!/usr/bin/env python3
"""render_views.py — the standard render set for any OpenSCAD part (MSF "3D Printing for All").

Produces, for one parameter set:
  <name>_front.png  <name>_top.png  <name>_side.png   orthographic views
  <name>_iso.png                                       isometric (OpenSCAD's default diagonal)
  <name>_context.png / _exploded.png / _section.png    from a context scene file (--context)
  <name>_sheet.png                                     captioned overview sheet = README product picture
Every image is rendered at 2x and downsampled (LANCZOS) and saved without metadata.
2021.01 cannot render PNG without a display: the script wraps openscad in `xvfb-run -a` when
no DISPLAY is set. Works with any .scad — it only needs the file and its -D overrides.

Usage
  python3 render_views.py part.scad --out img --name part
  python3 render_views.py part.scad --out img --name part -D 'part="holder"' -D wall_t=2.7
  python3 render_views.py part.scad --out img --name part --context part_context.scad
  python3 render_views.py part.scad --out img --name part --preview   # OpenCSG preview instead of --render (faster, may show artefacts)
"""
import argparse
import os
import shutil
import subprocess
import sys

VIEWS = {
    # name: (extra openscad args)  — rotations are OpenSCAD's standard views
    "front": ["--projection=o", "--camera=0,0,0,90,0,0,500"],
    "top":   ["--projection=o", "--camera=0,0,0,0,0,0,500"],
    "side":  ["--projection=o", "--camera=0,0,0,90,0,90,500"],
    "iso":   ["--projection=p", "--camera=0,0,0,55,0,25,500"],
}
SCENES = {
    "installed": ["--projection=p", "--camera=0,0,0,60,0,30,500"],
    "exploded":  ["--projection=p", "--camera=0,0,0,60,0,30,500"],
    "section":   ["--projection=o", "--camera=0,0,0,90,0,90,500"],
}


def openscad_cmd(openscad):
    cmd = [openscad]
    if not os.environ.get("DISPLAY") and shutil.which("xvfb-run"):
        cmd = ["xvfb-run", "-a", openscad]
    return cmd


def render(openscad, scad, out_png, extra, defines, size, render_mode, timeout):
    cmd = openscad_cmd(openscad) + ["-o", out_png, f"--imgsize={size[0]},{size[1]}", "--viewall", "--autocenter",
                                    "--colorscheme=Cornfield"] + extra
    if render_mode:
        cmd.append("--render=true")  # 2021.01 needs the explicit value; a bare --render swallows the next option
    for d in defines:
        cmd += ["-D", d]
    cmd.append(scad)
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    if p.returncode != 0 or not os.path.exists(out_png):
        err = [l for l in (p.stdout + p.stderr).splitlines() if "ERROR" in l or "WARNING" in l]
        return False, "; ".join(err[-3:]) or p.stderr[-300:]
    return True, ""


def downsample(path, factor=2):
    try:
        from PIL import Image
    except ImportError:
        return
    im = Image.open(path).convert("RGB")
    im = im.resize((im.width // factor, im.height // factor), Image.LANCZOS)
    im.save(path)  # Pillow drops EXIF unless asked to keep it


def sheet(images, captions, out, title):
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        return
    ims = [Image.open(p).convert("RGB") for p in images if os.path.exists(p)]
    if not ims:
        return
    w = max(i.width for i in ims); h = max(i.height for i in ims)
    cols = 3 if len(ims) > 4 else 2
    rows = (len(ims) + cols - 1) // cols
    cap_h = 28
    board = Image.new("RGB", (cols * w, 40 + rows * (h + cap_h)), "white")
    d = ImageDraw.Draw(board)
    d.text((12, 10), title, fill="black")
    for k, (im, cap) in enumerate(zip(ims, captions)):
        x = (k % cols) * w; y = 40 + (k // cols) * (h + cap_h)
        board.paste(im, (x, y))
        d.text((x + 10, y + h + 6), cap, fill="black")
    board.save(out)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("scad")
    ap.add_argument("--out", default="img")
    ap.add_argument("--name", default=None, help="file name stem (default: the .scad stem)")
    ap.add_argument("-D", action="append", default=[], dest="defines", help="parameter override, e.g. wall_t=2.7 or part=\\\"holder\\\"")
    ap.add_argument("--context", default=None, help="context scene .scad (installed / exploded / section)")
    ap.add_argument("--openscad", default="openscad")
    ap.add_argument("--size", default="1600x1200", help="final image size; rendered at 2x")
    ap.add_argument("--full", action="store_true", help="full CGAL render of the part views (slow); default is the OpenCSG preview, which is what the user sees on F5")
    ap.add_argument("--preview", action="store_true", help="(kept for compatibility; preview is the default)")
    ap.add_argument("--timeout", type=int, default=600)
    ap.add_argument("--title", default="")
    ap.add_argument("--ghosts", action="store_true", help="keep ghost/mating parts in the part views (default: pass -D show_ghosts=false, the convention of the file layout)")
    a = ap.parse_args(argv)
    name = a.name or os.path.splitext(os.path.basename(a.scad))[0]
    os.makedirs(a.out, exist_ok=True)
    fw, fh = (int(v) for v in a.size.lower().split("x"))
    size = (fw * 2, fh * 2)
    made, caps, failed = [], [], []
    part_defines = a.defines if a.ghosts else a.defines + ["show_ghosts=false"]  # part views show the part alone
    for view, extra in VIEWS.items():
        png = os.path.join(a.out, f"{name}_{view}.png")
        ok, msg = render(a.openscad, a.scad, png, extra, part_defines, size, a.full, a.timeout)
        print(("ok   " if ok else "FAIL ") + png + ("" if ok else "  " + msg))
        if ok:
            downsample(png); made.append(png); caps.append(view)
        else:
            failed.append(view)
    if a.context:
        for scene, extra in SCENES.items():
            png = os.path.join(a.out, f"{name}_{scene}.png")
            ok, msg = render(a.openscad, a.context, png, extra, [f'scene="{scene}"'] + a.defines, size, False, a.timeout)
            print(("ok   " if ok else "FAIL ") + png + ("" if ok else "  " + msg))
            if ok:
                downsample(png); made.append(png); caps.append(scene + " (stand-ins are illustration only)")
            else:
                failed.append(scene)
    sheet(made, caps, os.path.join(a.out, f"{name}_sheet.png"), a.title or f"{name} — render set")
    print("sheet:", os.path.join(a.out, f"{name}_sheet.png"))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
