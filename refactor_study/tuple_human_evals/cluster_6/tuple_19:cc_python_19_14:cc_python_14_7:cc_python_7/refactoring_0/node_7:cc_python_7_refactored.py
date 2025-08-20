from codebank import *

def main():
    board = [list(map(int, input().split())) for _ in range(10)]
    lj = build_ladder_jump(board)
    E = expected_turns(lj)
    print(E[-1])

if __name__ == "__main__":
    main()