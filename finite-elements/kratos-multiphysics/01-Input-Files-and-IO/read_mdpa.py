# -*- coding: utf-8 -*-
import KratosMultiphysics as km

# This will implicitly register `TotalLagrangianElement2D4N`.
import KratosMultiphysics.StructuralMechanicsApplication

model = km.Model()
model_part = model.CreateModelPart("model_part")

# Adding variables BEFORE reading the .mdpa
model_part.AddNodalSolutionStepVariable(km.DISPLACEMENT)

model_part_io = km.ModelPartIO("data/high_rise_building_csm")
model_part_io.ReadModelPart(model_part)

print(model_part_io)
