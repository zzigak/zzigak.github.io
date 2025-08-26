# ########## PROGRAM: node_15:cc_python_15 ##########

from codebank import *

def main():
    mod = 10**9 + 7
    n = int(input())
    print(count_max_gcd_perms(n, mod))

if __name__ == "__main__":
    main()