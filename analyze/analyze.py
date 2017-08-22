import argparse
from hashlib import md5
import uuid
import glob
from datetime import datetime #, date
import re
import csv
#import time
import os
import platform
from pyzbar.pyzbar import decode
from PIL import Image


# File extensions that are scanned and logged
INPUT_FILE_TYPES = ('.jpg', '.jpeg', '.JPG', '.JPEG')
# File type extensions that are logged when filename matches a scanned input file
ARCHIVE_FILE_TYPES = ('.CR2', '.cr2', '.RAW', '.raw')
# Barcode symbologies accepted, others ignored
ACCEPTED_SYMBOLOGIES = ['CODE39']
#TODO add accepted barcode string patterns
FIELD_DELIMITER = ',' # delimiter used in output CSV

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

# Attempts to get actual path of files with correct case
def get_actual_filename(name):
    # From https://stackoverflow.com/a/14742779
    dirs = name.split('\\')
    # disk letter
    test_name = [dirs[0].upper()]
    for d in dirs[1:]:
        test_name += ["%s[%s]" % (d[:-1], d[-1])]
    res = glob.glob('\\'.join(test_name))
    if not res:
        #File not found
        return None
    return res[0]

def get_actual_filename2(name):
    # from https://stackoverflow.com/a/7133137
    name = "%s[%s]" % (name[:-1], name[-1])
    return glob.glob(name)#[0]

def casedpath(path):
    # from https://stackoverflow.com/a/35229734
    r = glob.glob(re.sub(r'([^:/\\])(?=[/\\]|$)', r'[\1]', path))
    return r and r[0] or path

def log_file_data(path=None, file_name=None, file_hash=None, barcodes=None):
    print(path, file_name, file_hash, file_uuid, barcodes)

# set up argument parser
ap = argparse.ArgumentParser()
ap.add_argument("-s", "--source", required=True, \
    help="Path to the directory that contains the images to be analyzed.")
ap.add_argument("-m", "--models", required=False, \
    help="Path to the model file for folder identification through histogram analysis.")
args = vars(ap.parse_args())

analysis_start_time = datetime.now()
batch_id = uuid.uuid4()

# Create file for results
log_file_name = analysis_start_time.date().isoformat() + '_' + str(batch_id) + '.csv'# Convert date to string in ISO format 
#log_file_name = log_file_name.replace(':', '--')  # replace : in startTime to make filename work in various file systems   
print(log_file_name)
reportFile = open(log_file_name, "w")
reportWriter = csv.writer(reportFile, delimiter = FIELD_DELIMITER, escapechar='#')
# write header
reportWriter.writerow(["ImagePath", "DirPath" , "BaseName", "FileName", "FileExtension", "Code", "CodeType" , "Scan time"])
#TODO extract name of imager from directory path and save in log file


#TODO extract information from directory name (imager, station, etc)
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
    print(file_name, file_extension)
    # Get file creation time
    file_creation_time = datetime.fromtimestamp(creation_date(image_path))
    print('Time:', file_creation_time)
    #generate MD5 hash
    file_hash = md5hash(image_path)
    #generate UUID for JPG image
    file_uuid = uuid.uuid4()
    # check if a companion archive file exists
    # iterate through potential extensions for archive files
    arch_file_path = None
    for archive_extension in ARCHIVE_FILE_TYPES:
        potential_arch_file_name = file_name + archive_extension
        potential_arch_file_path = os.path.join(directory_path, potential_arch_file_name)
        # test if archive file exists
        # TODO change filename comparison be case-sensitive

        if os.path.exists(potential_arch_file_path):
            # Trying to get the path with correct case, file extension in particular
            """
            print('Matched ext:', archive_extension, 'Matched filename:', potential_arch_file_name)
            print(os.path.realpath(potential_arch_file_path))
            print(os.path.abspath(potential_arch_file_path))
            print(casedpath(potential_arch_file_path))
            arch_file_path = get_actual_filename2(potential_arch_file_path)
            """
            arch_file_path = potential_arch_file_path
            break

    # print archive filepath
    print('Archive file:', arch_file_path)
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

analysis_end_time = datetime.now()
print('Started:', analysis_start_time)
print('Completed:', analysis_end_time)
print('Duration:', analysis_end_time - analysis_start_time)

