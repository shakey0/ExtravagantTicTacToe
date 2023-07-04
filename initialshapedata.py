

def get_line_start_checks(line_length):  # LINE PATTERNS
    # This creates the line patterns depending on the winning line_length for the game
    horizontal_line, vertical_line, diagonal_to_right, diagonal_to_left = [], [], [], []
    for number in range(line_length):
        horizontal_line.append([0, number])
        vertical_line.append([number, 0])
        diagonal_to_right.append([number, number])
        diagonal_to_left.append([number, (line_length - 1) - number])
    line_coordinates = [horizontal_line, vertical_line, diagonal_to_right, diagonal_to_left]
    # The numbers in these message will be added later, after check_patterns has determined the actual line_length made
    # The grammar will also be fixed later depending on how many lines of a single type are made in a single turn
    message_list = ["lay down {0} perfectly horizontal line{3} of " + str(line_length),
                    "hung {0} terrifyingly vertical line{3} of " + str(line_length),
                    "drew {0} diagonal line{3} of " + str(line_length) + " rising like the sun",
                    "placed {0} diagonal line{3} of " + str(line_length) + " representing a majestic sunset"]
    return line_coordinates, 0, message_list


def get_square_start_checks(expander):
    return [[[0, 0], [0, 1], [1, 0], [1, 1]]], expander, [  # SQUARE PATTERN
        "built {0} robust square{3}", "discovered the magic corners of {1} almost invisible square{3}"]


def get_diamond_start_checks(expander):
    return [[[0, 1], [1, 0], [1, 2], [2, 1]]], expander, [  # DIAMOND PATTERN
        "dug up {0} shiny diamond{3}", "brought to vision the sparkling corners of {0} never before seen diamond{3}"]


def get_corner_start_checks(expander, board_length):
    message = "cast a spell producing "
    o_cs = board_length - 1  # OUTER_CORNERS
    if expander == 1:
        expander = [[0, 1], [1, 0], [-1, 0], [0, -1]]
    return [[[0, 0], [0, o_cs], [o_cs, 0], [o_cs, o_cs]]], expander, [  # CORNER PATTERN
        f"{message}the magic corners of the board", f"{message}the majestically rotating corners of the board"]


def get_l_pattern_start_checks():  # L PATTERNS
    return [[[0, 0], [1, 0], [2, 0], [2, 1]]], 2, [
        "made {0} perfect representation{3} of the letter L", "formed {0} rotated L{3}", "hung {1} upside down L{3}",
        "demonstrated {0} lying down L{3}"]


def get_reverse_l_pattern_start_checks():  # REVERSE L PATTERNS
    return [[[0, 1], [1, 1], [2, 0], [2, 1]]], 2, [
        "painted {0} brilliantly reversed L{3}", "found {1} odd lying down L{3}", "spun up {1} extremely dizzy L{3}",
        "drew {0} pretty cool reversed L{3}"]


def get_lightning_start_checks():  # LIGHTING PATTERNS
    message = "produced {0} powerful lightning strike{3} from the "
    return [
        [[0, 0], [1, 0], [1, 1], [2, 1]],  # 1st rotation
        [[0, 1], [0, 2], [1, 0], [1, 1]],  # 2nd rotation
        [[0, 1], [1, 0], [1, 1], [2, 0]],  # 1st rotation reversed
        [[0, 0], [0, 1], [1, 1], [1, 2]]   # 2nd rotation reversed
    ], 0, [f"{message}northwest", f"{message}west", f"{message}northeast", f"{message}east"]


def get_t_pattern_start_checks():  # T SHAPE PATTERNS
    return [[[0, 0], [0, 1], [0, 2], [1, 1]]], 2, [
        "made {0} brilliant T{3}", "discovered {0} fallen down T{3}", "came across {0} hanging T{3}",
        "stumbled upon {0} rather crooked T{3}"]


def get_horseshoe_start_checks():  # HORSESHOE PATTERNS
    return [[[0, 0], [0, 2], [1, 0], [1, 1], [1, 2]]], 2, [
        "found {1} upside down horseshoe{3}", "drew {0} slanted horseshoe{3}", "found {0} sturdy horseshoe{3}",
        "stumbled upon {0} horseshoe{3} on {5} side{3}"]


