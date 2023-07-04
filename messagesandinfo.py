

def get_each_pattern(shape_data):  # This creates boards with each winning pattern for printing (as examples)
    all_patterns, shape_messages = [], []
    more_than_4 = False
    for shape in shape_data:
        st_co, messages, end_count = shape_data[shape]  # st_co = START_COORDINATES
        rots, all_rots = 0, []  # ROTATIONS, ALL_ROTATIONS
        shape_name = str(shape)  # This part makes the shape names more readable and neater looking
        if "exp" in shape_name or "rot" in shape_name or "rev" in shape_name or "_" in shape_name:
            shape_name = shape_name.replace("exp", "corners of unseeable")
            shape_name = shape_name.replace("rot", "rotating")
            shape_name = shape_name.replace("rev", "seemingly reversed")
            shape_name = shape_name.replace("_", " ")
        shape_name = shape_name.title()
        shape_name = shape_name.replace("Of", "of")
        i, j = shape[0].upper(), "."  # Gets the shape's initial for printing on the example board
        amend_initials = ["exp_squares", "exp_diamonds", "lightning", "turning_lines", "rev_l_patterns", "crosses"]
        new_initials = ["S", "D", "V", "L", "L", "X"]  # Replaces the shape initial for a more preferred one
        if shape in amend_initials:
            i = new_initials[amend_initials.index(shape)]
        shape_messages.append(i + " = " + shape_name)
        more_than_4 = True if len(st_co) > 4 else False
        while rots < len(st_co) and rots < 4:
            st_co[rots].sort()
            row_c, rows = 0, []  # row_c = ROW_COUNTER
            c_mov = 0  # c_mov = COLUMN_MOVER
            while row_c <= end_count[rots][0]:
                col_c, columns = 0, []  # col_ = COLUMN_COUNTER
                while col_c <= end_count[rots][1]:
                    if c_mov != len(st_co[0]) and st_co[rots][c_mov][0] == row_c and st_co[rots][c_mov][1] == col_c:
                        columns.append(i)
                        c_mov += 1
                    else:
                        columns.append(j)
                    col_c += 1
                rows.append(columns)
                row_c += 1
            k = "," if "corners" not in shape else "!"  # This is so the edges can be cut of corner print-outs
            rows.insert(0, [k] * len(rows[0]))
            rows.append([k] * len(rows[0]))
            for row in rows:
                row.insert(0, k)
                row.append(k)
            all_rots.append(rows)
            rots += 1
        all_patterns.append(all_rots)
    return all_patterns, shape_messages, more_than_4


def print_pattern_board(pattern_board, board_size, pattern_messages, more_patterns, printed):
    pattern_board = equalise_rows(pattern_board)  # Equalises all the rows to be the same length
    counter = 0
    if pattern_board[0][0] != " ":
        while counter < len(pattern_board):
            pattern_board[counter] += ". "
            counter += 1
    if len(pattern_board) > board_size:
        pattern_board.pop(0)
        pattern_board.pop(-1)
    if pattern_board[0][2] == "C":  # SPECIAL CASE - For corner patterns
        while counter < len(pattern_board):
            pattern_board[counter] = pattern_board[counter].lstrip(" ")
            counter += 1
    grid = "\n".join(pattern_board)
    print("\n" + grid)
    rest_of = "" if not printed else "rest of the "
    print(f"\nAbove are the {rest_of}different winning patterns: " + ", ".join(pattern_messages))
    if more_patterns:
        input("\nAND ... your game has more winning patterns! Press Enter to see them. ")
    return [""], [], True


def create_pattern_board(shape_data, board_size):  # Creates the full board with all winning patterns for the game
    pat_board, pattern_mes = [""], []
    patterns, messages, more_than_4 = get_each_pattern(shape_data)
    corners = False
    printed = False
    for pattern in patterns:
        if pattern[0][0][0] == "!" and not corners and pat_board != [""]:
            corners = True
            pat_board, pattern_mes, printed = print_pattern_board(pat_board, board_size, pattern_mes, True, printed)
        elif pattern[0][0][0] == "!":
            corners = True
        elif pattern[0][0][0] == "," and corners and pat_board != [""]:
            pat_board, pattern_mes, printed = print_pattern_board(pat_board, board_size, pattern_mes, True, printed)
            corners = False
        pattern_mes.append(messages[0])
        messages.pop(0)
        top = True
        for rotation in pattern:
            while len(rotation) > len(pat_board):
                if top:
                    pat_board.insert(0, "")
                else:
                    pat_board.append("")
                top = True if not top else False
            pat_board = equalise_rows(pat_board)
            counter = 0
            aligner = 0
            if len(rotation) + 1 < len(pat_board):
                aligner = 1
            while counter < len(rotation):
                pat_board[counter + aligner] += " ". join(rotation[counter]) + " "
                counter += 1
            counter = 0
            while counter < len(pat_board):
                pat_board[counter] = pat_board[counter].replace(",", ".")
                pat_board[counter] = pat_board[counter].replace("! ", "  ")
                pat_board[counter] = pat_board[counter][:-2]
                counter += 1
    print_pattern_board(pat_board, board_size, pattern_mes, False, printed)
    if len(patterns) == 1 and len(patterns[0]) == 1:
        print("\nThat should be easy to remember!")
    elif len(patterns) == 1:
        print("\nNot too many to remember!")
    elif len(patterns) > 2:
        print("\nThat's a lot of patterns! Good luck remembering them all!")
    else:
        print("\nBe sure to remember them all!")
    if more_than_4:
        print("NOTE: Since you chose a large board, only up to 4 examples of each pattern are shown here.")


def equalise_rows(pattern_board):
    greatest_row_len = 0
    for row in pattern_board:
        if len(row) > greatest_row_len:
            greatest_row_len = len(row)
    counter = 0
    while counter < len(pattern_board):
        while len(pattern_board[counter]) < greatest_row_len:
            pattern_board[counter] += ". "
        counter += 1
    return pattern_board
