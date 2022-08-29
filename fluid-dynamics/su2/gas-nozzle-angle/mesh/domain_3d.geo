// ************************************************************* //
//                         BURNER NOZZLE                         //
// ************************************************************* //

// Characteristic mesh size [m].
SIZE = 0.0003;

// Refining factor dividing SIZE.
REFINEMENT = 1;

// Conversion of degrees to radians.
DEG2RAD = Pi / 180.0;

// ************************************************************* //
//                   ANGLES AND SLOPE LENGTHS                    //
// ************************************************************* //

// Angle of attack for inner outlet.
theta1 = 20.0 * DEG2RAD;

// Angle of exit for outer outlet.
theta2 = 45.0 * DEG2RAD;

// Angle of attack for outer outlet.
theta3 = 106.19 * DEG2RAD;
theta4 = Pi - theta3 - theta2;

// Length of inner outlet plane.
slope1 = 0.01535 + 0.0157498;

// Length of outer outlet plane.
slope2 = 0.029881;

// Length of attack plane of outer outlet.
slope3 =  0.0078416;

// Length of free volume extension of noozle.
slope4 = 0.5;

// ************************************************************* //
//                        X-COORDINATES                          //
// ************************************************************* //

// First step coordinate.
x00 = 0.0340000;

// Second step coordinate.
x01 = x00 + 0.0057757;

// Outlet coordinate.
x02 = x01 + slope1 * Cos(theta1);

// Top indentation coordinate.
x03 = x02 - slope2 * Cos(theta2);

// Transition to flat top wall.
x04 = x03 - slope3 * Cos(theta4);

// Intermediate point to smooth mesh.
x05 = 0.5 * (x01 + x04);

//
x06 = x02 + slope4 * Cos(theta1 + Pi/12);

// ************************************************************* //
//                        Y-COORDINATES                          //
// ************************************************************* //

// Height of first step.
y00 = 0.001725;

// Height of second step.
y01 = y00 + 0.0005;

// Lower position of outlet.
y02 = y01 + slope1 * Sin(theta1);

// Top position of outlet.
y03 = y02 + 0.0193632;

// Position of top indentation.
y04 = y03 - slope2 * Sin(theta2);

// Height of top flat wall.
y05 = y04 + slope3 * Sin(theta4);

// Position of BL projection in flat zone.
y06 = y01 + 0.0010;

// Position of lower BL over outlet.
y07 = y02 + 0.0010;

// Position of projection in flat zone.
y08 = y05 - 0.0010;

// Position of BL below indentation.
y09 = y04 - 0.0010;

// Position of upper BL over outlet.
y10 = y03 - 0.0010;

// Position of third slice.
y11 = y01 + (x03 - x01) * Tan(theta1);

// Position of BL over lower part of third slice.
y12 = y06 + (x03 - x01) * Tan(theta1) * 0.9;

//
y13 = y02 + slope4 * Sin(theta1 - Pi/8);

//
y14 = y13 + 0.050;

//
y15 = y03 + slope4 * Sin(theta1 + Pi/12);

//
y16 = y15 - 0.050; 

// ************************************************************* //
//                      LENGTHS AND NODES                        //
// ************************************************************* //

// Horizontal lengths.
HL1 = x00;
HL2 = x01 - x00;
HL3 = x03 - x01;
HL4 = x02 - x03;
HL5 = slope4;

// Vertical lengths.
VL1 = y00;
VL2 = y01 - y00;
VL3 = y06 - y01;
VL4 = y09 - y12;
VL5 = y05 - y08;

// Scaling factor.
no_nodes = REFINEMENT / SIZE;

// Compute number of nodes over lines.
NH1 = 1 + HL1 * no_nodes;
NH2 = 1 + HL2 * no_nodes;
NH3 = 1 + HL3 * no_nodes;
NH4 = 1 + HL4 * no_nodes;
NH5 = 1 + 200;

NV1 = 1 + VL1 * no_nodes;
NV2 = 1 + VL2 * no_nodes;
NV3 = 1 + VL3 * no_nodes;
NV4 = 1 + VL4 * no_nodes;
NV5 = 1 + VL5 * no_nodes;

