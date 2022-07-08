# -*- coding: utf-8 -*-
import KratosMultiphysics as km
from KratosMultiphysics.\
    StructuralMechanicsApplication.\
        structural_mechanics_analysis import StructuralMechanicsAnalysis

if __name__ == "__main__":
    with open("data/parameters.json") as fp:
        parameters = km.Parameters(fp.read())

    model = km.Model()
    simulation = StructuralMechanicsAnalysis(model, parameters)
    simulation.Run()
