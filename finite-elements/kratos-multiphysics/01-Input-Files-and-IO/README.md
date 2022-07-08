# Input Files and IO

A basic Kratos Multiphyics case is constructed by and script and its data files. Here, for a specific structural mechanics case, one is expected to find at least:

- [Settings for simulation](data/parameters.json):simulation parameters in convenient JSON format introduced [here](https://github.com/KratosMultiphysics/Kratos/wiki/Python-Script-Tutorial:-Reading-ProjectParameters) and further described [here](https://github.com/KratosMultiphysics/Kratos/wiki/How-to-write-a-JSON-configuration-file).

- [Material properties](data/materials.json): material properties as described in settings (respecting relative path from runner script).

- [Model part information](data/high_rise_building_csm.mdpa): this is a Kratos-specific format used to provide the numerical mesh. More about it and conversion methods can be found [here](https://github.com/KratosMultiphysics/Kratos/wiki/Input-data).

- [Runner script](run.py): basically loads parameters, creates model, and calls specified physics running module.

Simulation is run through `python run.py`. Here and in the following tutorials, [GiD](https://www.gidsimulation.com/) is not supported and only VTK outputs are generated.
