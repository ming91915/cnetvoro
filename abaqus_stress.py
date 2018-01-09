#!/usr/bin/env python
# -*- coding: utf-8 -*-

from part import *
from material import *
from section import *
from assembly import *
from step import *
from interaction import *
from load import *
from mesh import *
from job import *
from sketch import *
from visualization import * 

import time
import sys, os
work_dir = os.environ["BeamDir"]
sys.path.append(work_dir)
from constModu import *

skipjob = True

try:
    CNT = int(sys.argv[-1])
except:
    CNT = 0
myModel = mdb.Model(name='Model-%d' % (CNT))
myViewport=session.viewports['Viewport: 1']

print modelstp
step = mdb.openStep(modelstp, scaleFromFile=OFF)
myPart = basePart = myModel.PartFromGeometryFile(name=modelname, geometryFile=step, 
    combine=False, dimensionality=THREE_D, type=DEFORMABLE_BODY)
a = myModel.rootAssembly
myInstance = modelInstance = a.Instance(name=modelname, part=basePart, dependent=ON)

if skipjob:
    porousInstances = []
    stpdir = parts_dir
    porousfiles = [f for f in os.listdir(stpdir) if re.search('voro_\d{1,2}\.stp', f)]
    if len(porousfiles):
        for f in porousfiles:
            step = mdb.openStep(stpdir + f, scaleFromFile=OFF)
            partName = f.split('.')[0]
            p = myModel.PartFromGeometryFile(name=partName, geometryFile=step, combine=False, dimensionality=THREE_D, type=DEFORMABLE_BODY)
            porousInstances.append(a.Instance(name=partName, part=p, dependent=ON))

        myInstance = a.InstanceFromBooleanCut(name='boolean', instanceToBeCut=modelInstance, cuttingInstances=tuple(porousInstances), originalInstances=DELETE)
        myPart = myModel.parts['boolean']

    myViewport.setValues(displayedObject=a)
    myViewport.view.fitView()
    myViewport.assemblyDisplay.geometryOptions.setValues(geometryEdgesInShaded=OFF, geometrySilhouetteEdges=OFF)
    myViewport.viewportAnnotationOptions.setValues(triad=OFF,legend=OFF, title=OFF, state=OFF, annotations=OFF, compass=OFF)
    myViewport.assemblyDisplay.setValues(activeCutName='Y-Plane', viewCut=ON)
    myViewport.assemblyDisplay.viewCuts['Y-Plane'].setValues(showModelAboveCut=True, showModelBelowCut=False)
    myViewport.view.setValues(session.views['Bottom'])
    session.pngOptions.setValues(imageSize=(4096, 2689))
    imagename = image_dir+modelname+'_porous_cut_%d.png' % (CNT)
    while os.path.exists(imagename):
        CNT = CNT + 1
        imagename = image_dir+modelname+'_porous_cut_%d.png' % (CNT)
    session.printToFile(fileName=imagename, format=PNG, canvasObjects=(myViewport, ))

else:
    #创建材料
    mySteel = myModel.Material(name='steel')
    #定义弹性材料属性
    elasticProperties= (2410,0.39)
    mySteel.Elastic(table= (elasticProperties,))

    #创建实体截面
    mySection=myModel.HomogeneousSolidSection(name='section',
    material='steel',thickness=1.0)
    #为部件分配截面属性
    myPart.SectionAssignment(region=(myPart.cells,),sectionName='section')

    #在初始分析步Initial之后创建一个分析步。静力分析步的时间为1.0,初始增量为0.1.
    myModel.StaticStep(name="Step",previous='Initial',timePeriod=1.0,
        initialInc=0.1,description='Load the top of the model.')

    myJob=mdb.Job(name=modelname,model=myModel,description=modelname)
    def writeStress():
        myOdb=session.openOdb(name=modelname+'.odb')
        myInstance = myOdb.rootAssembly.instances[modelname.upper()]

        with open(initStress, 'w') as f:
            f.write("x,y,z,mises\n")
            for elem in myInstance.elements:
                mises=myOdb.steps['Step'].frames[-1].fieldOutputs['S'].getSubset(region=elem,position=CENTROID).values[0].mises
                coors = [myInstance.nodes[ind - 1].coordinates for ind in elem.connectivity]
                x, y, z = zip(*coors)
                l = len(x)
                x, y, z=sum(x)/l,sum(y)/l,sum(z)/l
                f.write("%.4f,%.4f,%.4f,%.4f\n" % (x, y, z, mises))
