# -*- coding: utf-8 -*-
import math
import KratosMultiphysics
import KratosMultiphysics.ConvectionDiffusionApplication

from KratosMultiphysics\
    .ConvectionDiffusionApplication\
    .convection_diffusion_analysis import ConvectionDiffusionAnalysis


class GaussianHillWithDiffusionExplicit(ConvectionDiffusionAnalysis):
    """ Problem specification with variable boundary condition. """
    def __init__(self,model,parameters):
        super().__init__(model, parameters)
        self.apply_initial_condition = True

    def ApplyBoundaryConditions(self):
        """ Time-dependent boundary condition. """
        super().ApplyBoundaryConditions()

        if self.apply_initial_condition:
            pars = self.project_parameters

            model_part_name = pars["problem_data"]["model_part_name"]\
                .GetString()

            x0 = 2 / 15
            l = 7 * math.sqrt(2) / 300

            for node in self.model.GetModelPart(model_part_name).Nodes:
                phi_analytical = (5 / 7) * math.exp(-((node.X - x0) / l)**2)
                node.SetSolutionStepValue(
                    KratosMultiphysics.TEMPERATURE, 1, phi_analytical)

                if node.X == 0.0 or node.X == 1.0:
                    node.SetSolutionStepValue(
                        KratosMultiphysics.TEMPERATURE, 0.0)
                    node.SetSolutionStepValue(
                        KratosMultiphysics.TEMPERATURE, 1, 0.0)
                    node.Fix(KratosMultiphysics.TEMPERATURE)

            self.apply_initial_condition = False


if __name__ == "__main__":
    with open("settings/parameters.json") as fp:
        parameters = KratosMultiphysics.Parameters(fp.read())

    model = KratosMultiphysics.Model()
    simulation = GaussianHillWithDiffusionExplicit(model, parameters)
    simulation.Run()
