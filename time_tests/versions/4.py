import numpy as np
import random
import time
import math

# This file does exactly the same as the file basic_functions.py, but stores the cube state in cubie method in a linear list instead of a nested one. This increases performance by ≈10%, but decreases readability

""" Colors:
GREY = (150, 150, 150)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
ORANGE = (255, 100, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
"""

COLORS = {"GREY": (150, 150, 150), "BLACK": (0, 0, 0), "WHITE": (255, 255, 255), "YELLOW": (255, 255, 0), "GREEN": (0, 255, 0), "BLUE": (0, 0, 255), "RED": (255, 0, 0), "ORANGE": (255, 100, 0)}
COLORS_LIST = list(COLORS)

# list that stores the colors of all the differrent cubies (constant)
CUBIE_LIST = [[[0, 5, 3], [0, 3, 4], [0, 4, 2], [0, 2, 5], [1, 3, 5], [1, 4, 3], [1, 2, 4], [1, 5, 2]],[[0, 3], [0, 4], [0, 2], [0, 5], [1, 3], [1, 4], [1, 2], [1, 5], [3, 5], [3, 4], [2, 4], [2, 5]]]

# list that stores the solved state in linear cubie method (constant)
SOLVED_STATE_CUBIE_LINEAR = [0 for i in range(40)]
SOLVED_STATE_CUBIE_LINEAR[:15:2] = [i for i in range(8)]
SOLVED_STATE_CUBIE_LINEAR[16:39:2] = [i for i in range(12)]


def n_of_swaps(arr): # this function is copied and slighlty modified from geeksforgeeks.org (https://www.geeksforgeeks.org/minimum-number-swaps-required-sort-array/)
    """Returns the minimum number of swaps required to sort the list.
    
    Args:
        arr: list
        
    Returns:
        An integer with the minimum number of swaps needed to sort the list "arr"
    """

    n = len(arr)

    # Create nested array with pairs where the first item per pair is the index and the second item the value
    arrpos = [*enumerate(arr)]

    # Sort the array by array element values to get right position of every element as the elements of nested array
    arrpos.sort(key = lambda it : it[1])

    # To keep track of visited elements. Initialize all elements as not visited (False).
    vis = {k : False for k in range(n)}

    # Initialize result
    ans = 0
    for i in range(n):
        # already swapped or already present at correct position
        if vis[i] or arrpos[i][0] == i:
            continue

        # find number of nodes in this cycle and add it to ans
        cycle_size = 0
        j = i
        while not vis[j]:
            # mark node as visited
            vis[j] = True
             
            # move to next node
            j = arrpos[j][0]
            cycle_size += 1
        
        # update answer by adding current cycle
        if cycle_size > 0:
            ans += (cycle_size - 1)
    
    # return answer
    return ans

