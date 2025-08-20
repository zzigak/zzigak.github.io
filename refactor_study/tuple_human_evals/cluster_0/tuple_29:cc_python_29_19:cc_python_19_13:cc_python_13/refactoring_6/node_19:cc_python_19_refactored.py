from codebank import *

def main():
    import sys
    input=sys.stdin.readline
    n=int(input())
    parents=[int(input())-1 for _ in range(n-1)]
    children=build_children(n, parents)
    for ch in children:
        if ch and sum(1 for c in ch if not children[c])<3:
            print("No")
            return
    print("Yes")

if __name__=="__main__":
    main()