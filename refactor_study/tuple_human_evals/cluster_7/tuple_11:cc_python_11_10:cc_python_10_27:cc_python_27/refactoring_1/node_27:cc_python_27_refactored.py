from codebank import *

def main():
    import sys
    input = sys.stdin.readline
    n = int(input())
    a = list(map(int, input().split()))
    if n <= 10:
        sol = find_small_operations(a[:])
        if sol is None:
            print("NO"); return
        print("YES"); print(len(sol))
        for x, y, z in sol:
            print(x, y, z)
        return
    operations = []
    while len(a) > 10:
        l = len(a)
        last = a[-3:]
        if last == [1, 1, 1]:
            operations.append([l - 2, l - 1, l])
        elif last == [1, 1, 0]:
            operations.append([l - 3, l - 2, l - 1])
            a[-4] ^= 1
        elif last == [1, 0, 1]:
            operations.append([l - 4, l - 2, l])
            a[-5] ^= 1
        elif last == [0, 1, 1]:
            nxt = a[-6:-3]
            if nxt == [1, 1, 1]:
                operations.append([l - 8, l - 4, l])
                operations.append([l - 5, l - 3, l - 1])
                a[-9] ^= 1
            elif nxt == [1, 1, 0]:
                operations.append([l - 8, l - 4, l])
                operations.append([l - 9, l - 5, l - 1])
                a[-9] ^= 1; a[-10] ^= 1
            elif nxt == [1, 0, 1]:
                operations.append([l - 6, l - 3, l])
                operations.append([l - 9, l - 5, l - 1])
                a[-7] ^= 1; a[-10] ^= 1
            elif nxt == [0, 1, 1]:
                operations.append([l - 6, l - 3, l])
                operations.append([l - 7, l - 4, l - 1])
                a[-7] ^= 1; a[-8] ^= 1
            elif nxt == [1, 0, 0]:
                operations.append([l - 2, l - 1, l])
                operations.append([l - 8, l - 5, l - 2])
                a[-9] ^= 1
            elif nxt == [0, 1, 0]:
                operations.append([l - 2, l - 1, l])
                operations.append([l - 6, l - 4, l - 2])
                a[-7] ^= 1
            elif nxt == [0, 0, 1]:
                operations.append([l - 10, l - 5, l])
                operations.append([l - 5, l - 3, l - 1])
                a[-11] ^= 1
            elif nxt == [0, 0, 0]:
                operations.append([l - 8, l - 4, l])
                operations.append([l - 7, l - 4, l - 1])
                a[-9] ^= 1; a[-8] ^= 1
        elif last == [1, 0, 0]:
            operations.append([l - 4, l - 3, l - 2])
            a[-5] ^= 1; a[-4] ^= 1
        elif last == [0, 1, 0]:
            operations.append([l - 5, l - 3, l - 1])
            a[-6] ^= 1; a[-4] ^= 1
        elif last == [0, 0, 1]:
            operations.append([l - 6, l - 3, l])
            a[-7] ^= 1; a[-4] ^= 1
        a.pop(); a.pop(); a.pop()
    while len(a) < 8:
        a.append(0)
    sol_small = find_small_operations(a)
    print("YES")
    sol = operations + sol_small
    print(len(sol))
    for x, y, z in sol:
        print(x, y, z)

if __name__ == "__main__":
    main()