from codebank import *

def main():
    import sys
    input = sys.stdin.readline
    n = int(input())
    a = list(map(int, input().split()))
    ops = []
    if n <= 10:
        res = brute_solve_small(a)
        if res is None:
            print("NO"); return
        print("YES"); print(len(res))
        for x,y,z in res:
            print(x, y, z)
        return
    while len(a) > 10:
        l = len(a)
        last = a[-3:]
        if last == [1,1,1]:
            ops.append((l-2, l-1, l))
        elif last == [1,1,0]:
            ops.append((l-3, l-2, l-1)); a[-4] ^= 1
        elif last == [1,0,1]:
            ops.append((l-4, l-2, l)); a[-5] ^= 1
        elif last == [0,1,1]:
            nxt = a[-6:-3]
            if nxt == [1,1,1]:
                ops.append((l-8,l-4,l)); ops.append((l-5,l-3,l-1)); a[-9] ^= 1
            elif nxt == [1,1,0]:
                ops.append((l-8,l-4,l)); ops.append((l-9,l-5,l-1)); a[-9] ^= 1; a[-10] ^= 1
            elif nxt == [1,0,1]:
                ops.append((l-6,l-3,l)); ops.append((l-9,l-5,l-1)); a[-7] ^= 1; a[-10] ^= 1
            elif nxt == [0,1,1]:
                ops.append((l-6,l-3,l)); ops.append((l-7,l-4,l-1)); a[-7] ^= 1; a[-8] ^= 1
            elif nxt == [1,0,0]:
                ops.append((l-2,l-1,l)); ops.append((l-8,l-5,l-2)); a[-9] ^= 1
            elif nxt == [0,1,0]:
                ops.append((l-2,l-1,l)); ops.append((l-6,l-4,l-2)); a[-7] ^= 1
            elif nxt == [0,0,1]:
                ops.append((l-10,l-5,l)); ops.append((l-5,l-3,l-1)); a[-11] ^= 1
            elif nxt == [0,0,0]:
                ops.append((l-8,l-4,l)); ops.append((l-7,l-4,l-1)); a[-9] ^= 1; a[-8] ^= 1
            a.pop(); a.pop(); a.pop()
            continue
        elif last == [1,0,0]:
            ops.append((l-4,l-3,l-2)); a[-5] ^= 1; a[-4] ^= 1
        elif last == [0,1,0]:
            ops.append((l-5,l-3,l-1)); a[-6] ^= 1; a[-4] ^= 1
        elif last == [0,0,1]:
            ops.append((l-6,l-3,l)); a[-7] ^= 1; a[-4] ^= 1
        a.pop(); a.pop(); a.pop()
    res = brute_solve_small(a)
    print("YES")
    sol = ops + (res or [])
    print(len(sol))
    for x,y,z in sol:
        print(x, y, z)

if __name__ == "__main__":
    main()