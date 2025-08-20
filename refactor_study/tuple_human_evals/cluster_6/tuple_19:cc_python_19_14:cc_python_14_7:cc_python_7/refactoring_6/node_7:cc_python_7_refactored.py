from codebank import generate_path_mappings, build_ladder_jump, expected_turns

def main():
    import sys
    ladders = [list(map(int, sys.stdin.readline().split())) for _ in range(10)]
    Y, Z = generate_path_mappings()
    jump = build_ladder_jump(ladders, Y, Z)
    print(expected_turns(jump))

if __name__ == "__main__":
    main()