def minmax_decision(state):
    def max_value(state):
        if is_terminal(state):
            return utility_of(state)
        v = -infinity
        for (a, s) in successors_of(state, False):
            v = max(v, min_value(s))
        print('V: ' + str(v))
        return v

    def min_value(state):
        if is_terminal(state):
            return utility_of(state)
        v = infinity
        for (a, s) in successors_of(state, True):
            v = min(v, max_value(s))
        return v

    infinity = float('inf')
    action, state = argmax(successors_of(state, False), lambda a: min_value(a[1]))
    print(action)
    return action


def is_terminal(state):
    """
    returns True if the state is either a win or a tie (board full)
    :param state: State of the checkerboard. Ex: [0; 1; 2; 3; X; 5; 6; 7; 8]
    :return:
    """
    if utility_of(state) != 0 or check_board_moves(state) == 0:
        return True
    else:
        return False


def utility_of(state):
    """
    returns +1 if winner is X (MAX player), -1 if winner is O (MIN player), or 0 otherwise
    :param state: State of the checkerboard. Ex: [0; 1; 2; 3; X; 5; 6; 7; 8]
    :return:
    """
    wins = win_conditions(state)
    for win in wins:
        if win == ("X", "X", "X"):

            return 1
        elif win == ("O", "O", "O"):
            return -1
    return 0


def successors_of(state, player):
    """
    returns a list of tuples (move, state) as shown in the exercise slides
    :param state: State of the checkerboard. Ex: [0; 1; 2; 3; X; 5; 6; 7; 8]
    :return:
    """
    count = 0
    list_index = 0
    successors = list()
    for tile in state:
        if tile != "X" and tile != "O":
            move = state.copy()
            if not player:
                move[list_index] = "X"
            else:
                move[list_index] = "O"
            successors.append((count, move))
        list_index += 1
        count += 1
    return successors



def win_conditions(state):
    wins = [(state[0], state[1], state[2]), (state[3], state[4], state[5]),
            (state[6], state[7], state[8]), (state[0], state[3], state[6]),
            (state[1], state[4], state[7]), (state[2], state[5], state[8]),
            (state[0], state[4], state[8]), (state[6], state[4], state[2])]
    return wins


def check_board_moves(state):
    moves_left = 0
    for tile in state:
        if tile != "X" and tile != "O":
            moves_left += 1
    return moves_left


def display(state):
    print("-----")
    for c in [0, 3, 6]:
        print(state[c + 0], state[c + 1], state[c + 2])


def main():
    board = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    while not is_terminal(board):
        board[minmax_decision(board)] = 'X'
        if not is_terminal(board):
            display(board)
            board[int(input('Your move? '))] = 'O'
    display(board)


def argmax(iterable, func):
    return max(iterable, key=func)


if __name__ == '__main__':
    main()
