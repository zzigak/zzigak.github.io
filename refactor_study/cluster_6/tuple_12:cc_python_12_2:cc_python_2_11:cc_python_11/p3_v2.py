# ########## PROGRAM: node_2:cc_python_2 ##########

from codebank import *

def main():
    x, y = map(int, input().split())
    z = 7 - max(x, y)
    num, den = simplify_fraction(z, 6)
    print(f"{num}/{den}")

if __name__ == "__main__":
    main()