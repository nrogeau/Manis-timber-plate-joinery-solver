# Manis -  A collaborative design tool for integrally-attached timber plate structures.

* [Introduction](#introduction)
* [For users](#for-users)
* [For developers](#for-developers)

## Introduction

### Tool purpose
Manis is a grasshopper plugin developed at the laboratory for timber constructions (IBOIS, EPFL) for creating joints between timber panels .
The tool allows:
* generating joints geometry according to topological constraints and assembly sequence
* generating CNC cutting toolpath to automate the fabrication of the plates
* generating robotic trajectories to automate the assembly of the plates

As images are often more powerfull than words, have a look at our [short trailer](https://vimeo.com/635101614) if you didn't see it yet!

### Reference
For research applications, please refer to the following publication. It includes a detailed description of the algorithms behind the code: 
> __Nicolas Rogeau, Pierre Latteur, Yves Weinand, _An integrated design tool for timber plate structures to generate joints geometry, fabrication toolpath, and robot trajectories_, Automation in Construction, Volume 130, October 2021__
> [https://doi.org/10.1016/j.autcon.2021.103875](https://doi.org/10.1016/j.autcon.2021.103875)

## For users

### Plugin installation
1. Download the file `Manis.x.ghpy`.
2. Place the file inside Grasshopper Components folder `C:\Users\yourname\AppData\Roaming\Grasshopper\Libraries` or `Grasshopper -> File -> Special folders -> Components folder`.
3. Verify that the file is unblocked: `Right-click on the file -> Properties -> General -> Unblock`.
4. Restart Rhino and open Grasshopper. There should be a new tab in Grasshopper named Manis.

Note (robotic assembly): To simulate robot trajectories generated by Manis, we rely on the plugin ["Robots"](https://github.com/visose/Robots). The latest release of robots is available [here](https://github.com/visose/Robots/releases). Once the plugin is installed, download the folder "Robots" from Manis repository and place it in your "Documents" folder: `C:\Users\yourname\Documents\Robots`. It contains the xml file and 3D model of our robot at IBOIS, EPFL. It is the one we use in the example file but you can of course use your own robot instead.

Note (structural analysis): To run the structural analysis, we rely on [Compas](https://compas.dev), an open-source framework developed by our colleagues at the NCCR Digital Fabrication to foster collaboration between AEC stakeholders. If you want to use this part of Manis, you will first need to install Compas and the module [Compas_fea](https://compas.dev/compas_fea). You will also need to have a valid license of [Abaqus](https://www.3ds.com/products-services/simulia/products/abaqus/) in order to perform the analysis. Once both are installed, go to `C:\Users\yourname\AppData\Roaming\McNeel\Rhinoceros\7.0\scripts\compas_fea\cad\` and open 'rhino.py'. We need to bring a small change to this file for our Grasshopper component to work. At line 236, replace `mesh = RhinoMesh.from_guid(guid).to_compas()` with those two lines: `mesh = rs.coercerhinoobject(guid)`
and `mesh = RhinoMesh.from_object(mesh).to_compas()`

### Plugin structure
The plugin has 9 different tabs:
* _Adjacency_: where you can get useful data about how the plates of the model are connected. 
* _Assembly_: where you can create your own insertion constraints and access plate modules properties.
* _FEM_: where you can create a simplified model and run a structural analysis using [Compas_fea](https://compas.dev/compas_fea) and [Abaqus](https://www.3ds.com/products-services/simulia/products/abaqus/).
* _Joints_: where you can create different kind of joints between adjacent plates. 
* _Properties_: where you can access the geometric properties of each plate (contour, face, thickness...).
* _Robotics_: where you can generate robotic trajectories and simulate the robotic assembly of the plates using [Robots](https://github.com/visose/Robots) plugin.
* _Solver_: where you can find the component to build the model and other computationally intensive solvers.
* _Transform_: where you can rearrange the plates in the 3D space (for example for fabrication or assembly purposes).
* _Utility_: where you can find other components that couldn't find a place in the other tabs...

### Example file and tutorial
The file `manis_demo.gh` contains some examples showing different applications of the joinery solver.
A video tutorial is also available on IBOIS vimeo channel. The [first part](https://vimeo.com/635110679) focuses on the 3D modeling of the joints and the concept of modular assemblies while [the second part](https://vimeo.com/635112019) covers the generation of CNC toolpath and robot trajectories.

For a general overview of Manis workflow, you can refer to [this video](https://vimeo.com/635127909) in which the solver is applied to a boxed vault of 36 plates.
We also recorded a [detailed explanation](https://vimeo.com/635128815) of the code that is behind the grasshopper component we use to perform the structural analysis of this doubly-curved timber vault. You can test it yourself by downloading the file `manis_annen.gh`

## For developers

### Improving the code
The source code consists of one single python file: `platesjoinery.py`. 
It is not necessary to recompile the Grasshopper plugin when debugging or developing new functions.
Instead, you can test your modifications directly inside a custom Grasshopper python component.
You need to execute the following steps to be able to call the functions from the python file inside the Grasshopper environment: 
1. Download the file `platesjoinery.py`.
2. Place the file inside Rhinoceros IronPython folder `C:\Users\yourname\AppData\Roaming\McNeel\Rhinoceros\7.0\Plug-ins\IronPython\settings\lib`.
3. Verify that the path is correctly specified in Rhino: `Type _EditPythonScript -> Tools -> Options -> Files -> Add to search path (if necessary)`.
4. Restart Rhino and open Grasshopper. You should now be able to import the module `platesjoinery` inside a Grasshopper python component and access its classes and functions.

### Code structure
The source code is split in 4 classes:
* _PlateModel_: The main class of the solver. A plate model instance is created for each new timber plate structures. Adjacencies and insertion vectors are computed during the instanciation of the plate model. This class also containts methods to create timber joints and generate fabrication toolpath.
* _PlateModule_: A sub-class of the plate model to deal with modular assemblies. For each group of plates specified by the user, a new module is created.
* _Plate_: A sub-class of the plate model containing the information about a single element of the structure. An instance of the plate class contains geometric information such as the plate thickness or the plate contours.
* _Toolbox_: A list of methods extending the Rhino framework. 

### Re-compiling a new version of the plugin
Once the modifications brought to the source code have been validated, a new version of the plugin can be generated.

1. Download the folder `Grasshopper compilation files`.
2. Open the file `build.py` in an editor and replace the 5 classes with their new version from the updated source code.
3. If necessary, update the parameters and/or the definition of the plugin components (each file corresponds to a single component of the plugin).
4. In Rhino, run the command `_EditPythonScript` and open the file `main.py`.
5. Update the version number of the plugin in the first argument of the function `clr.CompileModules(" Manis.v1.2.3.ghpy"...`
6. Run the file `main.py`. It will create a file `Manis.v1.2.3.ghpy` in the folder `Grasshopper compilation files`.
7. Move the newly created file to the Grasshopper Components folder `C:\Users\yourname\AppData\Roaming\Grasshopper\Libraries` or `Grasshopper -> File -> Special folders -> Components folder`.
8. Restart Rhino and open Grasshopper. The plugin should be updated.

For further information about how to create a custom grasshopper component with python, you can refer to [this tutorial](https://discourse.mcneel.com/t/tutorial-creating-a-grasshopper-component-with-the-python-ghpy-compiler/38552).
