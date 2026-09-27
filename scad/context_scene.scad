// context_scene.scad — context-of-use renders for any part (MSF "3D Printing for All")
// OpenSCAD 2021.01 or newer.
//
// HOW TO USE: copy this file next to <item>.scad as <item>_context.scad, then edit the three marked
// places: (1) the `use` line, (2) the part modules, (3) the stand-ins. `use` loads the item's modules
// and functions without running its top-level build, so nothing here can leak into the item's STL, and
// every -D override given to this file reaches the item too (render_views.py passes the variant's).
// Stand-in parameters start with ctx_ so they never collide with a part parameter of the same name.
// Size the stand-ins from functions of the item (ex_device() below) where it offers them, so a variant
// shows the right device; plain ctx_ sliders otherwise. This file is never exported — the guard below
// refuses to render outside preview mode.
//
// Render (native 2021.01 needs xvfb-run -a in a headless sandbox) — scripts/render_views.py does it all:
//   python3 tools/render_views.py item.scad --out img --name item --context item_context.scad --section-axis x

include <common.scad>
include <helpers.scad>
use <example_part.scad>                      // (1) <item>.scad

/* [Scene] */
// Scene to render
scene = "installed"; // [installed:Installed, exploded:Exploded, section:Section]
// Separation between the parts in the exploded view, mm
ctx_explode = 40; // [0:5:100]
// Normal of the section plane
section_axis = "x"; // [x:X - cut from left to right, y:Y - cut from front to back]
// Position of the section plane along its normal, mm
ctx_section_at = 0; // [-100:1:100]

/* [Stand-ins — illustration only] */
// Wall or board width, mm
ctx_wall_w = 240; // [100:10:600]
// Wall or board height, mm
ctx_wall_h = 240; // [100:10:600]
// Wall or board thickness, mm
ctx_wall_t = 18; // [5:1:50]

assert($preview, "context_scene.scad is for preview renders only — export the part from its own file");
assert(scene == "installed" || scene == "exploded" || scene == "section", str("unknown scene: ", scene));
assert(section_axis == "x" || section_axis == "y", str("section_axis must be x or y, not ", section_axis));

// (2) the part as installed, and its pieces for the exploded view (modules of the item)
module part_installed() { assembled(); }                      // example: pocket with the floor insert in place
module part_exploded(e) { holder(); translate([0, 0, e]) floor_insert_in_place(); }
module floor_insert_in_place() { translate([0, 0, ex_device_z() - ex_insert_t()]) floor_insert(); }

// (3) stand-ins — plain shapes sized from the item's functions, labelled colours, never exported
dev = ex_device();                                             // [w, d, h] of the device the item holds
module wall_standin(dy = 0) { color("wheat") translate([-ctx_wall_w / 2, ex_back_y() + dy, 0]) cube([ctx_wall_w, ctx_wall_t, ctx_wall_h]); }
module device_standin(dz = 0) { color("lightblue") translate([0, 0, ex_device_z() + 0.5 + dz + dev[2] / 2]) cube(dev, center = true); }

module scene_installed() {
    color("white") render() part_installed();
    wall_standin();
    device_standin();
}
module scene_exploded() {
    color("white") render() part_exploded(ctx_explode);
    wall_standin(ctx_explode);                                  // wall pulled back
    device_standin(2 * ctx_explode + ex_size()[2]);             // device lifted clear of the pocket
}
module scene_section() {
    // Cut faces take the cutter's colour in the OpenCSG preview; render() each part first.
    cutter = section_axis == "x" ? [ctx_section_at, -1000, -1000] : [-1000, ctx_section_at, -1000];
    color("white") render() difference() { part_installed(); translate(cutter) cube(2000); }
    color("lightblue") render() difference() { device_standin(); translate(cutter) cube(2000); }
}

if (scene == "installed") scene_installed();
else if (scene == "exploded") scene_exploded();
else scene_section();
