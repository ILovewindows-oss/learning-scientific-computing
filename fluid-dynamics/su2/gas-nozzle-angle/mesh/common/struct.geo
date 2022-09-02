// ************************************************************* //
//                       MESH STRUCTURING                        //
// ************************************************************* //

If (DOMAIN == 0)
    // Horizontal discretization (structured).
    Transfinite Line {1,-29,-31,-35,-39,13} = NH1 Using Progression 1.00;
    Transfinite Line {3,-30,-34,-38,12}     = NH2 Using Progression 1.00;
    Transfinite Line {5,-33,-37,11}         = NH3 Using Progression 1.00;
    Transfinite Line {6,-36,-32,10}         = NH4 Using Progression 1.00;

    // Vertical discretization (structured).
    Transfinite Line {2,-18}                = NV1 Using Progression 1.00;
    Transfinite Line {4,19,-17}             = NV2 Using Progression 1.00;
    Transfinite Line {7,26}                 = NV3 Using Progression 1.00;
    Transfinite Line {23,20,-16}            = NV3 Using Progression 1.00;
    Transfinite Line {8,27,24,21,-15}       = NV4 Using Progression 1.00;
    Transfinite Line {9,28,25,22,-14}       = NV5 Using Progression 1.00;

    // Recombine to force restructuring.
    Transfinite Surface {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15};
    Recombine Surface   {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15};
Else
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
EndIf

// ************************************************************* //
//                       MESH EXTRUSION                          //
// ************************************************************* //

If (DIMS == 2)
    depth = 0.1;
    layers = 1;

    If (DOMAIN == 0)
        Extrude {0, 0, depth} {
            Surface{1,2,3,4,5,6,7,8,9,10,11,12,13,14,15};
            Layers{layers};
            Recombine;
        }
    Else
        Extrude {0, 0, depth} {
            Surface{1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18};
            Layers{layers};
            Recombine;
        }
    EndIf
Else
    depth = 0.006;
    layers = 10;
    // layers = 0.006 * no_nodes;

    If (DOMAIN == 0)
        Extrude {0, 0, depth} {
            Surface{1,2,3,4,5,6,7,8,9,10,11,12,13,14,15};
            Layers{layers};
            Recombine;
        }
    Else
        Extrude {0, 0, depth} {
            Surface{1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18};
            Layers{layers};
            Recombine;
        }
    EndIf
EndIf
