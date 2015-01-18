def chunks(l, n):
    """
    Yields chunks of size n from the list l.
    """
    for i in range(0, len(l), n):
        yield l[i: i+n]