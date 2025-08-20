from codebank import *

def main():
    grid = [list(map(int, input().split())) for _ in range(10)]
    result = expected_turns(grid)
    print(result)

if __name__ == "__main__":
    main()