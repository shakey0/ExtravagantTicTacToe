

def check_patterns(row, column, board, checking_for, shape_data):
    discovered = 0  # This is for the total number of all patterns that will be discovered from the users last move
    win_messages = []  # For storing all the winning messages for the patterns found from the users last move
    gained_free_spaces = []  # For storing the coordinates of ? spaces that the player gained during their last move
    for pattern in shape_data:  # Goes through each pattern in the shape data one at a time
        st_co, messages, end_count = shape_data[pattern]
        if "corners" in pattern:  # If the user didn't choose any edge of the board, this skips checking all corners
            if row != 0 and row != (len(board) - 1) and column != 0 and column != (len(board) - 1):
                continue
        cycles, sm_count = 0, 0  # CYCLES moves through the line_type/rotation/expansion coordinates for checking
        while cycles != len(st_co):
            coord_counter = [row - end_count[cycles][0], column - end_count[cycles][1]]  # COORDINATE_COUNTER
            if "exp" not in pattern:
                sm_count = 0  # SAME_COUNTER (This keeps track of how many times the same pattern has been discovered)
            while coord_counter[0] <= row and coord_counter[0] < len(board) - end_count[cycles][0]:  # Stops overflow
                while coord_counter[0] < 0:  # Stops underflow (coordinates off the edge of the board (as above))
                    coord_counter[0] += 1
                while coord_counter[1] < 0:  # As above
                    coord_counter[1] += 1
                check_set = []  # This is the set of coordinates that will be checked
                for number in range(len(st_co[cycles])):
                    pair = [coord_counter[0] + st_co[cycles][number][0], coord_counter[1] + st_co[cycles][number][1]]
                    check_set.append(pair)  # Each pair is calculated from start_coordinates and coordinates_counter
                if [row, column] in check_set:  # If the user's chosen row and column are here, the set will be checked
                    found = 0
                    checked_spaces = []  # This is for storing either the player's name or ? for later use
                    for cos in check_set:
                        if board[cos[0]][cos[1]] != checking_for and board[cos[0]][cos[1]] != "?":
                            break  # As soon as one position is False, the check will be terminated
                        found += 1
                        checked_spaces.append(board[cos[0]][cos[1]])
                    if found == len(st_co[cycles]):  # At this point, a successful pattern has been found
                        discovered += 1
                        sm_count += 1
                        counter = 0
                        for space in checked_spaces:  # This will append the coordinates of the ?(s) used
                            if space == "?":
                                board[check_set[counter][0]][check_set[counter][1]] = checking_for
                                gained_free_spaces.append(check_set[counter])  # For later message printing
                            counter += 1
                coord_counter[1] += 1  # Moves the check to the next column along
                if coord_counter[1] > column or coord_counter[1] == len(board) - end_count[cycles][1]:  # Stops overflow
                    coord_counter[1] = column - end_count[cycles][1]  # Moves the check back to the left
                    coord_counter[0] += 1  # Moves the check down to the next line
            # This part deals with preparing the appropriate message(s) for the user, especially the correct grammar
            if sm_count > 0 and ("exp" not in pattern or cycles == len(st_co) - 1):
                longer_lines = False
                if "lines_of" in pattern:  # Lines will be checked again to see if the stretch any longer
                    longer_lines, message, extra_found, extra_gained_free_spaces =\
                        check_lines(row, column, board, checking_for, cycles, len(st_co[0]), gained_free_spaces)
                    discovered += extra_found
                    gained_free_spaces += extra_gained_free_spaces
                    if longer_lines:  # If a longer line is found, the other function send the appropriate message back
                        win_messages.append(message)
                if sm_count == 1 and ("lines_of" not in pattern or not longer_lines):  # For 1 pattern
                    win_messages.append(messages[cycles].format("a", "an", "the", "", "", "its"))
                elif sm_count > 1 and "lines_of" not in pattern:  # For multiple patterns of the same rotation/size
                    win_messages.append(messages[cycles].format(sm_count, sm_count, sm_count, "s", "es", "their"))
            cycles += 1
    return discovered, win_messages, gained_free_spaces  # Returns any successful data from the user's last move


