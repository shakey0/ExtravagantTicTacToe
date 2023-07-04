from commonfunctions import is_input_valid


def make_a_move(board, player, strike, guard):  # This deals with making a move and whether the position is allowed
    # SHOULD USE A DICTIONARY HERE
    opponent = "O" if player == "X" else "X"
    while True:
        row, column = get_positions(len(board))  # Gets the row and column of the space from the user
        if strike:  # This part is specifically for the Strike Card
            if board[row][column] == opponent:
                board[row][column] = "."
                return board, row, column
            elif board[row][column] == player:
                print("\nYou don't want to strike yourself!\n")
            elif board[row][column] == ".":
                print("\nThere's nothing to strike there!\n")
            elif board[row][column] == "G":
                print("\nYou can't strike a guard!\n")
            else:
                print("\nYou can't strike there!\n")
        elif board[row][column] == player and guard == "G":
            print("\nGuards will stand next to you, not on top of you!\n")
        elif board[row][column] == player:
            print("\nYou're already sitting in that space!\n")
        elif board[row][column] == opponent:
            print(f"\nThat space belongs to {opponent}!\n")
        elif board[row][column] == "G" and guard == "G":
            print("\nYou've already got a guard in that space!\n")
        elif board[row][column] == "G" and guard == opponent:
            print(f"\n{opponent} has put that space under surveillance!\n")
        elif board[row][column] == "V":
            print("\nYou'll get electrocuted if you go here!\n")
        elif board[row][column] == "Z":
            print("\nThis space is fully charged!\n")
        elif board[row][column] == "H":
            print("\nEven lions don't mess with honey badgers!\n")
        elif board[row][column] == "S":
            print("\nA stone is currently occupying this space!\n")
        elif board[row][column] == "K":
            print("\nNobody can make a move on a King Rock!\n")
        elif board[row][column] == "C":
            print("\nLeave this poor grazing cow alone!\n")
        elif board[row][column] == "B":
            print("\nMess with a bull and you'll end up in A&E!\n")
        elif board[row][column] == "U":
            print("\nYou'll be swallowed into a dark oblivion here!\n")
        elif board[row][column] == "T":
            print("\nThat part of the toadstool will kill you!\n")
        elif board[row][column] == "?":
            print("\nFree spaces are to be earned!\n")
        elif board[row][column] == " ":
            print("\nThat space isn't even on the board!\n")
        else:
            if guard == "G":  # This part is specifically for the Guard Card
                board[row][column] = "G"
                break
            confirm = input(f"\nYou have chosen ROW {row + 1}, COLUMN {column + 1}."
                            f"\nPress Enter to CONFIRM, or any other key + Enter to choose again. ")
            if confirm == "":
                if board[row][column] == "G":
                    print(f"\n{player}'s guard stepped away after a well done job.")
                board[row][column] = player  # This places X or O in their chosen position on the board
                break
    return board, row, column


def get_positions(board_size):  # Gets the valid row and column of the space from the user
    counter = 0
    while True:
        if counter == 1:
            print("")
        row = input("Enter a row: ")
        if is_input_valid(row, (1, board_size)):
            row = int(row) - 1
            break
        else:
            counter = 1
    counter = 0
    while True:
        if counter == 1:
            print("")
        column = input("Enter a column: ")
        if is_input_valid(column, (1, board_size)):
            column = int(column) - 1
            break
        else:
            counter = 1
    return row, column


def create_board(board_size):  # Creates the board at the start of the game according to the size the players chose
    final_board = []
    row_counter = 1
    while row_counter <= board_size:
        line = []
        line_counter = 1
        while line_counter <= board_size:
            line.append(".")
            line_counter += 1
        final_board.append(line)
        row_counter += 1
    return final_board


def print_board(board, title, player_x_score, player_o_score, blank_types):  # Formats the board and prints it
    formatted_rows = []
    # This part adds the column numbers along the top of the board
    top_numbers = []
    column_counter = 1
    while column_counter <= len(board):
        column_counter_str = str(column_counter)
        top_numbers.append(column_counter_str)
        column_counter += 1
    formatted_rows.append(" ".join(top_numbers))
    # This part formats the rows of the board (including the column numbers along the top)
    for row in board:
        formatted_rows.append(" ".join(row))
    # This part adds the row numbers down the side of the board and the side info on the right of the board
    row_counter = 0
    while row_counter <= len(board):
        if blank_types == "h":
            formatted_rows[row_counter] = formatted_rows[row_counter].replace("?", "H")
        row_counter_str = str(row_counter)
        if row_counter_str == "0":
            row_counter_str = " "
        formatted_rows[row_counter] = " " + row_counter_str + " " + formatted_rows[row_counter]
        if row_counter == 0:
            formatted_rows[0] += (4 * " ") + title
        elif row_counter == 2:
            formatted_rows[2] += (4 * " ") + "Player X Score: " + str(player_x_score)
        elif len(board) < 5 and row_counter == 3:
            formatted_rows[3] += (4 * " ") + "Player O Score: " + str(player_o_score)
        elif len(board) >= 5 and row_counter == 4:
            formatted_rows[4] += (4 * " ") + "Player O Score: " + str(player_o_score)
        row_counter += 1
    # Finally, this part formats the whole board and layers all the rows to make the board
    grid = "\n".join(formatted_rows)
    return "\n" + grid
