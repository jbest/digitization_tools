import argparse
import glob

# set up argument parser
ap = argparse.ArgumentParser()
ap.add_argument("-s", "--source", required = True,
    help = "Path to the directory that contains the images to be analyzed.")
#ap.add_argument("-m", "--model", required = True,
#    help = "Path to location of generated model file.")
args = vars(ap.parse_args())

#iterate JPG file list passed from args
for imagePath in glob.glob(args["source"] + "/*.JPG"):
    # get filename and use as the model name
    #k = imagePath[imagePath.rfind("/") + 1:]
    print (imagePath)


#generate MD5
#generate UUID
#read barcode(s)
#if no barcode, compare to folder models
#log JPG data
#log CR2 data
#write to DB?
