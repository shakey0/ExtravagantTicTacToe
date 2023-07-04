import random
from commonfunctions import is_input_valid, get_total_specified_spaces, scatter_items_around_board
from boardstuff import make_a_move, get_positions, print_board


def get_actions():  # Gets the random numbers for Cards, so they can be drawn randomly
    random_numbers = []
    counter = 0
    while counter < 6:
        new_number = random.randint(1, 6)
        if new_number not in random_numbers:
            random_numbers.append(new_number)
            counter += 1
    return random_numbers


def draw_cards(board, player, title, player_x_score, player_o_score, blank_types, used_cards, random_cards):
    first_player, guard = "", ""
    print(f"\nIt's time to draw the cards!\n\nThe cards are laid out in a fan.")
    input("Press Enter to see them. ")
    cards = ["A", "B", "C", "D", "E", "F"]
    if len(used_cards) == 6 or len(random_cards) == 0:  # If all the cards have been drawn, the deck is reset
        random_cards, used_cards = get_actions(), []
    draw_counter = 0
    while draw_counter < 2:  # Each player will draw a card
        print(f"\nPlayer {player}, choose one of these cards: ")
        print("\n" + "  ".join(cards))
        while True:
            card = input("")
            card = card.lower()
            if card == "a" and card not in used_cards:
                action = random_cards[0]
                break
            elif card == "b" and card not in used_cards:
                action = random_cards[1]
                break
            elif card == "c" and card not in used_cards:
                action = random_cards[2]
                break
            elif card == "d" and card not in used_cards:
                action = random_cards[3]
                break
            elif card == "e" and card not in used_cards:
                action = random_cards[4]
                break
            elif card == "f" and card not in used_cards:
                action = random_cards[5]
                break
            else:
                print("There's none of that card!")
        used_cards.append(card)
        opponent = "O" if player == "X" else "X"
        if action == 1:  # STRIKE OUT CARD
            print(print_board(board, title, player_x_score, player_o_score, blank_types))
            print(f"\n{player} has picked a STRIKE OUT card. Strike out up to {len(board) - 4} of {opponent}'s spaces!")
            struck_coordinates = []  # This is for printing out the messages of which spaces were struck out
            counter = 0
            while counter < len(board) - 4 and get_total_specified_spaces(board, opponent) > 0:
                prompt_message = "\nThe first space:" if counter == 0 else "\nThe next space:"
                print(prompt_message)
                board, row, col = make_a_move(board, player, True, "")
                struck_coordinates.append([row, col])
                counter += 1
                print(print_board(board, title, player_x_score, player_o_score, blank_types))
                if get_total_specified_spaces(board, opponent) == 0:
                    break
                if counter != len(board) - 4:
                    print(f"\n{player} struck {opponent} off the board at Row {row+1} Column {col+1}!")
            struck_spaces_message, grammar, grammar_counter = "", ",", len(board) - 4
            for coordinates in struck_coordinates:
                grammar = ", " if grammar_counter > 2 else ", and " if grammar_counter == 2 else "."
                struck_spaces_message += f"Row {coordinates[0]+1} Column {coordinates[1]+1}{grammar}"
                grammar_counter -= 1
            print(f"\n{player} struck their opponent from the board at {struck_spaces_message}")
        elif action == 2:  # STRIKE LINE CARD
            print(print_board(board, title, player_x_score, player_o_score, blank_types))
            print("\nYou have picked a STRIKE LINE card. Strike out an entire line from the board!")
            board, message, row_or_col, guard_in_line = strike_line(board)
            print(print_board(board, title, player_x_score, player_o_score, blank_types))
            print(f"\n{player} completely wiped {message} {row_or_col+1} clean!")
            if guard != "" and guard_in_line:
                print(f"{guard}'s guards managed to stay on the board, but fled to different spaces.")
        elif action == 3:  # FIRST USER CARD
            print("\nYou have picked a ME FIRST card. If you aren't already first, you will be now!")
            first_player = player
        elif action == 4:  # STINK BOMB CARD
            print(print_board(board, title, player_x_score, player_o_score, blank_types))
            print("\nYou have picked a STINK BOMB card. Players in the close by area will run far away!")
            board, row, col, guard_in_line = get_stink_bomb(board)
            print(print_board(board, title, player_x_score, player_o_score, blank_types))
            print(f"\n{player} threw a stenching stink bomb onto the board at Row {row+1} Column {col+1}!"
                  f"\nAll player pieces fled the area!")
            if guard != "" and guard_in_line:
                print(f"{guard}'s guards did their job and withstood the horribly unpleasant stench.")
        elif action == 5:  # TORNADO CARD
            print(print_board(board, title, player_x_score, player_o_score, blank_types))
            print("\nYou have picked a TORNADO card. Chose an area of the board to strike with a powerful tornado!")
            board, coming_from, line, guard_in_line = get_tornado(board)
            print(print_board(board, title, player_x_score, player_o_score, blank_types))
            r_or_c = "row" if coming_from == "east" or coming_from == "west" else "column"
            print(f"\n{player} sent a powerful tornado from the {coming_from} that hit {r_or_c} {line+1}!")
            if guard != "" and guard_in_line:
                print(f"{guard}'s guards put up a strong defense, but were still blown around by the wind.")
        else:  # GUARD CARD
            print(print_board(board, title, player_x_score, player_o_score, blank_types))
            print(f"\nYou have picked a GUARD card. Choose {len(board) - 4} spaces to guard.")
            counter = 0
            while counter < len(board) - 4:
                prompt_message = "\nThe first space to guard:" if counter == 0 else "\nThe next space to guard:"
                print(prompt_message)
                board, row, col = make_a_move(board, player, False, "G")
                counter += 1
                print(print_board(board, title, player_x_score, player_o_score, blank_types))
                print(f"\n{player} guarded Row {row+1} Column {col+1}!")
            print("Your spaces will be guarded until you need them. Just remember that bulls may still charge them "
                  "down,\nlightning may still strike them out, and sinkholes may still swallow them.")
            guard = player
        draw_counter += 1
        input("\nPress Enter to continue. ")
        player = "O" if player == "X" else "X"
    return first_player, guard, used_cards, random_cards


