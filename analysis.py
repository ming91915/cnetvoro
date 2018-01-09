#!/usr/bin/env python
import subprocess
import os
import re
import shutil
from constModu import *

def genVoroByRhion():
    scriptName = work_dir + "genvoro.py"
    rhinoPath = "C:\Program Files\Rhinoceros 5 (64-bit)\System\Rhino.exe"
    scriptCall = "-_RunPythonScript {0}".format(scriptName)
    callScript = '"{0}" /nosplash /runscript="{1}"'.format(rhinoPath, scriptCall)
    subprocess.call(callScript)

def genVoroByScale():
    os.environ["curDir"] = os.getcwd()
    scriptName = work_dir + "scale.py"
    rhinoPath = "C:\Program Files\Rhinoceros 5 (64-bit)\System\Rhino.exe"
    scriptCall = "-_RunPythonScript {0}".format(scriptName)
    callScript = '"{0}" /nosplash /runscript="{1}"'.format(rhinoPath, scriptCall)
    subprocess.call(callScript)

def compMiseByAbaqus(itr=0):
    AbaqusPath=r"C:\SIMULIA\Abaqus\Commands\abaqus.bat"
    scriptCall = work_dir + "abaqus_stress.py"
    callScript = '"{0}" cae noGUI="{1}" -- {2}'.format(AbaqusPath, scriptCall, itr)
    subprocess.call(callScript)
    # FNULL = open(os.devnull, 'w')
    # subprocess.call(callScript, stdout=FNULL, stderr=subprocess.STDOUT)
    print "%d: analysis done." % itr

if __name__ == '__main__':
    genVoroByRhion()
    # compMiseByAbaqus()
    # genVoroByScale()
