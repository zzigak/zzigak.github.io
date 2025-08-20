from codebank import *

def main():
    a, b = map(int, input().split())
    if a == b:
        print(0)
        return
    ca, a2, a3, a5 = decompose_number(a)
    cb, b2, b3, b5 = decompose_number(b)
    if ca != cb:
        print(-1)
    else:
        ops = abs(a2 - b2) + abs(a3 - b3) + abs(a5 - b5)
        print(ops)

if __name__ == "__main__":
    main()