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

// These are specific for extended domains.
If (DOMAIN == 1)
    //
    Line Loop(16) = { 40,  41,  42,  -7};
    Line Loop(17) = {-42,  43,  44,  -8};
    Line Loop(18) = {-44,  45,  46,  -9};

    Plane Surface(16) = {16};
    Plane Surface(17) = {17};
    Plane Surface(18) = {18};
EndIf
