import Rhino
import rhinoscriptsyntax as rs
import myutil
import os
from constModu import *

rs.Command("_-SelAll")
rs.Command("Delete")

Grasshopper = Rhino.RhinoApp.GetPlugInObject("Grasshopper")
Grasshopper.DisableSolver()
Grasshopper.OpenDocument(work_dir + "voro.gh")
Grasshopper.AssignDataToParameter("StressPath", initStress.replace('/', "\\"))
brepobj = myutil.importfile(modelstp.replace('/', "\\"))
Grasshopper.AssignDataToParameter("InputBrep", brepobj)
Grasshopper.AssignDataToParameter("vorocnt", vorocnt)
Grasshopper.EnableSolver()
