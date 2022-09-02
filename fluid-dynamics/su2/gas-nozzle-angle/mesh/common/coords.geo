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
