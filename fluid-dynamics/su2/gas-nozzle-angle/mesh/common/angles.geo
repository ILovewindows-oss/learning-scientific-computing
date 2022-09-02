// ************************************************************* //
//                   ANGLES AND SLOPE LENGTHS                    //
// ************************************************************* //

// Conversion of degrees to radians.
DEG2RAD = Pi / 180.0;

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
