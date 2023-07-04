import random
from commonfunctions import infinite_loop_checker, get_total_specified_spaces, change_symbols, add_symbols,\
    get_blank_positions, get_board_areas, ensure_usable_free_spaces


def determine_blank_amounts(board_size, mode, more_blanks):
    amount_of_type = board_size - 3
    amount_of_free = board_size - 3
    amount_of_static = board_size - 3
    if mode[0] == "A":
        amount_of_type *= 2  # This double the amount of type_blanks for the As Many As You Can and Cards modes
    if more_blanks >= 1:
        amount_of_type += board_size - 3  # This increases the amount of type_blanks for easier game types
    if more_blanks >= 2:
        if mode[0] != "C":
            amount_of_static += board_size - 3  # This increases the amount of static_blanks for very easy game types
        else:
            amount_of_type += board_size - 3  # For Cards mode, the type blanks are increase here instead
    return amount_of_type, amount_of_free, amount_of_static


def get_blanks(board, mode, more_blanks):
    if len(board) == 3 or (mode[0] == "S" and more_blanks == 3):  # No blanks for 3 by 3 boards or standard lines of 3
        return board, "n", 0
    type_blanks, free_blanks, static_blanks = determine_blank_amounts(len(board), mode, more_blanks)
    if len(board) >= 6:  # The board_length must be at least 6 for honey_badgers and toadstools
        hb_bls_mes = "\nH = Honey Badgers (You can't reckon with these, they simply can't be used, nor do they move." \
                     "\n    However, some of them are Cheetah Cubs, which are free tiles, good luck spotting them!)"
        ts_bls_mes = "\nT = Toadstools (NOT YET AVAILABLE BUT COMING SOON!)"
    else:
        hb_bls_mes = ""
        ts_bls_mes = ""
    print("\n" + "-" * 25 + "CHOOSE YOUR BLANKS" + "-" * 40)
    print("\nWhat kind of blanks and free tiles would you like?"
          "\n(Blank tiles cannot be used, and free tiles can be used to make a pattern with.)"
          "\n\nE = Electrical Storm (These blanks are of high voltage and will block your path.)"
          f"{hb_bls_mes}"
          "\nS = Stepping Stones (These usually take one step each turn, in any of 8 directions though.)"
          "\nC = Cattle Farm (The cows will block your way, and the bulls will charge your spaces out!)"
          "\nV = Lightning (These blanks strike the board, and they will strike your spaces!)"
          "\nU = Sinkholes (Big holes will appear on the board, and they will swallow your spaces!)"
          f"{ts_bls_mes}"
          "\nN = No Blanks")
    while True:
        blank_types = input("")
        blank_types = blank_types.lower()
        # This part is for electrical_storm_blanks and stepping_stones_blanks and cattle_farm_blanks
        if blank_types == "e" or blank_types == "s" or blank_types == "c":
            symbol = "Z" if blank_types == "e" else "K" if blank_types == "s" else "C"
            board = fix_static_blanks(board, static_blanks, symbol)
            return board, blank_types, [type_blanks, free_blanks]
        elif blank_types == "h" and len(board) >= 6:  # This part is for honey_badger_blanks
            honey_badgers = ((static_blanks + type_blanks) // 2) + (len(board) - 3)
            board = fix_honey_badger_blanks(board, honey_badgers, free_blanks * 2)
            return board, "h", []
        elif blank_types == "v" or blank_types == "u":  # This part is for lightning_blanks and sink_holes_blanks
            return board, blank_types, [type_blanks + static_blanks, free_blanks]
        elif blank_types == "t":  # This part is for toadstool_blanks
            print("SORRY! Toadstools are coming soon!")
        elif blank_types == "n":  # If the user chooses this, then the game will be set up without any blanks
            return board, "n", []
        else:  # In this case, the loop will continue until a valid command is entered
            print("Invalid command.")


def fix_static_blanks(board, static_blanks, symbol):  # Fixes the static_blanks evenly around the board (NOT for Cards)
    lo, up = (len(board) - 1) // 2, len(board) // 2  # LOW, UP - LOW = LEFT/TOP, UP = RIGHT/BOTTOM
    if len(board) == 8:
        lo -= 1
        up += 1
    centre_blanks = [[lo, lo], [lo, up], [up, lo], [up, up]] if len(board) % 2 == 0 else [[up, up]]
    outer_centre_blanks_odd = [[up-1, up], [up, up+1], [up+1, up], [up, up-1]]
    out_outer_centre_blanks_odd = [[up-2, up], [up, up+2], [up+2, up], [up, up-2]]
    corner_outer_blanks = [[1, 1], [1, len(board)-2], [len(board)-2, 1], [len(board)-2, len(board)-2]]
    outer_centre_even_ver = [[lo-1, lo], [lo-1, up], [up+1, up], [up+1, lo]]
    outer_centre_even_hor = [[lo, up+1], [up, up+1], [up, lo-1], [lo, lo-1]]
    used_spaces = []  # This collects the coordinates for spaces that have been used, so they aren't used again
    error_counter = 0  # This closes the program in the case the program becomes stuck in an infinite loop
    while static_blanks > 0:
        error_counter += 1
        infinite_loop_checker(error_counter, "fixing static blanks")
        space = random.randint(0, 3)  # Generates a random space which will be taken from the commanded blanks list
        if len(board) % 2 != 0 and centre_blanks[0] not in used_spaces:  # This fixes the centre blank for odd boards
            board[centre_blanks[0][0]][centre_blanks[0][1]] = symbol
            used_spaces.append([centre_blanks[0][0], centre_blanks[0][1]])
            static_blanks -= 1
            continue
        if len(board) == 4:
            space_coordinates = [centre_blanks[space][0], centre_blanks[space][1]]
        elif len(board) == 5:
            space_coordinates = [outer_centre_blanks_odd[space][0], outer_centre_blanks_odd[space][1]]
        elif len(board) == 6:
            if static_blanks < 4:
                space_coordinates = [centre_blanks[space][0], centre_blanks[space][1]]
            else:
                space_coordinates = [corner_outer_blanks[space][0], corner_outer_blanks[space][1]]
        elif len(board) == 7:
            if static_blanks < 4:
                space_coordinates = [out_outer_centre_blanks_odd[space][0], out_outer_centre_blanks_odd[space][1]]
            else:
                space_coordinates = [corner_outer_blanks[space][0], corner_outer_blanks[space][1]]
        elif len(board) == 8:
            if static_blanks < 5:
                space_coordinates = [centre_blanks[space][0], centre_blanks[space][1]]
            else:
                if static_blanks < 7:
                    space_coordinates = [outer_centre_even_hor[space][0], outer_centre_even_hor[space][1]]
                elif static_blanks < 9:
                    space_coordinates = [outer_centre_even_ver[space][0], outer_centre_even_ver[space][1]]
                else:
                    space_coordinates = [corner_outer_blanks[space][0], corner_outer_blanks[space][1]]
        else:  # This is for 9 by 9 boards
            out_outer_centre_blanks_odd = [[up-3, up], [up, up+3], [up+3, up], [up, up-3]]
            random_move = random.randint(-1, 1)
            if static_blanks < 5:
                space_coordinates = [out_outer_centre_blanks_odd[space][0], out_outer_centre_blanks_odd[space][1]]
            elif static_blanks < 9:
                space_coordinates = [outer_centre_blanks_odd[space][0] + random_move,
                                     outer_centre_blanks_odd[space][1] + random_move]
            else:
                space_coordinates = [corner_outer_blanks[space][0], corner_outer_blanks[space][1]]
        if space_coordinates in used_spaces:  # After all that, if the space has already been used, it will be scrapped
            continue
        board[space_coordinates[0]][space_coordinates[1]] = symbol  # Fixes the static_blank to the board
        used_spaces.append(space_coordinates)  # Records the coordinates of the space, so it won't be used again
        static_blanks -= 1
    return board


def get_blanks_for_cards(board, blank_types, more_blanks):
    replaceable = ["."]
    amount_of_type, amount_of_free, amount_of_static = determine_blank_amounts(len(board), "Cards", more_blanks)
    # !!!!!! THIS PART BELOW SHOULDN'T BE NEEDED AFTER EAGLE_EYED_EAGLE WAS PUT IN !!!!!!
    '''counter = 1
    while get_total_specified_spaces(board, ".") + len(board) < amount_of_type + amount_of_free + amount_of_static:
        amount_of_type -= 1
        amount_of_static -= 1
        if counter % 3 == 0:
            amount_of_free -= 1
        counter += 1'''
    if blank_types == "e":
        print("\nAn electrical storm just came over the board!")
        board = add_symbols(board, amount_of_static, replaceable, "Z", False)
        board, blanks_tracker = get_electricity(board, [amount_of_type, amount_of_free], 0, 0)
        return board, [amount_of_type, amount_of_free], blanks_tracker
    elif blank_types == "h":
        print("\nA group of honey badgers just appeared on the board!")
        board = fix_honey_badger_blanks(board, amount_of_type + amount_of_static, amount_of_free)
        return board, [], 0
    elif blank_types == "s":
        print("\nA group of spirited stepping stones just appeared on the board!")
        board = add_symbols(board, amount_of_static, replaceable, "K", False)
        board, blanks_tracker = get_stepping_stones(board, [amount_of_type, amount_of_free], 0)
        return board, [amount_of_type, amount_of_free], blanks_tracker
    elif blank_types == "c":
        print("\nA cattle farm just moved onto the board! Watch out for bulls!")
        board = add_symbols(board, amount_of_static, replaceable, "C", False)
        board, blanks_tracker = get_cows_and_bulls(board, [amount_of_type, amount_of_free], 0)
        return board, [amount_of_type, amount_of_free], blanks_tracker
    elif blank_types == "v":
        print("\nA powerful lightning storm just started! Watch out!")
        board, blanks_tracker = get_lightning(board, [amount_of_type + amount_of_static, amount_of_free], 0)
        return board, [amount_of_type + amount_of_static, amount_of_free], blanks_tracker
    else:
        print("\nWatch out! Sinkholes!")
        board, blanks_tracker = get_sinkholes(board, [amount_of_type + amount_of_static, amount_of_free], 0)
        return board, [amount_of_type + amount_of_static, amount_of_free], blanks_tracker


def get_electricity(board, no_of_blanks, blanks_tracker, free_spaces_used):
    electricity, free_spaces = no_of_blanks
    # This parts calculates the True number of empty_spaces considering the amount of free_spaces taken by the users
    empty_spaces_left = get_total_specified_spaces(board, ".")
    free_spaces_used_turns = free_spaces - get_total_specified_spaces(board, "?")
    if empty_spaces_left < (len(board) + free_spaces_used_turns) and blanks_tracker < 3:  # This reduces the electricity
        blanks_tracker = 3
    elif (empty_spaces_left < (len(board) + free_spaces_used) and blanks_tracker == 3) or blanks_tracker == 4:
        if blanks_tracker != 4:  # This is the first turn the storm is over
            print("\nIt seems the voltage is no longer dangerous. Enjoy!")
            board = change_symbols(board, "V", ".")
            board = change_symbols(board, "?", ".")
        else:  # This part is for all subsequent turns the storm is over
            print(f"\nEnjoy the calm with just {empty_spaces_left} moves left!")
        blanks_tracker = 4
        return board, blanks_tracker
    if blanks_tracker == 0 or blanks_tracker == 3:
        if blanks_tracker == 0:
            print("\nThe electrical storm is in full power!")
        else:  # For the final part of the storm, this reduces the amount of electricity by half
            print("\nThe electricity is moving, although it seems to be running out of charge.")
            electricity //= 2
        board = change_symbols(board, "V", ".")
        board = add_symbols(board, electricity, [".", "?"], "V", True)
        board = change_symbols(board, "?", ".")
        board = add_symbols(board, free_spaces, ["."], "?", False)
        board = ensure_usable_free_spaces(board)
    if blanks_tracker == 0:
        blanks_tracker = 1
    elif blanks_tracker == 1:
        blanks_tracker = 2
    elif blanks_tracker == 2:
        blanks_tracker = 0
    return board, blanks_tracker


def fix_honey_badger_blanks(board, honey_badger_blanks, cheetah_cub_blanks):
    board = add_symbols(board, honey_badger_blanks + cheetah_cub_blanks, ["."], "H", False)
    # This part randomly selects fixed_blanks and changes then to free_blanks according to the amount of free_blanks
    positions = get_blank_positions(board, "H")
    change_to = len(positions) - honey_badger_blanks
    cheetah_cubs = []
    while change_to > 0:
        cheetah_cub = random.randint(0, len(positions) - 1)
        if positions[cheetah_cub] in cheetah_cubs:
            continue
        cheetah_cubs.append(positions[cheetah_cub])
        change_to -= 1
    for cheetah_cub in cheetah_cubs:
        board[cheetah_cub[0]][cheetah_cub[1]] = "?"  # This ? symbol will be changed back to H when the board is printed
    board = ensure_usable_free_spaces(board)
    return board


def move_stepping_stones(board, steps, replaceable, symbol):
    directions = [[[0, -1], [1, 0], [0, -2]], [[1, 0], [0, 1], [2, 0]], [[0, 1], [-1, 0], [0, 2]],
                  [[-1, 0], [0, -1], [-2, 0]]]
    left_magnet_spaces, bottom_magnet_spaces, right_magnet_spaces, top_magnet_spaces = get_board_areas(board)
    for step in steps:  # This part tells the process when the stepping_stone needs to change direction
        if step in left_magnet_spaces:
            follow = directions[0]
        elif step in bottom_magnet_spaces:
            follow = directions[1]
        elif step in right_magnet_spaces:
            follow = directions[2]
        elif step in top_magnet_spaces:
            follow = directions[3]
        else:
            print("\nERROR GETTING STEPPING STONE DIRECTIONS!")
            exit()
        temp_replaceable = replaceable
        while True:  # Finds the direction to move the stepping_stone according to what might be in the way
            if board[step[0] + follow[0][0]][step[1] + follow[0][1]] in replaceable:
                board[step[0] + follow[0][0]][step[1] + follow[0][1]] = symbol
                break
            elif board[step[0] + follow[1][0]][step[1] + follow[1][1]] in replaceable:
                board[step[0] + follow[1][0]][step[1] + follow[1][1]] = symbol
                break
            elif board[step[0] + follow[2][0]][step[1] + follow[2][1]] in replaceable:
                board[step[0] + follow[2][0]][step[1] + follow[2][1]] = symbol
                break
            else:
                if "P" not in temp_replaceable:  # Now, it's okay to take the position of a previous stepping_stone
                    temp_replaceable.append("P")
                    continue
            # If the process gets here, the stepping_stone will be moved to any available part of the board
            board = add_symbols(board, 1, temp_replaceable, symbol, True)
            break
    return board


def get_stepping_stones(board, no_of_blanks, blanks_tracker):
    stepping_stones, free_spaces = no_of_blanks
    if get_total_specified_spaces(board, "S") == 0 and blanks_tracker == 0:  # FOR THE FIRST TIME ONLY
        board = add_symbols(board, stepping_stones, ["."], "S", True)
        board = add_symbols(board, free_spaces, ["."], "?", True)
        return board, blanks_tracker
    # This parts calculates the True number of empty_spaces considering the amount of free_spaces taken by the users
    step_coordinates, free_coordinates = get_blank_positions(board, "S"), get_blank_positions(board, "?")
    empty_spaces_left = get_total_specified_spaces(board, ".")
    free_spaces_used_turns = (free_spaces - (blanks_tracker // 3)) - get_total_specified_spaces(board, "?")
    empty_spaces_left -= free_spaces_used_turns
    empty_space_limit = len(board)
    while empty_spaces_left < empty_space_limit:  # This reduces the amount of stepping_stones near the end of the game
        blanks_tracker += 3
        for number in range(2):  # 2 stepping_stones are removed
            if len(step_coordinates) == 0:
                break
            pop_step = random.randint(0, len(step_coordinates) - 1)
            step_coordinates.pop(pop_step)
        if len(free_coordinates) > 0:  # 1 free_space is removed
            pop_free = random.randint(0, len(free_coordinates) - 1)
            free_coordinates.pop(pop_free)
        empty_spaces_left += 3
    if len(step_coordinates) == stepping_stones:  # For usual turns
        print("\nThe stepping stones are stepping in high spirits.")
    elif len(step_coordinates) > 0:  # Near the end when the stepping_stones have started to be removed
        print("\nThe stepping stones are still stepping, although they appear to be fewer in number...")
    else:  # For very near the end when all the stepping_stones have been removed
        print("\nOnly the King Rocks remain...")
    board = change_symbols(board, "S", "P")  # Changes the stepping stones to try to avoid clusters
    board = move_stepping_stones(board, step_coordinates, [".", "?"], "S")  # Adds the moved/stepped stepping_stones
    board = change_symbols(board, "P", ".")  # Removes the stepping_stones from the last turn
    board = change_symbols(board, "?", ".")  # Removes the free_spaces from the last turn
    board = move_stepping_stones(board, free_coordinates, ["."], "?")  # Adds the moved/stepped free_spaces
    # This part checks that the number of free_spaces meet the specified number, in the case some have been taken
    remaining_free_spaces = get_total_specified_spaces(board, "?")
    if remaining_free_spaces < (free_spaces - (blanks_tracker // 3)):
        board = add_symbols(board, (free_spaces - (blanks_tracker // 3)) - remaining_free_spaces, ["."], "?", True)
    return board, blanks_tracker


def move_bulls(board, bull_positions):
    directions = [[0, -1], [1, 0], [0, 1], [-1, 0], [0, -1]]
    left_magnet_spaces, bottom_magnet_spaces, right_magnet_spaces, top_magnet_spaces = get_board_areas(board)
    moved_cows, moved_bulls = 0, 0
    for bull in bull_positions:  # This part tells the process which directions the bulls can charge in
        if bull in left_magnet_spaces:
            direction = directions[random.randint(0, 1)]
        elif bull in bottom_magnet_spaces:
            direction = directions[random.randint(1, 2)]
        elif bull in right_magnet_spaces:
            direction = directions[random.randint(2, 3)]
        elif bull in top_magnet_spaces:
            direction = directions[random.randint(3, 4)]
        else:
            print("\nERROR GETTING BULL DIRECTIONS!")
            exit()
        counter = 1
        while True:  # This moves the bull and removes anything in its way - cows and other bulls are re-added later on
            row, col = bull[0] + (direction[0] * counter), bull[1] + (direction[1] * counter)
            if row not in range(len(board)) or col not in range(len(board)) or board[row][col] == " ":
                if counter == 1:
                    moved_bulls += 1
                break
            if board[row][col] == "B":
                moved_bulls += 1
            if board[row][col] == "C":
                moved_cows += 1
            board[row][col] = "B"
            last_row, last_col = bull[0] + (direction[0] * (counter - 1)), bull[1] + (direction[1] * (counter - 1))
            if counter != 1:
                board[last_row][last_col] = "."
            counter += 1
            if counter > (len(board) // 2):  # This is to randomly stop the bulls to stop cluttering at the edges
                random_stop = random.randint(0, 1)
                if random_stop == 1:
                    break
    board = add_symbols(board, moved_bulls, [".", "X", "O"], "B", False)  # Charged bulls are re-added
    board = add_symbols(board, moved_cows, ["."], "C", False)  # Charged cows are re-added
    return board


def get_cows_and_bulls(board, no_of_blanks, blanks_tracker):
    if blanks_tracker % 5 != 0:  # The bulls charge every 5 turns
        blanks_tracker += 1
        return board, blanks_tracker
    bulls, free_spaces = no_of_blanks
    number_of_cows = get_total_specified_spaces(board, "C")
    if bulls > number_of_cows:
        bulls -= bulls - number_of_cows
    if get_total_specified_spaces(board, "B") == 0 and blanks_tracker == 0:  # FOR THE FIRST TIME ONLY
        board = add_symbols(board, bulls, [".", "X", "O", "G"], "B", True)
        board = add_symbols(board, free_spaces, ["."], "?", False)
        blanks_tracker += 1
        return board, blanks_tracker
    print("\nThe bulls are charging again! Watch out!")
    bull_positions = get_blank_positions(board, "B")  # Gets the positions of the current bulls
    board = change_symbols(board, "B", ".")  # Removes the bulls from their current positions
    board = move_bulls(board, bull_positions)  # Charges bulls to their new positions
    board = change_symbols(board, "?", ".")  # Removes the free_spaces from their current positions
    board = add_symbols(board, free_spaces, ["."], "?", False)  # Randomly adds free_spaces in new positions
    blanks_tracker += 1
    board = ensure_usable_free_spaces(board)
    return board, blanks_tracker


def get_lightning(board, no_of_blanks, blanks_tracker):
    if blanks_tracker % 5 != 0:  # Lightning is changed every 5 turns
        blanks_tracker += 1
        return board, blanks_tracker
    print("\nThe board has just been struck by powerful lightning!")
    board = change_symbols(board, "V", ".")  # Removes the lightning from the last time
    board = change_symbols(board, "?", ".")  # Removes the free_spaces from the last time
    lightning, free_spaces = no_of_blanks
    if blanks_tracker > (len(board) * len(board)) - ((len(board) * len(board)) - ((len(board) - 1) * (len(board) - 1))):
        lightning //= 2
        free_spaces = (free_spaces + 1) // 2
        print("Although there seems to be less of it compared to before.")
    board = add_symbols(board, lightning, [".", "X", "O", "G"], "V", True)
    board = add_symbols(board, free_spaces, [".", "X", "O"], "?", False)
    blanks_tracker += 1
    board = ensure_usable_free_spaces(board)
    return board, blanks_tracker


def get_sinkholes(board, no_of_blanks, blanks_tracker):
    if blanks_tracker % 5 != 0:  # Sinkholes are changed every 5 turns
        blanks_tracker += 1
        return board, blanks_tracker
    print("\nParts of the board have just been swallowed by a power from under the ground!")
    board = change_symbols(board, "U", ".")  # Removes the sinkholes from the last time
    board = change_symbols(board, "?", ".")  # Removes the free_spaces from the last time
    sinkholes, free_spaces = no_of_blanks
    # This part is for near the end of the game - at this point the sinkhole sizes will be halved
    if blanks_tracker > (len(board) * len(board)) - ((len(board) * len(board)) - ((len(board) - 1) * (len(board) - 1))):
        sinkholes //= 2
        free_spaces = (free_spaces + 1) // 2
        print("Although they seem to be a little bit smaller than before.")
    used_coordinates = []  # This keeps track of spaces that haven already been taken by a sinkhole
    random_areas = []  # The board is cut horizontally and vertically to create 4 areas - only 3 will be used each time
    areas = [sinkholes // 3, sinkholes // 3, (sinkholes // 3) + sinkholes % 3]  # The amount of spaces for each sinkhole
    frees = [free_spaces // 3, free_spaces // 3, (free_spaces // 3) + free_spaces % 3]  # The amount of free_spaces
    areas_counter = 0  # Each of the 3 generated areas will be done one at a time
    while areas_counter < 3:
        core = [[0, 0]]  # This is the middle and starting point for the sinkhole
        in_core = [[-1, 0], [0, 1], [1, 0], [0, -1]]  # These are the immediate parts - north, south, east, and west
        in_corns = [[-1, -1], [-1, 1], [1, 1], [1, -1]]  # These are the immediate diagonal spaces
        out_core = [[-2, -1], [-2, 0], [-2, 1], [-1, 2], [0, 2], [1, 2],  # These are more surrounding spaces
                    [2, 1], [2, 0], [2, -1], [1, -2], [0, -2], [-1, -2]]
        random_hor = random.randint(0, 1)  # The left OR right side of the board is chosen randomly
        random_ver = random.randint(0, 1)  # The top OR bottom of the board is chosen randomly
        random_hor *= len(board) - (len(board) // 2)  # If the right side of the board is chosen
        random_ver *= len(board) - (len(board) // 2)  # If the bottom of the board is chosen
        random_hor += 1 if random_hor == 0 else 0  # If the left side of the board is chosen
        random_ver += 1 if random_ver == 0 else 0  # If the top of the board is chosen
        if [random_hor, random_ver] in random_areas:  # If the random space has already been chosen it will be scrapped
            continue
        random_areas.append([random_hor, random_ver])  # The random space is recorded, so it won't be used again
        # A random core/centre_space is chosen within the part of the board predetermined before
        rand_core = [random.randint(0, (len(board) // 2) - 2), random.randint(0, (len(board) // 2) - 2)]
        rand_row, rand_col = rand_core[0] + random_ver, rand_core[1] + random_hor
        done = False  # This is for when all the sinkhole parts have been added and free_spaces need to be added
        while areas[areas_counter] > 0 or frees[areas_counter] > 0:  # Add the core, if it's not already taken
            if len(core) == 1 and [core[0][0] + rand_row, core[0][1] + rand_col] not in used_coordinates:
                board[core[0][0] + rand_row][core[0][1] + rand_col] = "U" if not done else "?"
                used_coordinates.append([core[0][0] + rand_row, core[0][1] + rand_col])
                core = []  # The coordinates are left empty to record they have been used
            elif len(in_core) > 0:  # Adds the immediate parts if they are not already taken
                rand_space = random.randint(0, len(in_core) - 1)
                if [in_core[rand_space][0] + rand_row, in_core[rand_space][1] + rand_col] in used_coordinates:
                    in_core.pop(rand_space)  # The space is popped to record it has been used
                    continue  # In the case the space has already been taken by another sinkhole, the space is scrapped
                board[in_core[rand_space][0] + rand_row][in_core[rand_space][1] + rand_col] = "U" if not done else "?"
                used_coordinates.append([in_core[rand_space][0] + rand_row, in_core[rand_space][1] + rand_col])
                in_core.pop(rand_space)  # The space is popped to record it has been used
            elif len(in_corns) > 0:  # Adds the immediate diagonal spaces
                rand_space = random.randint(0, len(in_corns) - 1)
                if [in_corns[rand_space][0] + rand_row, in_corns[rand_space][1] + rand_col] in used_coordinates:
                    in_corns.pop(rand_space)  # The space is popped to record it has been used
                    continue  # In the case the space has already been taken by another sinkhole, the space is scrapped
                board[in_corns[rand_space][0] + rand_row][in_corns[rand_space][1] + rand_col] = "U" if not done else "?"
                used_coordinates.append([in_corns[rand_space][0] + rand_row, in_corns[rand_space][1] + rand_col])
                in_corns.pop(rand_space)  # The space is popped to record it has been used
            else:  # Chooses more outer_spaces to add if necessary
                rand_space = random.randint(0, len(out_core) - 1)
                if (out_core[rand_space][0] + rand_row) not in range(len(board)):  # Scraps spaces outside the board
                    continue
                if (out_core[rand_space][1] + rand_col) not in range(len(board)):  # Scraps spaces outside the board
                    continue
                if [out_core[rand_space][0] + rand_row, out_core[rand_space][1] + rand_col] in used_coordinates:
                    out_core.pop(rand_space)  # The space is popped to record it has been used
                    continue  # In the case the space has already been taken by another sinkhole, the space is scrapped
                board[out_core[rand_space][0] + rand_row][out_core[rand_space][1] + rand_col] = "U" if not done else "?"
                used_coordinates.append([out_core[rand_space][0] + rand_row, out_core[rand_space][1] + rand_col])
                out_core.pop(rand_space)  # The space is popped to record it has been used
            if areas[areas_counter] > 0:  # When all sinkhole spaces are added, this moves to add the free_spaces
                areas[areas_counter] -= 1
                done = False if areas[areas_counter] > 0 else True
            else:
                frees[areas_counter] -= 1
        areas_counter += 1
    # This part switches the free_spaces to fairer positions where they have a high change of being able to be used
    blanks_tracker += 1
    board = ensure_usable_free_spaces(board)
    return board, blanks_tracker
