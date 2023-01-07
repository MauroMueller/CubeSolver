"""Script for testing list performance

This script shows the comparison of list performance in terms of runtime.
It compares the following three types of list operations:

Nested: A three-dimensional nested list with n elements in each dimension
    (n**3 elements total). The operations measured are three nested for loops
    (for the three dimensions), accessing the respective list item and storing
    it as x and storing x back at the same place in the list.
Linear: A one-dimensional list with n**3 elements. The operations measured are
    a for loop, accessing the respective list item and storing it as x and
    storing x back at the same place in the list.
Sliced: A one-dimensional list with n**3 elements. The operations measured are
    a for loop skipping over every second element, accessing the respective
    element and the next one (with slicing) and storing it as x and storing x
    back at the same place in the list.

The lists are generated before the time measurement starts.
"""



import time

n = 1000


list = [[[i for i in range(n)] for i in range(n)] for i in range(n)]

starttime = time.time()
for i in range(n):
    for j in range(n):
        for k in range(n):
            x = list[i][j][k]
            list[i][j][k] = x
print(f"Nested: {time.time()-starttime} seconds")



list = [i for i in range(n**3)]

starttime = time.time()
for i in range(n**3):
    x = list[i]
    list[i] = x
print(f"Linear: {time.time()-starttime} seconds")



list = [i for i in range(n**3)]

starttime = time.time()
for i in range(0, n**3, 2):
    x = list[i:i+2]
    list[i:i+2] = x
print(f"Sliced: {time.time()-starttime} seconds")


