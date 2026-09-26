// common.scad — MSF "3D Printing for All" shared design defaults
// OpenSCAD 2021.01 or newer. No external libraries.
// Copy this file next to your part, then:  include <common.scad>
// Values are starting points, not guarantees — tune them after the coupon / first article,
// and record what was confirmed in the README ("Confirmed by test print").
// Sources: MSF 3D Printing Process Guideline V1.1 Parts 2–4; Hydra Research design rules;
//          MSF project values (tagged "project" in the workflow file).

/* [Print process] */
layer_h        = 0.2;    // [0.1:0.05:0.3] layer height (SPEED preset)
ext_w          = 0.45;   // extrusion width with a 0.4 mm nozzle

/* [Fits — clearance PER SIDE unless the name says otherwise] */
clr_free_pp    = 0.3;    // [0.2:0.05:0.5] sliding fit, printed-printed (MSF: >= 0.6 total)
clr_free_pm    = 0.15;   // [0.1:0.05:0.4] sliding fit, printed-machined (MSF: >= 0.3 total)
clr_tight_pp   = 0.15;   // [0.05:0.05:0.3] tight fit, printed-printed (MSF: 0.3 total)
clr_tight_pm   = 0.075;  // [0.0:0.025:0.3] tight fit, printed-machined (MSF: 0.15 total)
clr_dropin     = 0.8;    // [0.4:0.1:1.5] loose drop-in, removable for cleaning
hole_clr       = 0.2;    // [0:0.05:0.5] added to the DIAMETER of vertical holes (holes print small)

/* [Minimum features] */
min_wall       = 1.6;    // MSF minimum wall
struct_wall    = 4 * ext_w;   // 1.8 mm: four perimeters, solid at any slicer setting
min_base       = 2.0;    // base of flat parts
min_handle     = 2.4;    // handled protrusions, both directions
min_hole_v     = 1.5;    // vertical hole diameter
min_pin_d      = 1.8;    // pin diameter
max_bridge     = 10;     // avoid bridges; hard limit if unavoidable
max_overhang   = 45;     // degrees from vertical (60 only where the brief allows it)
overhang_tol   = 0.05;   // degrees, float32 STL rounding on exact 45° faces
max_part       = [200, 200, 200];

/* [Edges] */
chamfer_bottom = 0.4;    // [0.3:0.1:0.6] elephant's foot
chamfer_top    = 0.8;    // [0.6:0.1:1.0] exposed edges
fillet_min     = 1.0;    // internal concave corners (IPC)
base_corner_r  = 4;      // vertical edge radius at the plate, closed corners

/* [Hardware] */
bolt_wall      = 2.5;    // material around bolt holes (four to five perimeters)
min_thread_d   = 10;     // modelled threads only above this diameter ...
min_thread_p   = 1.5;    // ... and this pitch
tap_factor     = 0.90;   // hole for tapping (Hydra)
selftap_factor = 0.96;   // hole for a self-tapping screw (Hydra)
insert_factor  = 0.98;   // hole for a heat-set insert (Hydra) — or the insert maker's value

/* [Drainage and adhesion] */
drain_d        = 6;      // [0:1:12] drainage hole in closed floors, 0 = none (blind sockets >= 2)
brim_ear_d     = 0;      // [0:1:15] built-in brim ears for tall or narrow parts, 0 = none
brim_ear_t     = 0.4;    // two layers

/* [Text — non-clinical items only] */
font           = "Liberation Sans:style=Bold";
text_size_min  = 6;      // letter height (MSF > 6 mm); training set used size 5 (4.8 mm caps)
text_depth     = 0.8;    // [0.6:0.1:1.0] emboss / deboss depth

/* [Colour bands — single extruder, manual changes] */
band_base      = 2.0;    // colour band base
band_min       = 3 * layer_h;   // 0.6 mm per colour

/* [NFC pocket — larger non-clinical items only] */
nfc_pocket     = [19, 19, 1];

/* [Resolution] */
fn_preview     = 32;     // [16:8:64] segments in preview (F5)
fn_export      = 96;     // [48:8:180] segments for export (F6 / command line)
$fn = $preview ? fn_preview : fn_export;

/* [Hidden] */
EPS = 0.01;              // boolean overlap to avoid coincident faces (see boolean hygiene)
assert(version_num() >= 20210100, "OpenSCAD 2021.01 or newer is required");
