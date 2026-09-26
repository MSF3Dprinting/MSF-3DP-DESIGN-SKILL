// context_scene.scad — context-of-use renders for any part (MSF "3D Printing for All")
// OpenSCAD 2021.01 or newer.
//
// HOW TO USE: copy this file next to <item>.scad as <item>_context.scad, then edit the three
// marked places: (1) the `use` line, (2) part_module() so it calls the item's main module,
// (3) the stand-in sizes. `use` loads the item's modules without running its top-level build,
// so nothing here can leak into the item's STL. This file is never exported itself — the guard
// below refuses to render outside preview mode.
//
// Render (2021.01 needs xvfb-run -a in a headless sandbox):
//   openscad -o img/item_context.png  -D 'scene="installed"' --viewall --autocenter --imgsize=2400,1800 item_context.scad
//   openscad -o img/item_exploded.png -D 'scene="exploded"'  ...
//   openscad -o img/item_section.png  -D 'scene="section"'   --camera=<facing the cut> ...
// then downsample 2x (scripts/render_views.py does all of this).

include <common.scad>
include <helpers.scad>
use <example_part.scad>                      // (1) <item>.scad

/* [Scene] */
scene = "installed";   // [installed, exploded, section]
explode = 30;          // [0:5:100] separation between parts in the exploded view
section_axis = "x";    // [x, y] plane normal of the section cut
section_at = 0;        // [-100:1:100] position of the section plane (mm)

/* [Stand-ins — illustration only, sized to the interfaces] */
wall_w = 240;          // [100:10:600]
wall_h = 240;          // [100:10:600]
wall_t = 20;           // [10:5:50]
wall_y = 16;           // [-100:0.5:100] Y of the wall face the part is fixed to (+Y = behind the part)
device_size = [60, 25, 120];   // device stand-in W x D x H
device_offset = [0, 0, 3.5];   // where the device sits relative to the part origin

assert($preview, "context_scene.scad is for preview renders only — export the part from its own file");

// (2) the part, in its print position, as a module
module part_module() { holder_body(); }

// (3) stand-ins — plain shapes, labelled colours, never exported
module wall_standin()   { color("wheat")     translate([-wall_w / 2, wall_y, 0]) cube([wall_w, wall_t, wall_h]); }
module device_standin() { color("lightblue") translate(device_offset + [0, 0, device_size[2] / 2]) cube(device_size, center = true); }

module scene_installed() {
    color("white") render() part_module();
    wall_standin();
    device_standin();
}
module scene_exploded() {
    color("white") render() part_module();
    translate([0, explode, 0]) wall_standin();
    translate([0, 0, explode]) device_standin();
}
module scene_section() {
    // Cut faces take the cutter's colour in the OpenCSG preview; render() each part first.
    cutter = section_axis == "x" ? [section_at, -1000, -1000] : [-1000, section_at, -1000];
    color("white") render() difference() { part_module(); translate(cutter) cube(2000); }
    color("lightblue") render() difference() { device_standin(); translate(cutter) cube(2000); }
}

if (scene == "installed") scene_installed();
else if (scene == "exploded") scene_exploded();
else if (scene == "section") scene_section();
