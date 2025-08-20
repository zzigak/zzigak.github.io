from codebank import *

def main():
    import sys
    board = [list(map(int, line.split())) for line in sys.stdin]
    idx_to_rc, rc_to_idx = build_path_mappings()
    E = compute_expected_turns(board, idx_to_rc, rc_to_idx)
    print("{:.10f}".format(E[0]))

if __name__ == "__main__":
    main()