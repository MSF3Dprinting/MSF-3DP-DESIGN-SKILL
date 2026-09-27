#!/usr/bin/env node
// openscad_manifold.mjs — run OpenSCAD 2025.07 (Manifold engine) from the npm package `openscad-wasm`
// with the same command line as the native binary, for geometry export. MSF "3D Printing for All".
//
//   node openscad_manifold.mjs -o out.stl --export-format binstl -D 'wall_t=2.7' -D 'part="holder"' part.scad
//   node openscad_manifold.mjs -o out.stl -p part.json -P large part.scad
//   node openscad_manifold.mjs -o part.param --export-format param part.scad   (Customizer description, JSON)
//   node openscad_manifold.mjs --version
//
// What it does: copies every .scad (and .json/.txt/.csv/.dat) file from the model's folder (3 levels of
// sub-folders) into the wasm virtual file system, mounts the system Liberation and DejaVu fonts, runs
// OpenSCAD there with --backend=manifold, and writes the exported file back. Messages are printed like
// the native binary prints them ("ECHO: ...", "WARNING: ...", "ERROR: ..."), without the npm package's
// "[OpenSCAD]: " prefix, so the same greps work for both engines.
// Formats: stl, binstl, off, amf, csg, echo, param, ast. Not available: png (no OpenGL in wasm — use the
// native openscad through render_views.py) and 3mf (crashes in this build — export STL).
// Limits: include <...> / use <...> resolve inside the model's folder and its sub-folders only (not ../).
// Install once:  npm install --prefix "$HOME/.openscad-wasm" openscad-wasm@0.0.4   (scripts/install_openscad.sh does it)
import fs from "node:fs";
import path from "node:path";
import { pathToFileURL } from "node:url";

const t0 = Date.now();
const argv = process.argv.slice(2);
if (argv.length === 0 || argv.includes("--help")) {
  console.log("usage: openscad_manifold.mjs -o OUT [--export-format FMT] [-D name=value ...] [-p params.json -P set] FILE.scad\n" +
              "       openscad_manifold.mjs --version | --info");
  process.exit(argv.length === 0 ? 2 : 0);
}
const die = (msg, code) => { console.error(`[openscad_manifold] ${msg}`); process.exit(code); };

// ---- parse and check the arguments before loading the 14 MB engine ---------------------------------
const infoMode = argv.includes("--version") ? "--version" : argv.includes("--info") ? "--info" : null;
let outHost = null, paramFile = null, inputHost = null, format = null;
const passthrough = [];
for (let i = 0; i < argv.length; i++) {
  const a = argv[i];
  if (a === "-o") { outHost = argv[++i]; continue; }
  if (a.startsWith("-o=")) { outHost = a.slice(3); continue; }
  if (a === "-p") { paramFile = argv[++i]; continue; }
  if (/\.scad$/i.test(a) && !a.startsWith("-")) { inputHost = a; continue; }
  if (a === "--export-format") { format = argv[i + 1]; }
  if (a.startsWith("--export-format=")) { format = a.split("=")[1]; }
  passthrough.push(a);
}
if (!infoMode) {
  if (!inputHost) die("input .scad file missing on the command line", 2);
  if (!fs.existsSync(inputHost)) die(`input file not found: ${inputHost}`, 2);
  if (!outHost) die("-o OUT is required", 2);
  if (paramFile && !fs.existsSync(paramFile)) die(`parameter file not found: ${paramFile}`, 2);
  format = (format || path.extname(outHost).slice(1)).toLowerCase();
  if (format === "png") die("PNG export is not available in the wasm build — use the native openscad for images (render_views.py)", 4);
  if (format === "3mf") die("3MF export is not available in this wasm build (it crashes) — export STL; PrusaSlicer saves a 3MF project from it", 4);
  if (!passthrough.some((a) => a.startsWith("--backend"))) passthrough.push("--backend=manifold");
}

// ---- locate the wasm package ---------------------------------------------------------------------
const candidates = [
  process.env.OPENSCAD_WASM_DIR,
  path.join(process.env.HOME || "", ".openscad-wasm", "node_modules", "openscad-wasm"),
  path.join(path.dirname(new URL(import.meta.url).pathname), "node_modules", "openscad-wasm"),
].filter(Boolean);
const pkgDir = candidates.find((d) => fs.existsSync(path.join(d, "openscad.js")));
if (!pkgDir) die("openscad-wasm not found. Install it:  npm install --prefix \"$HOME/.openscad-wasm\" openscad-wasm@0.0.4", 3);
const { createOpenSCAD } = await import(pathToFileURL(path.join(pkgDir, "openscad.js")).href);

