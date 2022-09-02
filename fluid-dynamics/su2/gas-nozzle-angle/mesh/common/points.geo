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

// These are specific for extended domains.
If (DOMAIN == 1)
    //
    Point(26) = {x06, y13, 0.0};
    Point(27) = {x06, y14, 0.0};
    Point(28) = {x06, y16, 0.0};
    Point(29) = {x06, y15, 0.0};
EndIf
