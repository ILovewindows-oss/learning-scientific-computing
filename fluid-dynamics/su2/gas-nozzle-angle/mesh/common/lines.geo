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

// These are specific for extended domains.
If (DOMAIN == 1)
    //
    Line(40) = { 7, 26};
    Line(41) = {26, 27};
    Line(42) = {27, 8};
    Line(43) = {27, 28};
    Line(44) = {28,  9};
    Line(45) = {28, 29};
    Line(46) = {29, 10};
EndIf
