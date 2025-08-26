# ########## PROGRAM: node_14:cc_python_14 ##########

from codebank import count_subsets_by_size_and_sum, compute_expected_fail_first

def main():
    import sys
    data = sys.stdin.read().split()
    n = int(data[0])
    a = list(map(int, data[1:1+n]))
    p = int(data[1+n])
    if sum(a) <= p:
        print(n)
    else:
        print(compute_expected_fail_first(a, p))

if __name__ == "__main__":
    main()