def check_lines(row, column, board, checking_for, cycle, line_length, gained_free_spaces):
    mover = [[0, 1], [1, 0], [1, 1], [1, -1]]  # This controls the direction of the check pattern
    line_to_check, chosen_row, chosen_column, found_neg, extra_found = mover[cycle], row, column, 0, 0
    free_found, free_spaces_found, free_yes, free_in_line = 0, [], False, 0
    while True:  # This part checks previous to the user's chosen space (this turn)
        row -= line_to_check[0]  # Moves the row backwards
        column -= line_to_check[1]  # Moves the row forwards
        if (0 <= row < len(board) and 0 <= column < len(board)) and (board[row][column] == checking_for):
            found_neg += 1  # A space behind or above the user's chosen position has been found
            # The next 6 lines identify free spaces in lines that were previously incomplete lines
            if free_in_line > 0:
                free_in_line += 1  # Keeps track of any already completed lines that shouldn't be scored
            if 0 < free_in_line <= line_length <= found_neg:
                extra_found += 1  # Adds 1 to the player's score
            if [row, column] in gained_free_spaces:  # Checks for free spaces already found by check_patterns
                free_yes = True  # This is for giving the user the correct message
                free_in_line = 1  # Resets the counter so incomplete lines are added to the player's score
        elif (0 <= row < len(board) and 0 <= column < len(board)) and (board[row][column] == "?"):
            found_neg += 1
            free_in_line = 1
            free_found += 1  # A free spaces that was not found by check_patterns has been found here
            board[row][column] = checking_for  # Free spaces beyond the line_length will be changed to the player's
            free_spaces_found.append([row, column])  # Gives the free space coordinates for later message printing
        else:
            break  # As soon as a position is found to not be taken by the user, the check is terminated
    row, column, found_pos, free_in_line = chosen_row, chosen_column, 0, 0
    while True:  # This part check the parts after the user's chosen space (this turn)
        row += line_to_check[0]  # Moves the row backwards
        column += line_to_check[1]  # Moves the row forwards
        if (0 <= row < len(board) and 0 <= column < len(board)) and (board[row][column] == checking_for):
            found_pos += 1  # A space in front of or below the user's chosen position has been found
            # The next 6 lines identify free spaces in lines that were previously incomplete lines
            if free_in_line > 0:
                free_in_line += 1  # Keeps track of any already completed lines that shouldn't be scored
            if 0 < free_in_line <= line_length <= found_pos:
                extra_found += 1  # Adds 1 to the player's score
            if [row, column] in gained_free_spaces:  # Checks for free spaces already found by check_patterns
                free_yes = True  # This is for giving the user the correct message
                free_in_line = 1  # Resets the counter so incomplete lines are added to the player's score
        elif (0 <= row < len(board) and 0 <= column < len(board)) and (board[row][column] == "?"):
            found_pos += 1
            free_in_line = 1
            free_found += 1  # A free spaces that was not found by check_patterns has been found here
            board[row][column] = checking_for  # Free spaces beyond the line_length will be changed to the player's
            free_spaces_found.append([row, column])  # Gives the free space coordinates for later message printing
        else:
            break  # As soon as a position is found to not be taken by the user, the check is terminated
    total_found = found_neg + found_pos
    line_types = ["a perfectly horizontal", "a terrifyingly vertical", "a gleaming diagonal", "a majestic diagonal"]
    line_type = line_types[cycle]
    if found_neg + 1 + found_pos > line_length and free_yes:
        message = f"cast an impressive spell stringing out {line_type} line of {found_neg + 1 + found_pos}"
        return True, message, free_found + extra_found, free_spaces_found
    if found_neg + 1 > line_length and found_pos == 0:  # For longer lines that extend in the previous range
        message = f"extended {line_type} line of {total_found - free_found} to {line_type} line of {found_neg + 1}"
        return True, message, free_found + extra_found, free_spaces_found
    elif found_pos + 1 > line_length and found_neg == 0:  # For longer lines that extend in the after range
        message = f"extended {line_type} line of {total_found - free_found} to {line_type} line of {found_pos + 1}"
        return True, message, free_found + extra_found, free_spaces_found
    elif found_neg + 1 + found_pos > line_length:  # For longer lines that extend both ways
        message = f"threw themself between themself to make {line_type} line of " \
                  f"{found_neg + 1 + found_pos}"
        return True, message, free_found + extra_found, free_spaces_found
    else:
        return False, "", free_found + extra_found, free_spaces_found