// ************************************************************* //
//                            POINTS                             //
// ************************************************************* //

// Create points for outer shape.
Point(1)  = {0.0, 0.0, 0.0};
Point(2)  = {x00, 0.0, 0.0};
Point(3)  = {x00, y00, 0.0};
Point(4)  = {x01, y00, 0.0};
Point(5)  = {x01, y01, 0.0};
Point(6)  = {x03, y11, 0.0};
Point(7)  = {x02, y02, 0.0};
Point(8)  = {x02, y07, 0.0};
Point(9)  = {x02, y10, 0.0};
Point(10) = {x02, y03, 0.0};
Point(11) = {x03, y04, 0.0};
Point(12) = {x04, y05, 0.0};
Point(13) = {x00, y05, 0.0};
Point(14) = {0.0, y05, 0.0};
Point(15) = {0.0, y08, 0.0};
Point(16) = {0.0, y06, 0.0};
Point(17) = {0.0, y01, 0.0};
Point(18) = {0.0, y00, 0.0};

// First vertical slice.
Point(19) = {x00, y01, 0.0};
Point(20) = {x00, y06, 0.0};
Point(21) = {x00, y08, 0.0};

// Second vertical slice.
Point(22) = {x05, y06, 0.0};
Point(23) = {x05, y08, 0.0};

// Third vertical slice.
Point(24) = {x03, y12, 0.0};
Point(25) = {x03, y09, 0.0};

//
Point(26) = {x06, y13, 0.0};
Point(27) = {x06, y14, 0.0};
Point(28) = {x06, y16, 0.0};
Point(29) = {x06, y15, 0.0};

// ************************************************************* //
//                            LINES                              //
// ************************************************************* //

// Outer domain envelope.
Line(1)  = { 1,  2};
Line(2)  = { 2,  3};
Line(3)  = { 3,  4};
Line(4)  = { 4,  5};
Line(5)  = { 5,  6};
Line(6)  = { 6,  7};
Line(7)  = { 7,  8};
Line(8)  = { 8,  9};
Line(9)  = { 9, 10};
Line(10) = {10, 11};
Line(11) = {11, 12};
Line(12) = {12, 13};
Line(13) = {13, 14};
Line(14) = {14, 15};
Line(15) = {15, 16};
Line(16) = {16, 17};
Line(17) = {17, 18};
Line(18) = {18,  1};

// First vertical slice.
Line(19) = { 3, 19};
Line(20) = {19, 20};
Line(21) = {20, 21};
Line(22) = {21, 13};

// Second vertical slice.
Line(23) = { 5, 22};
Line(24) = {22, 23};
Line(25) = {23, 12};

// Third vertical slice.
Line(26) = { 6, 24};
Line(27) = {24, 25};
Line(28) = {25, 11};

// First horizontal slice.
Line(29) = { 3, 18};

// Second horizontal slice.
Line(30) = { 5, 19};
Line(31) = {19, 17};

// Third horizontal slice.
Line(32) = { 8, 24};
Line(33) = {24, 22};
Line(34) = {22, 20};
Line(35) = {20, 16};

// Fourth horizontal slice.
Line(36) = { 9, 25};
Line(37) = {25, 23};
Line(38) = {23, 21};
Line(39) = {21, 15};

//
Line(40) = { 7, 26};
Line(41) = {26, 27};
Line(42) = {27, 8};
Line(43) = {27, 28};
Line(44) = {28,  9};
Line(45) = {28, 29};
Line(46) = {29, 10};

// ************************************************************* //
//                      LOOPS AND SURFACES                       //
// ************************************************************* //

// First vertical slice.
Line Loop(1) = {  1,   2,  29,  18};
Line Loop(2) = {-29,  19,  31,  17};
Line Loop(3) = {-31,  20,  35,  16};
Line Loop(4) = {-35,  21,  39,  15};
Line Loop(5) = {-39,  22,  13,  14};

// Second vertical slice.
Line Loop(6) = {  3,   4,  30, -19};
Line Loop(7) = {-30,  23,  34, -20};
Line Loop(8) = {-34,  24,  38, -21};
Line Loop(9) = {-38,  25,  12, -22};

