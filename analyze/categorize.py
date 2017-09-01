import argparse
import glob
import features
import cv2
import pickle

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--images", required = True,
    help = "Path to the directory that contains the images representing model categories.")
ap.add_argument("-m", "--models", required = True,
    help = "Path to location of generated model file.")
args = vars(ap.parse_args())
histograms = {}
print ('Reading images...')
for imagePath in glob.glob(args["images"] + "/*.JPG"):
    k = imagePath[imagePath.rfind("/") + 1:]
    image = cv2.imread(imagePath)
    histogram = features.describe(image)
    histograms[k] = histogram

print ('Image histograms created.')
print ('Loading models...')
# load the models
#models = pickle.loads(open(args["models"]).read())
models = pickle.load(open(args["models"], "rb"))

for image, image_histogram in histograms.items():
    print ('Evaluating:', image)
    #print image_histogram
    candidates = {}

    for model_key, model_histogram in models.items():
        diff = features.chi2_distance(image_histogram, model_histogram)
        candidates[model_key] = diff
    # http://stackoverflow.com/questions/3282823/get-key-with-the-least-value-from-a-dictionary
    # http://stackoverflow.com/a/3282904
    #print min(candidates, key=candidates.get)
    min_value = min(candidates.values())
    min_keys = {}
    # http://stackoverflow.com/questions/9944963/python-get-key-with-the-least-value-from-a-dictionary-but-multiple-minimum-valu
    #min_keys = [k for k in candidates if candidates[k] == min_value]
    print('Min Val:', min_value)
    for k, v in candidates.items():
        print(k, v)
        print(candidates[k])
        if candidates[k] == min_value:
            min_keys[k] = v
    print (min_keys)
