#
# Get max value from a specific index of a dictionary of lists.
#
# The dictionary's keys are the joint (node) number and refers to a list
# that contains the X, Y, and Z coordinates for the joint (node).
#
# The following code shows how to get the max and min of each coordinate.
#
# Source coded based on:
# https://stackoverflow.com/questions/64152228/python-dictionary-with-lists-get-key-of-a-list-which-contains-max-value-at-spec
#


jts = {'001L': [-48.1, -48.1, -203], '002L': [48.1, -48.1, -203],
       '003L': [-48.1, 48.1, -203], '004L': [48.1, 48.125, -203],
       '101L': [-47.75, -47.75, -200], '102L': [47.75, -47.75, -200],
       '103L': [-47.75, 47.75, -200], '104L': [47.75, 47.75, -200],
       '101P': [-47.75, -47.75, -200], '102P': [47.75, -47.75, -200],
       '103P': [-47.75, 47.75, -200], '104P': [47.75, 47.75, -200],
       '401L': [-20.875, -20.875, 15], '402L': [20.875, -20.875, 15],
       '403L': [-20.875, 20.875, 15], '404L': [20.875, 20.875, 15],
       '401P': [-20.875, -20.875, 15], '402P': [20.875, -20.875, 15],
       '403P': [-20.875, 20.875, 15], '404P': [20.875, 20.875, 15],
       '501L': [-20.375, -20.375, 19], '502L': [20.375, -20.375, 19],
       '503L': [-20.375, 20.375, 19], '504L': [20.375, 20.375, 19],
       '501P': [-20.375, -20.375, 19], '502P': [20.375, -20.375, 19],
       '503P': [-20.375, 20.375, 19], '504P': [20.375, 20.375, 19]}


# get the max and min value of X, Y, and Z coorinate.
# returns a tuple with (max or min value, key) where the key is the joint number.
maxX = max((jts[key][0],key) for key in jts)
minX = min((jts[key][0],key) for key in jts)
maxY = max((jts[key][1],key) for key in jts)
minY = min((jts[key][1],key) for key in jts)
maxZ = max((jts[key][2],key) for key in jts)
minZ = min((jts[key][2],key) for key in jts)


print("-------------")
print("print the tuples produced above")
print(maxX)
print(minX)
print(maxY)
print(minY)
print(maxZ)
print(minZ)

print("-------------")
print("print min or max value from the tuples produced")
print(maxX[0])
print(minX[0])
print(maxY[0])
print(minY[0])
print(maxZ[0])
print(minZ[0])


# optionally, in liue of saving the tuple, just get assigne the 1st item the
# tuple to the variable as shown below
minZ = min((jts[key][2],key) for key in jts)[0]
print("-------------")
print(minZ)
