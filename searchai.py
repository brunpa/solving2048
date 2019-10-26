import sys
from copy import deepcopy

from numpy import ndindex

import game
import heuristicai as heuristic

# Author:      chrn (original by nneonneo)
# Date:        11.11.2016
# Copyright:   Algorithm from https://github.com/nneonneo/2048-ai
# Description: The logic to beat the game. Based on expectimax algorithm.


UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3
move_args = [UP, DOWN, LEFT, RIGHT]
scores = [float(UP), float(DOWN), float(LEFT), float(RIGHT)]


def find_best_move(board):
    """
    find the best move for the next turn.
    """
    bestmove = -1
    print("find_best_move called")
    result = [score_toplevel_move(i, board) for i in range(len(move_args))]
    print("result set got returned with values: ", result)
    # bestmove = result.index(max(result))

    best_score = max(result)

    # Create new boards for each direction
    new_board_up = execute_move(UP, board)
    new_board_down = execute_move(DOWN, board)
    new_board_left = execute_move(LEFT, board)
    new_board_right = execute_move(RIGHT, board)

    # Check if the move in the direction UP, DOWN, LEFT or RIGHT is possible
    up_move_possible = heuristic.control_if_move_is_possible(board, new_board_up)
    down_move_possible = heuristic.control_if_move_is_possible(board, new_board_down)
    left_move_possible = heuristic.control_if_move_is_possible(board, new_board_left)
    right_move_possible = heuristic.control_if_move_is_possible(board, new_board_right)

    # Create a list of the best possible moves in a sequential order
    list_of_best_possible_moves = []

    # if down_move_possible and best_score == result[DOWN]:
    #     list_of_best_possible_moves.append(DOWN)
    #
    # if right_move_possible and best_score == result[RIGHT]:
    #     list_of_best_possible_moves.append(RIGHT)
    #
    # if left_move_possible and best_score == result[LEFT]:
    #     list_of_best_possible_moves.append(LEFT)
    #
    # if up_move_possible and best_score == result[UP]:
    #     list_of_best_possible_moves.append(UP)

    """
    If the best move is not a valid move, choose the second best move. If a move is not a valid move, the score of that
    move will be set to -10 ^308, the smallest float representation possible in Python. 
    """

    if not down_move_possible:
        result[DOWN] = -float('inf')

    if not right_move_possible:
        result[RIGHT] = -float('inf')

    if not up_move_possible:
        result[UP] = -float('inf')

    if not left_move_possible:
        result[LEFT] = -float('inf')

    # best_move = scores.index(max(scores))

    best_move = result.index(max(result))

    list_of_best_possible_moves.append(best_move)

    # bestmove = list_of_best_possible_moves[0]

    for m in move_args:
        print("move: %d score: %.4f" % (m, result[m]))
    # print("The best move is: ", bestmove)
    print("The best move is: ", list_of_best_possible_moves[0])
    # return bestmove
    return list_of_best_possible_moves[0]


def score_toplevel_move(move, board):
    """
    Entry Point to score the first move.
    """
    print("score_toplevel_move called\n")
    print("Move: ", move, "\nBoard: \n", board)
    newboard = execute_move(move, board)

    if board_equals(board, newboard):
        print("The move", move, "is not valid.")
        return 0
    else:
        print("In else branch of score_toplevel_move")
        # Start the recursion
        if calculate_empty_tiles(newboard) <= 5:
            return expectimax(newboard, 4)
        else:
            return expectimax(newboard, 2)


def execute_move(move, board):
    """
    move and return the grid without a new random tile
	It won't affect the state of the game in the browser.
    """

    UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3

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


def board_equals(board, newboard):
    """
    Check if two boards are equal
    """
    return (newboard == board).all()


def amount_of_empty_board_fields(board):
    """
    Returns a list with the indices of the empty board fields
    """
    empty_board_fields_counter = 0
    list_with_indices_of_empty_fields = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 0:
                empty_board_fields_counter += 1
                list_with_indices_of_empty_fields.append([i, j])
    return list_with_indices_of_empty_fields


def game_over(board):
    """
    Check if the game state is game over
    :param board:
    :return: True, if the game is over
    """
    for i in range(len(move_args)):
        print("Game Over called. i is: ", i)
        new_board = execute_move(i, board)
        if not board_equals(board, new_board):
            return False
    return True


def expectimax(board, depth, turnHeuristics=False):
    print("Expectimax called")
    # When you reach the leaf calculate the board score
    if depth == 0 or (turnHeuristics and game_over(board)):
        print("In depth==0 branch of expectimax with depth", depth)
        return calculate_board_score(board)

    # Take the valid move that maximises the score
    score = calculate_board_score(board)
    if turnHeuristics:
        print(" in turnHeuristics with depth", depth)
        for action in range(len(move_args)):
            print("The action is: ", action)
            child = execute_move(action, board)
            # Check if the move was a valid move
            if not board_equals(board, child):
                return max(score, expectimax(child, depth - 1, False))
            else:
                return score

    # When you don't reach the last depth, get all possible board states and calculate their scores dependence of the
    # probability this will occur. (recursively)
    else:
        print("In else branch of expectimax with depth", depth)
        score = 0
        print("After alpha=0 in else branch of expectimax")
        probability = 1 / (calculate_empty_tiles(board)) if calculate_empty_tiles(board) > 0 else 0
        for i, j in ndindex(board.shape):
            current_score = 0
            if board[i, j] == 0:
                c1 = deepcopy(board)
                c1[i, j] = 2
                print("c1 is: \n")
                print(c1)
                score += 0.9 * expectimax(c1, depth - 1, True) * probability
                c2 = deepcopy(board)
                c2[i, j] = 4
                print("c2 is: \n")
                print(c2)
                score += 0.1 * expectimax(c2, depth - 1, True) * probability
        return score


def calculate_board_score(board):
    grid_score = heuristic.score_grid_value(board)
    neighbor_score = heuristic.compare_neighbor_tile(board)
    snake_score = heuristic.score_snake(board)
    min_score = calculate_empty_tiles(board)
    # result = (grid_score * neighbor_score)
    print("snake_score is: ", snake_score)
    print("min_score is: ", min_score)
    print("neighbor_score is: ")
    # if calculate_empty_tiles(board) <= 4:
    # result = snake_score * (2 / 10) + min_score * (4 / 10) + neighbor_score * (2 / 10) + grid_score * (2 / 10)
    # else:
    # result = snake_score + min_score + neighbor_score + grid_score
    # result = snake_score * (2) + min_score * (3) + neighbor_score * (2) + grid_score * (2)
    result = min_score + snake_score + neighbor_score
    print("The board score is ", result)
    return result


def calculate_empty_tiles(board):
    empty_tiles = 0
    for x, y in ndindex(board.shape):
        if board[x, y] == 0:
            empty_tiles += 1
    return empty_tiles
