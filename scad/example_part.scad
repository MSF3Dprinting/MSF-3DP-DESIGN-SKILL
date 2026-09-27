/* ===== DESIGN SUMMARY =====
 * Part / purpose:    Example wall pocket — an open box fixed to a wall or board by a back plate with two side
 *                    tabs, holding one handheld device, plus a removable perforated floor insert that keeps the
 *                    device out of spilled fluid and lifts out for cleaning. A worked example of the file
 *                    conventions of the msf-3dp-design skill; not an MSF product.
 * Version:           1.4 2026-09-27   Designer: Claude, msf-3dp-design skill v1.4.0
 * Critical part:     no
 * Material:          any on the shelf (PETG or PLA); clinical use -> light colour
 * Environment:       indoor, wiped with Surfanios / bleach / IPA
 * Loads:             device weight (<= 1 kg) on the insert and floor, carried by the side walls into the back plate
 *                    and two fasteners in shear. Every load path runs along the layers: the back plate and its
 *                    tabs are vertical plates joined to the side walls over their full height, and each fastener
 *                    clamps a tab through its thickness (in the layer plane) — nothing pulls layers apart.
 *                    Hand estimate: 10 N on two fasteners; bearing on a tab 5 N / (4.7 mm x 4 mm) = 0.3 MPa.
 * Print orientation: holder standing on its floor (Z = 0 = underside of the floor); insert flat; supports: none;
 *                    brim ears optional (ear_d)
 * Mating hardware:   menu `mount`: kit M6 or M3 bolts DIN 912 + washers DIN 125A + self-locking nuts DIN 985
 *                    through a board, or two local wall screws with plugs; the HARDWARE echo names the parts
 * Fits used:         loose drop-in for the device and for the insert (0.8 mm per side, common.scad clr_dropin)
 * Interfaces:        device W x D x H = dev_w, dev_d, dev_h (EXAMPLE VALUES — measure the real device)
 * Unverified values: dev_w, dev_d, dev_h (example only)
 * Flags:             none
 * Deviations:        none
 * Verified:          checks and sweep with scripts/ (OpenSCAD 2025.07 Manifold export)
 * Not verified:      physical print
 * Approval:          n/a (example)
 * ========================== */
include <common.scad>
include <helpers.scad>

/* [Part selection] */
// Part to show or export: each part in its print position; all parts on one print plate; or the assembled view
part = "holder"; // [holder:Wall pocket, insert:Floor insert, all:All parts - one print plate, assembly:Assembled view - not for printing]

/* [Device it holds] */
// Device width (X), mm — measure the real device
dev_w = 60; // [30:1:150]
// Device depth (Y), mm
dev_d = 25; // [10:1:80]
// Device height, mm
dev_h = 120; // [40:1:180]
// Pocket height as a fraction of the device height
pocket_frac = 0.5; // [0.3:0.05:0.8]

/* [Fit] */
// Clearance per side around the device, mm (loose drop-in)
dev_clr = 0.8; // [0.4:0.1:1.5]
// Wall thickness, mm (multiples of 0.45 mm print solid)
wall_t = 2.7; // [1.8:0.45:4.5]
// Floor thickness, mm
floor_t = 3; // [2:0.5:6]

/* [Floor insert] */
// Insert plate thickness, mm
insert_t = 2.4; // [2:0.2:4]
// Clearance per side between the insert and the pocket, mm (loose, lifts out for cleaning)
insert_clr = 0.8; // [0.4:0.1:1.5]
// Size of the hexagonal openings, mm across flats
hex_cell = 8; // [5:1:12]

/* [Mounting] */
// How the pocket is fixed
mount = "m6"; // [m6:Kit M6 bolts through a board or panel, m3:Kit M3 bolts through a board or panel, screw:Two wall screws with plugs - local hardware]
// Thickness of the board or panel behind the pocket, mm (kit bolts only)
board_t = 18; // [3:1:40]
// Wall screw diameter, mm (wall screws only)
screw_d = 4.5; // [3:0.5:6]
// Width of each side tab, mm (grows by itself when the washer or screw head needs more)
tab_w = 16; // [12:1:30]
// Thickness of the back plate and its tabs, mm
tab_t = 4; // [3:0.5:8]
// Height of the fixing holes above the underside, mm (kept inside the tab)
hole_z = 20; // [8:1:100]