def get_tornado(board):
    print("Press N to strike from the NORTH, E to strike from the EAST,"
          "\nS to strike from the SOUTH, and W to strike from the WEST.")
    directions = ["n", "e", "s", "w"]
    direction_words = {"n": "north", "e": "east", "s": "south", "w": "west"}
    while True:
        wind_coming_from = input("")
        wind_coming_from = wind_coming_from.lower()
        if wind_coming_from in directions:
            break
        else:
            print("That's not a direction!")
    print(f"\nChoose a line from {2} to {len(board) - 1}")
    while True:
        line = input("")
        if is_input_valid(line, (2, len(board) - 1)):
            break
    line = int(line) - 1
    if wind_coming_from == "n":
        row, col, mover, side_mover = 0, line, [1, 0], [[0, 1], [0, -1]]
    elif wind_coming_from == "e":
        row, col, mover, side_mover = line, len(board) - 1, [0, -1], [[1, 0], [-1, 0]]
    elif wind_coming_from == "s":
        row, col, mover, side_mover = len(board) - 1, line, [-1, 0], [[0, 1], [0, -1]]
    else:
        row, col, mover, side_mover = line, 0, [0, 1], [[1, 0], [-1, 0]]
    tornado_lines, blown_coordinates, all_blown_items = 0, [], []
    while tornado_lines < 3:  # 3 lines of the board are blown by the tornado
        sides = [0, 0] if tornado_lines == 0 else side_mover[0] if tornado_lines == 1 else side_mover[1]
        counter, blown_items = 0, []
        blow_distance = len(board) - 3 if tornado_lines == 0 else len(board) - 4  # Middle tornado line 1 space longer
        while counter < blow_distance:  # Picks up all the blown items and empties the spaces
            current_row, current_col = row + (mover[0] * counter) + sides[0], col + (mover[1] * counter) + sides[1]
            blown_items.append(board[current_row][current_col])
            blown_coordinates.append([current_row, current_col])
            board[current_row][current_col] = "."
            counter += 1
        destroyable = [".", "X", "O", "?"]
        while counter < len(board) and len(blown_items) > 0:  # This eliminates empty spaces from blown_items
            if blown_items[0] == ".":
                blown_items.pop(0)
                continue
            current_row, current_col = row + (mover[0] * counter) + sides[0], col + (mover[1] * counter) + sides[1]
            blown_items.append(board[current_row][current_col])  # Picks up the last item in the space
            board[current_row][current_col] = blown_items[0]  # Adds the blown item from x spaces before to the space
            blown_items.pop(0)  # Pops the blown item from x spaces before from the list (marking it as done)
            counter += 1
        if len(blown_items) > 0:  # This pops all items that are eligible to be removed from the board
            counter = 0
            while counter < len(blown_items):
                if blown_items[counter] in destroyable:
                    blown_items.pop(counter)
                else:
                    counter += 1
        tornado_lines += 1
        all_blown_items += blown_items
    # This part scatters all the blown_items that are to be kept around the board
    board, guard_in_line = scatter_items_around_board(board, all_blown_items, blown_coordinates)
    return board, direction_words[wind_coming_from], line, guard_in_line