def get_turning_line_start_checks():  # TURNING LINE PATTERNS
    message = "sighted and reported {2} turning clock hands "
    return [[[0, 0], [1, 0], [2, 0], [2, 1], [2, 2]]], 2, [
        f"{message}bang on 3 o'clock", f"{message}at almost quarter past 6", f"{message}at almost quarter to 6",
        f"{message}bang on 9 o'clock"]


def get_zigzag_pattern_start_checks():  # ZIGZAG LINE PATTERNS
    message = "drew {0} sharp meandering zigzag{3} heading "
    return [[[0, 0], [1, 0], [1, 1], [2, 1], [2, 2]]], 2, [
        f"{message}southeast", f"{message}northeast", f"{message}northwest", f"{message}southwest"]


def get_funny_shape_start_checks():  # FUNNY SHAPE PATTERNS
    mes = "came across {1} indescribably funny shape{3} in {5} apparently "
    return [
        [[0, 0], [0, 1], [1, 1], [2, 1], [2, 2]],  # 1st rotation
        [[0, 2], [1, 0], [1, 1], [1, 2], [2, 0]],  # 2nd rotation
        [[0, 0], [1, 0], [1, 1], [1, 2], [2, 2]],  # 1st rotation reversed
        [[0, 1], [0, 2], [1, 1], [2, 0], [2, 1]]   # 2nd rotation reversed
    ], 0, [mes + "original form{3}", mes + "first rotation{3}", mes + "reversed form{3}", mes + "most odd form{3}"]


def get_cross_start_checks():
    return [[[0, 0], [0, 2], [1, 1], [2, 0], [2, 2]]], 0, ["slammed down {0} powerful cross{4}"]  # CROSS PATTERN


def get_plus_start_checks():
    return [[[0, 1], [1, 0], [1, 1], [1, 2], [2, 1]]], 0, ["made {0} powerful addition{3}"]  # PLUS PATTERN


def get_coordinates(shape_types, board_length):  # The winning pattern(s) name(s) are used to call the functions
    coordinates_dictionary = {
        "lines_of_3": get_line_start_checks(3),
        "lines_of_4": get_line_start_checks(4),
        "lines_of_5": get_line_start_checks(5),
        "lines_of_6": get_line_start_checks(6),
        "squares": get_square_start_checks(0),
        "exp_squares": get_square_start_checks(1),
        "diamonds": get_diamond_start_checks(0),
        "exp_diamonds": get_diamond_start_checks(1),
        "corners": get_corner_start_checks(0, board_length),
        "rot_corners": get_corner_start_checks(1, board_length),
        "l_patterns": get_l_pattern_start_checks(),
        "rev_l_patterns": get_reverse_l_pattern_start_checks(),
        "lightning": get_lightning_start_checks(),
        "t_patterns": get_t_pattern_start_checks(),
        "horseshoes": get_horseshoe_start_checks(),
        "turning_lines": get_turning_line_start_checks(),
        "zigzag_patterns": get_zigzag_pattern_start_checks(),
        "funny_shapes": get_funny_shape_start_checks(),
        "crosses": get_cross_start_checks(),
        "pluses": get_plus_start_checks()
    }
    basic_shape_data_for_current_game = {}
    for shape in shape_types:  # Gets all the types of winning patterns for the game_type
        basic_shape_data_for_current_game[shape] = coordinates_dictionary[shape]
    return basic_shape_data_for_current_game


def get_full_shape_data(board_size, shape_types):
    # shape_types = ["corners", "rot_corners"]  # !!!!! THIS LIST WILL BE GIVEN TO THE FUNCTION FROM USER SETUP !!!!!
    basic_shape_data = get_coordinates(shape_types, board_size)  # Gets the preset coordinates and winning messages
    shape_data = {}
    for item in basic_shape_data:
        start_coordinates, expander, messages = basic_shape_data[item]
        if expander == 0:  # If expander == 0 all the checking coordinates are preset
            pass
        elif expander == 1:  # If expander == 1 only the first size is preset and the larger sizes need to be generated
            start_coordinates, messages = expand_shape(board_size, start_coordinates, messages)
        elif expander == 2:  # If the expander == 2 only the first rotation is preset and the others need generating
            start_coordinates = add_rotations(start_coordinates)
        else:  # ONLY FOR ROTATING CORNERS - SPECIAL CASE
            start_coordinates, messages = add_corner_rotations(start_coordinates, expander, messages)
        end_count = get_end_count(start_coordinates)  # Generates coordinates that control checking movements
        shape_data[item] = start_coordinates, messages, end_count
    return shape_data


