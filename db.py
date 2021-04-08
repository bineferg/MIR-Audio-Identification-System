"""
Database abstraction
"""

import pickle
import os
from operator import itemgetter

class Database(object):
    def __init__(self, data_dir):
        self.data_dir = data_dir
    
    def store(self, title, hashes):
        # Sort the peaks by time
        hashes.sort(key=itemgetter(1))
        with open(os.path.join(self.data_dir, title)+".pk", "wb") as picklefile:
            pickle.dump(hashes, picklefile)
        picklefile.close()

    def match(self, q_track, q_hashes):
        pickfiles = [x for x in os.listdir(self.data_dir) if x.endswith('.pk')]
        matches = {}
        # Brute force loop
        for q_hash, q_offset in q_hashes:
            for pk in pickfiles:
                with open(os.path.join(self.data_dir, pk), "rb") as p_file:
                    track = pk.split("/")[-1][:-3] 
                    hashset = pickle.load(p_file)
                    for hash, offset in hashset:
                        if hash == q_hash:
                            diff = offset - q_offset
                            if track in matches:
                                if diff in matches[track]:
                                    matches[track][diff] += 1
                                    candidate = matches[track][diff]
                                else:
                                    matches[track][diff] = 1
                            else:
                                matches[track] = {diff: 1}
                p_file.close()
        return(sort_matches(matches))

def sort_matches(matches):
    r_matches={}
    max_count_sum=0
    for match in matches:
        count_sum=0
        for diff in matches[match]:
            count_sum+=matches[match][diff]
        r_matches[match] = count_sum
    return sorted(r_matches, key=r_matches.get, reverse=True)[0:3]
