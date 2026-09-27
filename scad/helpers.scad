// helpers.scad — MSF "3D Printing for All" helper modules
// OpenSCAD 2021.01 or newer. No external libraries.
// Usage:  include <common.scad>   then   include <helpers.scad>
// Every helper is product-agnostic. All sizes in mm. Parts sit on Z = 0 (print position).
//
// Contents
//   2D:  rounded_rect, rounded_poly, teardrop2d, hex_grid
//   3D:  chamfered_prism, rounded_box, section_cut
//   Holes (cutters): vertical_hole, teardrop_hole, flat_top_hole, cone_roof_bore, nut_trap, drain_hole, flared_cutter
//   Kit hardware (cutters, M3 / M6 from common.scad): kit_hole, kit_hole_h, kit_counterbore, kit_nut_well
//   Several parts: print_plate (all parts on one plate, print position)
//   Adhesion / standing parts: brim_ear, brim_ears, corner_ears, breakaway_support, tab, slot
//   Previews: ghost_tube, ghost_pole, ghost_device, ghost_wall
//
// Boolean hygiene (2021.01 / CGAL): cutters extend EPS or more beyond the faces they cut; never let a
// cutter face coincide with a part face. Clip cutters to the region they are meant to cut.

// ---------------------------------------------------------------- 2D --------------------------------

// Rectangle centred at the origin with rounded corners. size = [x, y]. The radius is clamped just below half
// the shorter side, so a large r never collapses the shape to nothing.
module rounded_rect(size, r = 2) {
    rr = min(r, size[0] / 2 - 0.01, size[1] / 2 - 0.01);
    if (rr <= 0) square(size, center = true);
    else offset(r = rr) square([size[0] - 2 * rr, size[1] - 2 * rr], center = true);
}

function _unit(v) = v / norm(v);
function _ang(v) = atan2(v[1], v[0]);
// Fillet arc replacing vertex p1 (neighbours p0, p2) with radius r, n segments.
function _fillet_pts(p0, p1, p2, r, n) =
    let(a = _unit(p0 - p1), b = _unit(p2 - p1),
        theta = acos(max(-1, min(1, a * b))),          // angle between the two edges at p1
        t = r / tan(theta / 2),                        // tangent length along each edge
        ta = p1 + a * t, tb = p1 + b * t,
        c = p1 + _unit(a + b) * (r / sin(theta / 2)), // arc centre on the bisector
        a0 = _ang(ta - c), a1 = _ang(tb - c),
        d = ((a1 - a0 + 540) % 360) - 180)             // signed sweep, always the short way
    [for (i = [0 : n]) c + r * [cos(a0 + d * i / n), sin(a0 + d * i / n)]];

// Polygon with a fillet radius per vertex: pts = [[[x, y], r], ...] (r = 0 keeps a sharp corner).
// Works for convex and concave corners. Every r must be small enough for its two edges.
module rounded_poly(pts, fn = 16) {
    n = len(pts);
    polygon([for (i = [0 : n - 1])
        let(p1 = pts[i][0], r = pts[i][1], p0 = pts[(i - 1 + n) % n][0], p2 = pts[(i + 1) % n][0])
        each (r > 0 ? _fillet_pts(p0, p1, p2, r, fn) : [p1])]);
}

// Teardrop profile for a horizontal hole: circle of radius r plus a roof whose faces are `angle`
// degrees from vertical, apex on the +Y axis (a true point, so no bridge is needed).
module teardrop2d(r, angle = 45) {
    union() {
        circle(r = r);
        polygon([[-r * cos(angle), r * sin(angle)], [0, r / sin(angle)], [r * cos(angle), r * sin(angle)]]);
    }
}

