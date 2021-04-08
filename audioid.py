"""
Author: Eva Fineberg 
Queen Mary University of London 
Music Informatics 2021
"""
import os
from db import Database
from fingerprint import process_audio, DEFAULT_FS

# Read in query recordings and match them with the top 3
# existing fingerprint. 
# :param q_path is the path to the query recordings
# :param fp_path points to the already stored fingerprints
# :param o_path where to write the outupt to
def audioIdentification(q_path, fp_path, o_path):
    # Get all query recording files
    q_files = [x for x in os.listdir(q_path) if x.endswith('.wav')]
    
    # Initialise db
    db = Database(fp_path)

    # Loop through query files and match them to the top 3 best candidates
    f = open(o_path, "w")
    for file in q_files:
        hashes = process_audio(os.path.join(q_path, file), sr=DEFAULT_FS)
        matches = db.match(file, hashes)
        out = file + "\t"+ "\t".join(matches)+"\n"
        f.write(out)
        print(out)
    f.close()
