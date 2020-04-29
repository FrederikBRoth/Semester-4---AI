def alpha_beta_decision(state):
    infinity = float('inf')

    def max_value(state, alpha, beta):
        if is_terminal(state, False):
            return utility_of(state, False)
        v = -infinity
        for (a, successor) in successors_of(state):
            v = max(v, min_value(successor, alpha, beta))
            if v >= beta:
                return v
            alpha = min(alpha, v)
        return v

    def min_value(state, alpha, beta):
        if is_terminal(state, True):
            return utility_of(state, True)
        v = infinity

        for (a, successor) in successors_of(state):
            v = min(v, max_value(successor, alpha, beta))
            if v <= alpha:
                return v
            beta = max(beta, v)
        return v

    action, state = argmin(successors_of(state), lambda a: max_value(a[1], infinity, -infinity))
    return action


def is_terminal(state, player=True):
    """
    returns True if the state is either a win or a tie (board full)
    :param state: State of the checkerboard. Ex: [0; 1; 2; 3; X; 5; 6; 7; 8]
    :return:
    """
    if utility_of(state, player) != 0:
        return True
    else:
        return False


def utility_of(state, player):
    """
    returns +1 if winner is X (MAX player), -1 if winner is O (MIN player), or 0 otherwise
    :param state: State of the checkerboard. Ex: [0; 1; 2; 3; X; 5; 6; 7; 8]
    :return:
    """
    player1 = player
    if len(successors_of(state)) == 0:
        if player:
            return -1
        else:
            return 1

    return 0


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
            if partition[0] == partition[1]:
                continue
            move.append(partition[0])
            move.append(partition[1])
            move.sort(reverse=True)
            successors.append((count, move))
            count += 1
    return successors


def new_board(board, index):
    count = 0
    move = []
    for partition in sum_to_n(board[index], 2):
        move = board.copy()
        move.pop(index)
        if partition[0] == partition[1]:
            count += 1
            continue
        move.append(partition[0])
        move.append(partition[1])
        move.sort(reverse=True)
        count += 1
    return move


def check_board_moves(state):
    moves_left = 0
    for tile in state:
        if tile != "X" and tile != "O":
            moves_left += 1
    return moves_left


def main():
    player = bool()
    board = [15]
    while not is_terminal(board, False):
        player = False
        board = new_board(board, alpha_beta_decision(board))
        if not is_terminal(board, True):
            player = True
            print(board)
            input_str = input('Your move? ');
            input_list = input_str.split(" ")
            for i in range(0, len(input_list)):
                input_list[i] = int(input_list[i])
            board = input_list.copy()
    if is_terminal(board):
        if player:
            print("player won!")
        else:
            print("computer won!")
    print(board)


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


def argmax(iterable, func):
    return max(iterable, key=func)


def argmin(iterable, func):
    return min(iterable, key=func)


if __name__ == '__main__':
    main()
