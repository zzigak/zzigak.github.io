from codebank import *

def main():
    n = read_int()
    # parents for nodes 2..n, zero-based
    parents = [read_int()-1 for _ in range(n-1)]
    children = build_children(n, parents)
    for i in range(n):
        if children[i] and count_leaf_children(children, i) < 3:
            print("No")
            return
    print("Yes")

if __name__ == "__main__":
    main()