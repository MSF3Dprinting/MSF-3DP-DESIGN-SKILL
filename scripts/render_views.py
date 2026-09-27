#!/usr/bin/env python3
"""render_views.py — the standard render set for any OpenSCAD part (MSF "3D Printing for All").

Produces, for one parameter set:
  <name>_front.png  <name>_top.png  <name>_side.png   orthographic views
  <name>_iso.png                                       isometric
  <name>_context.png / _exploded.png / _section.png    from a context scene file (--context): the scenes
                                                       "installed", "exploded" and "section"
  <name>_sheet.png                                     captioned overview sheet = README product picture
Every image is rendered at 2x and downsampled (LANCZOS) and saved without metadata.
Native OpenSCAD 2021.01 renders PNG only with a display: the script wraps openscad in `xvfb-run -a` when
no DISPLAY is set. Works with any .scad — it only needs the file and its -D overrides.
A render counts as failed when OpenSCAD fails, times out, writes no image, or reports an unknown module
or function (a scene that calls a module the part file does not have renders an empty picture).

Usage
  python3 render_views.py part.scad --out img --name part
  python3 render_views.py part.scad --out img --name part -D 'part="holder"' -D wall_t=2.7
  python3 render_views.py part.scad --out img --name part --context part_context.scad --section-axis y
  python3 render_views.py coupon.scad --out img --name part_coupon --views top --no-sheet
  python3 render_views.py part.scad --out img --name part --full     # CGAL render instead of the preview
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
SCENES = {   # scene value in the context file -> (image suffix, camera)
    "installed": ("context",  ["--projection=p", "--camera=0,0,0,60,0,30,500"]),
    "exploded":  ("exploded", ["--projection=p", "--camera=0,0,0,60,0,30,500"]),
    "section":   ("section",  None),   # camera follows the section axis
}
SECTION_CAMERA = {"x": ["--projection=o", "--camera=0,0,0,90,0,90,500"],   # cut plane normal X: look along X
                  "y": ["--projection=o", "--camera=0,0,0,90,0,0,500"]}    # cut plane normal Y: look along Y
BROKEN = ("unknown module", "unknown function", "Ignoring unknown module", "Ignoring unknown function")


def openscad_cmd(openscad):
    cmd = [openscad]
    if not os.environ.get("DISPLAY") and shutil.which("xvfb-run"):
        cmd = ["xvfb-run", "-a", openscad]
    return cmd


def render(openscad, scad, out_png, extra, defines, size, render_mode, timeout):
    if os.path.exists(out_png):
        os.remove(out_png)
    cmd = openscad_cmd(openscad) + ["-o", out_png, f"--imgsize={size[0]},{size[1]}", "--viewall", "--autocenter",
                                    "--colorscheme=Cornfield"] + extra
    if render_mode:
        cmd.append("--render=true")  # 2021.01 needs the explicit value; a bare --render swallows the next option
    for d in defines:
        cmd += ["-D", d]
    cmd.append(scad)
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        msg = f"timeout after {timeout} s"
    else:
        out = p.stdout + p.stderr
        broken = [l for l in out.splitlines() if any(b in l for b in BROKEN)]
        if p.returncode == 0 and os.path.exists(out_png) and os.path.getsize(out_png) > 0 and not broken:
            return True, ""
        err = broken or [l for l in out.splitlines() if "ERROR" in l or "WARNING" in l]
        msg = "; ".join(err[-3:]) or out.strip()[-300:] or f"exit {p.returncode}, no image"
    if os.path.exists(out_png):
        os.remove(out_png)   # never leave an empty or partial picture behind
    return False, msg


def downsample(path, factor=2):
    from PIL import Image
    im = Image.open(path).convert("RGB")
    im = im.resize((im.width // factor, im.height // factor), Image.LANCZOS)
    im.save(path)  # Pillow drops EXIF unless asked to keep it


def font(px):
    from PIL import ImageFont
    for f in ("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"):
        if os.path.exists(f):
            return ImageFont.truetype(f, px)
    try:
        return ImageFont.load_default(size=px)
    except TypeError:  # Pillow < 10.1
        return ImageFont.load_default()


def sheet(images, captions, out, title):
    from PIL import Image, ImageDraw
    ims = [Image.open(p).convert("RGB") for p in images if os.path.exists(p)]
    if not ims:
        return False
    w = max(i.width for i in ims); h = max(i.height for i in ims)
    cols = 3 if len(ims) > 4 else 2
    rows = (len(ims) + cols - 1) // cols
    fs = max(18, w // 40)                      # caption size follows the image size
    cap_h, top = int(fs * 1.8), int(fs * 2.6)
    board = Image.new("RGB", (cols * w, top + rows * (h + cap_h)), "white")
    d = ImageDraw.Draw(board)
    d.text((fs, fs // 2), title, fill="black", font=font(int(fs * 1.3)))
    for k, (im, cap) in enumerate(zip(ims, captions)):
        x = (k % cols) * w; y = top + (k // cols) * (h + cap_h)
        board.paste(im, (x, y))
        d.text((x + fs // 2, y + h + fs // 3), cap, fill="black", font=font(fs))
    board.save(out)
    return True


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("scad")
    ap.add_argument("--out", default="img")
    ap.add_argument("--name", default=None, help="file name stem (default: the .scad stem)")
    ap.add_argument("-D", action="append", default=[], dest="defines", help="parameter override, e.g. wall_t=2.7 or part=\\\"holder\\\"")
    ap.add_argument("--views", default="front,top,side,iso", help="part views to render, comma list of front, top, side, iso")
    ap.add_argument("--context", default=None, help="context scene .scad (scenes installed / exploded / section)")
    ap.add_argument("--section-axis", choices=["x", "y"], default="x", help="normal of the section plane in the context scene")
    ap.add_argument("--openscad", default="openscad")
    ap.add_argument("--size", default="1600x1200", help="final image size; rendered at 2x")
    ap.add_argument("--full", action="store_true", help="full CGAL render of the part views (slow); default is the OpenCSG preview, which is what the user sees on F5")
    ap.add_argument("--preview", action="store_true", help="(kept for compatibility; preview is the default)")
    ap.add_argument("--timeout", type=int, default=600)
    ap.add_argument("--title", default="")
    ap.add_argument("--no-sheet", action="store_true", help="do not assemble the overview sheet")
    ap.add_argument("--ghosts", action="store_true", help="keep ghost/mating parts in the part views (default: pass -D show_ghosts=false, the convention of the file layout)")
    a = ap.parse_args(argv)
    name = a.name or os.path.splitext(os.path.basename(a.scad))[0]
    os.makedirs(a.out, exist_ok=True)
    fw, fh = (int(v) for v in a.size.lower().split("x"))
    size = (fw * 2, fh * 2)
    made, caps, failed = [], [], []
    views = [v.strip() for v in a.views.split(",") if v.strip()]
    unknown = [v for v in views if v not in VIEWS]
    if unknown:
        ap.error(f"unknown view(s): {', '.join(unknown)} — choose from {', '.join(VIEWS)}")
    part_defines = a.defines if a.ghosts else a.defines + ["show_ghosts=false"]  # part views show the part alone
    for view in views:
        png = os.path.join(a.out, f"{name}_{view}.png")
        ok, msg = render(a.openscad, a.scad, png, VIEWS[view], part_defines, size, a.full, a.timeout)
        print(("ok   " if ok else "FAIL ") + png + ("" if ok else "  " + msg))
        if ok:
            downsample(png); made.append(png); caps.append(view)
        else:
            failed.append(view)
    if a.context:
        for scene, (suffix, extra) in SCENES.items():
            png = os.path.join(a.out, f"{name}_{suffix}.png")
            defs = [f'scene="{scene}"'] + a.defines
            if scene == "section":
                extra = SECTION_CAMERA[a.section_axis]
                defs.append(f'section_axis="{a.section_axis}"')
            ok, msg = render(a.openscad, a.context, png, extra, defs, size, False, a.timeout)
            print(("ok   " if ok else "FAIL ") + png + ("" if ok else "  " + msg))
            if ok:
                downsample(png); made.append(png); caps.append(f"{suffix} (stand-ins are illustration only)")
            else:
                failed.append(scene)
    if not a.no_sheet:
        out = os.path.join(a.out, f"{name}_sheet.png")
        if sheet(made, caps, out, a.title or f"{name} — render set"):
            print("sheet:", out)
        else:
            print("FAIL sheet: no image to assemble")
            failed.append("sheet")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
