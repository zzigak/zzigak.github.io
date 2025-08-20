from codebank import *

def main():
    u, v = map(int, input().split())
    if u > v or (v - u) & 1:
        print(-1)
    elif u == v:
        if u == 0:
            print(0)
        else:
            print(1)
            print(u)
    else:
        diff = (v - u) // 2
        if diff & u == 0:
            print(2)
            print(diff + u, diff)
        else:
            print(3)
            print(u, diff, diff)

if __name__ == "__main__":
    main()