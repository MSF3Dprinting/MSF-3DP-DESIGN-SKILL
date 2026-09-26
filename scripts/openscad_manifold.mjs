#!/usr/bin/env node
// openscad_manifold.mjs — run OpenSCAD 2025.07 (Manifold engine) from the npm package `openscad-wasm`
// with the same command line as the native binary, for geometry export. MSF "3D Printing for All".
//
//   node openscad_manifold.mjs -o out.stl --export-format binstl -D 'wall_t=2.7' -D 'part="holder"' part.scad
//   node openscad_manifold.mjs -o out.stl -p part.json -P large part.scad
//
// What it does: copies every .scad (and .json) file from the model's folder into the wasm virtual
// file system, runs OpenSCAD there with --backend=manifold, and writes the exported file back.
// Limits: geometry export only (stl, binstl, 3mf, off, amf, csg, echo) — no PNG (the wasm build has no
// OpenGL); include <...> resolves inside the model's folder and its sub-folders; use <...> likewise.
// Install once:  npm install --prefix "$HOME/.openscad-wasm" openscad-wasm@0.0.4   (scripts/install_openscad.sh does it)
import fs from "node:fs";
import path from "node:path";
import { createRequire } from "node:module";
import { pathToFileURL } from "node:url";

const argv = process.argv.slice(2);
if (argv.length === 0 || argv.includes("--help")) {
  console.log("usage: openscad_manifold.mjs -o OUT [--export-format FMT] [-D name=value ...] [-p params.json -P set] FILE.scad");
  process.exit(argv.length === 0 ? 2 : 0);
}

// ---- locate the wasm package -------------------------------------------------------------------
const candidates = [
  process.env.OPENSCAD_WASM_DIR,
  path.join(process.env.HOME || "", ".openscad-wasm", "node_modules", "openscad-wasm"),
  path.join(path.dirname(new URL(import.meta.url).pathname), "node_modules", "openscad-wasm"),
].filter(Boolean);
let pkgDir = candidates.find((d) => fs.existsSync(path.join(d, "openscad.js")));
if (!pkgDir) {
  console.error("openscad-wasm not found. Install it:  npm install --prefix \"$HOME/.openscad-wasm\" openscad-wasm@0.0.4");
  process.exit(3);
}
const { createOpenSCAD } = await import(pathToFileURL(path.join(pkgDir, "openscad.js")).href);

// ---- parse the arguments we must translate ------------------------------------------------------
let outHost = null, paramFile = null, inputHost = null;
const passthrough = [];
for (let i = 0; i < argv.length; i++) {
  const a = argv[i];
  if (a === "-o") { outHost = argv[++i]; continue; }
  if (a.startsWith("-o=")) { outHost = a.slice(3); continue; }
  if (a === "-p") { paramFile = argv[++i]; continue; }
  if (a.endsWith(".scad") && !a.startsWith("-")) { inputHost = a; continue; }
  passthrough.push(a);
}
if (!inputHost || !fs.existsSync(inputHost)) { console.error("input .scad file missing"); process.exit(2); }
if (!outHost) { console.error("-o OUT is required"); process.exit(2); }
if (/\.png$/i.test(outHost)) { console.error("PNG export is not available in the wasm build — use the native openscad for images (render_views.py)"); process.exit(4); }
if (!passthrough.some((a) => a.startsWith("--backend"))) passthrough.push("--backend=manifold");

// ---- mount the model folder into the virtual FS ---------------------------------------------------
const o = await createOpenSCAD();
const inst = o.getInstance();
const FS = inst.FS;
const root = path.resolve(path.dirname(inputHost));
const W = "/work";
FS.mkdir(W);
function copyTree(hostDir, vDir, depth) {
  for (const name of fs.readdirSync(hostDir)) {
    const h = path.join(hostDir, name);
    const st = fs.statSync(h);
    if (st.isDirectory()) {
      if (depth < 3 && !name.startsWith(".") && name !== "node_modules") { FS.mkdir(vDir + "/" + name); copyTree(h, vDir + "/" + name, depth + 1); }
    } else if (/\.(scad|json|txt|csv|dat)$/i.test(name) && st.size < 20_000_000) {
      FS.writeFile(vDir + "/" + name, fs.readFileSync(h));
    }
  }
}
copyTree(root, W, 0);
if (paramFile) FS.writeFile(W + "/__params.json", fs.readFileSync(paramFile));
const vIn = W + "/" + path.basename(inputHost);
const vOut = W + "/__out" + path.extname(outHost).toLowerCase();
const args = ["-o", vOut, ...passthrough];
if (paramFile) args.push("-p", W + "/__params.json");
args.push(vIn);

// ---- run ------------------------------------------------------------------------------------------
const t0 = Date.now();
let rc = 0;
try { FS.chdir(W); rc = inst.callMain(args) || 0; } catch (e) { rc = typeof e === "number" ? e : 1; if (typeof e !== "number") console.error(String(e)); }
let written = false;
try {
  const data = FS.readFile(vOut);
  fs.mkdirSync(path.dirname(path.resolve(outHost)), { recursive: true });
  fs.writeFileSync(outHost, data);
  written = data.length > 0;
} catch (e) { /* no output */ }
const secs = ((Date.now() - t0) / 1000).toFixed(1);
if (written && rc === 0) { console.log(`[openscad_manifold] wrote ${outHost} in ${secs} s (Manifold)`); process.exit(0); }
console.error(`[openscad_manifold] FAILED (rc ${rc}) after ${secs} s — see the OpenSCAD messages above`);
process.exit(rc || 1);
