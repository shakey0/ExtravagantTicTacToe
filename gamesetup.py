from initialshapedata import get_full_shape_data
from commonfunctions import is_input_valid


def choose_game_type():
    opening_program_welcome_messages()  # Displays the welcoming messages and basic information
    game_type = ""
    mode_types = {}
    while True:
        initial_choose_game()  # Displays all the game types and options with the letter commands for each one
        print("Press the letter of the game you want to play and then press Enter.")
        board_size = 0
        mode = ""
        while True:
            choice = input("")
            choice = choice.lower()
            game_data = dictionary_of_lines_and_shapes(choice, 1)  # Gets the required game data for the game type
            if game_data == 0:  # If game_data is 0 then the user entered a choice that wasn't in the dictionary
                print("Unrecognised choice.")
                continue
            else:
                board_size, mode = get_board_size_and_mode(game_data)  # Gets the board size and mode of game
                break
        if board_size == 0:  # If board_size == 0, then the user quit setting up this game type
            continue
        mode_types = {"s": "Standard", "a": "As Many As You Can", "c": "Cards"}  # GAME MODE TYPES
        n = "n" if board_size == 8 else ""  # Adjusts the grammar for 8, since it starts with a vowel
        game_type = game_data[0]  # This is the type or name of the game that the players selected
        print(f"\nYou have chosen {game_type}, in {mode_types[mode]} mode, on a{n} {board_size} by {board_size}"
              f" board.\nAre you sure? Press Y + Enter to confirm, or Q + Enter to go back to the main menu.")
        while True:
            confirm = input("")
            confirm = confirm.lower()
            if confirm == "y" or confirm == "q":
                break
            print("Press Y + Enter to confirm, or Q + Enter to go back to the main menu.")
        if confirm == "y":
            break
    shape_types = game_data[1]  # This has the winning shape names
    shape_data = get_full_shape_data(board_size, shape_types)  # The winning shape data is retrieved from the dictionary
    more_blanks = game_data[5]  # This gets a number that says how many blanks are needed (to make the level reasonable)
    return board_size, shape_data, game_type, mode_types[mode], shape_types, more_blanks


def get_board_size_and_mode(game_data):  # Gets the mode and board_size for the game
    game_type = game_data[0]
    print("\n" + 66 * "-" + f"\nYou have chosen {game_type}.")
    play_styles = [f"\nCHOOSE YOUR PLAY STYLE:                   AVAILABLE BOARD SIZES",
                   f"S = Standard (One line or shape to win)   ",
                   f"A = As Many As You Can (The most wins)    ",
                   f"C = Cards (CR = Cards Rules)              "]
    print(play_styles[0])  # Prints the titles above
    counter = 1
    m_b_sizes = [game_data[2], game_data[3], game_data[4]]  # MIN_BOARD_SIZES
    while counter < 4:
        if m_b_sizes[counter - 1] != 0:  # If m_b_sizes == 0, the play style is not available for the game type
            if m_b_sizes[counter - 1] < 8:  # This is the message for most boards
                board_min_message = f"{m_b_sizes[counter - 1]} by {m_b_sizes[counter - 1]} to 9 by 9 board"
            elif m_b_sizes[counter - 1] == 8:  # Adjusts the grammar/message
                board_min_message = "8 by 8 or 9 by 9 board"
            else:  # Adjusts the grammar/message
                board_min_message = "9 by 9 board only"
            print(play_styles[counter] + board_min_message)  # Adds the message to the message above and prints it
        counter += 1
    print("\nChoose your style of game and press Enter. Or press Q + Enter to go back to the main page.")
    min_board_size = 0
    mode = ""
    while min_board_size == 0:  # Sets the minimum board size to the listed minimum size for the game type and mode
        mode = input()
        mode = mode.lower()
        if mode == "s":
            min_board_size = game_data[2]
            print("\nYou have chosen STANDARD mode.")
        elif mode == "a" and game_data[3] != 0:  # Some games can't be played in As Many As You Can mode (this skips it)
            min_board_size = game_data[3]
            print("\nYou have chosen AS MANY AS YOU CAN mode.")
        elif mode == "c":
            min_board_size = game_data[4]
            print("\nYou have chosen CARDS mode.")
        elif mode == "q":  # Quits setting up the mode and returns to the main menu
            return 0, ""
        else:
            print("Unrecognised choice.")
    if min_board_size < 8:  # This is the message for most boards
        message = f"(Between {min_board_size} and 9 inclusive)"
    elif min_board_size == 8:  # Adjusts the grammar/message
        message = "(8 or 9)"
    else:  # Automatically sets the board size, as 6 in a row in Standard mode can only be played on a 9 by 9 board
        return 9, mode
    print(f"Choose your board size - x by x squares. " + message)
    while True:
        board_size = input("\nBoard size: ")
        if board_size == "q":  # Quits setting up the board size and returns to the main menu
            return 0, ""
        if is_input_valid(board_size, (min_board_size, 9)):
            return int(board_size), mode  # Returns the chosen board size and mode
        else:
            continue


