# ==== RETRIEVED HELPER FUNCTIONS ====

# Selected Helper Functions

def read_str():
    """Read a full line string from input."""
    return input().strip()
# Selected because: the solution needs to read the input string s efficiently.


# Selected Helper Functions

def read_int():
    """Reads a single integer from input."""
    return int(input())

def read_str():
    """Reads a single string (line) from input."""
    return input().strip()


# Selected Helper Functions

def read_str():
    """Read a line as a stripped string from standard input."""
    return input().strip()
# Selected because: We need to read the input string for the single‐pass DP routine.


# ==== NEW HELPER FUNCTIONS ====
def read_str():
    """Reads a stripped line from input."""
    return input().strip()

def read_int():
    """Reads a single integer from input."""
    return int(input())

def truncate_str(s, max_len=10):
    """Truncates s to first 5+'...'+last 2 if len(s)>max_len."""
    return s if len(s)<=max_len else s[:5]+'...'+s[-2:]
