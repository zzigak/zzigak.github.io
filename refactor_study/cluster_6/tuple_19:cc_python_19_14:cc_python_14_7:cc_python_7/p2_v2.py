# ########## PROGRAM: node_19:cc_python_19 ##########

from codebank import build_prefix_dp, compute_expectation_from_prefix_dp

def main():
    import sys
    data = sys.stdin.read().split()
    n = int(data[0])
    arr = list(map(int, data[1:1+n]))
    p = int(data[1+n])
    dp = build_prefix_dp(arr, p)
    print(compute_expectation_from_prefix_dp(dp, n, p))

if __name__ == "__main__":
    main()