// Print like the native binary: stdout stays stdout, stderr stays stderr, no prefix; drop two lines of
// wasm noise that the native binary never prints.
const NOISE = /^(Could not initialize localization|\s*Status:\s+NoError\s*$)/;
const print = (t) => { if (!NOISE.test(t)) process.stdout.write(t + "\n"); };
const printErr = (t) => { if (!NOISE.test(t)) process.stderr.write(t + "\n"); };
const inst = (await createOpenSCAD({ print, printErr })).getInstance();
const FS = inst.FS;
const callMain = (args) => { try { return inst.callMain(args) || 0; } catch (e) { if (typeof e !== "number") printErr(String(e)); return typeof e === "number" ? e : 1; } };

if (infoMode) process.exit(callMain([infoMode]));

// ---- mount the model folder ------------------------------------------------------------------------
const root = path.resolve(path.dirname(inputHost));
const W = "/work";
FS.mkdir(W);
function copyTree(hostDir, vDir, depth) {
  for (const name of fs.readdirSync(hostDir)) {
    const h = path.join(hostDir, name);
    let st; try { st = fs.statSync(h); } catch (e) { continue; }
    if (st.isDirectory()) {
      if (depth < 3 && !name.startsWith(".") && name !== "node_modules") { FS.mkdir(vDir + "/" + name); copyTree(h, vDir + "/" + name, depth + 1); }
    } else if (/\.(scad|json|txt|csv|dat)$/i.test(name) && st.size < 20_000_000) {
      FS.writeFile(vDir + "/" + name, fs.readFileSync(h));
    }
  }
}
copyTree(root, W, 0);

// ---- fonts: the wasm build ships none, so text() would be empty (coupon digits, non-clinical labels) ----
// This build's fontconfig reads /fonts. Liberation Sans is the skill's font; DejaVu is mounted as a fallback.
const fontDirs = [process.env.OPENSCAD_WASM_FONTS, "/usr/share/fonts/truetype/liberation", "/usr/share/fonts/liberation",
                  "/usr/share/fonts/truetype/dejavu", "/usr/share/fonts/TTF", "/usr/local/share/fonts"]
                 .filter((d) => d && fs.existsSync(d));
let nFonts = 0;
try { FS.mkdir("/fonts"); } catch (e) { /* exists */ }
FS.writeFile("/fonts/fonts.conf", '<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE fontconfig SYSTEM "urn:fontconfig:fonts.dtd">\n<fontconfig><dir>/fonts</dir><cachedir>/tmp/fc</cachedir></fontconfig>\n');
for (const d of fontDirs) for (const f of fs.readdirSync(d)) {
  if (/\.(ttf|otf)$/i.test(f)) { try { FS.writeFile("/fonts/" + f, fs.readFileSync(path.join(d, f))); nFonts++; } catch (e) { /* unreadable */ } }
}
if (nFonts === 0) printErr("WARNING: [openscad_manifold] no .ttf fonts found (apt install fonts-liberation, or set OPENSCAD_WASM_FONTS) — text() will produce nothing");

// ---- run ---------------------------------------------------------------------------------------------
if (paramFile) FS.writeFile(W + "/__params.json", fs.readFileSync(paramFile));
const vIn = W + "/" + path.basename(inputHost);
const vOut = W + "/__out" + (path.extname(outHost).toLowerCase() || "." + format);
const args = ["-o", vOut, ...passthrough];
if (paramFile) args.push("-p", W + "/__params.json");
args.push(vIn);
FS.chdir(W);
const rc = callMain(args);

let data = null;
try { data = FS.readFile(vOut); } catch (e) { /* nothing written */ }
const emptyOk = ["echo", "ast", "csg", "term"].includes(format);   // an echo export with no echo() is legitimately empty
const ok = rc === 0 && data !== null && (data.length > 0 || emptyOk);
const secs = ((Date.now() - t0) / 1000).toFixed(1);
if (ok) {
  fs.mkdirSync(path.dirname(path.resolve(outHost)), { recursive: true });
  fs.writeFileSync(outHost, data);
  console.log(`[openscad_manifold] wrote ${outHost} in ${secs} s (Manifold)`);
  process.exit(0);
}
try { fs.unlinkSync(outHost); } catch (e) { /* no stale file to remove — a failed export never leaves a file */ }
console.error(`[openscad_manifold] FAILED (rc ${rc}) after ${secs} s — see the OpenSCAD messages above`);
process.exit(rc || 1);
