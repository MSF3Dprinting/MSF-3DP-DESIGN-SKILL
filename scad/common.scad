// common.scad — MSF "3D Printing for All" shared design defaults
// OpenSCAD 2021.01 or newer. No external libraries.
// Copy this file next to your part, then:  include <common.scad>
// Values are starting points, not guarantees — tune them after the coupon / first article,
// and record what was confirmed in the README ("Confirmed by test print").
// The Customizer shows only the part file's own parameters; these values are library defaults
// (the one-file Customizer version puts them under [Hidden]).
// Sources: MSF 3D Printing Process Guideline V1.1 Parts 2–4; Hydra Research design rules; DIN 912, 934, 985,
//          125A and ISO 273 for the kit hardware; MSF project values (tagged "project" in the workflow file).

/* [Print process] */
// Layer height, mm (SPEED preset)
layer_h        = 0.2;    // [0.1:0.05:0.3]
// Extrusion width with a 0.4 mm nozzle, mm
ext_w          = 0.45;

/* [Fits — clearance PER SIDE unless the name says otherwise] */
// Sliding fit, printed-printed (MSF: >= 0.6 total)
clr_free_pp    = 0.3;    // [0.2:0.05:0.5]
// Sliding fit, printed-machined (MSF: >= 0.3 total)
clr_free_pm    = 0.15;   // [0.1:0.05:0.4]
// Tight fit, printed-printed (MSF: 0.3 total)
clr_tight_pp   = 0.15;   // [0.05:0.05:0.3]
// Tight fit, printed-machined (MSF: 0.15 total)
clr_tight_pm   = 0.075;  // [0:0.025:0.3]
// Loose drop-in, removable for cleaning
clr_dropin     = 0.8;    // [0.4:0.1:1.5]
// Added to the DIAMETER of vertical holes (holes print small)
hole_clr       = 0.2;    // [0:0.05:0.5]

/* [Minimum features] */
// MSF minimum wall, mm
min_wall       = 1.6;
// Four perimeters: 1.8 mm, solid at any slicer setting
struct_wall    = 4 * ext_w;
// Base of flat parts, mm
min_base       = 2.0;
// Handled protrusions, both directions, mm
min_handle     = 2.4;
// Vertical hole diameter, mm
min_hole_v     = 1.5;
// Pin diameter, mm
min_pin_d      = 1.8;
// Avoid bridges; hard limit if unavoidable, mm
max_bridge     = 10;
// Degrees from vertical (60 only where the brief allows it)
max_overhang   = 45;
// Degrees, float32 STL rounding on exact 45° faces
overhang_tol   = 0.05;
max_part       = [200, 200, 200];
// Print bed of the MSF kit printer (Original Prusa MK4S), mm — print plates must fit
bed_size       = [250, 210];

/* [Edges] */
// Elephant's foot chamfer at the bed, mm
chamfer_bottom = 0.4;    // [0.3:0.1:0.6]
// Exposed top edges on walls of 3 mm and more, mm; thinner walls use top_chamfer(t)
chamfer_top    = 0.8;    // [0.6:0.1:1.0]
// Internal concave corners (IPC), mm
fillet_min     = 1.0;
// Vertical edge radius at the plate, closed corners, mm
base_corner_r  = 4;

/* [Hardware — general] */
// Material around bolt holes (four to five perimeters), mm
bolt_wall      = 2.5;
// Modelled threads only above this diameter ...
min_thread_d   = 10;
// ... and this pitch
min_thread_p   = 1.5;
// Hole for tapping (Hydra)
tap_factor     = 0.90;
// Hole for a self-tapping screw (Hydra)
selftap_factor = 0.96;
// Hole for a heat-set insert (Hydra) — or the insert maker's value
insert_factor  = 0.98;

/* [Drainage and adhesion] */
// Drainage hole in closed floors, mm, 0 = none (blind sockets >= 2)
drain_d        = 6;      // [0:1:12]
// Built-in brim ears for tall or narrow parts, mm, 0 = none
brim_ear_d     = 0;      // [0:1:15]
// Brim ear thickness: two layers, mm
brim_ear_t     = 0.4;

/* [Text — non-clinical items only] */
font           = "Liberation Sans:style=Bold";
// Letter height, mm (MSF > 6 mm); training set used size 5 (4.8 mm caps)
text_size_min  = 6;
// Emboss / deboss depth, mm
text_depth     = 0.8;    // [0.6:0.1:1.0]

