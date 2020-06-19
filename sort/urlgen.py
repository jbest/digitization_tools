
"""
urlgen takes an output log of powersort.py and extracts all the web image paths
and converts the paths into a web URL and an export file appropriate for 
import into Symbiota using the URL Mapping profile.

"""

import csv
import argparse
import os.path
from urllib.parse import urljoin

FILE_BASE_PATH = '/corral-repl/projects/TORCH/web/'
URL_BASE = 'https://web.corral.tacc.utexas.edu/torch/'
FILE_PREFIX = 'BRIT'


# set up argument parser
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True, \
    help="Path to the input log file generated by powersort.py.")
ap.add_argument("-v", "--verbose", action="store_true", \
    help="Detailed output.")
args = vars(ap.parse_args())

"""
config = configparser.ConfigParser()
config_file = args["config"]
config.read(config_file)
"""
input_file = args["input"]


def generate_url(file_base_path=FILE_BASE_PATH, file_path=None, url_base=URL_BASE):
    """
    """
    common_path = os.path.commonpath([file_base_path, file_path])
    relative_path = os.path.relpath(file_path, start=common_path)
    image_url = urljoin(URL_BASE, relative_path)
    return image_url


# /corral-repl/projects/TORCH/web/TEST/BRIT0001000/BRIT1280.JPG
# sample file path
image_path = '/corral-repl/projects/TORCH/web/TEST/BRIT0001000/BRIT1385.JPG'
print(generate_url(file_path=image_path))


with open(input_file, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # check if JPG
        # check if success
        # get catalog number

        print(row['destination'])
        print(generate_url(file_path=row['destination']))


