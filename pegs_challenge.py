import time, sys, itertools, argparse

class SolutionException(Exception):
    def __init__(self, history):
        self.history = history

def main(args = None):
    global TRI_SIZE, triangle, jump_lookup
    start = time.time()

    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser()
    parser.add_argument('--size', type=int, default=5, dest='size',
                        help='The size of the triangle. Defaults to 5, the size of the original puzzle. Should be >= 5.')
    parser.add_argument('start_position', type=lambda s: tuple(map(int, s.split(","))),
                        help='The initial empty spot as a (row, peg) tuple, where row 0 is at the top and pegs start at 0 going from the left.')
    parsed_args = parser.parse_args(args)

    start_row, start_peg = parsed_args.start_position
    TRI_SIZE = parsed_args.size

    # Constructs the triangle, a 2D jagged array of booleans
    triangle = [[True] * i for i in range(1, TRI_SIZE + 1)]
    triangle[start_row][start_peg] = False

    # Construct a dictionary which maps a (row, peg) tuple : a list of locations that can be jumped to from there
    jump_lookup = {
                    (row, peg) : [
                                    (row + Δrow, peg + Δpeg) for Δrow, Δpeg in itertools.product([-2, 0, 2], [-2, 0, 2])
                                    if is_valid(row + Δrow, peg + Δpeg)
                                    and (Δrow != -2 or Δpeg != 2)
                                    and (Δrow, Δpeg) != (0, 0)
                                 ]
                    for row, peg in itertools.product(range(TRI_SIZE), range(TRI_SIZE))
                  }

    # Run the search algorithm, which raises a StopIteration exception when it finds something.
    try:
        search(triangle)
    except SolutionException as solution:
        print_history(solution.history)

    print(time.time() - start)

def is_valid(row, peg):
    """
    Checks a row & peg combination to see if it refers to a real place in the triangle.
    """
    return (
                (row < TRI_SIZE) and
                (row >= 0) and
                (peg < TRI_SIZE) and
                (peg >= 0) and
                (peg <= row)
            )

def copy_triangle(tri):
    """
    Returns a copy of the triangle (faster than deepcopy).
    """
    return [[peg for peg in row] for row in tri]

def print_triangle(tri):
    """
    Pretty-prints the triangle.
    """
    for i in range(TRI_SIZE):
        for _ in range(TRI_SIZE - i): print(" ", end='')
        for peg in range(len(tri[i])):
            print("x" if tri[i][peg] else "o", "", end='')
        print()

def jump(tri, A, B, C):
    """
    Performs a jump between an occupied (row, peg) tuple A and an unoccupied C, passing over B.
    If anything is bad with the jump, returns False; otherwise returns True.
    """
    start_row, start_peg = A
    mid_row, mid_peg = B
    end_row, end_peg = C

    # Check to make sure A is occupied and B is clear
    if tri[start_row][start_peg] == False: return False
    if tri[end_row][end_peg]: return False

    # Make sure we're jumping over an occupied space.
    if tri[mid_row][mid_peg] == False: return False
    
    # Clear B, clear A and set C
    tri[mid_row][mid_peg] = False
    tri[start_row][start_peg] = False
    tri[end_row][end_peg] = True

    return True

def mid(start_row, start_peg, end_row, end_peg):
    """
    Returns a (mid_row, mid_peg) tuple between (start_row, start_peg) and (end_row, end_peg).
    """
    if start_row + 2 == end_row:
        mid_row = start_row + 1
    elif start_row == end_row + 2:
        mid_row = start_row - 1
    elif start_row == end_row:
        mid_row = start_row

    if start_peg + 2 == end_peg:
        mid_peg = start_peg + 1
    elif start_peg == end_peg + 2:
        mid_peg = start_peg - 1
    elif start_peg == end_peg:
        mid_peg = start_peg

    return (mid_row, mid_peg)

def print_history(hist):
    """
    Prints out the history of states.
    """
    print_triangle(triangle)
    for past_triangle in hist:
        print_triangle(past_triangle)

    print()

def search(tri, history = []):
    """
    Searches, using recursive backtracking.
    """
    count = 0
    children = []

    for start_row in range(len(tri)):
        for start_peg in range(len(tri[start_row])):
            if tri[start_row][start_peg] == True:
                count += 1

                for end_row, end_peg in jump_lookup[(start_row, start_peg)]:
                    if tri[end_row][end_peg] == False:

                        mid_row, mid_peg = mid(start_row, start_peg, end_row, end_peg)
                        if (tri[mid_row][mid_peg] == True):

                            new_tri = copy_triangle(tri)
                            jump(new_tri, (start_row, start_peg), (mid_row, mid_peg), (end_row, end_peg))

                            children.append(new_tri)

    if children:
        return min([search(new_tri, history=history + [new_tri]) for new_tri in children])

    else:
        if count <= 1:
            raise SolutionException(history)

        return count


if __name__ == "__main__":
    main()