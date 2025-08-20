from codebank import *

def main():
    n = int(input())
    adj = read_tree(n)
    print(max_product_tree(adj))

if __name__ == "__main__":
    main()