# ########## PROGRAM: node_4:cc_python_4 ##########

from codebank import *

def main():
    n = int(input())
    points = [tuple(map(int, input().split())) for _ in range(n)]
    groups = group_lines(points)
    print(count_intersections(groups))

if __name__ == "__main__":
    main()