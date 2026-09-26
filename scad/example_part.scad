// @name: Example wall pocket
// @description: Open box screwed to a wall that holds one handheld device — worked example of the file conventions.
// @category: Example
// @credit: MSF 3D Printing for All
/* ===== DESIGN SUMMARY =====
 * Part / purpose:    Example wall pocket — an open box screwed to a wall, holding one handheld device.
 *                    A worked example of the file conventions; not an MSF product.
 * Version:           1.1 2026-09-26   Designer: MSF 3D Printing for All
 * Critical part:     no
 * Material:          any on the shelf (PETG or PLA); clinical use -> light colour
 * Environment:       indoor, wiped with Surfanios / bleach / IPA
 * Loads:             device weight (< 1 kg) resting in the pocket; screws in shear
 * Print orientation: standing on the pocket floor (Z = 0 = underside of the floor); supports: none; brim ears optional
 * Mating hardware:   2 x screws d 4-5 mm (parameter screw_d) with wall plugs
 * Fits used:         loose drop-in for the device (clr_dropin per side)
 * Interfaces:        device W x D x H = parameters dev_w, dev_d, dev_h (EXAMPLE VALUES — measure the real device)
 * Unverified values: dev_w, dev_d, dev_h (example only)
 * Flags:             none
 * Deviations:        none
 * Verified:          renders in OpenSCAD 2021.01; see tools/check_stl.py output
 * Not verified:      physical print
 * Approval:          n/a (example)
 * ========================== */
include <common.scad>
include <helpers.scad>

/* [Part selection] */
part = "holder";      // [holder]
/* [Main dimensions — the device it holds] */
dev_w = 60;           // [20:1:150] device width (X)
dev_d = 25;           // [10:1:80]  device depth (Y)
dev_h = 120;          // [20:1:180] device height; the pocket is pocket_frac of it
pocket_frac = 0.5;    // [0.3:0.05:0.8] pocket height as a fraction of the device height
/* [Interface / fit] */
dev_clr = 0.8;        // [0.4:0.1:1.5] clearance per side around the device (loose drop-in, common.scad clr_dropin)
wall_t = 2.7;         // [1.8:0.45:4.5] wall thickness (multiples of 0.45 mm print solid)
floor_t = 3;          // [2:0.5:6] floor thickness
/* [Mounting] */
screw_d = 4.5;        // [3:0.5:6] wall screw diameter (kit / local hardware)
screw_spacing = 40;   // [20:5:120] distance between the two screw holes (X)
screw_z = 30;         // [10:5:150] screw height above the floor underside
/* [Printability] */
corner_r = 4;         // [2:0.5:8] vertical edge radius (closed corners)
drain = 6;            // [0:1:12] drainage hole in the floor, 0 = none
brim_ears = 0;        // [0:1:15] brim ear diameter, 0 = none
/* [Preview] */
show_ghosts = true;   // show the wall and the device in preview (never exported)

// ===== Derived values =====
in_w = dev_w + 2 * dev_clr;
in_d = dev_d + 2 * dev_clr;
out_w = in_w + 2 * wall_t;
out_d = in_d + 2 * wall_t;
h = floor_t + dev_h * pocket_frac;
back_y = out_d / 2;                        // back wall face (+Y, against the wall); the open front faces the viewer (-Y)

// ===== Input validation =====
assert(wall_t >= min_wall - 0.001, str("wall_t must be at least ", min_wall, " mm"));
assert(floor_t >= min_base - 0.001, str("floor_t must be at least ", min_base, " mm"));
assert(screw_spacing + screw_d + 2 * bolt_wall <= out_w + 0.001, "screw_spacing too wide for the back wall — reduce it or widen the device clearance");
assert(screw_z + screw_d / 2 + bolt_wall <= h + 0.001 && screw_z - screw_d / 2 >= floor_t, "screw_z must lie within the back wall height");
assert(out_w <= max_part[0] && out_d <= max_part[1] && h <= max_part[2], "part exceeds the maximum part size");
assert(drain == 0 || drain + 2 * bolt_wall <= min(in_w, in_d), "drain hole too large for the floor");

// ===== Part modules =====
module holder_body() {
    difference() {
        rounded_box([out_w, out_d, h], r = corner_r, c_bot = chamfer_bottom, c_top = chamfer_top);
        // pocket (its vertical edges filleted for cleaning; fillet_min at the floor is a documented default)
        translate([0, 0, floor_t]) linear_extrude(h) rounded_rect([in_w, in_d], r = max(corner_r - wall_t, fillet_min));
        // drainage hole in the floor
        translate([0, 0, 0]) drain_hole(drain, floor_t);
        // wall screw holes through the back wall, teardrop-compensated (horizontal holes)
        for (sx = [-1, 1]) translate([sx * screw_spacing / 2, back_y - wall_t / 2, screw_z])
            teardrop_hole(screw_d + hole_clr, wall_t);
    }
    if (brim_ears > 0) brim_ears([[-out_w / 2, -out_d / 2], [out_w / 2, -out_d / 2], [-out_w / 2, out_d / 2], [out_w / 2, out_d / 2]], brim_ears);
}

// ===== Build (print position: Z = 0 is the bed) =====
if (part == "holder") holder_body();

if ($preview && show_ghosts) {
    translate([0, back_y, 0]) ghost_wall(w = out_w + 100, h = h + 60, t = 20);
    translate([0, 0, floor_t + 0.5]) ghost_device([dev_w, dev_d, dev_h]);
}
