# digitization_tools
Tools for managing and analyzing digitization workflows for natural history collections.

Instructions:
These are very minimal right now, but should get you started. A virtual environment is optional but perhaps useful to reduce clutter and conflicts in your primary Python environment.

Create a virtual environment (optional):
virtualenv env

Activate the virtual environment (optional):
source env/bin/activate

Install required Python modules:
pip install -r requirements.txt
These requirements are for the  full suite of digitization tools. Not all are needed for each tool (and not all tools are in the repository yet).

Usage:
python productivity.py [session_folder_path]

TODO
Make a general file handler and import the various logging and manipulation tools