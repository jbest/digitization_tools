import argparse
import glob
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
for imagePath in glob.glob(args["dataset"] + "/*.jpg"):
    # get filename and use as the model name
    # TODO change model name to file basename
    k = imagePath[imagePath.rfind("/") + 1:]
    image = cv2.imread(imagePath)
    histogram = features.describe(image)
    models[k] = histogram

f = open(model_path, "wb")
f.write(pickle.dumps(models))
f.write(pickle.dump(models))
f.close()

print ('Model file written:', model_path)
