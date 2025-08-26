# ########## LIBRARY HELPERS ##########

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

# ==== NEW HELPER FUNCTIONS ====
def truncate_str(s, max_len=10):
    """Truncates s to first 5+'...'+last 2 if len(s)>max_len."""
    return s if len(s)<=max_len else s[:5]+'...'+s[-2:]


# ########################################
#
