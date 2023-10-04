# Enbios 2

This a ground up new implementation of enbios.

Compared to the original version of enbios, this version is more flexible does not make it's own LCA calculations, but
uses brightway2 for that.

The main functionality of enbios2 is currently to run experiments, which are described a set of (brightway) activities a
set of methods and a set of scenarios, which contain demand for the given activities.

In addition to get the results of the scenarios in the dendrogram (....) the user can also define a hierarchy, which
contains the activities at the bottom.

## Installation

Go into the enbios2 directory and create a new virtual environment (with pip or conda) of **python 3.9** or higher.

`conda create --name enbios2 python=3.9` or `python3.9 -m venv venv`

Activate the environment with `conda activate enbios2` or `source venv/bin/activate`

Then install the dependencies with
`pip install .` or `python3 -m pip install .`


# What is ENBIOS
ENBIOS (Environmental and Bioeconomic System Analysis) is an assessment framework designed for the assessment of the **environmental impacts and resource use of energy pathways resulting from energy system optimization models (ESOMs)**.

It  integrates Life Cycle Assessment (LCA) and Social Metabolism Assessment using the Multi-Scale Integrated Assessment of Socio-Ecosystem Metabolism (MuSIASEM). It has been been co-designed with decision makers and energy modellers.

The related python package [`enbios`](https://pypi.org/project/enbios/) takes data on energy system design and impact assessment methods to return a characterization matrix filled with bioeconomic and environmental indicators.  

More information on the roots of the framework and version 1 of the software can be found in [Deliverable 2.2]() of the [SENTINEL](https://sentinel.energy) project. Curently, we have upgraded to  version 2 of the software using Brightway2 for LCA analysis and inventory. Samples can be consulted in [deliverable 2.2](https://zenodo.org/record/7994038) of the [SEEDS](https://seeds-project.org/) project

### Data inputs
- Data on electricity production and power capacity from an energy model
    -Inputs from EuroCalliope model are accepted as is.
    - We are currently working in the integration with the TIMES model for the project LIVEN.  
- LCA inventories in .spold format
- Methods of analysis

### Outputs 
For each energy function and technology:
- Environmental impact indicators from the most used LCIA methods (Recipe2016, CML, AWARE, etc.)
- Environmental externalization rates
- Raw Material Recycling rates and Supply risk


### Features

- Integration of LCA and MuSIASEM evaluation methods
- Import of .spold LCA inventory data to a multi-level tree-like setting
- Library of impact assessment methods based on LCIA
- New impact assessment methods developed for raw materials and circularity
- Consideration of externalized environmental impacts
- Takes data from the friendly-data package (other formats under development)
- High level methods to quickly obtain/refresh analyses



## People


* [Ramin Soleymani](https://es.linkedin.com/in/ramin-soleymani-4703b17).  -[ICTA-UAB](https://www.uab.cat/icta/) 
* [Miquel Sierra Montoya](https://portalrecerca.uab.cat/en/persons/miquel-sierra-i-montoya).  -[ICTA-UAB](https://www.uab.cat/icta/) 
* [Alexander de Tomás](https://www.linkedin.com/in/alexander-de-tom%C3%A1s-pascual-a85348185/).  -[ICTA-UAB](https://www.uab.cat/icta/) 
* [Cristina Madrid-Lopez](https://portalrecerca.uab.cat/en/persons/cristina-madrid-lopez-3). - [ICTA-UAB](https://www.uab.cat/icta/) 

## Contact

- For questions about the enbios framework, please contact [cristina.madrid@uab.cat](mailto:cristina.madrid@uab.cat).


## Acknowledgements
 ENBIOS is developed by the [LIVENlab](https://livenlab.org/), a research lab of the the [SosteniPra](https://www.sostenipra.cat/) Research group, at [ICTA-UAB](https://www.uab.cat/icta/).
 

The first verion was built in collaboration with the Technical Institute of the Canary Islands ([ITC](https://www.itccanarias.org/web/es/)) and based on the Nexus Information System developed within the Horizon 2020 project [MAGIC-nexus](https://magic-nexus.eu/) and the LCA-MuSIASEM integration protocol developed in the Marie Curie project [IANEX](https://cordis.europa.eu/project/id/623593). This early development was funded by wthe Horizon 2020 project Sustainable Energy Transitions Laboratory ([SENTINEL](https://sentinel.energy>), GA 837089).

The second version of `enbios` is in development with funds from the Spanish Research Agency  (AEI) and the European Comission (CINEA):

* [SEEDS](https://seeds-project.org/) project with AEI grant PCI2020-120710-2 funds the ENBIOS 2 build based on Brightway framework, adding inventory manipulation to match the mixes of the energy scenarios
* LIVEN project with AEI grant PID2020-119565RJ-I00 funds the regionalization and conection with the TIMES energy model
* [JUSTWIND4ALL](https://justwind4all.eu/) project with Horizon Europe grant 101083936 funds the development of a higher resolution module for wind energy assessment, including new wind-specific holistic assessment methods.
