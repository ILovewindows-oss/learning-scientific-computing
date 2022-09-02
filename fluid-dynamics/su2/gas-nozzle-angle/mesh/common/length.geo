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
no_nodes = 1.0 / SIZE;

// Compute number of nodes over lines.
NH1 = 1 + HL1 * no_nodes;
NH2 = 1 + HL2 * no_nodes;
NH3 = 1 + HL3 * no_nodes;
NH4 = 1 + HL4 * no_nodes;
NH5 = 1 + 500;

NV1 = 1 + VL1 * no_nodes;
NV2 = 1 + VL2 * no_nodes;
NV3 = 1 + VL3 * no_nodes;
NV4 = 1 + VL4 * no_nodes;
NV5 = 1 + VL5 * no_nodes;

// ************************************************************* //
//                       REPORTING CHECK                         //
// ************************************************************* //

Printf("HL1 = %.8f, NP = %.0f", HL1, NH1);
Printf("HL2 = %.8f, NP = %.0f", HL2, NH2);
Printf("HL3 = %.8f, NP = %.0f", HL3, NH3);
Printf("HL4 = %.8f, NP = %.0f", HL4, NH4);
Printf("VL1 = %.8f, NP = %.0f", VL1, NV1);
Printf("VL2 = %.8f, NP = %.0f", VL2, NV2);
Printf("VL3 = %.8f, NP = %.0f", VL3, NV3);
Printf("VL4 = %.8f, NP = %.0f", VL4, NV4);
Printf("VL5 = %.8f, NP = %.0f", VL5, NV5);
