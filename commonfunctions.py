import random


def infinite_loop_checker(error_counter, location):
    if error_counter == 10000:
        print(f"\nThe program became stuck on an infinite loop while {location}!")
        exit()


def is_input_valid(value, limit):  # Checks if the value is a valid number and within the valid range
    if value.isnumeric() and limit[0] <= int(value) <= limit[1]:
        return True
    else:
        print("Command invalid or out of range.")


def get_total_specified_spaces(board, specified):  # Gets the total number of spaces taken by a particular symbol
    looking_for = 0
    for row in board:
        for col in row:
            if col == specified:
                looking_for += 1
    return looking_for


def change_symbols(board, previous, after):  # Changes all of a particular symbol to another character
    row_counter = 0
    while row_counter < len(board):
        col_counter = 0
        while col_counter < len(board):
            if board[row_counter][col_counter] == previous:
                board[row_counter][col_counter] = after
            col_counter += 1
        row_counter += 1
    return board


def scatter_items_around_board(board, to_be_moved, not_allowed_spaces):
    low_possibility = 0
    replaceable = [".", "?"]
    guard_in_line = True if "G" in to_be_moved else False
    for item in to_be_moved:
        while True:
            low_possibility += 1
            if low_possibility == (len(board) * len(board)) * 3:
                replaceable.append("X")
                replaceable.append("O")
            random_row, random_col = random.randint(0, len(board) - 1), random.randint(0, len(board) - 1)
            if board[random_row][random_col] in replaceable and [random_row, random_col] not in not_allowed_spaces:
                board[random_row][random_col] = item
                break
    return board, guard_in_line


def is_used_full(board, used_coordinates, replaceable, corners):
    # This function finds out if all the spaces that are trying to be avoided have been listed - if so, True is returned
    if not corners:
        used_coordinates += [[0, 0], [0, len(board) - 1], [len(board) - 1, 0], [len(board) - 1, len(board) - 1]]
    row_counter = 0
    while row_counter < len(board):
        col_counter = 0
        while col_counter < len(board):
            if [row_counter, col_counter] not in used_coordinates and board[row_counter][col_counter] in replaceable:
                return False
            col_counter += 1
        row_counter += 1
    return True


def add_symbols(board, no_of_blanks, replaceable, symbol, corners):  # Adds the symbols and tries to avoid clusters
    saved_coordinates = [[-1, -1], [-1, 0], [-1, 1], [0, 1], [1, 1], [1, 0], [1, -1], [0, -1]]
    avoid_corners = [[0, 0], [0, len(board) - 1], [len(board) - 1, 0], [len(board) - 1, len(board) - 1]]
    used_coordinates = []
    corner_tracker = 0
    error_counter = 0
    while no_of_blanks > 0:
        error_counter += 1
        infinite_loop_checker(error_counter, "adding symbols")
        row_num, col_num = random.randint(0, len(board) - 1), random.randint(0, len(board) - 1)
        if board[row_num][col_num] not in replaceable or [row_num, col_num] in used_coordinates:
            if board[row_num][col_num] in replaceable and is_used_full(board, used_coordinates, replaceable, corners):
                used_coordinates = []  # If every possible space is in used_coordinates, it will be reset
            else:
                continue  # If there are still possible spaces in used_coordinates, a possible space will be generated
        if not corners and [row_num, col_num] in avoid_corners:
            corner_tracker += 1
            if corner_tracker == 20:  # At this point, the only free spaces are probably corners, so corners = True
                corners = True
            continue  # Some patterns would be difficult to make without corners, so corners won't be blanked
        for pair in saved_coordinates:  # Adds all the close by spaces to used_coordinates to help avoid clusters
            used_coordinates.append([row_num + pair[0], col_num + pair[1]])
        board[row_num][col_num] = symbol  # This part fixes the symbol on the board
        no_of_blanks -= 1
    return board


