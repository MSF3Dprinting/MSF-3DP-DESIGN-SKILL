// test_coupon.scad — universal tolerance coupon (MSF "3D Printing for All")
// OpenSCAD 2021.01 or newer. Needs common.scad and helpers.scad in the same folder.
//
// A flat plate with one or two rows of openings at stepped clearances. Print it flat, in the same
// material and on the same printer as the part, push the real mating part into the openings and
// reply with the code of the step that fits as intended: "4" (row 1) or "B4" (row 2 = B, row 1 = 4).
// Enter the matching clearance as the part's parameter. The coupon tests the printer, not the design.
//
// Ranges by fit type (workflow §10.4):
//   sliding fit                     clr_start = -0.1, clr_step = 0.1,  n_steps = 10 (per side)
//   tight / push-on onto machined   clr_start = 0.0,  clr_step = 0.05, n_steps = 7  (per side)
//   clearance over a bushing / nut  clr_start = 0.0,  clr_step = 0.2,  n_steps = 3  (on the diameter, per_side = false)
//   push fit on rusty steel         clr_start = 0.075, clr_step = 0.0875, n_steps = 3 (0.075 / 0.15 / 0.25 per side), labels = "notch"
// Vertical holes print small: the coupon measures exactly that. Labels are debossed text — a coupon is a
// non-clinical test piece, so text is allowed. Use labels = "notch" where no text is wanted.

include <common.scad>
include <helpers.scad>

/* [Row 1 — steps numbered 1..n] */
feature   = "round";   // [round, square, rect, slot, dshaft]
nominal   = 6;         // [1:0.1:60] size of the mating part: diameter (round, dshaft), side (square), width (rect, slot)
length    = 30;        // [2:0.5:150] rect / slot: length of the opening
flat      = 4;         // [0:0.1:60] dshaft: across the flat (round side to the flat); 0 = full round
clr_start = 0.0;       // [-0.3:0.025:1] first step clearance
clr_step  = 0.05;      // [0.025:0.025:0.5] increment per step
n_steps   = 7;         // [1:1:12] number of steps
per_side  = true;      // clearance per side (added to both sides) — false: added once, on the diameter / width

/* [Row 2 — steps lettered A.. (optional second feature, e.g. a counterbore or nut)] */
feature2   = "none";   // [none, round, square, rect, slot, dshaft]
nominal2   = 9.4;      // [1:0.1:60]
length2    = 20;       // [2:0.5:150]
flat2      = 0;        // [0:0.1:60]
clr2_start = 0.0;      // [-0.3:0.025:1]
clr2_step  = 0.2;      // [0.025:0.025:0.5]
n2_steps   = 3;        // [1:1:12]
per_side2  = false;    // per side (true) or on the diameter (false)

/* [Plate] */
plate_t     = 4;       // [2:0.5:10] plate thickness
margin      = 4;       // [2:0.5:10] material between openings and to the edge
labels      = "deboss"; // [deboss, notch, none]
label_size  = 6.5;     // [5:0.5:10] letter height for deboss labels
label_depth = 0.6;     // [0.4:0.1:1] deboss depth
opening_c_bot = 0.4;   // [0:0.1:0.8] bottom chamfer of every opening (no elephant's foot closing it)
lead_in     = 0.6;     // [0:0.1:1.5] top lead-in chamfer of every opening
corner_r    = 3;       // [1:0.5:8] plate corner radius

// ===== Derived values =====
function add(c, ps) = ps ? 2 * c : c;                 // total growth of a dimension
function clr(i, c0, dc) = c0 + i * dc;                 // clearance of step i
function ext(f, nom, len, c, ps) =                     // [x, y] extent of an opening
    f == "round"  ? [nom + add(c, ps), nom + add(c, ps)] :
    f == "square" ? [nom + add(c, ps), nom + add(c, ps)] :
    f == "rect"   ? [nom + add(c, ps), len + add(c, ps)] :
    f == "slot"   ? [nom + add(c, ps), len + add(c, ps)] :
    f == "dshaft" ? [nom + add(c, ps), nom + add(c, ps)] : [0, 0];

row1_n  = n_steps;
row2_n  = feature2 == "none" ? 0 : n2_steps;
c1_max  = clr(row1_n - 1, clr_start, clr_step);
c2_max  = clr(max(row2_n - 1, 0), clr2_start, clr2_step);
e1      = ext(feature, nominal, length, c1_max, per_side);
e2      = row2_n > 0 ? ext(feature2, nominal2, length2, c2_max, per_side2) : [0, 0];
label_h = labels == "deboss" ? label_size + 2 : (labels == "notch" ? 3 : 0);
cell1   = [e1[0] + 2 * margin, e1[1] + 2 * margin + label_h];
cell2   = row2_n > 0 ? [e2[0] + 2 * margin, e2[1] + 2 * margin + label_h] : [0, 0];
plate_w = max(row1_n * cell1[0], row2_n * cell2[0]);
plate_h = cell1[1] + cell2[1];
row1_y  = plate_h / 2 - cell1[1] / 2;                  // row 1 at the top, row 2 below it
row2_y  = -plate_h / 2 + cell2[1] / 2;

