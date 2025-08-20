from codebank import *

def main():
    import sys
    s = sys.stdin.readline().strip()
    res = find_longest_border(s)
    if res:
        print(res)
    else:
        print("Just a legend")

if __name__ == "__main__":
    main()