# -*- coding: utf-8 -*-
import math
import KratosMultiphysics
import KratosMultiphysics.ConvectionDiffusionApplication

from KratosMultiphysics\
    .ConvectionDiffusionApplication\
    .convection_diffusion_analysis import ConvectionDiffusionAnalysis


class GaussianHillExplicit(ConvectionDiffusionAnalysis):
    """ Problem specification with variable boundary condition. """
    def __init__(self,model,parameters):
        super().__init__(model,parameters)
        self.apply_initial_condition = True

    def ApplyBoundaryConditions(self):
        """ Time-dependent boundary condition. """
        super().ApplyBoundaryConditions()

        if self.apply_initial_condition:
            pars = self.project_parameters

            model_part_name = pars["problem_data"]["model_part_name"]\
                .GetString()
            tstep = pars["solver_settings"]["time_stepping"]["time_step"]\
                .GetDouble()

            x0, y0 = 0.0, 0.5
            diffusivity = 0.001
            t = math.pi / 2 + simulation.time - tstep

            for node in self.model.GetModelPart(model_part_name).Nodes:
                x_bar = +x0 * math.cos(t) - y0 * math.sin(t)
                y_bar = -x0 * math.sin(t) + y0 * math.cos(t)
                r2 = (node.X - x_bar)**2 + (node.Y - y_bar)**2

                den = 4 * diffusivity * t
                phi_analytical = math.exp(-r2 / den) / (math.pi * den)
                
                node.SetSolutionStepValue(
                    KratosMultiphysics.TEMPERATURE, 1, phi_analytical)

            self.apply_initial_condition = False


if __name__ == "__main__":
    with open("settings/parameters.json") as fp:
        parameters = KratosMultiphysics.Parameters(fp.read())

    model = KratosMultiphysics.Model()
    simulation = GaussianHillExplicit(model, parameters)
    simulation.Run()
