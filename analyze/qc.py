"""
find records with 'ambiguous' image classifications
find records with multiple barcodes
find records with high (bad match) closest models
for each:
display image, prompt to fix


"""

import argparse
from datetime import datetime 
import csv
import ast
import os
from PIL import Image

MODEL_MATCH_MAX = 1.0 #Threshold above which records are flagged for further QC
MODELS = {'G':'generic specimen', 'S':'BRIT specimen', 'AL':'Alabama folder', 'TN': 'Tennessee folder', 'F':'Other folder', 'N':'no match'}
#TODO load models file to use as options for re-classification by user input

# set up argument parser
ap = argparse.ArgumentParser()
ap.add_argument("-s", "--source", required=True, \
    help="Path to the CSV file.")
ap.add_argument("-f", "--fix", action="store_true", \
    help="Prompt user to fix problems.")
#ap.add_argument("-o", "--output", required=False, \
#    help="Path to the directory where folder images are copied.")
args = vars(ap.parse_args())

#local_path = os.path.dirname(os.path.realpath(__file__))
analysis_start_time = datetime.now()
data = []
ambiguous = []
multiple_barcodes = []
poor_model_match = []

with open(args["source"]) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        data.append(row)

for row in data:
    model_match_string = None
    model_name = None
    model_similarity = None
    model_match_string = row['closest_model']
    barcodes_string = row['barcodes']
    if barcodes_string:
        barcodes = ast.literal_eval(barcodes_string)
    else:
        barcodes = None
    if model_match_string:
        model_match = ast.literal_eval(model_match_string)
        [(model_name, model_similarity)] = model_match.items()
        if model_similarity > MODEL_MATCH_MAX:
            #print('Poor model match:', model_similarity)
            poor_model_match.append(row)
    if 'ambiguous' in row['image_classifications']:
        #print ('AMBIG', row['image_path'])
        ambiguous.append(row)
    if barcodes:
        if len(barcodes) > 1:
            #print (barcodes, len(barcodes))
            multiple_barcodes.append(row)

"""
for row in ambiguous:
    print (row)
"""
print('Ambiguous:', len(ambiguous))
print('Poor model match: ', len(poor_model_match))
print('Mult. barcodes:', len(multiple_barcodes))

# Fix problems
# Ambiguous
if args["fix"]:
    for row in ambiguous:
        basename = os.path.basename(row['image_path'])
        filename, file_extension = os.path.splitext(basename)
        if file_extension == '.JPG':
            print('Image classifed as', row['image_classifications'])
            img = Image.open(row['image_path'])
            img.show()
            for k, v in MODELS.items():
                print(k, v)
            while True:
                i = input('Classify the image: ')
                i = i.upper()
                try:
                    print(MODELS[i])
                    new_model = MODELS[i]
                    break
                except KeyError:
                    print('Not a valid model.')


    #TODO scale image to reasonable size
    #TODO close image after classification
    # see https://stackoverflow.com/questions/6725099/how-can-i-close-an-image-shown-to-the-user-with-the-python-imaging-library


analysis_end_time = datetime.now()

print('Started:', analysis_start_time)
print('Completed:', analysis_end_time)
print('Duration:', analysis_end_time - analysis_start_time)