/* [Printability] */
// Vertical edge radius at the front corners, mm
corner_r = 4; // [2:0.5:8]
// Drainage hole in the floor, mm (0 = none)
drain = 6; // [0:1:12]
// Brim ear diameter at the corners, mm (0 = none)
ear_d = 0; // [0:1:15]
// Gap between parts on the print plate, mm
plate_gap = 5; // [3:1:20]

/* [Preview] */
// Show the board and the device in preview (never exported)
show_ghosts = true;

// ===== Derived values =====
in_w = dev_w + 2 * dev_clr;
in_d = dev_d + 2 * dev_clr;
out_w = in_w + 2 * wall_t;
out_d = in_d + 2 * wall_t;
h = floor_t + dev_h * pocket_frac;
back_y = out_d / 2;                                   // back face (+Y) against the board; the open top faces up
kit = mount != "screw";
m = mount == "m6" ? 6 : mount == "m3" ? 3 : 0;
hole_d = kit ? kit_clear_d(m) + hole_clr : screw_d + hole_clr;
seat_d = kit ? kit_washer_d(m) : 2 * screw_d;         // washer or screw head on the tab's front face
tab_we = max(tab_w, seat_d + 2 * fillet_min + 1);     // tab width actually used (adapts to the hardware)
total_w = out_w + 2 * tab_we;
hole_x = out_w / 2 + tab_we / 2;
hz = min(max(hole_z, seat_d / 2 + 1), h - seat_d / 2 - 1);   // hole height actually used (kept inside the tab)
tab_r = max(0.5, min(corner_r, tab_t / 2, (tab_we - hole_d) / 2 - bolt_wall));   // tab-end rounding that keeps bolt_wall round the hole
ct_wall = top_chamfer(wall_t);
ct_tab = top_chamfer(min(tab_t, wall_t));   // behind the pocket the plate is only wall_t thick
cav_r = max(corner_r - wall_t, fillet_min);
ins_w = in_w - 2 * insert_clr;
ins_d = in_d - 2 * insert_clr;
ins_r = max(cav_r - insert_clr, 0.5);
bolt_l = kit ? kit_bolt_for(m, tab_t + board_t) : 0;
screw_l = ceil((tab_t + 30) / 5) * 5;                 // wall screw: through the tab plus about 30 mm into the plug

// Stand-in sizes for the context scene (functions reach through `use`, with every -D override applied)
function ex_device() = [dev_w, dev_d, dev_h];
function ex_device_z() = floor_t + insert_t;
function ex_back_y() = back_y;
function ex_insert_t() = insert_t;
function ex_size() = [total_w, out_d, h];

// ===== Input validation =====
assert(wall_t >= min_wall - 0.001, str("wall_t must be at least ", min_wall, " mm"));
assert(floor_t >= min_base - 0.001, str("floor_t must be at least ", min_base, " mm"));
assert(insert_t >= min_base - 0.001, str("insert_t must be at least ", min_base, " mm"));
assert(h >= seat_d + 2, "the pocket is too low for the fixing hardware — raise dev_h or pocket_frac");
assert(drain == 0 || drain + 2 * bolt_wall <= min(in_w, in_d) + 0.001, "drain hole too large for the floor");
assert(total_w <= max_part[0] && out_d <= max_part[1] && h <= max_part[2], "part exceeds the maximum part size");
if (hz != hole_z) echo(str("NOTE: hole_z ", hole_z, " moved to ", hz, " mm to keep the hardware on the tab"));
if (tab_we != tab_w) echo(str("NOTE: tab_w ", tab_w, " widened to ", tab_we, " mm for the washer or screw head"));
if (kit && bolt_l > 0)
    echo(str("HARDWARE: kit - 2 x bolt M", m, " x ", bolt_l, " DIN 912, 4 x washer DIN 125A M", m,
             ", 2 x self-locking nut DIN 985 M", m));
if (kit && bolt_l == 0)
    echo(str("HARDWARE: no kit bolt is long enough - 2 x local bolt M", m, " x ", ceil(kit_bolt_need(m, tab_t + board_t) / 5) * 5,
             " stainless (DIN 912 or ISO 4017), 4 x washer DIN 125A M", m, ", 2 x self-locking nut DIN 985 M", m, " from the kit"));
