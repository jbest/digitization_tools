import argparse
from hashlib import md5
import uuid
import glob
from datetime import datetime, date, time
from pyzbar.pyzbar import decode
from PIL import Image

#TODO add accepted barcode types
#TODO add accepted barcode string patterns

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
ap.add_argument("-s", "--source", required=True, help="Path to the directory that contains the images to be analyzed.")
ap.add_argument("-m", "--models", required=False, help="Path to the model file for folder identification through histogram analysis.")
#ap.add_argument("-m", "--model", required = True,
#    help = "Path to location of generated model file.")
args = vars(ap.parse_args())

#TODO record time start of analysis
#iterate JPG file list passed from args
for imagePath in glob.glob(args["source"] + "/*.JPG"):
    scan_start_time = datetime.now()
    print(scan_start_time)
    # get filename and use as the model name
    #k = imagePath[imagePath.rfind("/") + 1:]
    print(imagePath)
    #generate MD5 hash
    print(md5hash(imagePath))
    #generate UUID for JPG image
    print(uuid.uuid4())
    # check exist of archive file
    # print archive filepath
    # read barcodes from JPG
    barcodes = decode(Image.open(imagePath))
    if len(barcodes) > 0:
        print(barcodes)
    else:
        print('No barcodes found')
        # compare to folder models
        # save matching models, ranked
        # generate suggested filename? Or should that be done in rename script?
        if args["models"] is None:
            print('No model file provided. No histogram analysis done.')
        else:
            print('TODO: analyze histogram')
            # read model file, make sure it exists
        # if no models provided, or no match, set new filename to a default
    # TODO record scan finish time
    scan_end_time = datetime.now()
    print(scan_end_time)
    # TODO report analysis progress and ETA
    #log JPG data
    #log CR2 data
    #write to DB?


