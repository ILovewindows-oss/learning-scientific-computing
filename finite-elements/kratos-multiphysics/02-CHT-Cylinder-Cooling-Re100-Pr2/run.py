# -*- coding: utf-8 -*-
import sys
import time
import KratosMultiphysics
import KratosMultiphysics.FluidDynamicsApplication
import KratosMultiphysics.ConvectionDiffusionApplication

from KratosMultiphysics\
    .ConvectionDiffusionApplication\
    .convection_diffusion_analysis import ConvectionDiffusionAnalysis


class ConvectionDiffusionAnalysisWithFlush(ConvectionDiffusionAnalysis):
    """ Add STDOUT flushing to problem analysis for better screen output. """
    def __init__(self,model, project_parameters, flush_frequency=10.0):
        super().__init__(model, project_parameters)

        self.flush_frequency = flush_frequency
        self.last_flush = time.time()

    def FinalizeSolutionStep(self):
        super().FinalizeSolutionStep()

        if self.parallel_type == "OpenMP":
            now = time.time()
            if now - self.last_flush > self.flush_frequency:
                sys.stdout.flush()
                self.last_flush = now


if __name__ == "__main__":
    with open("settings/parameters.json") as fp:
        parameters = KratosMultiphysics.Parameters(fp.read())

    model = KratosMultiphysics.Model()
    simulation = ConvectionDiffusionAnalysisWithFlush(model, parameters)
    simulation.Run()