// Honeycomb of pointy-top hexagonal openings filling `area` = [x, y] (centred), for perforated walls.
// cell = hexagon across flats, wall = web between openings. Openings that would cross the area edge
// are dropped, so the margin stays solid. Use as a 2D cutter:  linear_extrude(t) hex_grid(8, 1.6, [60, 40]);
module hex_grid(cell = 8, wall = 1.6, area = [60, 40]) {
    px = cell + wall; py = px * sqrt(3) / 2; R = cell / sqrt(3);
    nx = floor(area[0] / px) + 1; ny = floor(area[1] / py) + 1;
    for (j = [-ny : ny], i = [-nx : nx]) {
        x = i * px + (j % 2 == 0 ? 0 : px / 2); y = j * py;
        if (abs(x) + R * cos(30) <= area[0] / 2 && abs(y) + R <= area[1] / 2)
            translate([x, y]) rotate(30) circle(r = R, $fn = 6);
    }
}

// ---------------------------------------------------------------- 3D --------------------------------

// Extrude a CONVEX 2D child to height h with a 45° bottom chamfer c_bot (elephant's foot) and an
// optional 45° top chamfer c_top. hull() of inset slabs — no minkowski, fast in CGAL.
module chamfered_prism(h, c_bot = 0.4, c_top = 0) {
    hull() {
        if (c_bot > 0) linear_extrude(EPS) offset(r = -c_bot) children();
        translate([0, 0, c_bot]) linear_extrude(max(h - c_bot - c_top, EPS)) children();
        if (c_top > 0) translate([0, 0, h - EPS]) linear_extrude(EPS) offset(r = -c_top) children();
    }
}

// Box centred in XY on Z = 0 with filleted vertical edges (r) and chamfered bottom / top edges.
module rounded_box(size, r = 2, c_bot = 0.4, c_top = 0.8) {
    chamfered_prism(size[2], c_bot, c_top) rounded_rect([size[0], size[1]], r);
}

// Cut everything above z = h (preview sections; wrap in render() + color() for documentation renders).
module section_cut(h) {
    difference() { children(); translate([-1000, -1000, h]) cube(2000); }
}

// ---------------------------------------------------------------- Holes (cutters) -------------------
// All cutters are positioned by the caller (translate) and extend EPS beyond both faces.

// Vertical through-hole, diameter d + hole_clr (vertical holes print small), height h from z = 0.
module vertical_hole(d, h, clr = hole_clr) {
    translate([0, 0, -EPS]) cylinder(d = d + clr, h = h + 2 * EPS);
}

// Horizontal hole along the Y axis through a wall of thickness l (centred on the origin),
// teardrop-compensated so it prints round without support. angle = roof angle from vertical.
module teardrop_hole(d, l, angle = 45) {
    rotate([90, 0, 0]) linear_extrude(l + 2 * EPS, center = true) teardrop2d(d / 2, angle);
}

// Horizontal hole along the Y axis with a flattened top: a teardrop cut at cut * r, so the top is a
// short flat bridge (about 0.6 r wide at cut = 1.1). Use where the teardrop apex would break a surface.
module flat_top_hole(d, l, cut = 1.1) {
    r = d / 2;
    rotate([90, 0, 0]) linear_extrude(l + 2 * EPS, center = true)
        intersection() { teardrop2d(r, 45); translate([-r - 1, -r - 1]) square([2 * r + 2, r + 1 + cut * r]); }
}

// Blind bore rising from z = 0 to `depth` with a 45° cone roof that starts at the full bore
// width, so a flat-ended shaft still stops at `depth` and no support is needed.
module cone_roof_bore(d, depth, clr = hole_clr) {
    dd = d + clr;
    translate([0, 0, -EPS]) cylinder(d = dd, h = depth + EPS);
    translate([0, 0, depth - EPS]) cylinder(d1 = dd, d2 = 0.5, h = dd / 2);
}

// Hexagonal nut pocket. af = nut across flats, h = pocket depth, clr = total clearance on af.
// Orient the opening horizontally or give it a flat top when it must print without support.
module nut_trap(af, h, clr = 0.3) {
    translate([0, 0, -EPS]) cylinder(d = (af + clr) / cos(30), h = h + EPS, $fn = 6);
}

// Drainage hole through a floor of thickness t: chamfered on the underside (no elephant's foot
// closing it) and led in from above. d = 0 gives nothing, so the parameter can switch it off.
module drain_hole(d = drain_d, t = 2, clr = hole_clr, c = 0.6) {
    if (d > 0) {
        dd = d + clr;
        translate([0, 0, -EPS]) cylinder(d = dd, h = t + 2 * EPS);
        translate([0, 0, -EPS]) cylinder(d1 = dd + 2 * c, d2 = dd, h = c + EPS);
        translate([0, 0, t - c]) cylinder(d1 = dd, d2 = dd + 2 * c, h = c + EPS);
    }
}

