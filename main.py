import random
from boardstuff import make_a_move, create_board, print_board
from checkboard import check_patterns
from gamesetup import choose_game_type
from messagesandinfo import create_pattern_board
from blanks import get_blanks, get_blanks_for_cards, get_electricity, get_stepping_stones,\
    get_cows_and_bulls, get_lightning, get_sinkholes
from managecards import draw_cards
from commonfunctions import get_total_specified_spaces, change_symbols

'''
READ FIRST:
A pragmatic way to see what is happening with the code is to first run the game a few times and see the different
options and things you can do in the game. Then looking at the code should make more sense.
STAGES BEFORE THE GAME BEGINS:
- First, the user chooses the game type, which is essentially the patterns required to win the game.
- Second, the user chooses the play style or mode (Standard, As Many As You Can, or Cards).
- Third, the user chooses the board size.
- Fourth, the user is presented with the winning patterns, which are in some games created according to the board size.
- Fifth, if the play style or mode is Standard or As Many As You Can, the player will choose the blanks types.
'''


def play_game():
    board_size, shape_data, game_type, mode, shape_types, more_blanks = choose_game_type()
    board = create_board(board_size)
    if game_type == "Diamonds":  # SPECIAL CASE - Since corners are unusable in this game, they are removed
        board[0][0] = board[0][board_size - 1] = board[board_size - 1][0] = board[board_size - 1][board_size - 1] = " "
    title = game_type + " - " + mode
    print("\n" + title)
    create_pattern_board(shape_data, board_size)  # This prints the examples of winning patterns for the particular game
    input("\nPress Enter to continue. ")
    all_ls_shape_data = 0 if game_type != "Ls in Limbo" else shape_data  # SPECIAL CASE for l_patterns
    blank_types, no_of_blanks = "n", []
    if mode[0] != "C":  # Takes the user to the menu to choose the blanks_types for the game
        board, blank_types, no_of_blanks = get_blanks(board, mode, more_blanks)
    used_cards, random_cards = [], []  # For Cards mode - so all the cards will be used before the deck is reset
    blanks_tracker, turn_tracker, gained_free_spaces = 0, 0, []
    player, guard, player_x_score, player_o_score, congrats = "X", "", 0, 0, ""  # (congrats = winning/success message)
    print("\nIt's time to START the game!")
    is_game_over = False
    while not is_game_over and get_total_specified_spaces(board, ".") > 0:
        turn_tracker += 1
        title = game_type + " - " + mode + " - Turn: " + str(turn_tracker)
        if mode[0] == "C" and turn_tracker % 5 == 0:  # Removes players' spaces in Cards mode when board almost full
            board, change = eagle_eyed_eagle(board)
            if change:  # If change is True, then 1 or more spaces from each player was removed
                print(print_board(board, title, player_x_score, player_o_score, blank_types))
                input("\nPress Enter to continue.")
        if mode[0] == "C" and (turn_tracker - 5) % 10 == 0:  # For the next blank_types in Cards mode
            board, blank_types, no_of_blanks, blanks_tracker = next_blanks_for_cards(board, blank_types, more_blanks)
        if mode[0] == "C" and (turn_tracker - 1) % 10 == 0 and turn_tracker != 1:  # This is for Cards mode
            guards_message = ""
            if guard != "":  # Guard is one of the 6 kinds of cards (Guard Card)
                board = change_symbols(board, "G", ".")
                guards_message = f"\n\nAll of {guard}'s guards have finished their shifts."
            print(print_board(board, title, player_x_score, player_o_score, blank_types) + guards_message)
            first_player, guard, used_cards, random_cards =\
                draw_cards(board, player, title, player_x_score, player_o_score, blank_types, used_cards, random_cards)
            player = player if first_player == "" else first_player  # Makes the player who draws this card go first
            print("\nBack to the game!")
        if blank_types != "n":  # Moves the blanks to the next position depending on the blanks_types
            board, blanks_tracker, end_of_game = move_blanks(board, blank_types, no_of_blanks, blanks_tracker,
                                                             gained_free_spaces)
            if end_of_game:  # Declares the end of the game for some blanks_types
                break
        if game_type == "Ls in Limbo":  # Sets the winning l_patterns according to the timing
            shape_data = ls_in_limbo_count(all_ls_shape_data, shape_data, turn_tracker)
        print(print_board(board, title, player_x_score, player_o_score, blank_types))
        print("\nIt's " + player + "'s turn.")
        board, row, column = make_a_move(board, player, False, guard)  # Gets the next position from the user
        # The line below goes to the check_pattern function which provides data on new patterns made
        made_new_pattern, messages, gained_free_spaces = check_patterns(row, column, board, player, shape_data)
        if made_new_pattern > 0:  # This part processes the new pattern and declares a winner or adds to the score
            is_game_over, congrats = process_new_pattern(player, messages, mode, gained_free_spaces, blank_types)
        if player == "X":
            player_x_score += made_new_pattern  # made_new_pattern has the number of new patterns the player just made
            player = "O"
        else:
            player_o_score += made_new_pattern
            player = "X"
    title = game_type + " - " + mode + " - GAME OVER!"
    print(print_board(board, title, player_x_score, player_o_score, blank_types))
    game_over_messages(board, mode, congrats, player_x_score, player_o_score)  # Prints the messages for the end of game
    next_up = input("\nPress Enter to play again OR any key + Enter to terminate the program. ")
    if next_up == "":
        play_game()


