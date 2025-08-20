from codebank import *

def main():
    n = read_int()
    children = build_children_from_parents(n)
    print("Yes" if is_spruce(children) else "No")

if __name__ == "__main__":
    main()