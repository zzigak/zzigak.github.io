from codebank import *

def main():
    X = [list(map(int, input().split())) for _ in range(10)]
    ladder_dest = build_ladder_dest(X)
    expected = compute_expectation(ladder_dest, dice_sides=6)
    print(expected[99])

if __name__ == "__main__":
    main()