def get_end_count(start_coordinates):  # The end_count is used to tell check_patterns where the outer board limits are
    end_count = []
    for row in start_coordinates:
        end_count_pair = [0, 0]
        for row_and_column in row:
            if row_and_column[0] > end_count_pair[0]:
                end_count_pair[0] = row_and_column[0]
            if row_and_column[1] > end_count_pair[1]:
                end_count_pair[1] = row_and_column[1]
        end_count.append(end_count_pair)
    return end_count


def add_rotations(start_coordinates):  # This adds all the rotations for shapes that have rotations
    counter = 0
    while counter < 3:  # First rotation: preset  Second rotation: 0  Third rotation: 1  Fourth rotation: 2
        new_row = []  # For a new row of coordinates for the next rotation of the shape
        for pair in start_coordinates[counter]:  # The statements here move the coordinates to the next rotation
            new_pair = []
            if pair[1] == 0:
                new_pair.append(0)
            elif pair[1] == 1:
                new_pair.append(1)
            elif pair[1] == 2:
                new_pair.append(2)
            if pair[0] == 0:
                new_pair.append(2)
            elif pair[0] == 1:
                new_pair.append(1)
            elif pair[0] == 2:
                new_pair.append(0)
            new_row.append(new_pair)
        zero_check = 0
        while zero_check < 2:  # Checks for shapes that have shifted away from the edge during rotation
            count_zeros = 0
            for pair in new_row:
                if pair[zero_check] != 0:
                    count_zeros += 1
                else:  # Avoids any unnecessary checks
                    break
            if count_zeros == len(start_coordinates[0]):  # Shifts the shape back to the edge
                for pair in new_row:
                    pair[zero_check] -= 1
            zero_check += 1
        start_coordinates.append(new_row)
        counter += 1
    return start_coordinates  # Returns the full set of start coordinates


def expand_shape(board_length, start_coordinates, messages):  # Expands some shapes so expanded versions can be checked
    multiplier = 2
    expanded_coordinates = []  # Holds all the groups of coordinates for the shape sizes within the board limits
    expanded_messages = []  # For expanding the winning message, to be called in accordance with the cycle number
    end_count = get_end_count(start_coordinates)  # The end count is needed as a multiplier
    while (end_count[0][0] * multiplier) < board_length:  # Stops shapes larger than the board being added
        expanded_row = []
        for pair in start_coordinates[0]:
            expanded_pair = []
            for value in pair:
                expanded_pair.append(value * multiplier)
            expanded_row.append(expanded_pair)
        expanded_coordinates.append(expanded_row)
        expanded_messages.append(messages[1])
        multiplier += 1
    return expanded_coordinates, expanded_messages


def add_corner_rotations(start_coordinates, expander, messages):  # This is specifically for rotating_corners
    rotated_corners = []  # Holds all the groups of rotated corners
    add_messages = []  # For expanding the winning message, so it will be called in accordance with the cycle number
    rotater = 1  # Moves the corners to the next position around the edge of the board
    while rotater != start_coordinates[0][1][1]:  # Stops the addition of corners when all edge corners are added
        rotated_row = []  # The coordinates of an individual set of 4 corners
        counter = 0
        while counter < 4:
            rotated_pair = [start_coordinates[0][counter][0] + (rotater * expander[counter][0]),
                            start_coordinates[0][counter][1] + (rotater * expander[counter][1])]
            rotated_row.append(rotated_pair)
            counter += 1
        rotated_corners.append(rotated_row)
        add_messages.append(messages[1])
        rotater += 1
    return rotated_corners, add_messages
