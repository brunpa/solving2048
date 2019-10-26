import random
import sys

from numpy import zeros, hstack

import game

# Author:				chrn (original by nneonneo)
# Date:				11.11.2016
# Description:			The logic of the AI to beat the game.

UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3
scores = [float(UP), float(DOWN), float(LEFT), float(RIGHT)]


def find_best_move(board):
    # Build a heuristic agent on your own that is much better than the random agent.
    # Your own agent don't have to beat the game.

    # Reset all scores to 0 to calculate the new values correctly
    reset_score(scores)

    # Initialize help-lists and help-variables
    max_tiles = [0, 0, 0, 0]
    amount_tiles = [0, 0, 0, 0]
    lower_right_corner_move = -1
    best_move = -1

    # Create new boards for each direction
    new_board_up = execute_move(UP, board)
    new_board_down = execute_move(DOWN, board)
    new_board_left = execute_move(LEFT, board)
    new_board_right = execute_move(RIGHT, board)

    # Check if the move in the direction UP, DOWN, LEFT or RIGHT is possible
    up_move_possible = control_if_move_is_possible(board, new_board_up)
    down_move_possible = control_if_move_is_possible(board, new_board_down)
    left_move_possible = control_if_move_is_possible(board, new_board_left)
    right_move_possible = control_if_move_is_possible(board, new_board_right)

    neighbor_scores = [0, 0, 0, 0]

    neighbor_scores[UP] = compare_neighbor_tile(new_board_up)
    neighbor_scores[DOWN] = compare_neighbor_tile(new_board_down)
    neighbor_scores[RIGHT] = compare_neighbor_tile(new_board_right)
    neighbor_scores[LEFT] = compare_neighbor_tile(new_board_left)

    scores[UP] = score_grid_value(new_board_up) * neighbor_scores[UP]
    scores[DOWN] = score_grid_value(new_board_down) * neighbor_scores[DOWN]
    scores[LEFT] = score_grid_value(new_board_left) * neighbor_scores[LEFT]
    scores[RIGHT] = score_grid_value(new_board_right) * neighbor_scores[RIGHT]

    best_move = scores.index(max(scores))
    best_score = max(scores)

    # Create a list of the best possible moves in a sequential order
    list_of_best_possible_moves = []

    if down_move_possible and best_score == scores[DOWN]:
        list_of_best_possible_moves.append(DOWN)

    if right_move_possible and best_score == scores[RIGHT]:
        list_of_best_possible_moves.append(RIGHT)

    if left_move_possible and best_score == scores[LEFT]:
        list_of_best_possible_moves.append(LEFT)

    if up_move_possible and best_score == scores[UP]:
        list_of_best_possible_moves.append(UP)

    """
    If the best move is not a valid move, choose the second best move. If a move is not a valid move, the score of that
    move will be set to -10 ^308, the smallest float representation possible in Python. 
    """

    if not down_move_possible:
        scores[DOWN] = -float('inf')

    if not right_move_possible:
        scores[RIGHT] = -float('inf')

    if not up_move_possible:
        scores[UP] = -float('inf')

    if not left_move_possible:
        scores[LEFT] = -float('inf')

    best_move = scores.index(max(scores))

    list_of_best_possible_moves.append(best_move)
    print("The best move is: ", list_of_best_possible_moves[0])

    return list_of_best_possible_moves[0]


def find_best_move_random_agent():
    return random.choice([UP, DOWN, LEFT, RIGHT])


def execute_move(move, board):
    """
    move and return the grid without a new random tile
    It won't affect the state of the game in the browser.
    """

    if move == UP:
        return game.merge_up(board)
    elif move == DOWN:
        return game.merge_down(board)
    elif move == LEFT:
        return game.merge_left(board)
    elif move == RIGHT:
        return game.merge_right(board)
    else:
        sys.exit("No valid move")


def board_equals(board, new_board):
    """
    Check if two boards are equal
    """
    return (new_board == board).all()


def count_tiles(board):
    """
    count all tiles with a valid number (>= 2)
    :param board: a game board
    :return: The number of tiles on the board
    """
    tiles_counter = 0
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] >= 2:
                tiles_counter += 1
    return tiles_counter


