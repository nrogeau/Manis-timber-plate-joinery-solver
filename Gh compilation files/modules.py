"""Get modules from model."""

from ghpythonlib.componentbase import dotnetcompiledcomponent as component
import Grasshopper, GhPython
import System
import rhinoscriptsyntax as rs
import copy
from Grasshopper import DataTree
from Grasshopper.Kernel.Data import GH_Path

__author__ = "Nicolas Rogeau"
__laboratory__ = "IBOIS, Laboratory for Timber Construction" 
__university__ = "EPFL, Ecole Polytechnique Federale de Lausanne"
__funding__ = "NCCR Digital Fabrication, ETH Zurich"
__version__ = "2021.09"

class MyComponent(component):
    def __new__(cls):
        instance = Grasshopper.Kernel.GH_Component.__new__(cls,
            "Get Modules", "Modules", """Get modules from model.""", "Manis", "Assembly")
        return instance
    
    def get_ComponentGuid(self):
        return System.Guid("8b1633ef-c5f8-4fd7-b75c-d757d5131433")
    
    def SetUpParam(self, p, name, nickname, description):
        p.Name = name
        p.NickName = nickname
        p.Description = description
        p.Optional = True
    
    def RegisterInputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "model", "model", "Plate model.")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Integer()
        self.SetUpParam(p, "module_id", "module_id", "(Optional) ID of the module. If none is provided, all modules will be retrieved.")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
    
    def RegisterOutputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "module", "module", "Module(s) inheriting model functions.")
        self.Params.Output.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_String()
        self.SetUpParam(p, "sequence", "sequence", "Sub-sequence of the module.")
        self.Params.Output.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "step", "step", "Tag representing the position of the module in the full assembly sequence. 'M' stands for the final step of the Model.")
        self.Params.Output.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Brep()
        self.SetUpParam(p, "breps", "breps", "Module breps.")
        self.Params.Output.Add(p)
        
    
    def SolveInstance(self, DA):
        p0 = self.marshal.GetInput(DA, 0)
        p1 = self.marshal.GetInput(DA, 1)
        result = self.RunScript(p0, p1)

        if result is not None:
            if not hasattr(result, '__getitem__'):
                self.marshal.SetOutput(result, DA, 0, True)
            else:
                self.marshal.SetOutput(result[0], DA, 0, True)
                self.marshal.SetOutput(result[1], DA, 1, True)
                self.marshal.SetOutput(result[2], DA, 2, True)
                self.marshal.SetOutput(result[3], DA, 3, True)
        
    def get_Internal_Icon_24x24(self):
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAACxIAAAsSAdLdfvwAAADESURBVEhLzZDREYMwDEOZqTN1JmbqTP0JloMhMbFB+ehVdw+TKLYCSynlMSI8OEaDItDw/bwphoMijlsxjAZFQHIrlHq7WnXP8J5uzGBDBK+LpxsM1oOqA/qv7DzIFhRMwMx/7YbcBuwKDZH3ngdERtrEnI2MpImDDXitKwUdQDMRANXbnetWF88WFFQANhisB1UHuK9tPcgWFEyAKTRE3vujgMhIm5izkZE21Xqs/dmG08QrEdDJne0VDXFNvw1ovZyybMNIxM83vg1XAAAAAElFTkSuQmCC"
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

    
    def RunScript(self, model, module_id):
        
        def round_vector(vec, n=3):
            """round x,y,z components of a vector to n decimals"""
            for i in range(len(vec)):
                vec[i] = round(vec[i],n)
            return vec

        def list_to_datatree(raggedList):
            """Python to Grasshopper (from Chen Jingcheng)"""
            rl = raggedList
            result = DataTree[object]()
            for i in range(len(rl)):
                temp = []
                for j in range(len(rl[i])):
                    temp.append(rl[i][j])
                #print(i, " - ",temp)
                path = GH_Path(i)
                result.AddRange(temp, path)
            return result

        module = None
        sequence = None
        step = None
        breps = None
        
        if model:        
            if module_id != None:
                module_id = module_id % len(model.modules)
                module = model.modules[module_id]
                breps = model.modules[module_id].breps
                step = str(model.modules[module_id].step)
                sequence = str(model.modules[module_id].sequence)
                assembly_vectors = []
                for i in range(len(model.modules[module_id].assembly_vectors)):
                    vector = model.modules[module_id].assembly_vectors[i]
                    if vector == "gravity": vector = rs.VectorCreate((0,0,-1),(0,0,0))
                    assembly_vectors.append(round_vector(vector,6))
        
            else:
                module = []
                breps = []
                sequence = []
                step = []
                assembly_vectors = []
                for mod in model.modules:
                    module.append(mod)
                    breps.append(mod.breps)
                    sequence.append(str(mod.sequence))
                    step.append(str(mod.step))
                    sub_assembly_vectors = []
                    for vec in mod.assembly_vectors:
                        if vec == "gravity": vec = rs.VectorCreate((0,0,-1),(0,0,0))
                        sub_assembly_vectors.append(round_vector(vec,6))
                    assembly_vectors.append(sub_assembly_vectors)
                breps = list_to_datatree(breps)
                assembly_vectors = list_to_datatree(assembly_vectors)
        
        return (module, sequence, step, breps)


class AssemblyInfo(GhPython.Assemblies.PythonAssemblyInfo):
    def get_AssemblyName(self):
        return "Modules"
    
    def get_AssemblyDescription(self):
        return """"""

    def get_AssemblyVersion(self):
        return "0.1"

    def get_AuthorName(self):
        return "Nicolas Rogeau"
    
    def get_Id(self):
        return System.Guid("8b84a228-8858-4a01-9624-9af6a0036530")