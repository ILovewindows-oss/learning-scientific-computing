// ************************************************************* //
//                         BURNER NOZZLE                         //
// ************************************************************* //

// Domain (1) or nozzle (0) ?
DOMAIN = 1;

// Characteristic mesh size [m].
SIZE = 0.0002;

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
    67,89,111,133,155
};
Physical Surface("outlet") = {
    385,389,411,433,437
};
Physical Surface("walls") = {
    55,59,165,169,253,319,151,239,305,371
};
Physical Surface("front") = {
    1,2,3,4,5,6,7,8,9,10,11,12,13,14,15
};
Physical Surface("back") = {
    68,90,112,134,156,178,200,222,
    244,266,288,310,332,354,376
};
Physical Surface("front_outlet") = {
    16,17,18
};
Physical Surface("back_outlet") = {
    398,420,442
};
Physical Volume("internal") = {
    1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18
};