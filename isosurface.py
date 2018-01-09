#!/usr/bin/env python
from mayavi import mlab
import sys, os
vtkname = sys.argv[1]
src = mlab.pipeline.open(vtkname)
src2 = mlab.pipeline.set_active_attribute(src, point_scalars='T')
iso_surface = mlab.pipeline.iso_surface(src2)
iso_surface.contour.auto_contours = False
iso_surface.contour.contours[0:1] = [0.995]
objname = os.path.splitext(vtkname)[0] + ".obj"
mlab.savefig(objname)