def calculate_min_amount_of_tiles_of_a_list(list_to_compare):
    """
    calculate the index with the minimum number of tiles in it
    :param list_to_compare: a list
    :return: the index of the list with the minimum of tiles
    """

    # Compare if LEFT is equal to DOWN or if LEFT is equal to RIGHT
    # if True, set LEFT = 100
    if list_to_compare[LEFT] == list_to_compare[DOWN] or list_to_compare[LEFT] == list_to_compare[RIGHT]:
        list_to_compare[LEFT] = 100
    # Compare if UP is equal to DOWN or if UP is equal to RIGHT
    # if True, set UP = 100
    if list_to_compare[UP] == list_to_compare[DOWN] or list_to_compare[UP] == list_to_compare[RIGHT]:
        list_to_compare[UP] = 100

    return list_to_compare.index(min(list_to_compare))


def calculate_max_tile(board):
    """
    Determines the tile with the highest value on a specific game board
    :param board: a game board
    :return: the value of the maximum tile
    """
    max_tile = 0
    for i in range(len(board)):
        for j in range(len(board[i])):
            max_tile = max(board[i][j], max_tile)
    return max_tile


def calculate_max_of_a_list(list_to_compare):
    """
    calculates the maximum of a specific list
    :param list_to_compare: list to compare
    :return: the index in which the maximum value is
    """
    # Compare if LEFT is equal to DOWN or if LEFT is equal to RIGHT
    # if True, set LEFT = 0
    if list_to_compare[LEFT] == list_to_compare[DOWN] or list_to_compare[LEFT] == list_to_compare[RIGHT]:
        list_to_compare[LEFT] = 0
    # Compare if UP is equal to DOWN or if UP is equal to RIGHT
    # if True, set UP = 0
    if list_to_compare[UP] == list_to_compare[DOWN] or list_to_compare[UP] == list_to_compare[RIGHT]:
        list_to_compare[UP] = 0
    return list_to_compare.index(max(list_to_compare))


def calculate_scores(max_tiles_index, amount_tiles_index, lower_right_corner_move):
    """
    calculates the score for each direction (UP, DOWN, LEFT, RIGHT) with a different weight
    :param max_tiles_index: the index (UP, DOWN, LEFT, RIGHT) with the maximum tile
    :param amount_tiles_index: the index (UP, DOWN, LEFT, RIGHT) with the minimum number of tiles
    :param lower_right_corner_move: if the lower right corner is free, the best direction to move
    :return: the index with the number of the biggest score
    """

    # Check where will get the maximum tile, and add 1 to the specific score
    for i in range(len(max_tiles_index)):
        if max_tiles_index == i:
            scores[i] = scores[i] + 1

    # Check where will get the minimum number of tiles, and add 2 to the specific score
    for i in range(len(amount_tiles_index)):
        if amount_tiles_index == i:
            scores[i] = scores[i] + 3

    # If the lower right corner is free, add 3 to DOWN or RIGHT
    if lower_right_corner_move == DOWN:
        scores[DOWN] = scores[DOWN] + 3
    elif lower_right_corner_move == RIGHT:
        scores[RIGHT] = scores[RIGHT] + 3

    # Compare if LEFT is equal to DOWN or if LEFT is equal to RIGHT
    # if True, set LEFT = 0
    if scores[LEFT] == scores[DOWN] or scores[LEFT] == scores[RIGHT]:
        scores[LEFT] = 0
    # Compare if UP is equal to DOWN or if UP is equal to RIGHT
    # if True, set UP = 0
    if scores[UP] == scores[DOWN] or scores[UP] == scores[RIGHT]:
        scores[UP] = 0

    # Compare if UP is bigger or equal to LEFT
    # if True, set UP = 0
    # in that case we can make sure, that UP will one be the best score, if there is not possible to move to
    # any other direction
    if scores[UP] >= scores[LEFT]:
        scores[UP] = 0

    return scores.index(max(scores))


def control_if_move_is_possible(board, new_board):
    """
    check if the next move is an valid move
    :param board: current board
    :param new_board: board after the next move
    :return: True if boards aren't equal.  False if the boards equal
    """
    if board_equals(board, new_board):
        return False
    else:
        return True


def reset_score(score_list):
    """
    Set the score list to the initial values (=0)
    :param score_list: list with all scores in it
    """
    for i in range(len(score_list)):
        score_list[i] = -float('inf')


def is_lower_right_corner_free(board):
    """
    Check if lower right corner is free
    :param board: board to check
    :return: True, if lower right corner is empty. False, if lower right corner is occupied
    """
    if board[3][3] >= 2:
        return False
    else:
        return True


