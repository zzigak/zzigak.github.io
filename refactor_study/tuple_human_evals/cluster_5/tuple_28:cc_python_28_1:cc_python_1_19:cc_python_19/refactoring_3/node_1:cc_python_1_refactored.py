from codebank import *

MAX_VAL = 10**9

def main():
    n = read_int()
    prev = count_max_runs(read_str())
    for _ in range(n - 1):
        prev = merge_beauty(prev, read_str(), MAX_VAL)
    print(max(prev.values()))

if __name__ == "__main__":
    main()