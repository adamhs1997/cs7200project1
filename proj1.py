# Adam Horvath-Smith
# CS 7200 Project 1

"""
ALGO: 

Initialize each person to be free.
while (some man is free and hasn't proposed to every woman) {
  Choose such a man m
  w = 1st woman on m's list to whom m has not yet proposed
  if (w is free)
    assign m and w to be engaged
  else if (w prefers m to her fiancé m')
    assign m and w to be engaged, and m' to be free
  else w rejects m
}

EFFICIENCY IMPROVEMENTS (S19-S21):
Store men in list
Women can be determined with count and man preference arrays
Women's freedom determined with husband arrays
Engagements marked in husband array and wife array
Use inverse array from women's prefs
"""

from queue import Queue
from copy import deepcopy

# Hold on to men/women in lists--use to represent engagements
residents = {}
hospitals = {}

# Queue up free men
free_residents = Queue()

# Store men's prefs as list of pref lists
resident_prefs = {}

# Track which residents have exhausted all options
exhausted_residents = {}

# Store inverse preference list of men for each woman
hospital_prefs = {}

################

# PRE-PRO AND DATA READ ###

# Read input file
with open("input.csv", 'r') as inf:
    lines = inf.readlines()
    
# Get hospital data
for line in lines:
    if line.strip() == "":  break
    data = line.strip().split(',')
    hospitals[data[0]] = (int(data[1]), [])
    hospital_prefs[data[0]] = {}
    num = 0
    for res in data[2:]:
        hospital_prefs[data[0]][res] = num
        num += 1
    lines = lines[1:]
    
# Get resident data
for line in lines[1:]:
    data = line.strip().split(',')
    residents[data[0]] = ""
    resident_prefs[data[0]] = data[1:]
    free_residents.put(data[0])
    exhausted_residents[data[0]] = False
    
# Copy our resident prefs to another list for stability checker
resident_prefs_copy = deepcopy(resident_prefs)

################

# PROCESSING ###

# Initialize each person to be free.
# <<already done>>

# while (some man is free and hasn't proposed to every woman) {
# Note that if a man is free, he hasn't proposed to every woman
while not free_residents.empty():
    # Choose such a man m
    res = free_residents.get()
    
    # If resident is exhausted, will not get matched
    if exhausted_residents[res]:
        continue
    
    # w = 1st woman on m's list to whom m has not yet proposed
    hos = resident_prefs[res].pop(0)
    
    # Determine if this is last choice for resident
    if not resident_prefs[res]:
        exhausted_residents[res] = True

    # if (w is free)
    if hospitals[hos][0] is not len(hospitals[hos][1]) \
      and res in hospital_prefs[hos]:
        # assign m and w to be engaged
        hospitals[hos][1].append(res)
        hospitals[hos][1].sort(
            key=lambda x: hospital_prefs[hos][x], reverse=True)
        residents[res] = hos
        continue
        
    # else if (w prefers m to her fiancé m')
    for matched_res in hospitals[hos][1]:
        if hospital_prefs[hos][res] < hospital_prefs[hos][matched_res]:
            # assign m and w to be engaged, and m' to be free
            residents[res] = hos
            hospitals[hos][1].remove(matched_res)
            hospitals[hos][1].append(res)
            residents[matched_res] = ""
            free_residents.put(matched_res)
            break
        
    # else w rejects m
    else:
        free_residents.put(res)
        
# Ensure that matching is stable
# TODO
        
print(residents)
print(hospitals)     
print(resident_prefs)
print(resident_prefs_copy)  
