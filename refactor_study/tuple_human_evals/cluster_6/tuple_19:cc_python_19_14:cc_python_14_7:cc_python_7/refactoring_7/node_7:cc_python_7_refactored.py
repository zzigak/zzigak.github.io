from codebank import *

def main():
    ladders = [list(map(int, input().split())) for _ in range(10)]
    result = compute_min_expected(ladders)
    print("{:.10f}".format(result))

if __name__ == "__main__":
    main()