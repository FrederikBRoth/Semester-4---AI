def sum_to_n(n, size, limit=None):
    if size == 1:
        yield [n]
        return
    if limit is None:
        limit = n
    start = (n + size - 1) // size
    stop = min(limit, n - size + 1) + 1
    for i in range(start, stop):
        for tail in sum_to_n(n - i, size - 1, i):
            yield [i] + tail


def successors_of(state):
    """
    returns a list of tuples (move, state) as shown in the exercise slides
    :param state: State of the checkerboard. Ex: [0; 1; 2; 3; X; 5; 6; 7; 8]
    :return:
    """
    successors = list()
    count = 0
    for index, number in enumerate(state):
        for partition in sum_to_n(number, 2):
            move = state.copy()
            move.pop(index)
            move.append(partition[0])
            move.append(partition[1])
            print(move)
            move.sort(reverse=True)
            successors.append((count, move))
            count += 1


    for succ in successors:
        print(succ)

successors_of([10, 5, 2, 5])