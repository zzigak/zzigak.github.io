from codebank import *

def main():
    u, v = map(int, input().split())
    res = find_array_for_xor_sum(u, v)
    if res is None:
        print(-1)
    else:
        print(len(res))
        if res:
            print(*res)

if __name__ == "__main__":
    main()