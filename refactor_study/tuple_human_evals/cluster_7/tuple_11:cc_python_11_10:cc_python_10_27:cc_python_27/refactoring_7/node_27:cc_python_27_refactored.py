from codebank import *

def main():
    import sys
    input = sys.stdin.readline
    n = int(input())
    a = list(map(int, input().split()))
    if n <= 10:
        sol = solve_small(a)
        if sol is None:
            print("NO")
            return
        print("YES")
        print(len(sol))
        for op in sol:
            print(*op)
        return
    ops = []
    while len(a) > 10:
        l = len(a)
        last = a[-3:]
        if last == [1, 1, 1]:
            flip_positions(a, ops, [l-2, l-1, l])
        elif last == [1, 1, 0]:
            flip_positions(a, ops, [l-3, l-2, l-1])
            a[-4] ^= 1
        elif last == [1, 0, 1]:
            flip_positions(a, ops, [l-4, l-2, l])
            a[-5] ^= 1
        elif last == [0, 1, 1]:
            nxt = a[-6:-3]
            if nxt == [1, 1, 1]:
                flip_positions(a, ops, [l-8, l-4, l])
                flip_positions(a, ops, [l-5, l-3, l-1])
                a[-9] ^= 1
            elif nxt == [1, 1, 0]:
                flip_positions(a, ops, [l-8, l-4, l])
                flip_positions(a, ops, [l-9, l-5, l-1])
                a[-9] ^= 1; a[-10] ^= 1
            elif nxt == [1, 0, 1]:
                flip_positions(a, ops, [l-6, l-3, l])
                flip_positions(a, ops, [l-9, l-5, l-1])
                a[-7] ^= 1; a[-10] ^= 1
            elif nxt == [0, 1, 1]:
                flip_positions(a, ops, [l-6, l-3, l])
                flip_positions(a, ops, [l-7, l-4, l-1])
                a[-7] ^= 1; a[-8] ^= 1
            elif nxt == [1, 0, 0]:
                flip_positions(a, ops, [l-2, l-1, l])
                flip_positions(a, ops, [l-8, l-5, l-2])
                a[-9] ^= 1
            elif nxt == [0, 1, 0]:
                flip_positions(a, ops, [l-2, l-1, l])
                flip_positions(a, ops, [l-6, l-4, l-2])
                a[-7] ^= 1
            elif nxt == [0, 0, 1]:
                flip_positions(a, ops, [l-10, l-5, l])
                flip_positions(a, ops, [l-5, l-3, l-1])
                a[-11] ^= 1
            elif nxt == [0, 0, 0]:
                flip_positions(a, ops, [l-8, l-4, l])
                flip_positions(a, ops, [l-7, l-4, l-1])
                a[-9] ^= 1; a[-8] ^= 1
            a.pop(); a.pop(); a.pop()
            continue
        elif last == [1, 0, 0]:
            flip_positions(a, ops, [l-4, l-3, l-2])
            a[-5] ^= 1; a[-4] ^= 1
        elif last == [0, 1, 0]:
            flip_positions(a, ops, [l-5, l-3, l-1])
            a[-6] ^= 1; a[-4] ^= 1
        elif last == [0, 0, 1]:
            flip_positions(a, ops, [l-6, l-3, l])
            a[-7] ^= 1; a[-4] ^= 1
        a.pop(); a.pop(); a.pop()
    while len(a) < 8:
        a.append(0)
    sol = solve_small(a)
    total = ops + sol
    print("YES")
    print(len(total))
    for op in total:
        print(*op)

if __name__ == "__main__":
    main()