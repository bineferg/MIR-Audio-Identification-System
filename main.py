"""
Author: Eva Fineberg 
Queen Mary University of London 
Music Informatics 2021
"""

from audioid import audioIdentification
from fingerprint import fingerprintBuilder

# Directory where all data recordings are
REC_PATH='./database_recordings'

# Directory where all query reocrdings are
QUERY_PATH='./query_recordings'

# Directory where the pickle "database" files are stored
DATA_PATH='./data'

# Output file for results
output="output.txt"

fingerprintBuilder(REC_PATH, DATA_PATH)
audioIdentification(QUERY_PATH, DATA_PATH, output)
