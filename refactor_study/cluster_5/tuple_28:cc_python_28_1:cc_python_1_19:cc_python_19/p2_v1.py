# ########## PROGRAM: node_1:cc_python_1 ##########

from codebank import *

def main():
    n = read_int()
    MAX = 10 ** 9
    c = count_max_runs(read_str())
    for _ in range(n - 1):
        c = update_counts(c, read_str(), MAX)
    print(max(c.values()))

if __name__ == "__main__":
    main()