def dictionary_of_lines_and_shapes(choice_or_keys, one_or_all):  # The # list below explains the list items
    lines_and_types_dictionary = {  # VALUES OF DICTIONARY LISTS EXPLAINED ON LINE BELOW
        # VALUES IN EACH LIST: [0 = name, 1 = shape_list, 2 = min_board_size for 'Standard' games,
        # 3 = min_board_size for 'As Many As You Can' games, 4 = min_board_size for 'Card' games], 5 = more_blanks
        "3": ["Lines of 3", ["lines_of_3"], 3, 5, 6, 3],
        "4": ["Lines of 4", ["lines_of_4"], 5, 7, 7, 1],
        "5": ["Lines of 5", ["lines_of_5"], 7, 0, 7, 0],
        "6": ["Lines of 6", ["lines_of_6"], 9, 0, 8, 0],
        "s": ["Squares", ["squares"], 5, 7, 7, 1],
        "d": ["Diamonds", ["diamonds", "exp_diamonds"], 6, 8, 8, 0],
        "v": ["Lightning", ["lightning"], 4, 6, 7, 2],
        "t": ["T-Shapes", ["t_patterns"], 4, 6, 7, 2],
        "h": ["Horseshoes", ["horseshoes"], 5, 0, 8, 1],
        "u": ["Turning Lines", ["turning_lines"], 6, 0, 8, 0],
        "z": ["Zigzag Lines", ["zigzag_patterns"], 6, 0, 8, 0],
        "f": ["Funny Shapes", ["funny_shapes"], 6, 0, 8, 0],
        "c": ["Magical Corners", ["corners", "rot_corners", "exp_squares", "exp_diamonds"], 5, 7, 7, 0],
        "q": ["Square Quest", ["squares", "exp_squares"], 4, 6, 7, 1],
        "n": ["Ts & Lightning", ["t_patterns", "lightning"], 4, 5, 6, 2],
        "x": ["Corners & Lightning", ["corners", "rot_corners", "lightning"], 4, 6, 7, 2],
        "l": ["Ls in Limbo", ["l_patterns", "rev_l_patterns"], 4, 5, 6, 2],
        "a": ["Classic 4s Mix", ["lines_of_4", "squares", "diamonds", "corners", "rot_corners"], 4, 6, 7, 1],
        "b": ["Classic 5s Mix", ["lines_of_5", "turning_lines", "zigzag_patterns"], 6, 0, 7, 0],
        "w": ["Wacky 5s", ["zigzag_patterns", "funny_shapes"], 5, 0, 7, 0],
        "m": ["Mathematical Madness", ["lines_of_5", "turning_lines", "crosses", "pluses"], 6, 0, 7, 0],
        "j": ["5s & Funny Shapes", ["lines_of_5", "funny_shapes"], 6, 0, 7, 0]
    }
    if one_or_all == 1 and choice_or_keys in lines_and_types_dictionary:  # Gets the chose game type data
        return lines_and_types_dictionary[choice_or_keys]
    elif one_or_all == 0:  # Gets all the game type names to print in the main menu
        list_of_games = {}
        for letter in lines_and_types_dictionary:
            list_of_games[letter] = lines_and_types_dictionary[letter][0]
        return list_of_games
    else:
        return 0  # If game_data is 0 then the user entered a choice that wasn't in the dictionary


def initial_choose_game():
    print("-" * 30 + "ALL GAME TYPES" + "-" * 33 + "\n" + 77 * "-")  # Prints the lines and title
    list_of_games = dictionary_of_lines_and_shapes("", 0)  # Gets the game type names from the dictionary
    list_of_games_to_display = [["SIMPLE 4 GAMES", "s", "d", "v", "t"],
                                ["SIMPLE 5 GAMES", "h", "u", "z", "f"],
                                ["SIMPLE LINE GAMES", "3", "4", "5", "6"],
                                ["CLASSIC MIXES", "c", "q", "n", "x", "l", "a", "b", "w", "m", "j"]]
    for line in list_of_games_to_display:  # Takes the letters above and gets their names from the dictionary
        counter = 0
        for item in line:
            if item in list_of_games:
                line[counter] = item.upper() + " = " + list_of_games[item]
            counter += 1
    counter = 0
    choose_game_display_message = ""
    while counter < 5:  # Prints the 'SIMPLE GAMES' line by line in 3 columns
        choose_game_display_message += list_of_games_to_display[0][counter]
        choose_game_display_message += " " * (30 - len(list_of_games_to_display[0][counter]))
        choose_game_display_message += list_of_games_to_display[1][counter]
        choose_game_display_message += " " * (30 - len(list_of_games_to_display[1][counter]))
        choose_game_display_message += list_of_games_to_display[2][counter] + "\n"
        counter += 1
    counter = 1
    choose_game_display_message += "\n" + (23 * "-") + list_of_games_to_display[3][0] + (41 * "-") + "\n"
    while counter < 11:  # Prints the 'CLASSIC MIXES' line by line in 2 columns
        choose_game_display_message += list_of_games_to_display[3][counter]
        choose_game_display_message += " " * (40 - len(list_of_games_to_display[3][counter]))
        counter += 1
        choose_game_display_message += list_of_games_to_display[3][counter] + "\n"
        counter += 1
    print(choose_game_display_message)  # Prints the full main menu


def opening_program_welcome_messages():
    print("\nWelcome to extravagant Tic Tac Toe! Press any key to continue.")
    input("")
    print(37 * "-" + "\n\nWow! So many choices below! Enjoy!"
          "\n\nSquares, Diamonds, L-Shapes\nLighting Shapes, T-Shapes\nHorseshoes, Funny Shapes"
          "\nZigzag Lines, Turning Lines\nCrosses, Pluses\nRotating Corners, Invisible Corners"
          "\nLines of 4, Lines of 5, Lines of 6"
          "\n\nTo choose your game type press Enter.")
    input("")
