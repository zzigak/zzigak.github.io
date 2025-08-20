from codebank import *

def main():
    n = read_int()
    MAX = 10**9
    # first string
    c = get_run_max(read_str())
    # merge successive strings
    for _ in range(n - 1):
        t = read_str()
        c = merge_counts(c, t, MAX)
    # beauty is max run count
    print(max(c.values()))

if __name__ == "__main__":
    main()