def get_blank_positions(board, symbol):  # This finds the positions all of a particular symbol and returns them
    blanks = []
    row_counter = 0
    while row_counter < len(board):
        col_counter = 0
        while col_counter < len(board):
            if board[row_counter][col_counter] == symbol:
                blanks.append([row_counter, col_counter])
            col_counter += 1
        row_counter += 1
    return blanks


def get_board_areas(board):  # This is used for getting the appropriate directions to move objects around the board
    left_magnet_spaces, bottom_magnet_spaces, right_magnet_spaces, top_magnet_spaces = [], [], [], []
    bm2 = len(board) - 2
    hb = len(board) // 2
    hba = (len(board) // 2) - 1 if len(board) % 2 == 0 else len(board) // 2
    row = 0
    while row < len(board):
        col = 0
        while col < len(board):
            if (row < 2 and col > 1) or (1 < col <= hba and row < hb):
                left_magnet_spaces.append([row, col])
            elif (col < 2 and row < bm2) or (bm2 > row >= hb > col):
                bottom_magnet_spaces.append([row, col])
            elif (row >= bm2 > col) or (bm2 > col >= hb and row > hba):
                right_magnet_spaces.append([row, col])
            elif (col >= bm2 and row > 1) or (1 < row <= hb <= col):
                top_magnet_spaces.append([row, col])
            else:
                print("\nERROR GETTING BOARD LOCATIONS!")
                exit()
            col += 1
        row += 1
    return left_magnet_spaces, bottom_magnet_spaces, right_magnet_spaces, top_magnet_spaces


def possibility_check(board, step, directions, used_coordinates, possible):
    # This checks how many possible immediate steps there are next to a particular space, USED and UNUSED
    used_possibility = 0
    unused_possibility = 0
    for direction in directions:
        row = step[0] + direction[0]
        col = step[1] + direction[1]
        if row in range(len(board)) and col in range(len(board)) and board[row][col] in possible:
            if [row, col] in used_coordinates:
                used_possibility += 1
            else:
                unused_possibility += 1
    return used_possibility, unused_possibility


def ensure_usable_free_spaces(board):
    free_spaces = get_blank_positions(board, "?")
    while len(free_spaces) > 0:
        low_possibility, spaces = 0, 2  # This stops any infinite loops when there are no available spaces on the board
        error_counter = 0
        # If the possibility_check shows the free_space has a low change of being able to be used, it will be changed
        while possibility_check(board, free_spaces[0], [[-1, 0], [0, 1], [1, 0], [0, -1]], [], ["."])[1] < spaces:
            error_counter += 1
            infinite_loop_checker(error_counter, "amending free spaces")
            board[free_spaces[0][0]][free_spaces[0][1]] = "."  # The free_spaces is removed
            free_spaces.pop(0)  # The coordinates for the free_space are removed from the list
            while True:  # Once a space is found that doesn't have a U or player's mark, this loop will finish
                rand_row, rand_col = random.randint(0, len(board) - 1), random.randint(0, len(board) - 1)
                corners = [[0, 0], [0, len(board) - 1], [len(board) - 1, 0], [len(board) - 1, len(board) - 1]]
                if [rand_row, rand_col] in corners:
                    continue
                if board[rand_row][rand_col] == ".":
                    board[rand_row][rand_col] = "?"
                    free_spaces.insert(0, [rand_row, rand_col])  # The new free_space coordinates are recorded
                    break
            low_possibility += 1
            # At this point, a fairer space clearly hasn't been found, so the function will except a less fair space
            if low_possibility == (len(board) * len(board)) * 3 and spaces != 0:
                spaces -= 1
                low_possibility = 0
            elif low_possibility == (len(board) * len(board)) * 3 and spaces == 0:
                break  # At this point it is impossible to find any fairer space at all, so the process is abandoned
        free_spaces.pop(0)  # Once the free_space is accepted, it is removed from the coordinates
    return board
