# digitization_tools - productivity.py

Generates a productivity report based on the creation timestamps of image files.

See the instructions for the full digitization_tools suite for details of installing requirements.

## Usage:

python productivity.py [session_folder_path]

## Details

Information embeded in the session folder name will be extracted if it follows this format:

YYYY-MM-DD_ImagerName_OtherInfo

e.g: 2015-08-13_jbest_test


The following information is recorded in a CSV file generated when running the script:

ImagePath - the full path of the image

FileName - just the filename

ImagerUsername - extracted from the session folder name

SessionYear - extracted from the session folder name

SessionMonth - extracted from the session folder name

SessionDay - extracted from the session folder name

SessionOther - extracted from the session folder name

SessionDate - compiled from the dates extracted from the session folder name

CreationTime - from the file creation date

CreationDurationSecs - time since previous file was created

CumulativeTimeSecs - total elapsed time since first file creation 

CumulativeMeanSecs - mean creation duration time of current file and all previous files

CumulativeImagesPerMinute - 

MovingMeanSecs - "smoothed" mean creation duration. Window can be changed in script with the moving_mean_window variable
