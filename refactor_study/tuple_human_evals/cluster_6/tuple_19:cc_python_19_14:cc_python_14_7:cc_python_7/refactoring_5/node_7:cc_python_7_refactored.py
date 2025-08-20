from codebank import *

def main():
    import sys
    X = [list(map(int, sys.stdin.readline().split())) for _ in range(10)]
    print(expected_turns(X))

if __name__ == "__main__":
    main()