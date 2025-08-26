# Query for: node_27:cc_python_27
# =========================
"""
You are given an array a of length n that consists of zeros and ones.

You can perform the following operation multiple times. The operation consists of two steps: 

  1. Choose three integers 1 ≤ x < y < z ≤ n, that form an arithmetic progression (y - x = z - y). 
  2. Flip the values a_x, a_y, a_z (i.e. change 1 to 0, change 0 to 1). 



Determine if it is possible to make all elements of the array equal to zero. If yes, print the operations that lead the the all-zero state. Your solution should not contain more than (⌊ n/3 ⌋ + 12) operations. Here ⌊ q ⌋ denotes the number q rounded down. We can show that it is possible to make all elements equal to zero in no more than this number of operations whenever it is possible to do so at all.

Input

The first line contains a single integer n (3 ≤ n ≤ 10^5) — the length of the array.

The second line contains n integers a_1, a_2, …, a_n (0 ≤ a_i ≤ 1) — the elements of the array.

Output

Print "YES" (without quotes) if the answer exists, otherwise print "NO" (without quotes). You can print each letter in any case (upper or lower).

If there is an answer, in the second line print an integer m (0 ≤ m ≤ (⌊ n/3 ⌋ + 12)) — the number of operations in your answer.

After that in (i + 2)-th line print the i-th operations — the integers x_i, y_i, z_i. You can print them in arbitrary order.

Examples

Input

5
1 1 0 1 1


Output

YES
2
1 3 5
2 3 4


Input

3
0 1 0


Output

NO

Note

In the first sample the shown output corresponds to the following solution: 

  * 1 1 0 1 1 (initial state); 
  * 0 1 1 1 0 (the flipped positions are the first, the third and the fifth elements); 
  * 0 0 0 0 0 (the flipped positions are the second, the third and the fourth elements). 



Other answers are also possible. In this test the number of operations should not exceed ⌊ 5/3 ⌋ + 12 = 1 + 12 = 13.

In the second sample the only available operation is to flip all the elements. This way it is only possible to obtain the arrays 0 1 0 and 1 0 1, but it is impossible to make all elements equal to zero.
"""

# Original Problem: node_27:cc_python_27
# =========================
def solve(a):
    l = len(a)
    d = sum(a[i] * 2 ** i for i in range(l))
    if d == 0:
        return []
    usable = []
    if l >= 3:
        for i in range(l - 2):
            usable.append(0b111 << i)
    if l >= 5:
        for i in range(l - 4):
            usable.append(0b10101 << i)
    if l >= 7:
        for i in range(l - 6):
            usable.append(0b1001001 << i)
    ul = len(usable)
    best_answer = None
    for mask in range(1 << ul):
        start = 0
        clone = mask
        cnt = 0
        while clone:
            if clone % 2 == 1:
                start ^= usable[cnt]
            clone //= 2
            cnt += 1
        if start == d:
            answer = []
            clone = mask
            cnt = 0
            while clone:
                if clone % 2 == 1:
                    answer.append([])
                    used = usable[cnt]
                    cnt2 = 1
                    while used:
                        if used % 2 == 1:
                            answer[-1].append(cnt2)
                        cnt2 += 1
                        used //= 2
                clone //= 2
                cnt += 1
            if best_answer is None or len(best_answer) > len(answer):
                best_answer = answer
    return best_answer


if __name__ == '__main__':
    n = int(input())
    a = list(map(int, input().split()))
    if len(a) <= 10:
        sol = solve(a)
        if sol is None:
            print("NO")
            exit(0)
        print("YES")
        print(len(sol))
        for t in sol:
            print(' '.join(map(str, t)))
        exit(0)
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
                a[-9] ^= 1
                a[-10] ^= 1
            elif nxt == [1, 0, 1]:
                operations.append([l - 6, l - 3, l])
                operations.append([l - 9, l - 5, l - 1])
                a[-7] ^= 1
                a[-10] ^= 1
            elif nxt == [0, 1, 1]:
                operations.append([l - 6, l - 3, l])
                operations.append([l - 7, l - 4, l - 1])
                a[-7] ^= 1
                a[-8] ^= 1
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
                a[-9] ^= 1
                a[-8] ^= 1
            a.pop()
            a.pop()
            a.pop()
        elif last == [1, 0, 0]:
            operations.append([l - 4, l - 3, l - 2])
            a[-5] ^= 1
            a[-4] ^= 1
        elif last == [0, 1, 0]:
            operations.append([l - 5, l - 3, l - 1])
            a[-6] ^= 1
            a[-4] ^= 1
        elif last == [0, 0, 1]:
            operations.append([l - 6, l - 3, l])
            a[-7] ^= 1
            a[-4] ^= 1
        a.pop()
        a.pop()
        a.pop()
    while len(a) < 8:
        a.append(0)
    sol = solve(a)
    print("YES")
    sol = operations + sol
    print(len(sol))
    for t in sol:
        print(' '.join(map(str, t)))


# End of all problems.