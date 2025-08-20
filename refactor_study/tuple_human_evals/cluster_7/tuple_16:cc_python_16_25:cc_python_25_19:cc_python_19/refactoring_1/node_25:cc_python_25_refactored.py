from codebank import *

def main():
    u, v = map(int, input().split())
    if u > v or ((v - u) & 1):
        print(-1)
    elif u == 0 and v == 0:
        print(0)
    elif u == v:
        print(1)
        print(u)
    else:
        w = (v - u) // 2
        if (w & u) == 0:
            d = u + w
            print(2)
            print(d, w)
        else:
            print(3)
            print(u, w, w)

if __name__ == "__main__":
    main()