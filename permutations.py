def deleted(s, i):
    """
    Returns the string s with the character at index i deleted.
    """
    return s[:i] + s[i+1:]

def permutations(s):
    """
    Returns a list containing all permutations of string s.
    """
    if len(s) == 1:
        return [s]

    # For each char, delete it, take all the remaining permutations,
    # and append it onto each of them.
    return [char + substr
            for i, char in enumerate(s)
            for substr in permutations(deleted(s, i))]

if __name__ == "__main__":
    print(permutations("cat"))