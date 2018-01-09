import rhinoscriptsyntax as rs
import scriptcontext as sc
import Rhino

def importfile(filename):
    commandString = "_-Import " + filename + " _Enter"
    rs.Command(commandString)
    sc.doc=Rhino.RhinoDoc.ActiveDoc
    objs=rs.SelectedObjects()
    rs.UnselectObjects(objs)
    return objs[0]