class Cube():
    """A cube that can be visualised, permutated and solved.
    
    Attributes:
        size: An integer with the number of pieces along one side of the cube, always 3 in this project
        colors: A list containing the 6 colors of the cube as strings
        stickers_used: A boolean indicating if the "cube_stickers" or the "cube_cubies" attribute is used
        cube_stickers: A list containing the state of the cube in the sticker method (explained in "notation & basic principles.txt")
        cube_cubies: A list containing the state of the cube in the cubie method (explained in "notation & basic principles.txt")
    """

    def __init__(self, solved=True, scramble=None, size=3, colors=COLORS_LIST[2:]):
        """Inits Cube.

        Args:
            solved: A boolean indicating if the newly generated cube should be solved or not
            scramble: A list containing the scramble with which the newly generated cube is scrambled
            size: See class attributes
            colors: See class attributes
        """

        self.size = size
        self.colors = colors
        if solved: # generates a solved cube
            self.stickers_used = True
            self.cube_cubies = None
            self.cube_stickers = [[[k for i in range(self.size)] for j in range(self.size)] for k in range(len(self.colors))]
            """
            self.cube_stickers = [[[3, 2, 4],
                                [5, 0, 4],
                                [2, 4, 1]],

                                [[2, 5, 5],
                                [5, 1, 2],
                                [1, 1, 0]],

                                [[4, 1, 2],
                                [3, 2, 3],
                                [3, 5, 4]],

                                [[2, 4, 0],
                                [1, 3, 3],
                                [0, 3, 1]],

                                [[0, 2, 5],
                                [0, 4, 0],
                                [5, 0, 3]],

                                [[3, 4, 4],
                                [0, 5, 2],
                                [5, 1, 1]]]
            print(np.array(self.cube_stickers))
            """
        else: # genrates a scrambled cube
            self.stickers_used = False
            if scramble: # uses a scramble given
                self.cube_stickers = None
                self.cube_cubies = scramble
            else: # scrambles randomly (although quite inefficiently, it needs an average of 12 tries to guess a valid cube state)
                self.cube_stickers = None
                tries = 1
                corners = [[i, random.randint(0, 2)] for i in range(8)]
                edges = [[i, random.randint(0, 1)] for i in range(12)]
                random.shuffle(corners), random.shuffle(edges)
                self.cube_cubies = [corners, edges]
                while not self.check_solvable():
                    tries += 1
                    corners = [[i, random.randint(0, 2)] for i in range(8)]
                    edges = [[i, random.randint(0, 1)] for i in range(12)]
                    random.shuffle(corners), random.shuffle(edges)
                    self.cube_cubies = [corners, edges]


    def get_cube_state(self, sticker_notation=False, cubie_list=CUBIE_LIST):
        """Gives the current cube state in the preferred notation method.
        
        Can also be used to convert between the two different notations representing the state of the cube.

        Args:
            sticker_notation: A boolean indicating in which notation the representation should get returned

        Returns:
            A list containing the cube in the chosen representation
        
        Raises:
            Exception: no cubie with colors available (might occur when converting to cubie method if the cube is not solvable)
        """
        if sticker_notation:
            if not self.stickers_used:
                # convert cubie notation to sticker notation

                # solved cube in sticker notation
                self.cube_stickers = [[[k for i in range(self.size)] for j in range(self.size)] for k in range(len(self.colors))]
                
                # corners
                # 00
                self.cube_stickers[0][0][0] = cubie_list[0][self.cube_cubies[0]][-self.cube_cubies[1]%3]
                self.cube_stickers[5][0][2] = cubie_list[0][self.cube_cubies[0]][1-self.cube_cubies[1]%3]
                self.cube_stickers[3][0][2] = cubie_list[0][self.cube_cubies[0]][2-self.cube_cubies[1]%3]
                # 01
                self.cube_stickers[0][0][2] = cubie_list[0][self.cube_cubies[2]][-self.cube_cubies[3]%3]
                self.cube_stickers[3][0][0] = cubie_list[0][self.cube_cubies[2]][1-self.cube_cubies[3]%3]
                self.cube_stickers[4][0][0] = cubie_list[0][self.cube_cubies[2]][2-self.cube_cubies[3]%3]
                # 02
                self.cube_stickers[0][2][2] = cubie_list[0][self.cube_cubies[4]][-self.cube_cubies[5]%3]
                self.cube_stickers[4][2][0] = cubie_list[0][self.cube_cubies[4]][1-self.cube_cubies[5]%3]
                self.cube_stickers[2][0][2] = cubie_list[0][self.cube_cubies[4]][2-self.cube_cubies[5]%3]
                # 03
                self.cube_stickers[0][2][0] = cubie_list[0][self.cube_cubies[6]][-self.cube_cubies[7]%3]
                self.cube_stickers[2][0][0] = cubie_list[0][self.cube_cubies[6]][1-self.cube_cubies[7]%3]
                self.cube_stickers[5][2][2] = cubie_list[0][self.cube_cubies[6]][2-self.cube_cubies[7]%3]
                # 04
                self.cube_stickers[1][0][2] = cubie_list[0][self.cube_cubies[8]][-self.cube_cubies[9]%3]
                self.cube_stickers[3][2][2] = cubie_list[0][self.cube_cubies[8]][1-self.cube_cubies[9]%3]
                self.cube_stickers[5][0][0] = cubie_list[0][self.cube_cubies[8]][2-self.cube_cubies[9]%3]
                # 05
                self.cube_stickers[1][0][0] = cubie_list[0][self.cube_cubies[10]][-self.cube_cubies[11]%3]
                self.cube_stickers[4][0][2] = cubie_list[0][self.cube_cubies[10]][1-self.cube_cubies[11]%3]
                self.cube_stickers[3][2][0] = cubie_list[0][self.cube_cubies[10]][2-self.cube_cubies[11]%3]
                # 06
                self.cube_stickers[1][2][0] = cubie_list[0][self.cube_cubies[12]][-self.cube_cubies[13]%3]
                self.cube_stickers[2][2][2] = cubie_list[0][self.cube_cubies[12]][1-self.cube_cubies[13]%3]
                self.cube_stickers[4][2][2] = cubie_list[0][self.cube_cubies[12]][2-self.cube_cubies[13]%3]
                # 07
                self.cube_stickers[1][2][2] = cubie_list[0][self.cube_cubies[14]][-self.cube_cubies[15]%3]
                self.cube_stickers[5][2][0] = cubie_list[0][self.cube_cubies[14]][1-self.cube_cubies[15]%3]
                self.cube_stickers[2][2][0] = cubie_list[0][self.cube_cubies[14]][2-self.cube_cubies[15]%3]

                # edges
                # 10
                self.cube_stickers[0][0][1] = cubie_list[1][self.cube_cubies[16]][-self.cube_cubies[17]%2]
                self.cube_stickers[3][0][1] = cubie_list[1][self.cube_cubies[16]][1-self.cube_cubies[17]%2]
                # 11
                self.cube_stickers[0][1][2] = cubie_list[1][self.cube_cubies[18]][-self.cube_cubies[19]%2]
                self.cube_stickers[4][1][0] = cubie_list[1][self.cube_cubies[18]][1-self.cube_cubies[19]%2]
                # 12
                self.cube_stickers[0][2][1] = cubie_list[1][self.cube_cubies[20]][-self.cube_cubies[21]%2]
                self.cube_stickers[2][0][1] = cubie_list[1][self.cube_cubies[20]][1-self.cube_cubies[21]%2]
                # 13
                self.cube_stickers[0][1][0] = cubie_list[1][self.cube_cubies[22]][-self.cube_cubies[23]%2]
                self.cube_stickers[5][1][2] = cubie_list[1][self.cube_cubies[22]][1-self.cube_cubies[23]%2]
                # 14
                self.cube_stickers[1][0][1] = cubie_list[1][self.cube_cubies[24]][-self.cube_cubies[25]%2]
                self.cube_stickers[3][2][1] = cubie_list[1][self.cube_cubies[24]][1-self.cube_cubies[25]%2]
                # 15
                self.cube_stickers[1][1][0] = cubie_list[1][self.cube_cubies[26]][-self.cube_cubies[27]%2]
                self.cube_stickers[4][1][2] = cubie_list[1][self.cube_cubies[26]][1-self.cube_cubies[27]%2]
                # 16
                self.cube_stickers[1][2][1] = cubie_list[1][self.cube_cubies[28]][-self.cube_cubies[29]%2]
                self.cube_stickers[2][2][1] = cubie_list[1][self.cube_cubies[28]][1-self.cube_cubies[29]%2]
                # 17
                self.cube_stickers[1][1][2] = cubie_list[1][self.cube_cubies[30]][-self.cube_cubies[31]%2]
                self.cube_stickers[5][1][0] = cubie_list[1][self.cube_cubies[30]][1-self.cube_cubies[31]%2]
                # 18
                self.cube_stickers[3][1][2] = cubie_list[1][self.cube_cubies[32]][-self.cube_cubies[33]%2]
                self.cube_stickers[5][0][1] = cubie_list[1][self.cube_cubies[32]][1-self.cube_cubies[33]%2]
                # 19
                self.cube_stickers[3][1][0] = cubie_list[1][self.cube_cubies[34]][-self.cube_cubies[35]%2]
                self.cube_stickers[4][0][1] = cubie_list[1][self.cube_cubies[34]][1-self.cube_cubies[35]%2]
                # 110
                self.cube_stickers[2][1][2] = cubie_list[1][self.cube_cubies[36]][-self.cube_cubies[37]%2]
                self.cube_stickers[4][2][1] = cubie_list[1][self.cube_cubies[36]][1-self.cube_cubies[37]%2]
                # 111
                self.cube_stickers[2][1][0] = cubie_list[1][self.cube_cubies[38]][-self.cube_cubies[39]%2]
                self.cube_stickers[5][2][1] = cubie_list[1][self.cube_cubies[38]][1-self.cube_cubies[39]%2]

                self.cube_cubies = None
                self.stickers_used = True
            return self.cube_stickers
        if self.stickers_used:
            # convert sticker notation to cubie notation

            # outline in cubie notation:
            self.cube_cubies = [0 for i in range(40)]
            
            # corners
            # 00
            l = [self.cube_stickers[0][0][0], self.cube_stickers[5][0][2], self.cube_stickers[3][0][2]]
            rot = 0 # rotation of the corner
            while l not in cubie_list[0]:
                l = list(np.roll(l, -1))
                rot += 1
                if rot >= 3:
                    raise Exception(f"These three colors ({self.cube_stickers[0][0][0]}, {self.cube_stickers[5][0][2]}, {self.cube_stickers[3][0][2]}) are not an available cubie.")
            self.cube_cubies[0] = cubie_list[0].index(l)
            self.cube_cubies[1] = rot
            # self.cube_cubies[0][0] = [cubie_list[0].index(l), rot]
            # 01
            l = [self.cube_stickers[0][0][2], self.cube_stickers[3][0][0], self.cube_stickers[4][0][0]]
            rot = 0 # rotation of the corner
            while l not in cubie_list[0]:
                l = list(np.roll(l, -1))
                rot += 1
                if rot >= 3:
                    raise Exception(f"These three colors ({self.cube_stickers[0][0][2]}, {self.cube_stickers[3][0][0]}, {self.cube_stickers[4][0][0]}) are not an available cubie.")
            self.cube_cubies[2] = cubie_list[0].index(l)
            self.cube_cubies[3] = rot
            # 02
            l = [self.cube_stickers[0][2][2], self.cube_stickers[4][2][0], self.cube_stickers[2][0][2]]
            rot = 0 # rotation of the corner
            while l not in cubie_list[0]:
                l = list(np.roll(l, -1))
                rot += 1
                if rot >= 3:
                    raise Exception(f"These three colors ({self.cube_stickers[0][2][2]}, {self.cube_stickers[4][2][0]}, {self.cube_stickers[2][0][2]}) are not an available cubie.")
            self.cube_cubies[4] = cubie_list[0].index(l)
            self.cube_cubies[5] = rot
            # 03
            l = [self.cube_stickers[0][2][0], self.cube_stickers[2][0][0], self.cube_stickers[5][2][2]]
            rot = 0 # rotation of the corner
            while l not in cubie_list[0]:
                l = list(np.roll(l, -1))
                rot += 1
                if rot >= 3:
                    raise Exception(f"These three colors ({self.cube_stickers[0][2][0]}, {self.cube_stickers[2][0][0]}, {self.cube_stickers[5][2][2]}) are not an available cubie.")
            self.cube_cubies[6] = cubie_list[0].index(l)
            self.cube_cubies[7] = rot
            # 04
            l = [self.cube_stickers[1][0][2], self.cube_stickers[3][2][2], self.cube_stickers[5][0][0]]
            rot = 0 # rotation of the corner
            while l not in cubie_list[0]:
                l = list(np.roll(l, -1))
                rot += 1
                if rot >= 3:
                    raise Exception(f"These three colors ({self.cube_stickers[1][0][2]}, {self.cube_stickers[3][2][2]}, {self.cube_stickers[5][0][0]}) are not an available cubie.")
            self.cube_cubies[8] = cubie_list[0].index(l)
            self.cube_cubies[9] = rot
            # 05
            l = [self.cube_stickers[1][0][0], self.cube_stickers[4][0][2], self.cube_stickers[3][2][0]]
            rot = 0 # rotation of the corner
            while l not in cubie_list[0]:
                l = list(np.roll(l, -1))
                rot += 1
                if rot >= 3:
                    raise Exception(f"These three colors ({self.cube_stickers[1][0][0]}, {self.cube_stickers[4][0][2]}, {self.cube_stickers[3][2][0]}) are not an available cubie.")
            self.cube_cubies[10] = cubie_list[0].index(l)
            self.cube_cubies[11] = rot
            # 06
            l = [self.cube_stickers[1][2][0], self.cube_stickers[2][2][2], self.cube_stickers[4][2][2]]
            rot = 0 # rotation of the corner
            while l not in cubie_list[0]:
                l = list(np.roll(l, -1))
                rot += 1
                if rot >= 3:
                    raise Exception(f"These three colors ({self.cube_stickers[1][2][0]}, {self.cube_stickers[2][2][2]}, {self.cube_stickers[4][2][2]}) are not an available cubie.")
            self.cube_cubies[12] = cubie_list[0].index(l)
            self.cube_cubies[13] = rot
            # 07
            l = [self.cube_stickers[1][2][2], self.cube_stickers[5][2][0], self.cube_stickers[2][2][0]]
            rot = 0 # rotation of the corner
            while l not in cubie_list[0]:
                l = list(np.roll(l, -1))
                rot += 1
                if rot >= 3:
                    raise Exception(f"These three colors ({self.cube_stickers[1][2][2]}, {self.cube_stickers[5][2][0]}, {self.cube_stickers[2][2][0]}) are not an available cubie.")
            self.cube_cubies[14] = cubie_list[0].index(l)
            self.cube_cubies[15] = rot

            # edges
            # 10
            l = [self.cube_stickers[0][0][1], self.cube_stickers[3][0][1]]
            flip = 0 # if the edge is flipped or not
            while l not in cubie_list[1]:
                l = list(np.roll(l, 1))
                flip += 1
                if flip >= 2:
                    raise Exception(f"These two colors ({self.cube_stickers[0][0][1]}, {self.cube_stickers[3][0][1]}) are not an available cubie.")
            self.cube_cubies[16] = cubie_list[1].index(l)
            self.cube_cubies[17] = flip
            #self.cube_cubies[1][0] = [cubie_list[1].index(l), flip]
            # 11
            l = [self.cube_stickers[0][1][2], self.cube_stickers[4][1][0]]
            flip = 0 # if the edge is flipped or not
            while l not in cubie_list[1]:
                l = list(np.roll(l, 1))
                flip += 1
                if flip >= 2:
                    raise Exception(f"These two colors ({self.cube_stickers[0][1][2]}, {self.cube_stickers[4][1][0]}) are not an available cubie.")
            self.cube_cubies[18] = cubie_list[1].index(l)
            self.cube_cubies[19] = flip
            # 12
            l = [self.cube_stickers[0][2][1], self.cube_stickers[2][0][1]]
            flip = 0 # if the edge is flipped or not
            while l not in cubie_list[1]:
                l = list(np.roll(l, 1))
                flip += 1
                if flip >= 2:
                    raise Exception(f"These two colors ({self.cube_stickers[0][2][1]}, {self.cube_stickers[2][0][1]}) are not an available cubie.")
            self.cube_cubies[20] = cubie_list[1].index(l)
            self.cube_cubies[21] = flip
            # 13
            l = [self.cube_stickers[0][1][0], self.cube_stickers[5][1][2]]
            flip = 0 # if the edge is flipped or not
            while l not in cubie_list[1]:
                l = list(np.roll(l, 1))
                flip += 1
                if flip >= 2:
                    raise Exception(f"These two colors ({self.cube_stickers[0][1][0]}, {self.cube_stickers[5][1][2]}) are not an available cubie.")
            self.cube_cubies[22] = cubie_list[1].index(l)
            self.cube_cubies[23] = flip
            # 14
            l = [self.cube_stickers[1][0][1], self.cube_stickers[3][2][1]]
            flip = 0 # if the edge is flipped or not
            while l not in cubie_list[1]:
                l = list(np.roll(l, 1))
                flip += 1
                if flip >= 2:
                    raise Exception(f"These two colors ({self.cube_stickers[1][0][1]}, {self.cube_stickers[3][2][1]}) are not an available cubie.")
            self.cube_cubies[24] = cubie_list[1].index(l)
            self.cube_cubies[25] = flip
            # 15
            l = [self.cube_stickers[1][1][0], self.cube_stickers[4][1][2]]
            flip = 0 # if the edge is flipped or not
            while l not in cubie_list[1]:
                l = list(np.roll(l, 1))
                flip += 1
                if flip >= 2:
                    raise Exception(f"These two colors ({self.cube_stickers[1][1][0]}, {self.cube_stickers[4][1][2]}) are not an available cubie.")
            self.cube_cubies[26] = cubie_list[1].index(l)
            self.cube_cubies[27] = flip
            # 16
            l = [self.cube_stickers[1][2][1], self.cube_stickers[2][2][1]]
            flip = 0 # if the edge is flipped or not
            while l not in cubie_list[1]:
                l = list(np.roll(l, 1))
                flip += 1
                if flip >= 2:
                    raise Exception(f"These two colors ({self.cube_stickers[1][2][1]}, {self.cube_stickers[2][2][1]}) are not an available cubie.")
            self.cube_cubies[28] = cubie_list[1].index(l)
            self.cube_cubies[29] = flip
            # 17
            l = [self.cube_stickers[1][1][2], self.cube_stickers[5][1][0]]
            flip = 0 # if the edge is flipped or not
            while l not in cubie_list[1]:
                l = list(np.roll(l, 1))
                flip += 1
                if flip >= 2:
                    raise Exception(f"These two colors ({self.cube_stickers[1][1][2]}, {self.cube_stickers[5][1][0]}) are not an available cubie.")
            self.cube_cubies[30] = cubie_list[1].index(l)
            self.cube_cubies[31] = flip
            # 18
            l = [self.cube_stickers[3][1][2], self.cube_stickers[5][0][1]]
            flip = 0 # if the edge is flipped or not
            while l not in cubie_list[1]:
                l = list(np.roll(l, 1))
                flip += 1
                if flip >= 2:
                    raise Exception(f"These two colors ({self.cube_stickers[3][1][2]}, {self.cube_stickers[5][0][1]}) are not an available cubie.")
            self.cube_cubies[32] = cubie_list[1].index(l)
            self.cube_cubies[33] = flip
            # 19
            l = [self.cube_stickers[3][1][0], self.cube_stickers[4][0][1]]
            flip = 0 # if the edge is flipped or not
            while l not in cubie_list[1]:
                l = list(np.roll(l, 1))
                flip += 1
                if flip >= 2:
                    raise Exception(f"These two colors ({self.cube_stickers[3][1][0]}, {self.cube_stickers[4][0][1]}) are not an available cubie.")
            self.cube_cubies[34] = cubie_list[1].index(l)
            self.cube_cubies[35] = flip
            # 110
            l = [self.cube_stickers[2][1][2], self.cube_stickers[4][2][1]]
            flip = 0 # if the edge is flipped or not
            while l not in cubie_list[1]:
                l = list(np.roll(l, 1))
                flip += 1
                if flip >= 2:
                    raise Exception(f"These two colors ({self.cube_stickers[2][1][2]}, {self.cube_stickers[4][2][1]}) are not an available cubie.")
            self.cube_cubies[36] = cubie_list[1].index(l)
            self.cube_cubies[37] = flip
            # 111
            l = [self.cube_stickers[2][1][0], self.cube_stickers[5][2][1]]
            flip = 0 # if the edge is flipped or not
            while l not in cubie_list[1]:
                l = list(np.roll(l, 1))
                flip += 1
                if flip >= 2:
                    raise Exception(f"These two colors ({self.cube_stickers[2][1][0]}, {self.cube_stickers[5][2][1]}) are not an available cubie.")
            self.cube_cubies[38] = cubie_list[1].index(l)
            self.cube_cubies[39] = flip

            self.cube_stickers = None
            self.stickers_used = False
        return self.cube_cubies

    def turn(self, turns):
        """Executes one ore multiple given turn(s) on the cube.
        
        Args:
            turn: A string representing the turn executed on the cube ("U_", "U'", "U2", "D_", "D'", "D2", "F_", "F'", "F2", "B_", "B'", "B2", "R_", "R'", "R2", "L_", "L'", "L2") or any concatenation of these strings
        """

        # make sure the cube notation is set to cubies
        self.get_cube_state()

        turns_list = [turns[i:i+2] for i in range(0, len(turns), 2)] # list of blocks of 2 characters from the original string (seperates multiple moves)
        for turn in turns_list:
            match turn:
                case "U_":
                    self.turn_U()
                case "U'":
                    self.turn_U_prime()
                case "U2":
                    self.turn_U2()
                case "D_":
                    self.turn_D()
                case "D'":
                    self.turn_D_prime()
                case "D2":
                    self.turn_D2()
                case "F_":
                    self.turn_F()
                case "F'":
                    self.turn_F_prime()
                case "F2":
                    self.turn_F2()
                case "B_":
                    self.turn_B()
                case "B'":
                    self.turn_B_prime()
                case "B2":
                    self.turn_B2()
                case "R_":
                    self.turn_R()
                case "R'":
                    self.turn_R_prime()
                case "R2":
                    self.turn_R2()
                case "L_":
                    self.turn_L()
                case "L'":
                    self.turn_L_prime()
                case "L2":
                    self.turn_L2()

    def turn_U(self):
        """Executes a U turn on the cube."""

        # corners
        # save 00
        saved = self.cube_cubies[0:2]
        # move 03 to 00
        self.cube_cubies[0:2] = self.cube_cubies[6:8]
        # move 02 to 03
        self.cube_cubies[6:8] = self.cube_cubies[4:6]
        # move 01 to 02
        self.cube_cubies[4:6] = self.cube_cubies[2:4]
        # move saved to 01
        self.cube_cubies[2:4] = saved[0:2]

        # edges
        # save 10
        saved = self.cube_cubies[16:18]
        # move 13 to 10
        self.cube_cubies[16:18] = self.cube_cubies[22:24]
        # move 12 to 13
        self.cube_cubies[22:24] = self.cube_cubies[20:22]
        # move 11 to 12
        self.cube_cubies[20:22] = self.cube_cubies[18:20]
        # move saved to 11
        self.cube_cubies[18:20] = saved[0:2]
        
        return self

    def turn_U_prime(self):
        """Executes a U' turn on the cube."""

        # corners
        # save 00
        saved = self.cube_cubies[0:2]
        # move 01 to 00
        self.cube_cubies[0:2] = self.cube_cubies[2:4]
        # move 02 to 01
        self.cube_cubies[2:4] = self.cube_cubies[4:6]
        # move 03 to 02
        self.cube_cubies[4:6] = self.cube_cubies[6:8]
        # move saved to 03
        self.cube_cubies[6:8] = saved[0:2]

        # edges
        # save 10
        saved = self.cube_cubies[16:18]
        # move 11 to 10
        self.cube_cubies[16:18] = self.cube_cubies[18:20]
        # move 12 to 11
        self.cube_cubies[18:20] = self.cube_cubies[20:22]
        # move 13 to 12
        self.cube_cubies[20:22] = self.cube_cubies[22:24]
        # move saved to 13
        self.cube_cubies[22:24] = saved[0:2]

        return self

    def turn_U2(self):
        """Executes a U2 turn on the cube."""

        # corners
        # save 00
        saved = self.cube_cubies[0:2]
        # move 02 to 00
        self.cube_cubies[0:2] = self.cube_cubies[4:6]
        # move saved to 02
        self.cube_cubies[4:6] = saved[0:2]
        
        # save 01
        saved = self.cube_cubies[2:4]
        # move 03 to 01
        self.cube_cubies[2:4] = self.cube_cubies[6:8]
        # move saved to 03
        self.cube_cubies[6:8] = saved[0:2]

        # edges
        # save 10
        saved = self.cube_cubies[16:18]
        # move 12 to 10
        self.cube_cubies[16:18] = self.cube_cubies[20:22]
        # move saved to 12
        self.cube_cubies[20:22] = saved[0:2]

        # save 11
        saved = self.cube_cubies[18:20]
        # move 13 to 11
        self.cube_cubies[18:20] = self.cube_cubies[22:24]
        # move saved to 13
        self.cube_cubies[22:24] = saved[0:2]

        return self

    def turn_D(self):
        """Executes a D turn on the cube."""

        # corners
        # save 04
        saved = self.cube_cubies[8:10]
        # move 05 to 04
        self.cube_cubies[8:10] = self.cube_cubies[10:12]
        # move 06 to 05
        self.cube_cubies[10:12] = self.cube_cubies[12:14]
        # move 07 to 06
        self.cube_cubies[12:14] = self.cube_cubies[14:16]
        # move saved to 07
        self.cube_cubies[14:16] = saved[0:2]

        # edges
        # save 14
        saved = self.cube_cubies[24:26]
        # move 15 to 14
        self.cube_cubies[24:26] = self.cube_cubies[26:28]
        # move 16 to 15
        self.cube_cubies[26:28] = self.cube_cubies[28:30]
        # move 17 to 16
        self.cube_cubies[28:30] = self.cube_cubies[30:32]
        # move saved to 17
        self.cube_cubies[30:32] = saved[0:2]

        return self

    def turn_D_prime(self):
        """Executes a D' turn on the cube."""

        # corners
        # save 04
        saved = self.cube_cubies[8:10]
        # move 07 to 04
        self.cube_cubies[8:10] = self.cube_cubies[14:16]
        # move 06 to 07
        self.cube_cubies[14:16] = self.cube_cubies[12:14]
        # move 05 to 06
        self.cube_cubies[12:14] = self.cube_cubies[10:12]
        # move saved to 05
        self.cube_cubies[10:12] = saved[0:2]

        # edges
        # save 14
        saved = self.cube_cubies[24:26]
        # move 17 to 14
        self.cube_cubies[24:26] = self.cube_cubies[30:32]
        # move 16 to 17
        self.cube_cubies[30:32] = self.cube_cubies[28:30]
        # move 15 to 16
        self.cube_cubies[28:30] = self.cube_cubies[26:28]
        # move saved to 15
        self.cube_cubies[26:28] = saved[0:2]

        return self

    def turn_D2(self):
        """Executes a D2 turn on the cube."""

        # corners
        # save 04
        saved = self.cube_cubies[8:10]
        # move 06 to 04
        self.cube_cubies[8:10] = self.cube_cubies[12:14]
        # move saved to 06
        self.cube_cubies[12:14] = saved[0:2]
        
        # save 05
        saved = self.cube_cubies[10:12]
        # move 07 to 05
        self.cube_cubies[10:12] = self.cube_cubies[14:16]
        # move saved to 07
        self.cube_cubies[14:16] = saved[0:2]

        # edges
        # save 14
        saved = self.cube_cubies[24:26]
        # move 16 to 14
        self.cube_cubies[24:26] = self.cube_cubies[28:30]
        # move saved to 16
        self.cube_cubies[28:30] = saved[0:2]

        # save 15
        saved = self.cube_cubies[26:28]
        # move 17 to 15
        self.cube_cubies[26:28] = self.cube_cubies[30:32]
        # move saved to 17
        self.cube_cubies[30:32] = saved[0:2]

        return self

    def turn_F(self):
        """Executes a F turn on the cube."""

        # corners
        # save 02
        saved = self.cube_cubies[4:6]
        # move 03 to 02
        self.cube_cubies[4] = self.cube_cubies[6]
        self.cube_cubies[5] = (self.cube_cubies[7]+1)%3
        # move 07 to 03
        self.cube_cubies[6] = self.cube_cubies[14]
        self.cube_cubies[7] = (self.cube_cubies[15]-1)%3
        # move 06 to 07
        self.cube_cubies[14] = self.cube_cubies[12]
        self.cube_cubies[15] = (self.cube_cubies[13]+1)%3
        # move saved to 06
        self.cube_cubies[12] = saved[0]
        self.cube_cubies[13] = (saved[1]-1)%3

        # edges
        # save 12
        saved = self.cube_cubies[20:22]
        # move 111 to 12
        self.cube_cubies[20] = self.cube_cubies[38]
        self.cube_cubies[21] = 1-self.cube_cubies[39]
        # move 16 to 111
        self.cube_cubies[38] = self.cube_cubies[28]
        self.cube_cubies[39] = 1-self.cube_cubies[29]
        # move 110 to 16
        self.cube_cubies[28] = self.cube_cubies[36]
        self.cube_cubies[29] = 1-self.cube_cubies[37]
        # move saved to 110
        self.cube_cubies[36] = saved[0]
        self.cube_cubies[37] = 1-saved[1]

        return self

    def turn_F_prime(self):
        """Executes a F' turn on the cube."""

        # corners
        # save 02
        saved = self.cube_cubies[4:6]
        # move 06 to 02
        self.cube_cubies[4] = self.cube_cubies[12]
        self.cube_cubies[5] = (self.cube_cubies[13]+1)%3
        # move 07 to 06
        self.cube_cubies[12] = self.cube_cubies[14]
        self.cube_cubies[13] = (self.cube_cubies[15]-1)%3
        # move 03 to 07
        self.cube_cubies[14] = self.cube_cubies[6]
        self.cube_cubies[15] = (self.cube_cubies[7]+1)%3
        # move saved to 03
        self.cube_cubies[6] = saved[0]
        self.cube_cubies[7] = (saved[1]-1)%3

        # edges
        # save 12
        saved = self.cube_cubies[20:22]
        # move 110 to 12
        self.cube_cubies[20] = self.cube_cubies[36]
        self.cube_cubies[21] = 1-self.cube_cubies[37]
        # move 16 to 110
        self.cube_cubies[36] = self.cube_cubies[28]
        self.cube_cubies[37] = 1-self.cube_cubies[29]
        # move 111 to 16
        self.cube_cubies[28] = self.cube_cubies[38]
        self.cube_cubies[29] = 1-self.cube_cubies[39]
        # move saved to 111
        self.cube_cubies[38] = saved[0]
        self.cube_cubies[39] = 1-saved[1]

        return self

    def turn_F2(self):
        """Executes a F2 turn on the cube."""

        # corners
        # save 02
        saved = self.cube_cubies[4:6]
        # move 07 to 02
        self.cube_cubies[4:6] = self.cube_cubies[14:16]
        # move saved to 07
        self.cube_cubies[14:16] = saved[0:2]

        # save 03
        saved = self.cube_cubies[6:8]
        # move 06 to 03
        self.cube_cubies[6:8] = self.cube_cubies[12:14]
        # move saved to 06
        self.cube_cubies[12:14] = saved[0:2]

        # edges
        # save 12
        saved = self.cube_cubies[20:22]
        # move 16 to 12
        self.cube_cubies[20:22] = self.cube_cubies[28:30]
        # move saved to 16
        self.cube_cubies[28:30] = saved[0:2]

        # save 110
        saved = self.cube_cubies[36:38]
        # move 111 to 110
        self.cube_cubies[36:38] = self.cube_cubies[38:40]
        # move saved to 111
        self.cube_cubies[38:40] = saved[0:2]

        return self

    def turn_B(self):
        """Executes a B turn on the cube."""

        # corners
        # save 00
        saved = self.cube_cubies[0:2]
        # move 01 to 00
        self.cube_cubies[0] = self.cube_cubies[2]
        self.cube_cubies[1] = (self.cube_cubies[3]+1)%3
        # move 05 to 01
        self.cube_cubies[2] = self.cube_cubies[10]
        self.cube_cubies[3] = (self.cube_cubies[11]-1)%3
        # move 04 to 05
        self.cube_cubies[10] = self.cube_cubies[8]
        self.cube_cubies[11] = (self.cube_cubies[9]+1)%3
        # move saved to 04
        self.cube_cubies[8] = saved[0]
        self.cube_cubies[9] = (saved[1]-1)%3

        # edges
        # save 10
        saved = self.cube_cubies[16:18]
        # move 19 to 10
        self.cube_cubies[16] = self.cube_cubies[34]
        self.cube_cubies[17] = 1-self.cube_cubies[35]
        # move 14 to 19
        self.cube_cubies[34] = self.cube_cubies[24]
        self.cube_cubies[35] = 1-self.cube_cubies[25]
        # move 18 to 14
        self.cube_cubies[24] = self.cube_cubies[32]
        self.cube_cubies[25] = 1-self.cube_cubies[33]
        # move saved to 18
        self.cube_cubies[32] = saved[0]
        self.cube_cubies[33] = 1-saved[1]

        return self

    def turn_B_prime(self):
        """Executes a B' turn on the cube."""

        # corners
        # save 00
        saved = self.cube_cubies[0:2]
        # move 04 to 00
        self.cube_cubies[0] = self.cube_cubies[8]
        self.cube_cubies[1] = (self.cube_cubies[9]+1)%3
        # move 05 to 04
        self.cube_cubies[8] = self.cube_cubies[10]
        self.cube_cubies[9] = (self.cube_cubies[11]-1)%3
        # move 01 to 05
        self.cube_cubies[10] = self.cube_cubies[2]
        self.cube_cubies[11] = (self.cube_cubies[3]+1)%3
        # move saved to 01
        self.cube_cubies[2] = saved[0]
        self.cube_cubies[3] = (saved[1]-1)%3

        # edges
        # save 10
        saved = self.cube_cubies[16:18]
        # move 18 to 10
        self.cube_cubies[16] = self.cube_cubies[32]
        self.cube_cubies[17] = 1-self.cube_cubies[33]
        # move 14 to 18
        self.cube_cubies[32] = self.cube_cubies[24]
        self.cube_cubies[33] = 1-self.cube_cubies[25]
        # move 19 to 14
        self.cube_cubies[24] = self.cube_cubies[34]
        self.cube_cubies[25] = 1-self.cube_cubies[35]
        # move saved to 19
        self.cube_cubies[34] = saved[0]
        self.cube_cubies[35] = 1-saved[1]

        return self

    def turn_B2(self):
        """Executes a B2 turn on the cube."""

        # corners
        # save 00
        saved = self.cube_cubies[0:2]
        # move 05 to 00
        self.cube_cubies[0:2] = self.cube_cubies[10:12]
        # move saved to 05
        self.cube_cubies[10:12] = saved[0:2]

        # save 01
        saved = self.cube_cubies[2:4]
        # move 04 to 01
        self.cube_cubies[2:4] = self.cube_cubies[8:10]
        # move saved to 04
        self.cube_cubies[8:10] = saved[0:2]

        # edges
        # save 10
        saved = self.cube_cubies[16:18]
        # move 14 to 10
        self.cube_cubies[16:18] = self.cube_cubies[24:26]
        # move saved to 14
        self.cube_cubies[24:26] = saved[0:2]

        # save 18
        saved = self.cube_cubies[32:34]
        # move 19 to 18
        self.cube_cubies[32:34] = self.cube_cubies[34:36]
        # move saved to 19
        self.cube_cubies[34:36] = saved[0:2]

        return self

    def turn_R(self):
        """Executes a R turn on the cube."""

        # corners
        # save 01
        saved = self.cube_cubies[2:4]
        # move 02 to 01
        self.cube_cubies[2] = self.cube_cubies[4]
        self.cube_cubies[3] = (self.cube_cubies[5]+1)%3
        # move 06 to 02
        self.cube_cubies[4] = self.cube_cubies[12]
        self.cube_cubies[5] = (self.cube_cubies[13]-1)%3
        # move 05 to 06
        self.cube_cubies[12] = self.cube_cubies[10]
        self.cube_cubies[13] = (self.cube_cubies[11]+1)%3
        # move saved to 05
        self.cube_cubies[10] = saved[0]
        self.cube_cubies[11] = (saved[1]-1)%3

        # edges
        # save 11
        saved = self.cube_cubies[18:20]
        # move 110 to 11
        self.cube_cubies[18:20] = self.cube_cubies[36:38]
        # move 15 to 110
        self.cube_cubies[36:38] = self.cube_cubies[26:28]
        # move 19 to 15
        self.cube_cubies[26:28] = self.cube_cubies[34:36]
        # move saved to 19
        self.cube_cubies[34:36] = saved[0:2]

        return self

    def turn_R_prime(self):
        """Executes a R' turn on the cube."""

        # corners
        # save 01
        saved = self.cube_cubies[2:4]
        # move 05 to 01
        self.cube_cubies[2] = self.cube_cubies[10]
        self.cube_cubies[3] = (self.cube_cubies[11]+1)%3
        # move 06 to 05
        self.cube_cubies[10] = self.cube_cubies[12]
        self.cube_cubies[11] = (self.cube_cubies[13]-1)%3
        # move 02 to 06
        self.cube_cubies[12] = self.cube_cubies[4]
        self.cube_cubies[13] = (self.cube_cubies[5]+1)%3
        # move saved to 02
        self.cube_cubies[4] = saved[0]
        self.cube_cubies[5] = (saved[1]-1)%3

        # edges
        # save 11
        saved = self.cube_cubies[18:20]
        # move 19 to 11
        self.cube_cubies[18:20] = self.cube_cubies[34:36]
        # move 15 to 19
        self.cube_cubies[34:36] = self.cube_cubies[26:28]
        # move 110 to 15
        self.cube_cubies[26:28] = self.cube_cubies[36:38]
        # move saved to 110
        self.cube_cubies[36:38] = saved[0:2]

        return self

    def turn_R2(self):
        """Executes a R2 turn on the cube."""

        # corners
        # save 01
        saved = self.cube_cubies[2:4]
        # move 06 to 01
        self.cube_cubies[2:4] = self.cube_cubies[12:14]
        # move saved to 06
        self.cube_cubies[12:14] = saved[0:2]

        # save 02
        saved = self.cube_cubies[4:6]
        # move 05 to 02
        self.cube_cubies[4:6] = self.cube_cubies[10:12]
        # move saved to 05
        self.cube_cubies[10:12] = saved[0:2]

        # edges
        # save 11
        saved = self.cube_cubies[18:20]
        # move 15 to 11
        self.cube_cubies[18:20] = self.cube_cubies[26:28]
        # move saved to 15
        self.cube_cubies[26:28] = saved[0:2]

        # save 19
        saved = self.cube_cubies[34:36]
        # move 110 to 19
        self.cube_cubies[34:36] = self.cube_cubies[36:38]
        # move saved to 110
        self.cube_cubies[36:38] = saved[0:2]

        return self

    def turn_L(self):
        """Executes a L turn on the cube."""

        # corners
        # save 00
        saved = self.cube_cubies[0:2]
        # move 04 to 00
        self.cube_cubies[0] = self.cube_cubies[8]
        self.cube_cubies[1] = (self.cube_cubies[9]-1)%3
        # move 07 to 04
        self.cube_cubies[8] = self.cube_cubies[14]
        self.cube_cubies[9] = (self.cube_cubies[15]+1)%3
        # move 03 to 07
        self.cube_cubies[14] = self.cube_cubies[6]
        self.cube_cubies[15] = (self.cube_cubies[7]-1)%3
        # move saved to 03
        self.cube_cubies[6] = saved[0]
        self.cube_cubies[7] = (saved[1]+1)%3

        # edges
        # save 13
        saved = self.cube_cubies[22:24]
        # move 18 to 13
        self.cube_cubies[22:24] = self.cube_cubies[32:34]
        # move 17 to 18
        self.cube_cubies[32:34] = self.cube_cubies[30:32]
        # move 111 to 17
        self.cube_cubies[30:32] = self.cube_cubies[38:40]
        # move saved to 111
        self.cube_cubies[38:40] = saved[0:2]

        return self

    def turn_L_prime(self):
        """Executes a L' turn on the cube."""

        # corners
        # save 00
        saved = self.cube_cubies[0:2]
        # move 03 to 00
        self.cube_cubies[0] = self.cube_cubies[6]
        self.cube_cubies[1] = (self.cube_cubies[7]-1)%3
        # move 07 to 03
        self.cube_cubies[6] = self.cube_cubies[14]
        self.cube_cubies[7] = (self.cube_cubies[15]+1)%3
        # move 04 to 07
        self.cube_cubies[14] = self.cube_cubies[8]
        self.cube_cubies[15] = (self.cube_cubies[9]-1)%3
        # move saved to 04
        self.cube_cubies[8] = saved[0]
        self.cube_cubies[9] = (saved[1]+1)%3

        # edges
        # save 13
        saved = self.cube_cubies[22:24]
        # move 111 to 13
        self.cube_cubies[22:24] = self.cube_cubies[38:40]
        # move 17 to 111
        self.cube_cubies[38:40] = self.cube_cubies[30:32]
        # move 18 to 17
        self.cube_cubies[30:32] = self.cube_cubies[32:34]
        # move saved to 18
        self.cube_cubies[32:34] = saved[0:2]

        return self

    def turn_L2(self):
        """Executes a L2 turn on the cube."""

        # corners
        # save 00
        saved = self.cube_cubies[0:2]
        # move 07 to 00
        self.cube_cubies[0:2] = self.cube_cubies[14:16]
        # move saved to 07
        self.cube_cubies[14:16] = saved[0:2]

        # save 03
        saved = self.cube_cubies[6:8]
        # move 04 to 03
        self.cube_cubies[6:8] = self.cube_cubies[8:10]
        # move saved to 04
        self.cube_cubies[8:10] = saved[0:2]

        # edges
        # save 13
        saved = self.cube_cubies[22:24]
        # move 17 to 13
        self.cube_cubies[22:24] = self.cube_cubies[30:32]
        # move saved to 17
        self.cube_cubies[30:32] = saved[0:2]

        # save 18
        saved = self.cube_cubies[32:34]
        # move 111 to 18
        self.cube_cubies[32:34] = self.cube_cubies[38:40]
        # move saved to 111
        self.cube_cubies[38:40] = saved[0:2]

        return self

    def check_solvable(self):
        """Checks if the cube is solvable by any moves.

        This is needed because it is not possible to place the 54 stickers on a cube randomly while still being able to solve it with the 18 possible moves.

        Returns:
            A boolean indicating if the cube is solvable
        """
        
        # make sure the cube notation is set to cubies
        try:
            self.get_cube_state()
        except:
            return False

        # check for edge orientation (add up to even number)
        edge_orientations = [self.cube_cubies[i] for i in range(17, 40, 2)]
        if sum(edge_orientations)%2 != 0:
            return False
        
        # check for corner orientation  (add up to number divisible by 3)
        corner_orientations = [self.cube_cubies[i] for i in range(1, 16, 2)]
        if sum(corner_orientations)%3 != 0:
            return False

        # check for position (even number of swaps across edges and corners together)
        n = n_of_swaps([self.cube_cubies[i] for i in range(16, 39, 2)]) + n_of_swaps([self.cube_cubies[i] for i in range(0, 15, 2)])
        if n%2 != 0:
            return False

        # if nothing fails, the cube is solvable
        return True

    def check_step1(self):
        """Checks if the first step of the solving process on the cube is completed.

        The first step of solving a cube is completed if the cube can be solved by any combination of the moves U, U', U2, D, D', D2, F2, B2, R2 and L2.
        This means, all the cubies have to be oriented (because none of these moves changes the orientation of a cubie).
        The position of the cubies is completely free though (technically the rules to check if the cube is even solvable apply as well, but this method should be efficient because it is run very often).

        Returns:
            A boolean indicating if the first step is completed
        """

        # make sure the cube notation is set to cubies
        try:
            self.get_cube_state()
        except:
            return False

        # check corners
        for i in range(1, 16, 2):
            if self.cube_cubies[i] != 0:
                return False
        
        # check edges
        for i in range(17, 40, 2):
            if self.cube_cubies[i] != 0:
                return False

        # if nothing fails, step 1 is solved
        return True

    def check_solved(self, solved_state=SOLVED_STATE_CUBIE_LINEAR):
        """Checks if the cube is solved.

        Returns:
            A boolean indicating if the cube is solved
        """

        if self.get_cube_state() == solved_state:
            return True
        return False

    def recursive_solving(self, depth, prev_move="  "):
        """Solves the cube recursively up to a certain depth.
        
        Args:
            depth: An integer describing the number of moves in a row to consider
            prev_move: A string representing the family of the two previous moves (U, D, F, B, R, L) --> no two moves on the same layer in a row, no 3 moves on opposite layers in a row
            
        Returns:
            A tuple containing two values:
                A boolean indicating if this branch has found a solution
                A string containing the moves used to get to the fastest solution / An empty string if there is no solution on this branch or if the cube is already solved"""
        if self.check_solved():
            #print("solved")
            return True, ""
        #print(f"not solved yet {prev_move}")
        #print(self.cube_cubies)
        if depth > 0:
            depth -= 1
            found = -1

            if prev_move[0] != "U" and prev_move != "DU":
                solved, string = self.turn_U().recursive_solving(depth, "U"+prev_move[0])
                #print(f"{string} U accomplished (depth {depth}), Result: {solved}")
                if solved and (found == -1 or found > len(string)):
                    found = len(string)
                    foundstring = "U_"+string
                    #return True, "U_"+string
                self.turn_U_prime()

                solved, string = self.turn_U_prime().recursive_solving(depth, "U"+prev_move[0])
                #print(f"{string} U' accomplished (depth {depth}), Result: {solved}")
                if solved and (found == -1 or found > len(string)):
                    found = len(string)
                    foundstring = "U'"+string
                self.turn_U()

                solved, string = self.turn_U2().recursive_solving(depth, "U"+prev_move[0])
                #print(f"{string} U2 accomplished (depth {depth}), Result: {solved}")
                if solved and (found == -1 or found > len(string)):
                    found = len(string)
                    foundstring = "U2"+string
                self.turn_U2()

            if prev_move[0] != "D" and prev_move != "UD":
                solved, string = self.turn_D().recursive_solving(depth, "D"+prev_move[0])
                #print(f"{string} D accomplished (depth {depth}), Result: {solved}")
                if solved and (found == -1 or found > len(string)):
                    found = len(string)
                    foundstring = "D_"+string
                self.turn_D_prime()

                solved, string = self.turn_D_prime().recursive_solving(depth, "D"+prev_move[0])
                #print(f"{string} D' accomplished (depth {depth}), Result: {solved}")
                if solved and (found == -1 or found > len(string)):
                    found = len(string)
                    foundstring = "D'"+string
                self.turn_D()

                solved, string = self.turn_D2().recursive_solving(depth, "D"+prev_move[0])
                #print(f"{string} D2 accomplished (depth {depth}), Result: {solved}")
                if solved and (found == -1 or found > len(string)):
                    found = len(string)
                    foundstring = "D2"+string
                self.turn_D2()

            if prev_move[0] != "F" and prev_move != "BF":
                solved, string = self.turn_F().recursive_solving(depth, "F"+prev_move[0])
                #print(f"{string} F accomplished (depth {depth}), Result: {solved}")
                if solved and (found == -1 or found > len(string)):
                    found = len(string)
                    foundstring = "F_"+string
                self.turn_F_prime()

                solved, string = self.turn_F_prime().recursive_solving(depth, "F"+prev_move[0])
                #print(f"{string} F' accomplished (depth {depth}), Result: {solved}")
                if solved and (found == -1 or found > len(string)):
                    found = len(string)
                    foundstring = "F'"+string
                self.turn_F()

                solved, string = self.turn_F2().recursive_solving(depth, "F"+prev_move[0])
                #print(f"{string} F2 accomplished (depth {depth}), Result: {solved}")
                if solved and (found == -1 or found > len(string)):
                    found = len(string)
                    foundstring = "F2"+string
                self.turn_F2()

            if prev_move[0] != "B" and prev_move != "FB":
                solved, string = self.turn_B().recursive_solving(depth, "B"+prev_move[0])
                if solved and (found == -1 or found > len(string)):
                    found = len(string)
                    foundstring = "B_"+string
                self.turn_B_prime()

                solved, string = self.turn_B_prime().recursive_solving(depth, "B"+prev_move[0])
                if solved and (found == -1 or found > len(string)):
                    found = len(string)
                    foundstring = "B'"+string
                self.turn_B()

                solved, string = self.turn_B2().recursive_solving(depth, "B"+prev_move[0])
                if solved and (found == -1 or found > len(string)):
                    found = len(string)
                    foundstring = "B2"+string
                self.turn_B2()

            if prev_move[0] != "R" and prev_move != "LR":
                solved, string = self.turn_R().recursive_solving(depth, "R"+prev_move[0])
                if solved and (found == -1 or found > len(string)):
                    found = len(string)
                    foundstring = "R_"+string
                self.turn_R_prime()

                solved, string = self.turn_R_prime().recursive_solving(depth, "R"+prev_move[0])
                if solved and (found == -1 or found > len(string)):
                    found = len(string)
                    foundstring = "R'"+string
                self.turn_R()

                solved, string = self.turn_R2().recursive_solving(depth, "R"+prev_move[0])
                if solved and (found == -1 or found > len(string)):
                    found = len(string)
                    foundstring = "R2"+string
                self.turn_R2()

            if prev_move[0] != "L" and prev_move != "RL":
                solved, string = self.turn_L().recursive_solving(depth, "L"+prev_move[0])
                if solved and (found == -1 or found > len(string)):
                    found = len(string)
                    foundstring = "L_"+string
                self.turn_L_prime()

                solved, string = self.turn_L_prime().recursive_solving(depth, "L"+prev_move[0])
                #print(f"{string} L' accomplished (depth {depth}), Result: {solved}")
                if solved and (found == -1 or found > len(string)):
                    found = len(string)
                    foundstring = "L'"+string
                self.turn_L()

                solved, string = self.turn_L2().recursive_solving(depth, "L"+prev_move[0])
                if solved and (found == -1 or found > len(string)):
                    found = len(string)
                    foundstring = "L2"+string
                self.turn_L2()

            if found != -1:
                return True, foundstring
            return False, ""
        return False, ""

def generate_cube(solved=True, scramble=None):
    """Generates a new cube according to the parameters

    Args:
        solved: See __init__ method of class "Cube"
        scramble: See __init__ method of class "Cube"

    Returns:
        newly generated cube object
    """
    # This function generates a new Cube, either solved or scrambled randomly or scrambled according to the parameter "scramble"
    cube = Cube(solved, scramble)
    return cube

if __name__ == "__main__":
    cube = generate_cube()
    #cube.turn("U'R_L'F_B2L_")
    #cube.turn("B'D_B'D'R_U_F_")

    print(cube.get_cube_state())
    print(cube.get_cube_state(True))
    print(cube.get_cube_state())

    cube.turn("B_")

    print(cube.get_cube_state())

    print("\n\n\nsolving...\n\n\n")
    depth = 5
    starttime = time.time()
    solved, string = cube.recursive_solving(depth)
    endtime = time.time()
    if solved:
        print(f"Solution found in {endtime-starttime} seconds: {string}")
    else:
        print(f"Sadly there is no solution in the depth given ({depth}), time: {endtime-starttime} seconds")
