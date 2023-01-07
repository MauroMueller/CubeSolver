def sorting_function(line):
    listline = line.split(",")
    return int(listline[0]), int(listline[1])


def sort_results():
    with open("results.csv") as f:
        lines = f.readlines()

    lines.sort(key=sorting_function)

    with open("results_sorted_2.csv", "w+") as f:
        f.writelines(lines)

if __name__ == "__main__":
    sort_results()