// Straight cutter through a plate of thickness h (from z = 0) with a 45° flare at the bottom (c_bot: no
// elephant's foot closing the opening) and a lead-in at the top (c_top). The 2D child must be CONVEX.
// Each flare is a hull of two ADJACENT slabs only — one hull over both flares would widen the whole opening.
// c_bot = 0 or c_top = 0 simply leaves that flare out.
module flared_cutter(h, c_bot = 0.4, c_top = 0.6) {
    translate([0, 0, -EPS]) linear_extrude(h + 2 * EPS) children();
    if (c_bot > 0) hull() {
        translate([0, 0, -EPS]) linear_extrude(EPS) offset(delta = c_bot) children();
        translate([0, 0, c_bot]) linear_extrude(EPS) children();
    }
    if (c_top > 0) hull() {
        translate([0, 0, h - c_top]) linear_extrude(EPS) children();
        translate([0, 0, h]) linear_extrude(EPS) offset(delta = c_top) children();
    }
}

// ---------------------------------------------------------------- Kit hardware (M3 / M6) ------------
// Sizes come from common.scad (kit_* functions). Position the cutters with translate / rotate.

// Vertical clearance hole for a kit bolt through `h` mm from z = 0 (ISO 273 medium + hole_clr).
module kit_hole(m, h) {
    assert(kit_has(m), str("kit bolts are M3 or M6, not M", m));
    vertical_hole(kit_clear_d(m), h);
}

// Horizontal clearance hole for a kit bolt along Y through a wall of thickness l, teardrop-compensated.
module kit_hole_h(m, l) {
    assert(kit_has(m), str("kit bolts are M3 or M6, not M", m));
    teardrop_hole(kit_clear_d(m) + hole_clr, l);
}

// Counterbore for a DIN 912 head, `depth` mm deep, opening upward from z = 0 (the head sits below the
// surface; the part is printed with the counterbore opening up, so it needs no support).
module kit_counterbore(m, depth) {
    assert(kit_has(m), str("kit bolts are M3 or M6, not M", m));
    translate([0, 0, -EPS]) cylinder(d = kit_cbore_d(m), h = depth + EPS);
}

// Captive nut well for a DIN 934 (nyloc = false) or DIN 985 (nyloc = true) nut, opening upward from z = 0:
// across flats + 0.3 mm, depth = nut height + 0.5 mm unless given.
module kit_nut_well(m, nyloc = false, depth = undef) {
    assert(kit_has(m), str("kit nuts are M3 or M6, not M", m));
    nut_trap(kit_nut_af(m), is_undef(depth) ? (nyloc ? kit_nyloc_h(m) : kit_nut_h(m)) + 0.5 : depth);
}

// ---------------------------------------------------------------- Several parts on one plate --------
function _sum(v, i = 0) = i >= len(v) ? 0 : v[i] + _sum(v, i + 1);
function _before(v, i) = i <= 0 ? 0 : _sum([for (k = [0 : i - 1]) v[k]]);

// All parts of an item on one print plate, each child in its own print position and centred on the origin
// in XY; sizes = [[x, y], ...] = the footprint of each child. The children are laid out in a row along X,
// or along Y when the row is wider than the bed; a guard stops when neither fits. It announces the number
// of bodies for the checks (CHECK line read by export.sh and sweep.py).
module print_plate(sizes, gap = 5, bed = bed_size, bodies = undef) {
    n = len(sizes);
    assert($children == n, str("print_plate: ", $children, " children but ", n, " sizes"));
    xs = [for (s = sizes) s[0]]; ys = [for (s = sizes) s[1]];
    sx = _sum(xs) + gap * (n - 1); sy = _sum(ys) + gap * (n - 1);
    row = sx <= bed[0] && max(ys) <= bed[1];
    col = !row && sy <= bed[1] && max(xs) <= bed[0];
    assert(row || col, str("the parts do not fit on one ", bed[0], " x ", bed[1], " mm plate (", round(sx), " x ",
                           round(max(ys)), " or ", round(max(xs)), " x ", round(sy), " mm) - print them one by one"));
    echo(str("CHECK expect_bodies=", is_undef(bodies) ? n : bodies));
    for (i = [0 : n - 1])
        translate(row ? [-sx / 2 + _before(xs, i) + i * gap + xs[i] / 2, 0, 0]
                      : [0, -sy / 2 + _before(ys, i) + i * gap + ys[i] / 2, 0])
            children(i);
}

