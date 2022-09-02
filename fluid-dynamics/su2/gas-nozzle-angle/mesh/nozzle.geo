// ************************************************************* //
//                         BURNER NOZZLE                         //
// ************************************************************* //

// Domain (1) or nozzle (0) ?
DOMAIN = 0;

// Characteristic mesh size [m].
SIZE = 0.0001;

// Common files.
Include "common/angles.geo";
Include "common/coords.geo";
Include "common/length.geo";
Include "common/points.geo";
Include "common/lines.geo";
Include "common/loops.geo";
Include "common/struct.geo";

// ************************************************************* //
//                       PHYSICAL NAMES                          //
// ************************************************************* //

Physical Surface("inlet") = {
    60,82,104,126,148
};
Physical Surface("outlet") = {
    316,338,360
};
Physical Surface("walls") = {
    144,232,298,364,48,52,158,162,246,312
};
Physical Surface("front") = {
    1,2,3,4,5,6,7,8,9,10,11,12,13,14,15
};
Physical Surface("back") = {
    61,83,105,127,149,171,193,215,
    237,259,281,303,325,347,369
};
Physical Volume("internal") = {
    1,2,3,4,5,6,7,8,9,10,11,12,13,14,15
};