// ===== Input validation =====
assert(row1_n >= 1 && row1_n <= 12, "n_steps must be 1..12");
assert(nominal + add(clr_start, per_side) > 0.5, "row 1: first opening would be smaller than 0.5 mm — raise clr_start");
assert(row2_n == 0 || nominal2 + add(clr2_start, per_side2) > 0.5, "row 2: first opening would be smaller than 0.5 mm");
assert(feature != "dshaft" || flat == 0 || flat < nominal, "dshaft: flat must be smaller than the diameter");
assert(plate_w <= max_part[0] && plate_h <= max_part[1], "coupon larger than the maximum part — fewer steps or smaller margin");
assert(labels != "deboss" || label_size >= 5, "deboss labels need size >= 5");

echo(str("COUPON plate ", plate_w, " x ", plate_h, " x ", plate_t, " mm"));
for (i = [0 : row1_n - 1]) echo(str("row 1 step ", i + 1, ": clearance ", clr(i, clr_start, clr_step), per_side ? " per side" : " on the diameter/width"));
if (row2_n > 0) for (i = [0 : row2_n - 1]) echo(str("row 2 step ", chr(65 + i), ": clearance ", clr(i, clr2_start, clr2_step), per_side2 ? " per side" : " on the diameter/width"));

// ===== Modules =====
// 2D opening for one step; all shapes are centred on the origin and convex.
module opening2d(f, nom, len, fl, c, ps) {
    a = add(c, ps);
    if (f == "round") circle(d = nom + a);
    else if (f == "square") square(nom + a, center = true);
    else if (f == "rect") square([nom + a, len + a], center = true);
    else if (f == "slot") hull() { translate([0, -(len - nom) / 2]) circle(d = nom + a); translate([0, (len - nom) / 2]) circle(d = nom + a); }
    else if (f == "dshaft") intersection() {
        circle(d = nom + a);
        if (fl > 0) translate([-nom, -(nom + a) / 2]) square([2 * nom, fl + a]);
    }
}

// Through-opening cutter with bottom chamfer and top lead-in (hull of offset slabs, convex shapes).
module opening3d(f, nom, len, fl, c, ps) {
    hull() {
        translate([0, 0, -EPS]) linear_extrude(EPS) offset(delta = opening_c_bot) opening2d(f, nom, len, fl, c, ps);
        translate([0, 0, opening_c_bot]) linear_extrude(EPS) opening2d(f, nom, len, fl, c, ps);
    }
    translate([0, 0, opening_c_bot - EPS]) linear_extrude(plate_t - opening_c_bot - lead_in + 2 * EPS) opening2d(f, nom, len, fl, c, ps);
    hull() {
        translate([0, 0, plate_t - lead_in]) linear_extrude(EPS) opening2d(f, nom, len, fl, c, ps);
        translate([0, 0, plate_t]) linear_extrude(EPS) offset(delta = lead_in) opening2d(f, nom, len, fl, c, ps);
    }
}

module deboss(txt) {
    translate([0, 0, plate_t - label_depth])
        linear_extrude(label_depth + EPS)
            text(txt, size = label_size, font = font, halign = "center", valign = "center");
}

// k V-notches, 2 mm wide and 1 mm deep, cut into the plate edge at y_edge (direction sgn = ±1).
module notches(k, y_edge, sgn) {
    for (j = [0 : k - 1]) translate([(j - (k - 1) / 2) * 3, y_edge, -EPS])
        linear_extrude(plate_t + 2 * EPS) polygon([[-1, sgn * 0.01], [1, sgn * 0.01], [0, -sgn * 1]]);
}

module row(f, nom, len, fl, c0, dc, n, ps, y, cell_w, ey, lettered, edge_y, sgn) {
    for (i = [0 : n - 1]) {
        x = (i - (n - 1) / 2) * cell_w;
        c = clr(i, c0, dc);
        code = lettered ? chr(65 + i) : str(i + 1);
        translate([x, y + label_h / 2, 0]) opening3d(f, nom, len, fl, c, ps);      // opening above the label zone
        if (labels == "deboss") translate([x, y - ey / 2 - margin / 2, 0]) deboss(code);  // label margin/2 below the opening
        if (labels == "notch") translate([x, 0, 0]) notches(i + 1, edge_y, sgn);
    }
}

// ===== Build =====
difference() {
    rounded_box([plate_w, plate_h, plate_t], r = corner_r, c_bot = chamfer_bottom, c_top = 0.6);
    row(feature, nominal, length, flat, clr_start, clr_step, row1_n, per_side, row1_y, cell1[0], e1[1], false, plate_h / 2, 1);
    if (row2_n > 0)
        row(feature2, nominal2, length2, flat2, clr2_start, clr2_step, row2_n, per_side2, row2_y, cell2[0], e2[1], true, -plate_h / 2, -1);
}