/* [Colour bands — single extruder, manual changes] */
// Colour band base, mm
band_base      = 2.0;
// 0.6 mm per colour
band_min       = 3 * layer_h;

/* [NFC pocket — larger non-clinical items only] */
nfc_pocket     = [19, 19, 1];

/* [Resolution] */
// Segments in preview (F5)
fn_preview     = 32;     // [16:8:64]
// Segments for export (F6 / command line)
fn_export      = 96;     // [48:8:180]
$fn = $preview ? fn_preview : fn_export;

/* [Hidden] */
EPS = 0.01;              // boolean overlap to avoid coincident faces (see boolean hygiene)
assert(version_num() >= 20210100, "OpenSCAD 2021.01 or newer is required");

// ---------------------------------------------------------------- edge rule ----------------------------
// Top-edge chamfer for a wall of thickness t: chamfer_top on walls of 3 mm and more, (t - 1) / 2 on thinner
// walls, so at least 1 mm of the top stays flat and the wall under the chamfer keeps its minimum.
function top_chamfer(t) = min(chamfer_top, max(0, (t - 1) / 2));

// ---------------------------------------------------------------- MSF 3D printing kit hardware ---------
// Stainless steel, in every kit: socket-head bolts DIN 912 M3 x 20/30/40/50 and M6 x 20/30/40/50/60;
// washers DIN 125A M3 (3.2) and M6 (6.4); self-locking nuts DIN 985 M3 and M6; nuts DIN 934 M3 and M6.
// Use kit hardware first. Anything else is listed in the README with its exact standard, size, length and
// material, local alternatives and where it can be taken from (references/design-rules.md §5.4).
// All functions take the metric size m = 3 or 6 and return undef for anything else.
kit_sizes = [3, 6];
function kit_has(m)       = m == 3 || m == 6;
function kit_lengths(m)   = m == 3 ? [20, 30, 40, 50] : m == 6 ? [20, 30, 40, 50, 60] : undef;   // DIN 912
function kit_pitch(m)     = m == 3 ? 0.5 : m == 6 ? 1.0 : undef;                                   // coarse thread
function kit_clear_d(m)   = m == 3 ? 3.4 : m == 6 ? 6.6 : undef;    // ISO 273 medium clearance hole (add hole_clr when printed vertical)
function kit_head_d(m)    = m == 3 ? 5.5 : m == 6 ? 10.0 : undef;   // DIN 912 head diameter
function kit_head_h(m)    = m == 3 ? 3.0 : m == 6 ? 6.0 : undef;    // DIN 912 head height
function kit_cbore_d(m)   = m == 3 ? 6.5 : m == 6 ? 11.0 : undef;   // counterbore for the head (DIN 974-1)
function kit_key(m)       = m == 3 ? 2.5 : m == 6 ? 5.0 : undef;    // hex key size
function kit_nut_af(m)    = m == 3 ? 5.5 : m == 6 ? 10.0 : undef;   // DIN 934 / DIN 985 across flats
function kit_nut_h(m)     = m == 3 ? 2.4 : m == 6 ? 5.0 : undef;    // DIN 934 nut height
function kit_nyloc_h(m)   = m == 3 ? 4.0 : m == 6 ? 6.0 : undef;    // DIN 985 self-locking nut height
function kit_washer_d(m)  = m == 3 ? 7.0 : m == 6 ? 12.0 : undef;   // DIN 125A outer diameter
function kit_washer_h(m)  = m == 3 ? 0.5 : m == 6 ? 1.6 : undef;    // DIN 125A thickness

// Shortest kit bolt for a clamped stack of `grip` mm (printed part + board or other part), with `washers`
// washers and a self-locking (nyloc = true) or plain nut, and at least 2 threads past the nut.
// Returns 0 when no kit bolt is long enough — then a local bolt of kit_bolt_need(...) mm is needed.
function kit_bolt_need(m, grip, washers = 2, nyloc = true) =
    grip + washers * kit_washer_h(m) + (nyloc ? kit_nyloc_h(m) : kit_nut_h(m)) + 2 * kit_pitch(m);
function kit_bolt_for(m, grip, washers = 2, nyloc = true) =
    let(need = kit_bolt_need(m, grip, washers, nyloc), fits = [for (l = kit_lengths(m)) if (l >= need) l])
    len(fits) > 0 ? fits[0] : 0;
