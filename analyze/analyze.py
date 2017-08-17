import argparse
from hashlib import md5
import uuid
import glob
from datetime import datetime, date
import time
#import date
import os
import platform
from pyzbar.pyzbar import decode
from PIL import Image

# File extensions that are scanned and logged
INPUT_FILE_TYPES = ('.jpg', '.jpeg', '.JPG', '.JPEG')
# File type extensions that are logged when filename matches a scanned input file
ARCHIVE_FILE_TYPES = ('.CR2', '.cr2', '.RAW', '.raw')
ACCEPTED_SYMBOLOGIES = ['CODE39']
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

def creation_date(path_to_file):
    # From https://stackoverflow.com/a/39501288
    """
    Try to get the date that a file was created, falling back to when it was
    last modified if that isn't possible.
    See http://stackoverflow.com/a/39501288/1709587 for explanation.
    """
    if platform.system() == 'Windows':
        return os.path.getctime(path_to_file)
    else:
        stat = os.stat(path_to_file)
        try:
            return stat.st_birthtime
        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            return stat.st_mtime

# set up argument parser
ap = argparse.ArgumentParser()
ap.add_argument("-s", "--source", required=True, \
    help="Path to the directory that contains the images to be analyzed.")
ap.add_argument("-m", "--models", required=False, \
    help="Path to the model file for folder identification through histogram analysis.")
args = vars(ap.parse_args())

#TODO record time start of analysis
#iterate JPG files in directory passed from args
directory_path = os.path.realpath(args["source"])
print('Scanning directory:', directory_path)
for image_path in glob.glob(directory_path + "/*.JPG"):
    scan_start_time = datetime.now()
    #print(scan_start_time)
    # Gather file data
    print(image_path)
    basename = os.path.basename(image_path)
    file_name, file_extension = os.path.splitext(basename)
    # Get file creation time
    file_creation_time = datetime.fromtimestamp(creation_date(image_path))
    print ('Time:', file_creation_time)

    #generate MD5 hash
    #print(md5hash(image_path))
    #generate UUID for JPG image
    #print(uuid.uuid4())
    # check exist of archive file
    # print archive filepath
    # read barcodes from JPG
    barcodes = decode(Image.open(image_path))
    if barcodes:
        for barcode in barcodes:
            if str(barcode.type) in ACCEPTED_SYMBOLOGIES:
                print(barcode.data)
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
    #print(scan_end_time)
    # TODO report analysis progress and ETA
    #log JPG data
    #log CR2 data
    #write to DB?

# TODO report total analysis time and stop time
