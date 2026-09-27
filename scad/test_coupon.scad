// test_coupon.scad — universal tolerance coupon (MSF "3D Printing for All")
// OpenSCAD 2021.01 or newer. Needs common.scad and helpers.scad in the same folder.
//
// A flat plate with one or two rows of openings at stepped clearances. Print it flat, in the same
// material and on the same printer as the part, push the real mating part into the openings and
// reply with the code of the step that fits as intended: "4" (row 1) or "B4" (row 2 = B, row 1 = 4).
// Enter the matching clearance as the part's parameter. The coupon tests the printer, not the design.
//
// Row 1 steps come from the preset menu (workflow §10.4), or from the sliders when the preset is "custom":
//   sliding     -0.1 to +0.8 mm per side in 0.1 steps (10 steps)
//   tight       0.00 to 0.30 mm per side in 0.05 steps (7 steps) — tight or push-on onto a machined part
//   clearance   +0 / +0.2 / +0.4 mm on the diameter — counterbore over a head, nut or bushing
//   rusty       0.075 / 0.15 / 0.25 mm per side, notch labels — push fit on rusty or variable steel
// Vertical holes print small: the coupon measures exactly that. Labels are debossed digits — a coupon is a
// non-clinical test piece, so text is allowed — or notches where no text is wanted.

include <common.scad>
include <helpers.scad>

/* [Row 1 — steps numbered 1..n] */
// Clearance steps: a preset for the usual fits, or custom (then the sliders below apply)
preset = "tight"; // [tight:Tight or push-on onto a machined part - 0 to 0.30 per side, sliding:Sliding fit - -0.1 to +0.8 per side, clearance:Clearance over a head or nut - +0 +0.2 +0.4 on the diameter, rusty:Push fit on rusty steel - 0.075 0.15 0.25 per side, custom:Custom - use the sliders below]
// Shape of the opening
feature = "round"; // [round:Round hole, square:Square hole, rect:Rectangular hole, slot:Slot, dshaft:D-shaft - round with a flat]
// Size of the mating part: diameter (round, D-shaft), side (square) or width (rectangle, slot), mm
nominal = 6; // [1:0.1:60]
// Length of the opening (rectangle, slot), mm
length = 30; // [2:0.5:150]
// D-shaft: size across the flat (round side to the flat), mm; 0 = full round
flat = 4; // [0:0.1:60]
// Custom preset: clearance of the first step, mm
clr_start = 0.0; // [-0.3:0.025:1]
// Custom preset: increment per step, mm
clr_step = 0.05; // [0.025:0.025:0.5]
// Custom preset: number of steps
n_steps = 7; // [1:1:12]
// Custom preset: clearance added on both sides (on) or once on the diameter or width (off)
per_side = true;

/* [Row 2 — steps lettered A.. (optional second feature, e.g. a counterbore or nut)] */
// Shape of the second row, or none
feature2 = "none"; // [none:No second row, round:Round hole, square:Square hole, rect:Rectangular hole, slot:Slot, dshaft:D-shaft - round with a flat]
// Size of the second mating part, mm
nominal2 = 9.4; // [1:0.1:60]
// Length of the second opening (rectangle, slot), mm
length2 = 20; // [2:0.5:150]
// D-shaft across the flat for row 2, mm; 0 = full round
flat2 = 0; // [0:0.1:60]
// Clearance of the first step of row 2, mm
clr2_start = 0.0; // [-0.3:0.025:1]
// Increment per step of row 2, mm
clr2_step = 0.2; // [0.025:0.025:0.5]
// Number of steps of row 2
n2_steps = 3; // [1:1:12]
// Row 2 clearance added on both sides (on) or once on the diameter or width (off)
per_side2 = false;

/* [Plate] */
// Plate thickness, mm
plate_t = 4; // [2:0.5:10]
// Material between openings and to the edge, mm
margin = 4; // [2:0.5:10]
// How the steps are marked
labels = "auto"; // [auto:As the preset suggests, deboss:Debossed digits and letters, notch:Notches on the edge, none:No marks]
// Letter height of debossed labels, mm
label_size = 6.5; // [6.5:0.5:10]
// Deboss depth, mm
label_depth = 0.6; // [0.4:0.1:1]
// Bottom chamfer of every opening, mm (no elephant's foot closing it)
opening_c_bot = 0.4; // [0:0.1:0.8]
// Top lead-in chamfer of every opening, mm
lead_in = 0.6; // [0:0.1:1.5]
// Plate corner radius, mm
corner_r = 3; // [1:0.5:8]

// ===== Derived values =====
PRESETS = ["tight", "sliding", "clearance", "rusty", "custom"];
FEATURES = ["round", "square", "rect", "slot", "dshaft"];
function steps_of(p) =
    p == "sliding"   ? [for (i = [0 : 9]) -0.1 + 0.1 * i] :
    p == "tight"     ? [for (i = [0 : 6]) 0.05 * i] :
    p == "clearance" ? [0, 0.2, 0.4] :
    p == "rusty"     ? [0.075, 0.15, 0.25] :
                       [for (i = [0 : n_steps - 1]) clr_start + i * clr_step];
