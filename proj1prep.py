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

# Hold on to men/women in lists--use to represent engagements
men = []
women = []

# Queue up free men
free_men = Queue()

# Store men's prefs as list of pref lists
men_prefs = []

# Number of proposals made by man m in list
prop_count = []

# Store inverse preference list of men for each woman
women_inverse_prefs = []
women_prefs = []
"""
for i = 1 to n
  inverse[pref[i]] = i
"""

################

# PRE-PRO AND DATA READ ###

# Women's prefs (S13)
amy1 = [2, 3, 4, 5, 1]
bertha2 = [3, 4, 5, 1, 2]
clare3 = [4, 5, 1, 2, 3]
diane4 = [5, 1, 2, 3, 4]
erika5 = [1, 2, 3, 4, 5]
women_prefs = [amy1, bertha2, clare3, diane4, erika5]

# Men's prefs (S13)
victor1 = [1, 2, 3, 4, 5]
wyatt2 = [2, 3, 4, 1, 5]
xavier3 = [3, 4, 1, 2, 5]
yancey4 = [4, 1, 2, 3, 5]
zeus5 = [1, 2, 3, 4, 5]
men_prefs = [victor1, wyatt2, xavier3, yancey4, zeus5]

# Invert women's prefs
for woman_list in women_prefs:
    inv_list = [0] * len(woman_list)
    for idx, item in enumerate(woman_list):
        inv_list[woman_list[idx] - 1] = idx + 1
    women_inverse_prefs.append(inv_list)

print(women_prefs)
print(men_prefs)
print(women_inverse_prefs)

################

# PROCESSING ###

# Initialize each person to be free.
men = [0] * len(men_prefs)
women = [0] * len(women_prefs)
prop_count = [0] * len(men_prefs)
for i in range(len(men_prefs)):
    free_men.put(i)

# while (some man is free and hasn't proposed to every woman) {
# Note that if a man is free, he hasn't proposed to every woman
while not free_men.empty():
    # Choose such a man m
    m = free_men.get()
    
    # w = 1st woman on m's list to whom m has not yet proposed
    w = men_prefs[m].pop(0) - 1

    # if (w is free)
    if women[w] is 0:
        # assign m and w to be engaged
        women[w] = m + 1
        men[m] = w + 1
        
    # else if (w prefers m to her fiancé m')
    elif women_inverse_prefs[w][m] < women_inverse_prefs[w][women[w] - 1]:
        # assign m and w to be engaged, and m' to be free
        m_prime = women[w]
        men[m] = w + 1
        women[w] = m + 1
        men[m_prime - 1] = 0
        free_men.put(m_prime - 1)
        
    # else w rejects m
    else:
        free_men.put(m)
        
print(men)
print(women)
        