def game_over_messages(board, mode, congrats, player_x_score, player_o_score):
    if mode[0] == "S":  # In Standard mode, if the board is full at the end, it's a draw
        print("\n" + congrats)
        draw_message = " It's a draw!" if get_total_specified_spaces(board, ".") == 0 else ""
        print("\nGAME OVER!" + draw_message)
    else:  # For other modes, the winner is calculated according to the total amount of points
        print("\nGAME OVER!")
        if player_x_score > player_o_score:
            print(f"\nPlayer X has won with a score of {player_x_score}! Player O got a score of {player_o_score}.")
        elif player_o_score > player_x_score:
            print(f"\nPlayer O has won with a score of {player_o_score}! Player X got a score of {player_x_score}.")
        else:
            print(f"\nIt's a draw! Both players scored {player_x_score}.")


def ls_in_limbo_count(all_ls_shape_data, current_shape_data, turn_tracker):
    turn_tracker -= 1
    if turn_tracker == 0:  # For the very first turn of the game
        print("\nFor now, normal and reversed L patterns count.")
        return current_shape_data
    if turn_tracker % 3 != 0:  # The winning l_patterns change every 3 turns
        return current_shape_data
    normal_ls, reversed_ls, all_ls = {}, {}, {}
    normal_ls["l_patterns"] = all_ls_shape_data["l_patterns"]
    reversed_ls["rev_l_patterns"] = all_ls_shape_data["rev_l_patterns"]
    all_ls = all_ls_shape_data
    if turn_tracker % 3 == 0 and turn_tracker % 6 != 0 and turn_tracker % 9 != 0:
        print("\nTHE POWER OF NATURE will only allow reversed L patterns!")
        return reversed_ls
    elif turn_tracker % 6 == 0 and turn_tracker % 9 != 0:
        print("\nTHE POWER OF NATURE will only allow the most normal L patterns!")
        return normal_ls
    elif turn_tracker % 9 == 0:
        print("\nTHE POWER OF NATURE has calmed. All Ls count!")
        return all_ls


def eagle_eyed_eagle(board):  # This function removes players' spaces in Cards mode when the board is almost full
    if get_total_specified_spaces(board, ".") < len(board) + (len(board) - 3):
        print("\nThe eagle-eyed-eagle has seen that the board is too full.")
        spaces_poached = 0
        while get_total_specified_spaces(board, ".") < len(board) + (len(board) - 3):
            if get_total_specified_spaces(board, "X") == 0 or get_total_specified_spaces(board, "O") == 0:
                break
            x_row_num, x_col_num = random.randint(0, len(board) - 1), random.randint(0, len(board) - 1)
            o_row_num, o_col_num = random.randint(0, len(board) - 1), random.randint(0, len(board) - 1)
            if board[x_row_num][x_col_num] == "X" and board[o_row_num][o_col_num] == "O":
                board[x_row_num][x_col_num], board[o_row_num][o_col_num] = ".", "."
                spaces_poached += 2
        if spaces_poached > 0:
            print(f"{spaces_poached // 2} of X's spaces and {spaces_poached // 2} of O's spaces were poached.")
            return board, True
        else:
            print("\nBut it was impossible for the eagle to poach any spaces...")
            return board, False
    else:
        return board, False