c1 = steps_of(preset);                                          // row 1 clearances
ps1 = preset == "clearance" ? false : preset == "custom" ? per_side : true;
c2 = [for (i = [0 : max(n2_steps - 1, 0)]) clr2_start + i * clr2_step];
mark = labels == "auto" ? (preset == "rusty" ? "notch" : "deboss") : labels;
function add(c, ps) = ps ? 2 * c : c;                 // total growth of a dimension
function ext(f, nom, len, c, ps) =                     // [x, y] extent of an opening
    f == "rect" || f == "slot" ? [nom + add(c, ps), len + add(c, ps)] : [nom + add(c, ps), nom + add(c, ps)];

row1_n  = len(c1);
row2_n  = feature2 == "none" ? 0 : n2_steps;
e1      = ext(feature, nominal, length, max(c1), ps1);
e2      = row2_n > 0 ? ext(feature2, nominal2, length2, max(c2), per_side2) : [0, 0];
label_h = mark == "deboss" ? label_size + 2 : 0;       // notches sit in the plate edge, no label zone needed
cell1   = [e1[0] + 2 * margin, e1[1] + 2 * margin + label_h];
cell2   = row2_n > 0 ? [e2[0] + 2 * margin, e2[1] + 2 * margin + label_h] : [0, 0];
plate_w = max(row1_n * cell1[0], row2_n * cell2[0]);
plate_h = cell1[1] + cell2[1];
row1_y  = plate_h / 2 - cell1[1] / 2;                  // row 1 at the top, row 2 below it
row2_y  = -plate_h / 2 + cell2[1] / 2;
notch_pitch = 3;                                       // 2 mm wide notches, 1 mm apart

// ===== Input validation =====
assert(len([for (p = PRESETS) if (p == preset) p]) == 1, str("unknown preset: ", preset));
assert(len([for (f = FEATURES) if (f == feature) f]) == 1, str("unknown feature: ", feature));
assert(feature2 == "none" || len([for (f = FEATURES) if (f == feature2) f]) == 1, str("unknown feature2: ", feature2));
assert(mark == "deboss" || mark == "notch" || mark == "none", str("unknown labels: ", labels));
assert(nominal + add(min(c1), ps1) > 0.5, "row 1: first opening would be smaller than 0.5 mm — raise the first clearance");
assert(row2_n == 0 || nominal2 + add(clr2_start, per_side2) > 0.5, "row 2: first opening would be smaller than 0.5 mm");
assert(feature != "dshaft" || flat == 0 || flat < nominal, "dshaft: flat must be smaller than the diameter");
assert(feature2 != "dshaft" || flat2 == 0 || flat2 < nominal2, "row 2 dshaft: flat must be smaller than the diameter");
assert(plate_w <= max_part[0] && plate_h <= max_part[1], "coupon larger than the maximum part — fewer steps or a smaller margin");
assert(mark != "deboss" || label_size >= 6.5, "debossed labels need size 6.5 or more");
assert(mark != "notch" || max(row1_n, row2_n) * notch_pitch <= min(cell1[0], row2_n > 0 ? cell2[0] : cell1[0]) - 2,
       "too many steps for notch labels in this cell width — use debossed labels or fewer steps");

echo(str("COUPON plate ", plate_w, " x ", plate_h, " x ", plate_t, " mm, preset ", preset));
for (i = [0 : row1_n - 1]) echo(str("row 1 step ", i + 1, ": clearance ", c1[i], ps1 ? " per side" : " on the diameter/width"));
if (row2_n > 0) for (i = [0 : row2_n - 1]) echo(str("row 2 step ", chr(65 + i), ": clearance ", c2[i], per_side2 ? " per side" : " on the diameter/width"));

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

module deboss(txt) {
    translate([0, 0, plate_t - label_depth])
        linear_extrude(label_depth + EPS)
            text(txt, size = label_size, font = font, halign = "center", valign = "center");
}

// k V-notches, 2 mm wide and 1 mm deep, cut into the plate edge at y_edge (direction sgn = ±1).
module notches(k, y_edge, sgn) {
    for (j = [0 : k - 1]) translate([(j - (k - 1) / 2) * notch_pitch, y_edge, -EPS])
        linear_extrude(plate_t + 2 * EPS) polygon([[-1, sgn * 0.01], [1, sgn * 0.01], [0, -sgn * 1]]);
}

module row(f, nom, len, fl, cs, ps, y, cell_w, ey, lettered, edge_y, sgn) {
    n = len(cs);
    for (i = [0 : n - 1]) {
        x = (i - (n - 1) / 2) * cell_w;
        code = lettered ? chr(65 + i) : str(i + 1);
        translate([x, y + label_h / 2, 0]) flared_cutter(plate_t, opening_c_bot, lead_in) opening2d(f, nom, len, fl, cs[i], ps);
        if (mark == "deboss") translate([x, y - ey / 2 - margin / 2, 0]) deboss(code);  // label below the opening
        if (mark == "notch") translate([x, 0, 0]) notches(i + 1, edge_y, sgn);
    }
}

// ===== Build =====
difference() {
    rounded_box([plate_w, plate_h, plate_t], r = corner_r, c_bot = chamfer_bottom, c_top = 0.6);
    row(feature, nominal, length, flat, c1, ps1, row1_y, cell1[0], e1[1], false, plate_h / 2, 1);
    if (row2_n > 0)
        row(feature2, nominal2, length2, flat2, c2, per_side2, row2_y, cell2[0], e2[1], true, -plate_h / 2, -1);
}