// Second vertical slice.
Line Loop(10) = {  5,  26,  33, -23};
Line Loop(11) = {-33,  27,  37, -24};
Line Loop(12) = {-37,  28,  11, -25};

// Third vertical slice.
Line Loop(13) = {  6,   7,  32, -26};
Line Loop(14) = {-32,   8,  36, -27};
Line Loop(15) = {-36,   9,  10, -28};

//
Line Loop(16) = { 40,  41,  42,  -7};
Line Loop(17) = {-42,  43,  44,  -8};
Line Loop(18) = {-44,  45,  46,  -9};

// Create surfaces from loops.
Plane Surface(1)  = {1};
Plane Surface(2)  = {2};
Plane Surface(3)  = {3};
Plane Surface(4)  = {4};
Plane Surface(5)  = {5};
Plane Surface(6)  = {6};
Plane Surface(7)  = {7};
Plane Surface(8)  = {8};
Plane Surface(9)  = {9};
Plane Surface(10) = {10};
Plane Surface(11) = {11};
Plane Surface(12) = {12};
Plane Surface(13) = {13};
Plane Surface(14) = {14};
Plane Surface(15) = {15};
Plane Surface(16) = {16};
Plane Surface(17) = {17};
Plane Surface(18) = {18};

// ************************************************************* //
//                       REPORTING CHECK                         //
// ************************************************************* //

Printf("HL1 = %.8f, NP = %.0f", HL1, NH1);
Printf("HL2 = %.8f, NP = %.0f", HL2, NH2);
Printf("HL3 = %.8f, NP = %.0f", HL3, NH3);
Printf("HL4 = %.8f, NP = %.0f", HL4, NH4);
Printf("HL5 = %.8f, NP = %.0f", HL5, NH5);
Printf("VL1 = %.8f, NP = %.0f", VL1, NV1);
Printf("VL2 = %.8f, NP = %.0f", VL2, NV2);
Printf("VL3 = %.8f, NP = %.0f", VL3, NV3);
Printf("VL4 = %.8f, NP = %.0f", VL4, NV4);
Printf("VL5 = %.8f, NP = %.0f", VL5, NV5);

// ************************************************************* //
//                       MESH STRUCTURING                        //
// ************************************************************* //

// Horizontal discretization (structured).
Transfinite Line {1,-29,-31,-35,-39,13} = NH1 Using Progression 1.00;
Transfinite Line {3,-30,-34,-38,12}     = NH2 Using Progression 1.00;
Transfinite Line {5,-33,-37,11}         = NH3 Using Progression 1.00;
Transfinite Line {6,-36,-32,10}         = NH4 Using Progression 1.00;
Transfinite Line {-40,42,44,46}         = NH5 Using Progression 0.98;

// Vertical discretization (structured).
Transfinite Line {2,-18}                = NV1 Using Progression 1.00;
Transfinite Line {4,19,-17}             = NV2 Using Progression 1.00;
Transfinite Line {7,26}                 = NV3 Using Progression 1.00;
Transfinite Line {23,20,-16,41}         = NV3 Using Progression 1.00;
Transfinite Line {8,27,24,21,-15,43}    = NV4 Using Progression 1.00;
Transfinite Line {9,28,25,22,-14,45}    = NV5 Using Progression 1.00;

// Recombine to force restructuring.
Transfinite Surface {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18};
Recombine Surface   {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18};

// ************************************************************* //
//                       MESH EXTRUSION                          //
// ************************************************************* //

Extrude {0, 0, 0.006} {
    Surface{1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18};
    Layers{0.006 * no_nodes};
    Recombine;
}

// ************************************************************* //
//                       PHYSICAL NAMES                          //
// ************************************************************* //

Physical Surface("inlet") = {67,89,111,133,155};
Physical Surface("outlet") = {16,17,18,398,420,442,389,
                              411,433,437,385};
Physical Surface("walls") = {1,2,3,4,5,6,7,8,9,10,11,12,13,14,
                             15,68,90,112,134,156,178,200,222,
                             244,266,288,310,332,354,376,55,
                             59,165,169,253,319,151,239,305,371};
Physical Volume("internal") = {1,2,3,4,5,6,7,8,9,10,11,
                               12,13,14,15,16,17,18};
