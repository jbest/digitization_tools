"""
Imaging productivity stats
Jason Best - jbest@brit.org

Generates a productivity report based on the creation timestamps of image files.
Details of the imaging session are extracted from the folder name containing the images.
Assumed folder name format is: YYYY-MM-DD_ImagerID_OtherInfo

Usage:
python productivity.py [session_folder_path]

Requirements:
See requirements.txt.
"""

from datetime import datetime, date #, time
import sys
import time
import os
import csv
import re

# If you don't need moving mean calculated, 
# or don't want to have to install other modules, 
# you can remove the following imports then
# comment out the moving mean calculations
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# parameters
# File extensions that are used to determine productivity. Others are ignored.
inputFileTypes = ('.jpg', '.jpeg', '.JPG', '.JPEG') # Variations of JPEG extensions
#inputFileTypes = ('.CR2', '.cr2') # Variations of Canon RAW extensions.
fieldDelimiter = ',' # delimiter used in output CSV
moving_mean_window = 21

def getImages(local_path=None):
    """
    Generates a list of specimen files stored at a local path.
    """      
    imageFiles = []

    dirList = os.listdir(local_path)
    for fileName in dirList:
        #TODO ignore case for extension evaluation
        if fileName.endswith(inputFileTypes):
            #imageFiles.append(local_path + fileName)
            imageFiles.append(os.path.join(local_path, fileName))
    return imageFiles

def getImageData(images):
    stats_list = []
    for imageFile in images:
        #imageStats.append((imageFile, os.path.getmtime(imageFile)))
        stats_list.append((imageFile, os.path.getmtime(imageFile)))
    return stats_list

def get_session_data(session_folder=None):
    if session_folder is not None:
        print 'Analyzing: ', session_folder
        session_re = re.match('(\d\d\d\d)[-_](\d\d)[-_](\d\d)[-_]([a-zA-Z]*)(.*)', session_folder)
        #print session_re.group(1), session_re.group(2), session_re.group(3), session_re.group(4), session_re.group(5)
        #print len(session_re.groups())

        if session_re:    
            if session_re.group(1):
                year = int(session_re.group(1))
            else:
                year = 'NONE'

            if session_re.group(2):
                month = int(session_re.group(2))
            else:
                month = 'NONE'

            if session_re.group(3):
                day = int(session_re.group(3))
            else:
                day = 'NONE'

            if session_re.group(4):
                imager = session_re.group(4)
            else:
                imager = 'NONE'

            if session_re.group(5):
                other = session_re.group(5)
            else:
                other = 'NONE'
        else:
            return {'imager': 'NONE', 'year': 'NONE', 'month': 'NONE', 'day': 'NONE', 'other': 'NONE'}

        return {'imager': imager, 'year': year, 'month': month, 'day': day, 'other': other}
    else:
        print 'No session folder provided.'
        return None


# Analyze the image files
startTime = datetime.now()

# Determine session folder containing images
try:
    if os.path.exists(sys.argv[1]):
        #session_path = sys.argv[1]
        session_path = os.path.abspath(sys.argv[1])
    else:
        session_path = os.path.dirname(os.path.realpath(__file__))
        print 'No valid directory path provided. Assuming:' , session_path
except IndexError:
    # No path provided, assuming script directory
    session_path = os.path.dirname(os.path.realpath(__file__))
    print 'No valid directory path provided. Assuming:' , session_path

session_folder = os.path.basename(session_path)
print 'session_path', session_path, 'session_folder', session_folder

#dir_path = os.path.dirname(imageFile) # full path of parent directory
#basename = os.path.basename(imageFile) # filename with extension
#filename, file_extension = os.path.splitext(basename)

imagesToEvaluate = getImages(session_path)

session_data = get_session_data(session_folder)
print 'session_data:', session_data 

# populate imageStats
image_stats = getImageData(imagesToEvaluate)

# Create data structure
creation_time = None
creation_series = []
series_data = []
cumulative_time = 0
cumulative_mean = 0
image_count = 0
for image_data in sorted(image_stats,key=lambda x: x[1]): # sorted ensures results are in order of creation
    file_path = image_data[0]
    file_basename = os.path.basename(file_path) # filename with extension
    if creation_time is None:
        time_diff = 0
    else:
        time_diff = image_data[1] - creation_time
    cumulative_time = cumulative_time + time_diff
    image_count += 1
    cumulative_mean = cumulative_time/image_count
    creation_time = image_data[1]
    creation_series.append(time_diff)
    try:
        cumulative_images_per_min = 60/cumulative_mean
    except:
        cumulative_images_per_min = 0
    #TODO format floats
    session_date = str(session_data['month']) + '/' + str(session_data['day']) + '/' + str(session_data['year'])
    series_data.append([file_path, file_basename, session_data['imager'], session_data['year'], session_data['month'], session_data['day'], session_data['other'], session_date, time.ctime(creation_time),time_diff, cumulative_time, cumulative_mean, cumulative_images_per_min ])
    print 'Analyzing:', file_basename

# calculate moving mean
#TODO test to see if any data are available
data = pd.Series(creation_series)
data_mean = pd.rolling_mean(data, window=moving_mean_window).shift(-(moving_mean_window/2))
# Create file for results
log_file_base_name = session_data['imager'] + '_' + str(session_data['year']) + '-' + str(session_data['month']) + '-' + str(session_data['day'])
log_file_ext = '.csv'
if os.path.exists(log_file_base_name + log_file_ext):
    log_file_name = log_file_base_name + '_' + startTime.isoformat().replace(':', '--') + log_file_ext
else:
    log_file_name = log_file_base_name + log_file_ext
reportFile = open(log_file_name, "wb")
reportWriter = csv.writer(reportFile, delimiter = fieldDelimiter, escapechar='#')
# header
reportWriter.writerow(["ImagePath", "FileName", "ImagerUsername", "SessionYear", "SessionMonth", "SessionDay", "SessionOther", "SessionDate", "CreationTime" , "CreationDurationSecs", "CumulativeTimeSecs", "CumulativeMeanSecs", "CumulativeImagesPerMinute", "MovingMeanSecs"])

# Merge moving mean into original data and write to file
for index, item in enumerate(series_data):
    if str(data_mean[index]) == 'nan':
        running_mean = 0
    else:
        running_mean = data_mean[index]
    #print type(data_mean[index])
    item.append(running_mean)
    reportWriter.writerow(item)


# close file
reportFile.close()
print 'Analysis complete.'
