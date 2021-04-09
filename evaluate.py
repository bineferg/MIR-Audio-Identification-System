"""
Author: Eva Fineberg 
Queen Mary University of London 
Music Informatics 2021
"""

# File where results are stored
output = "output.txt"

# Open file for reading
f = open(output, "r")

# Read list of lines
lines = f.readlines()

# For accuracy calculations
pop_success = 0
pop_total = 0
classical_success = 0
classical_total = 0

# For match calculations
zero_count = 0
one_count = 0
two_count = 0

for line in lines:
    audios = line.strip().split("\t")
    source = audios[0].split("-")[0]
    if len(audios[1:]) == 0:
        zero_count+=1
    if len(audios[1:]) == 1:
        one_count+=1
    if len(audios[1:]) == 2:
        two_count+=1
    for comp in audios[1:]:
        c_audio = comp[:-4]
        if source == c_audio:
            if "pop" in source:
                pop_success +=1
            else:
                classical_success +=1
    if "pop" in source:
        pop_total+=1
    else:
        classical_total+=1
# Close file 
f.close()

# Display accuracy percentage
print("Your audio identificaiton system is {0}% accurate for {1}".format((pop_success/pop_total)*100, " pop tracks"))
print("Your audio identificaiton system is {0}% accurate for {1}".format((classical_success/classical_total)*100, " classical tracks"))
print("{0}% queries were not matched with any recordings".format((zero_count/(pop_total+classical_total))*100))
print("{0}% queries were matched with fewer than 3 recordings".format(((one_count+two_count+zero_count)/(pop_total+classical_total))*100))
