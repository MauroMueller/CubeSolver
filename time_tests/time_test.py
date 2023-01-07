import os
import sys
import random
import importlib
import time
import csv

sys.path.append("versions/")

def generate_scramble(length):
    movelist = ["U_", "U'", "U2", "D_", "D'", "D2", "F_", "F'", "F2", "B_", "B'", "B2", "R_", "R'", "R2", "L_", "L'", "L2"]
    opposite_move = {"U": "D", "D": "U", "F": "B", "B": "F", "R": "L", "L": "R"}
    scramble = 4*"_"
    while len(scramble)/2-2 < length:
        random.shuffle(movelist)
        for move in movelist:
            if move[0] != scramble[-2] and (move[0] != scramble[-4] and opposite_move[move[0]] != scramble[-2]):
                scramble += move
                break
    return scramble[4:]


def main():
    dir = "versions"

    filelist = sorted(os.listdir(dir))
    versionlist = []

    for version in filelist:
        f = os.path.join(dir, version)
        if os.path.isfile(f) and f[-3:] == ".py":
            versionlist.append(version)

    with open("progress.txt", "w+") as f:
        f.write("The following versions have been found:\n")
        f.write(", ".join(versionlist)+"\n")
        f.write("Importing versions...\n")
        modules = [0 for i in range(len(versionlist)+1)]
        for v in versionlist:
            modules[int(v[-4])] = getattr(importlib.import_module(v[-4]), "generate_cube")
        f.write("Import comlete.\n")

    for l in range(1,10):
        with open("progress.txt", "a+") as f:
            f.write(f"\nStarting with length {l}...\n")
            f.write(f"Generating random scramble of length {l}...\n")
            scramble = generate_scramble(l)
            f.write(f"Scramble of length {l} found: {scramble}\n")
        for v in versionlist:
            with open("progress.txt", "a+") as f:

                f.write(f"{l=}, v={v[-4]}, Starting with version {v[-4]}...  ")
                cube = modules[int(v[-4])]()
                cube.turn(scramble)
                starttime = time.time()
                cube.recursive_solving(l)
                endtime = time.time()
                f.write(f"Time used: {endtime-starttime} seconds.\n")
            with open("results.csv", "a+") as f:
                writer = csv.writer(f)
                writer.writerow([v[-4], l, endtime-starttime])


if __name__ == "__main__":
    main()