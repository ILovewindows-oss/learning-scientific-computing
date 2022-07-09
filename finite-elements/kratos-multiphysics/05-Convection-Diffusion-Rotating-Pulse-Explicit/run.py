# -*- coding: utf-8 -*-
from dis import dis
import math
import KratosMultiphysics
import KratosMultiphysics.ConvectionDiffusionApplication

from KratosMultiphysics\
    .ConvectionDiffusionApplication\
    .convection_diffusion_analysis import ConvectionDiffusionAnalysis


class RotatingPulse(ConvectionDiffusionAnalysis):
    """ Problem specification with variable boundary condition. """
    def _force(self, t, d):
        """ Forcing factor at instant of time. """
        return math.exp(-t**10) * math.cos(math.pi / 2 * d)
 
    def ApplyBoundaryConditions(self):
        """ Time-dependent boundary condition. """
        super().ApplyBoundaryConditions()

        pars = self.project_parameters

        model_part_name = pars["problem_data"]["model_part_name"]\
            .GetString()
        tstep = pars["solver_settings"]["time_stepping"]["time_step"]\
            .GetDouble()

        for node in self.model.GetModelPart(model_part_name).Nodes:
            convective_velocity = [-node.Y + 0.5, node.X - 0.5, 0.0]
            distance = math.sqrt(node.X**2 + node.Y**2)

            node.SetSolutionStepValue(
                KratosMultiphysics.VELOCITY, convective_velocity)
            node.SetSolutionStepValue(
                KratosMultiphysics.VELOCITY, 1, convective_velocity)
            
            if (distance <= 1):
                forcing_currents = self._force(self.time, distance)
                forcing_previous = self._force(self.time - tstep, distance)
            else:
                forcing_currents = 0
            
            node.SetSolutionStepValue(
                KratosMultiphysics.HEAT_FLUX, 0, forcing_currents)
            node.SetSolutionStepValue(
                KratosMultiphysics.HEAT_FLUX, 1, forcing_previous)


if __name__ == "__main__":
    with open("settings/parameters.json") as fp:
        parameters = KratosMultiphysics.Parameters(fp.read())

    model = KratosMultiphysics.Model()
    simulation = RotatingPulse(model, parameters)
    simulation.Run()
