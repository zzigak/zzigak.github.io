from codebank import *

def main():
    k, n, m = read_ints()
    a = read_ints()
    improvements = []
    for idx in range(1, n+1):
        t, i, b = read_ints()
        improvements.append((t, i, b, idx))
    res = select_best_improvements(k, m, a, improvements)
    print(len(res))
    if res:
        print(*res)

if __name__ == "__main__":
    main()