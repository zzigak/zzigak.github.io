from codebank import *

def main():
    n = int(input())
    points = [tuple(map(int, input().split())) for _ in range(n)]
    line_counts = count_line_groups(points)
    result = count_intersections(line_counts)
    print(result)

if __name__ == "__main__":
    main()