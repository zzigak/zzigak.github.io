from codebank import *

def main():
    n = int(input())
    points = [tuple(map(int, input().split())) for _ in range(n)]
    lines = get_lines(points)
    print(count_intersections(lines))

if __name__ == "__main__":
    main()