def get_stink_bomb(board):
    escape_area = [[0, 0], [-1, 0], [0, 1], [1, 0], [0, -1], [-1, -1], [-1, 1], [1, 1], [1, -1]]
    outer_area = [[-2, -1], [-2, 0], [-2, 1], [-1, 2], [0, 2], [1, 2],  # These are more surrounding spaces
                  [2, 1], [2, 0], [2, -1], [1, -2], [0, -2], [-1, -2]]
    row, column = get_positions(len(board))
    moved_xs, moved_os, guard_in_area = 0, 0, False
    counter = 0
    vacated_area = []
    while counter < 9:  # All players' pieces in the 9-space-square around the stink_bomb are removed
        current_row, current_col = row + escape_area[counter][0], column + escape_area[counter][1]
        vacated_area.append([current_row, current_col])
        if current_row in range(len(board)) and current_col in range(len(board)):
            if board[current_row][current_col] == "X":
                moved_xs += 1
                board[current_row][current_col] = "."
            elif board[current_row][current_col] == "O":
                moved_os += 1
                board[current_row][current_col] = "."
            elif board[current_row][current_col] == "G":  # For the slightly funny guards_message later
                guard_in_area = True
        counter += 1
    counter = 0
    outer_vacated = []  # The larger the board, the more spaces this next part will choose
    while counter < len(board) - 5:  # The outer_area of the stink_bomb-clear-zone are selected randomly
        random_outer = random.randint(0, 11)
        current_row, current_col = row + outer_area[random_outer][0], column + outer_area[random_outer][1]
        if [current_row, current_col] in outer_vacated:
            continue
        outer_vacated.append([current_row, current_col])
        if current_row in range(len(board)) and current_col in range(len(board)):
            if board[current_row][current_col] == "X":
                moved_xs += 1
                board[current_row][current_col] = "."
            elif board[current_row][current_col] == "O":
                moved_os += 1
                board[current_row][current_col] = "."
            elif board[current_row][current_col] == "G":
                guard_in_area = True
        counter += 1
    empty_spaces = get_total_specified_spaces(board, ".")  # If there aren't enough empty spaces, players' space removed
    while empty_spaces - (moved_xs + moved_os) < moved_xs + moved_os:
        if moved_xs > 0:
            moved_xs -= 1
        if moved_os > 0:
            moved_os -= 1
    low_possibility = 0
    while moved_xs > 0 or moved_os > 0:  # The players' pieces are added back to the board randomly
        low_possibility += 1
        if low_possibility == (len(board) * len(board)) * 3:
            break
        if moved_xs == 0 and moved_os == 0:  # If no players' pieces were affected by the stink_bomb, the process ends
            return board, row, column
        elif moved_xs > 0 and moved_os == 0:
            x_or_o = "X"
        elif moved_os > 0 and moved_xs == 0:
            x_or_o = "O"
        else:
            coin_flip = random.randint(0, 1)  # X and O are chosen randomly to keep it fair
            x_or_o = "X" if coin_flip == 0 else "O"
        random_row, random_col = random.randint(0, len(board) - 1), random.randint(0, len(board) - 1)
        if [random_row, random_col] in vacated_area or [random_row, random_col] in outer_vacated:
            continue
        if board[random_row][random_col] == ".":
            board[random_row][random_col] = x_or_o
            if x_or_o == "X":
                moved_xs -= 1
            else:
                moved_os -= 1
    return board, row, column, guard_in_area


def strike_line(board):
    print("Press R + Number to strike out a row, or C + Number to strike out a column.")
    direction = [[0, 1], [1, 0]]  # Directions for ROWS and COLUMNS
    line, row_or_col = [], ""
    message = ""
    while True:
        strike = input("")
        if len(strike) != 2:
            print("Unrecognised command!")
            continue
        if strike[0] == "R" or strike[0] == "r":
            line = direction[0]
            message = "Row"
        elif strike[0] == "C" or strike[0] == "c":
            line = direction[1]
            message = "Column"
        else:
            print("Unrecognised command!")
            continue
        row_or_col = strike[1]
        if is_input_valid(row_or_col, (1, len(board))):
            break
    row_or_col = int(row_or_col) - 1
    if line[0] == 0:
        coordinates = [row_or_col, 0]
    else:
        coordinates = [0, row_or_col]
    destroyable = [".", "X", "O", "?"]
    to_be_moved, struck_coordinates = [], []
    while coordinates[0] < len(board) and coordinates[1] < len(board):  # The line is cleared
        if board[coordinates[0]][coordinates[1]] not in destroyable:  # Keeps items that must be kept on the board
            to_be_moved.append(board[coordinates[0]][coordinates[1]])
        board[coordinates[0]][coordinates[1]] = "."
        struck_coordinates.append([coordinates[0], coordinates[1]])
        coordinates[0] += line[0]
        coordinates[1] += line[1]
    # All spaces that must be kept on the board are added back to the board in random places
    board, guard_in_line = scatter_items_around_board(board, to_be_moved, struck_coordinates)
    return board, message, row_or_col, guard_in_line
