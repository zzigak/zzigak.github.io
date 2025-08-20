from codebank import *

def main():
    X = [list(map(int,input().split())) for _ in range(10)]
    Y, Z = build_lattice_mappings()
    ladders = {}
    for i in range(100):
        r, c = Y[i]
        h = X[r][c]
        if h > 0:
            ladders[i] = Z[r-h][c]
    F = compute_expected_turns(ladders)
    print(F[99])

if __name__ == "__main__":
    main()