from codebank import *

def main():
    n = int(input())
    adj = read_tree(n)
    print(compute_max_product(adj))

if __name__ == "__main__":
    main()