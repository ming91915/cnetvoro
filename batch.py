import sh
import os
import pandas as pd
import re
from constModu import *

simple = sh.Command("/Users/hepburn/anaconda/lib/python2.7/site-packages/sfepy/script/simple.py")
temp = simple.bake(work_dir + "temperature_analysis.py")
convert_mesh = sh.Command("/Users/hepburn/anaconda/lib/python2.7/site-packages/sfepy/script/convert_mesh.py")
gmsh = sh.Command("/Users/hepburn/Applications/Gmsh/Gmsh.app/Contents/MacOS/gmsh")
isosurface = sh.Command(work_dir + "isosurface.py")
centroids = pd.read_csv(work_dir + modelname + "_centroid.csv", index_col="id")

for f in os.listdir(parts_dir):
    m = re.search('part_(\d{1,2}).stp', f)
    if m:
        ind = int(m.groups()[0])
        if ind not in centroids.index:
            continue
        stpfile = parts_dir + f
        print "processing..." + stpfile
        mshfile = os.path.splitext(stpfile)[0] + ".msh"
        gmsh("-3", "-clscale", "0.1", "-algo", "front3d" ,"-o", mshfile, stpfile)
        # meshfile = os.path.splitext(stpfile)[0] + ".mesh"
        # convert_mesh(mshfile, meshfile)

        c = centroids.loc[ind]
        c = "%f,%f,%f" % (c.x, c.y, c.z)
        vtkfilebase = os.path.splitext(stpfile)[0]
        temp('--define', 'meshname:"%s",c:"%s"' % (mshfile, c), o=vtkfilebase)

        isosurface(vtkfilebase + ".vtk")
