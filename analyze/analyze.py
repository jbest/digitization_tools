import argparse
from hashlib import md5
import uuid
#import glob


def md5hash(fname):
	# from https://stackoverflow.com/questions/3431825/generating-an-md5-checksum-of-a-file
	# using this approach to ensure larger files can be read into memory
    #hash_md5 = hashlib.md5()
    hash_md5 = md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


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
    #generate MD5 hash
    print (md5hash(imagePath))
    #generate UUID for JPG image
    print (uuid.uuid4())
    # check exist of archive file
    # print archive filepath
    # generate md5 of file
    # generate UUID




#read barcode(s)
#if no barcode, compare to folder models
#log JPG data
#log CR2 data
#write to DB?
