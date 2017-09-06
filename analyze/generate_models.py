import argparse
import glob
import os
import features
import cv2
import pickle

ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required = True,
    help = "Path to the directory that contains the images representing model categories.")
ap.add_argument("-m", "--model", required = True,
    help = "Path to location of generated model file.")
args = vars(ap.parse_args())

model_path = args["model"]
models = {}
print('Generating models...')
for image_path in glob.glob(args["dataset"] + "/*.jpg"):
    basename = os.path.basename(image_path)
    file_name, file_extension = os.path.splitext(basename)
    image = cv2.imread(image_path)
    histogram = features.describe(image)
    #TODO prompt user to enter name for model
    models[file_name] = histogram

f = open(model_path, "wb")
f.write(pickle.dumps(models))
f.close()

print ('Model file written:', model_path)
