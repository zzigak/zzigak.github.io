from codebank import *

def main():
    w, b = map(int, input().split())
    prob = compute_princess_prob(w, b)
    print(f"{prob:.9f}")

if __name__ == "__main__":
    main()