import os, sys
modelname = "femur"
work_dir = os.environ.get("BeamDir", "/Users/hepburn/Documents/beam/")
tmp_dir = work_dir + "tmp/"
image_dir = work_dir + "images/"
modelstp = work_dir + modelname + ".stp"
initStress = work_dir + modelname + ".csv"
parts_dir = work_dir + modelname + "_parts/"

for dirname in [tmp_dir, image_dir, parts_dir]:
    if not os.path.exists(dirname):
        os.mkdir(dirname)