if (!kit)
    echo(str("HARDWARE: local - 2 x wall screw ", screw_d, " x ", screw_l, " mm and 2 wall plugs to suit the wall"));

// ===== Part modules =====
// Concave vertical fillet filling the inside corner at the origin, in the quadrant +X / -Y. Its legs reach
// chamfer_bottom + 0.1 mm into both walls, so it stays joined to them where their bottom chamfers step back.
// The circle sits 0.05 mm off both walls: a fillet exactly tangent to a wall leaves zero-area specks in the
// mesh boolean; 0.05 mm is invisible in print.
module inside_fillet(r, hh) {
    e = chamfer_bottom + 0.1;
    linear_extrude(hh) difference() {
        translate([-e, -r - 0.05]) square([r + e + 0.05, r + e + 0.05]);
        translate([r + 0.05, -r - 0.05]) circle(r = r);
    }
}

module holder() {
    difference() {
        union() {
            // pocket body: rounded front corners; its square back ends halfway into the back plate, so the two
            // solids never share a face (boolean hygiene)
            chamfered_prism(h, chamfer_bottom, ct_wall)
                rounded_poly([[[-out_w / 2, -out_d / 2], corner_r], [[out_w / 2, -out_d / 2], corner_r],
                              [[out_w / 2, back_y - tab_t / 2], 0], [[-out_w / 2, back_y - tab_t / 2], 0]]);
            // back plate with the two side tabs, full height: joined to the side walls along their whole height
            translate([0, back_y - tab_t / 2, 0])
                chamfered_prism(h, chamfer_bottom, ct_tab) rounded_rect([total_w, tab_t], r = tab_r);
            // inside fillets where the tabs meet the side walls (IPC: no sharp inside corner)
            for (sx = [-1, 1]) translate([sx * out_w / 2, back_y - tab_t, 0]) mirror([sx < 0 ? 1 : 0, 0, 0])
                inside_fillet(fillet_min, h - max(ct_wall, ct_tab));
        }
        // pocket (vertical inside edges filleted for cleaning)
        translate([0, 0, floor_t]) linear_extrude(h) rounded_rect([in_w, in_d], r = cav_r);
        // drainage hole in the floor
        drain_hole(drain, floor_t);
        // fixing holes through the tabs, along Y, teardrop-compensated (horizontal holes)
        for (sx = [-1, 1]) translate([sx * hole_x, back_y - tab_t / 2, hz]) teardrop_hole(hole_d, tab_t);
    }
    if (ear_d > 0) brim_ears([[-total_w / 2, back_y], [total_w / 2, back_y], [-out_w / 2, -out_d / 2], [out_w / 2, -out_d / 2]], ear_d);
}

module floor_insert() {
    m_edge = 3;                                         // solid rim around the openings
    difference() {
        chamfered_prism(insert_t, chamfer_bottom, top_chamfer(insert_t)) rounded_rect([ins_w, ins_d], r = ins_r);
        translate([0, 0, -EPS]) linear_extrude(insert_t + 2 * EPS)
            hex_grid(hex_cell, struct_wall, [ins_w - 2 * m_edge, ins_d - 2 * m_edge]);
    }
}

// Every part in its installed position (the insert 0.1 mm above the floor, so the two stay separate bodies)
module assembled() {
    holder();
    translate([0, 0, floor_t + 0.1]) floor_insert();
}

// ===== Build (print position: Z = 0 is the bed) =====
if (part == "holder") holder();
else if (part == "insert") floor_insert();
else if (part == "all") print_plate([[total_w, out_d], [ins_w, ins_d]], plate_gap) { holder(); floor_insert(); }
else if (part == "assembly") {
    echo("CHECK view_only expect_bodies=2");
    if ($preview) { color("white") holder(); color("lightgrey") translate([0, 0, floor_t + 0.1]) floor_insert(); }
    else assembled();
}
else assert(false, str("unknown part: ", part));

if ($preview && show_ghosts && (part == "holder" || part == "assembly")) {
    translate([0, back_y, 0]) ghost_wall(w = total_w + 100, h = h + 60, t = kit ? board_t : 20);
    translate([0, 0, floor_t + insert_t + 0.5]) ghost_device([dev_w, dev_d, dev_h]);
}