def clear_blanks(board, blanks_types):  # Clears of the blanks of the last type so the next type can be added
    bls_change = {"e": ["V", "Z"], "h": ["H", "H"], "s": ["S", "K"], "c": ["C", "B"], "v": ["V", "V"], "u": ["U", "U"]}
    board = change_symbols(board, bls_change[blanks_types][0], ".")
    board = change_symbols(board, bls_change[blanks_types][1], ".")
    board = change_symbols(board, "?", ".")
    return board


def next_blanks_for_cards(board, blank_types, more_blanks):  # Adds the next blanks_types for Cards mode
    low_blank_types_list = ["e", "h", "s"]  # The game starts with these blanks_types
    high_blank_types_list = ["c", "v", "u"]  # The game will alternative between this list and the list above
    if blank_types != "n":
        board = clear_blanks(board, blank_types)
    if blank_types in low_blank_types_list:
        choose_blanks_from = high_blank_types_list
    else:
        choose_blanks_from = low_blank_types_list
    random_blanks = random.randint(0, 2)
    blank_types, blanks_tracker = choose_blanks_from[int(random_blanks)], 0
    board, no_of_blanks, blanks_tracker = get_blanks_for_cards(board, blank_types, more_blanks)
    return board, blank_types, no_of_blanks, blanks_tracker


def move_blanks(board, blank_types, no_of_blanks, blanks_tracker, gained_free_spaces):  # Moves the blanks around board
    end_of_game = False
    if blank_types == "e":
        board, blanks_tracker = get_electricity(board, no_of_blanks, blanks_tracker, len(gained_free_spaces))
    elif blank_types == "h":
        print("\nThe honey badgers remain BOLD - the ones that are honey badgers that is.")
    elif blank_types == "s":
        board, blanks_tracker = get_stepping_stones(board, no_of_blanks, blanks_tracker)
    elif blank_types == "c":
        board, blanks_tracker = get_cows_and_bulls(board, no_of_blanks, blanks_tracker)
        if blanks_tracker == (len(board) * len(board)) + 1:
            end_of_game = True
    elif blank_types == "v":
        board, blanks_tracker = get_lightning(board, no_of_blanks, blanks_tracker)
        if blanks_tracker == (len(board) * len(board)) + 1:
            end_of_game = True
    else:
        board, blanks_tracker = get_sinkholes(board, no_of_blanks, blanks_tracker)
        if blanks_tracker == (len(board) * len(board)) + 1:
            end_of_game = True
    return board, blanks_tracker, end_of_game


def process_new_pattern(player, messages, mode, free_spaces, blank_types):
    # This function creates the messages when a player makes a new winning/scoring pattern (It also declares game over)
    game_over, win_message, fr_space_message, free_space_coordinates = False, "", "", ""
    if mode[0] == "S":
        game_over, win_message = True, f" {player} has won!"
    congrats = f"{player} "
    counter = 0
    for message in messages:
        congrats += message if counter == 0 else ", AND " + message
        counter += 1
    if len(free_spaces) > 0:
        blank_message = "found {0} cheetah cub{1} and used {2}! " if blank_types == "h" else "grabbed {0} free gem{1}! "
        if len(free_spaces) == 1:
            blank_message = blank_message.format("a", "", "it")
        elif len(free_spaces) == 2:
            blank_message = blank_message.format(len(free_spaces), "s", "them")
        elif len(free_spaces) >= 3:
            blank_message = blank_message.format("a number of", "s", "them")
        free_spaces.sort()
        for free_space in free_spaces:
            free_space_coordinates += f"(Row {free_space[0] + 1} Column {free_space[1] + 1}) "
        fr_space_message = f"\n{player} also {blank_message}" + free_space_coordinates + "- Impressive job!"
    congrats += "!"
    if mode[0] != "S":
        print("\nACHIEVEMENT!\n" + congrats + fr_space_message)
    return game_over, congrats + win_message + fr_space_message


print("\nGame time!")
play_game()