// ---------------------------------------------------------------- Adhesion / standing parts ---------

// One brim ear (mouse ear) disc on the bed at the origin; union it onto a corner of the footprint.
module brim_ear(d = 10, t = brim_ear_t) { if (d > 0) cylinder(d = d, h = t); }

// Brim ears at a list of XY positions.
module brim_ears(positions, d = brim_ear_d, t = brim_ear_t) {
    for (p = positions) translate([p[0], p[1], 0]) brim_ear(d, t);
}

// Brim ears at the four corners of a centred rectangular footprint [w, dpt] — the usual case for a tall
// box that lifts at its corners. Prefer a larger base radius or a lower part first; ears are the fallback.
module corner_ears(w, dpt, d = brim_ear_d, t = brim_ear_t) {
    brim_ears([[-w / 2, -dpt / 2], [w / 2, -dpt / 2], [-w / 2, dpt / 2], [w / 2, dpt / 2]], d, t);
}

// Built-in breakaway support: a thin-walled column (single perimeter walls) from the bed up to `gap` below
// the overhanging face it supports; size = [x, y, z_of_face]. Snap off after printing. Use only where the
// geometry cannot be changed (45° roof, chamfer, orientation) — and never under a cleanable surface.
module breakaway_support(size, gap = 0.2, wall = 0.8) {
    h = size[2] - gap;
    if (h > 0) difference() {
        translate([-size[0] / 2, -size[1] / 2, 0]) cube([size[0], size[1], h]);
        if (size[0] > 2 * wall + 1 && size[1] > 2 * wall + 1)
            translate([-size[0] / 2 + wall, -size[1] / 2 + wall, -EPS]) cube([size[0] - 2 * wall, size[1] - 2 * wall, h + 2 * EPS]);
    }
}

// Standard tab for standing flat parts (training sets): l × w footprint, t thick, on Z = 0,
// centred in X, growing in -Y from the origin.
module tab(l = 30, w = 8, t = 2.0) {
    translate([-l / 2, -w, 0]) cube([l, w, t]);
}

// Matching slot cutter in a stand: tab + clearance, `depth` deep from z = top down, with an entry
// chamfer. Place it with translate([x, y, top - depth]).
module slot(l = 30, t = 2.0, depth = 8, clr = 0.3, entry = 0.4) {
    tt = t + 2 * clr; ll = l + 2 * clr;
    translate([-ll / 2, -tt / 2, -EPS]) cube([ll, tt, depth + 2 * EPS]);
    translate([0, 0, depth - entry])
        linear_extrude(entry + EPS, scale = [(ll + 2 * entry) / ll, (tt + 2 * entry) / tt])
            square([ll, tt], center = true);
}

// ---------------------------------------------------------------- Previews (never exported) ---------
// % makes them background objects: visible in preview, absent from render and export.

module ghost_tube(d, l, axis = "x") {          // horizontal tube or rail through the origin
    %color("silver", 0.4)
        if (axis == "x") rotate([0, 90, 0]) cylinder(d = d, h = l, center = true);
        else rotate([90, 0, 0]) cylinder(d = d, h = l, center = true);
}
module ghost_pole(d, h) { %color("silver", 0.4) translate([0, 0, -h / 2]) cylinder(d = d, h = h); }
module ghost_device(size) { %color("lightblue", 0.4) translate([0, 0, size[2] / 2]) cube(size, center = true); }
module ghost_wall(w = 200, h = 200, t = 20) { %color("wheat", 0.3) translate([-w / 2, 0, 0]) cube([w, t, h]); }
