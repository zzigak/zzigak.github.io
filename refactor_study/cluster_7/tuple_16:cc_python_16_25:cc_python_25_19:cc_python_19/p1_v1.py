# ########## PROGRAM: node_16:cc_python_16 ##########

from codebank import *

def main():
    import sys
    data = sys.stdin.readline()
    if not data:
        return
    n = int(data)
    perm, beauty = build_max_beauty_perm(n)
    print(beauty)
    print(*perm)

if __name__ == "__main__":
    main()