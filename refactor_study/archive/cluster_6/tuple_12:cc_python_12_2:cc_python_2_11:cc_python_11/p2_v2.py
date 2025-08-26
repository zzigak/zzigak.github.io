# ########## PROGRAM: node_12:cc_python_12 ##########

from codebank import *

def main():
    w, b = map(int, input().split())
    prob = get_princess_win_prob(w, b)
    print(f"{prob:.9f}")

if __name__ == "__main__":
    main()