def find_best_move_if_lower_right_corner_free(board):
    """
    Determine the best move to place a tile in the lower right corner
    :param board: board to check
    :return: DOWN if DOWN is the best move. RIGHT if RIGHT is the best move
    """
    # Find first value in the lowest row started from the right side
    first_value_row = 0
    last_row = board[3]
    last_row_reversed = last_row[::-1]
    for i in range(len(last_row_reversed)):
        if board[3][i] >= 2:
            first_value_row = board[3][i]
            break

    # Find first value in the right column started from the bottom side
    first_value_column = 0
    last_column = [row[-1] for row in board]
    last_column_reversed = last_column[::-1]
    # print("last_column: ", last_column, "last_column_reversed: ", last_column_reversed)
    for i in range(len(last_column_reversed)):
        if last_column_reversed[i] >= 2:
            first_value_column = last_column_reversed[i]
            break

    # Compare first_value_row with first_value_column
    higher_number = max(first_value_row, first_value_column)

    if higher_number == first_value_column:
        return DOWN
    elif higher_number == first_value_row:
        return RIGHT


def score_grid_value(new_board):
    """
    Determine a score for the new board based on a weighted 4x4 grid
    :return: The total sum of all tiles multiplied with their respective weights
    """

    # weight = [0, 1, 1, 10, 1, 50, 100, 250, 50, 100, 250, 400, 100, 250, 400, 800]
    # weight = [20, 50, 450, 500, 10, 100, 400, 600, 5, 200, 350, 700, 0, 300, 350, 800]
    # weight = [0, 0, 50, 200, 0, 100, 400, 600, 5, 200, 450, 700, 200, 300, 650, 800]
    # weight = [0, 0, 50, 200, 0, 100, 400, 450, 5, 200, 450, 600, 200, 300, 600, 1000]
    weight = [0, 0, 5, 20, 0, 10, 40, 45, 5, 20, 45, 60, 20, 30, 60, 100]
    # weight = [
    #     0, 0, 0, 100,
    #     0, 0, 0, 60,
    #     0, 0, 0, 40,
    #     0, 0, 0, 20
    # ]
    # weight = [-1000, -500, -125, -250, -100, 25, -150, -75, 75, 150, -25, 100, 250, 125, 500, 1000]
    # weight = [100, 50, 12, 25, 10, 250, 150, 75, 750, 1500, 25, 1000, 2500, 1250, 5000, 10000]
    # Initialize score grid array with zeros
    score_grid_array = zeros([4, 4])

    # Helper variable to access the weight with the correct index in the loop
    index = 16

    # Initialize score_grid_array with weights
    for i in range(len(score_grid_array)):
        for j in range(len(score_grid_array)):
            score_grid_array[i][j] = weight[len(weight) - index]
            index -= 1
            if index <= 0:
                break
        # Additional check to ensure the program exits the second loop once the score_grid_array is initialized
        if index <= 0:
            break

    # Determine score_grid_value
    score_grid_value_array = zeros([4, 4])
    for i in range(len(score_grid_value_array)):
        for j in range(len(score_grid_value_array)):
            score_grid_value_array[i][j] = score_grid_array[i][j] * new_board[i][j]

    # Calculate total sum of score_grid_value
    score = 0
    for i in range(len(score_grid_value_array)):
        for j in range(len(score_grid_value_array)):
            score += score_grid_value_array[i][j]

    print("Score Grid Value is: ", score)
    return score


def compare_neighbor_tile(board):
    return (score_count_neighbor(board) + score_mean_neighbor(board)) / 2


def score_snake(board, base=0.3):
    score = 0
    rewardArray = [base ** i for i in range(16)]
    for i in range(2):
        boardArray = hstack((board[0], board[1][::-1], board[2], board[3][::-1]))
        score = max(score, (rewardArray * boardArray).sum())
        score = max(score, (rewardArray[::-1] * boardArray).sum())
        boardArray = hstack((board[0][::-1], board[1], board[2][::-1], board[3]))
        score = max(score, (rewardArray * boardArray).sum())
        score = max(score, (rewardArray[::-1] * boardArray).sum())
        board = board.T
    return score


def score_mean_neighbor(newBoard):
    horizontal_sum, count_horizontal = check_neighbor(newBoard)
    vertical_sum, count_vertical = check_neighbor(newBoard.T)
    if count_horizontal == 0 or count_vertical == 0:
        return 0
    return horizontal_sum / count_horizontal + vertical_sum / count_vertical


def check_neighbor(board):
    """
    Returns the sum and total number (count) of tiles that are placed next to each other on the board with the same values.
    """
    count = 0
    sum = 0
    for row in board:
        previous = -1
        for tile in row:
            if previous == tile:
                sum += tile
                count += 1
            previous = tile
    return sum, count


def score_count_neighbor(board):
    _, horizontal_count = check_neighbor(board)
    _, vertical_count = check_neighbor(board.T)
    return horizontal_count + vertical_count
