import random

# Read a text file and 
# generate a board representation as a 2D array
def read_File(fname):
    board = []
    line_num = 0
    i_max = 0
    c_max = 0
    r_max = 0
    with open(fname, 'r', encoding='utf-8-sig') as layout:
        for line in layout:
            trantab = str.maketrans(dict.fromkeys(',\n'))
            cleaned_line = line.translate(trantab)
            line_array = [char for char in cleaned_line]
            for x in range(0, len(line_array)):
                if is_intstring(line_array[x]):
                    line_array[x] = int(line_array[x])
            if line_num == 0:
                i_max = line_array[0]
            elif line_num == 1:
                c_max = line_array[0]
            elif line_num == 2:
                r_max = line_array[0]
            else:
                board.append(line_array)
            line_num+=1
    return [board, i_max, c_max, r_max]

# checks the max width of the layout
def check_max(layout):
    max = 0
    for line in layout:
        if len(line) > max:
            max = len(line)
    return max

# checks if the provided index is out of bounds or not
def is_inRange (s, i):
    try:
        b = s[i]
        return True
    except IndexError:
        return False

# checks if the provided string is an int
def is_intstring (s):
    try:
        int(s)
        return True
    except ValueError:
        return False

# Should have 4 possibilities, I - Industrial,  C - Commerce, R - Residential, or no development
def gen_rand_solution(board, indust, comm, resid):
    sol_board = [plot[:] for plot in board]
    height = len(board) -1
    width = len(board[0]) -1
    i = 0
    for x in range(0, indust):
        rand_y = random.randint(0, height)
        rand_x = random.randint(0, width)
        while not is_intstring(sol_board[rand_y][rand_x]):
            rand_y = random.randint(0, height)
            rand_x = random.randint(0, width)
        sol_board[rand_y][rand_x] = 'I'
    for x in range(0, comm):
        rand_y = random.randint(0, height)
        rand_x = random.randint(0, width)
        while not is_intstring(sol_board[rand_y][rand_x]):
            rand_y = random.randint(0, height)
            rand_x = random.randint(0, width)
        sol_board[rand_y][rand_x] = 'C'
    for x in range(0, resid):
        rand_y = random.randint(0, height)
        rand_x = random.randint(0, width)
        while not is_intstring(sol_board[rand_y][rand_x]):
            rand_y = random.randint(0, height)
            rand_x = random.randint(0, width)
        sol_board[rand_y][rand_x] = 'R'
    return sol_board

def score_solution(orig_board, sol_board):
    score = 0
    x = 0
    y = 0
    r_coord = find_all_coordinates('R', sol_board)
    c_coord = find_all_coordinates('C', sol_board)
    i_coord = find_all_coordinates('I', sol_board)
    for row in sol_board:
        for plot in row:
            if plot == 'X':
                # Industrial zones within 2 tiles take a penalty of -10
                for coord in i_coord:
                    dist = abs(abs(coord[0] - y) + abs(coord[1] - x))
                    if dist <=2:
                        score -= 10
                # Commercial and residential zones within 2 tiles take a penalty of -20
                for coord in r_coord:
                    dist = abs(abs(coord[0] - y) + abs(coord[1] - x))
                    if dist <=2:
                        score -= 20
                for coord in c_coord:
                    dist = abs(abs(coord[0] - y) + abs(coord[1] - x))
                    if dist <=2:
                        score -= 20
            elif plot == 'S':
                # Residential zones within 2 tiles gain a bonus of 10 points
                for coord in r_coord:
                    dist = abs(abs(coord[0] - y) + abs(coord[1] - x))
                    if dist <=2:
                        score += 10
            elif plot == 'I':
                # For each industrial tile within 2 squares, there is a bonus of 2 points
                for coord in i_coord:
                    dist = abs(abs(coord[0] - y) + abs(coord[1] - x))
                    if dist <=2:
                        score += 2
                score -= 2 + orig_board[y][x]
            elif plot == 'R':
                # For each industrial site within 3 squares there is a penalty of 5 points
                for coord in i_coord:
                    dist = abs(abs(coord[0] - y) + abs(coord[1] - x))
                    if dist <=3:
                        score -= 5
                # However, for each commercial site with 3 squares there is a bonus of 4 points
                for coord in c_coord:
                    dist = abs(abs(coord[0] - y) + abs(coord[1] - x))
                    if dist <=3:
                        score += 4
                score -= 2 + orig_board[y][x]
            elif plot == 'C':
                # For each residential tile within 3 squares, there is a bonus of 4 points
                for coord in r_coord:
                    dist = abs(abs(coord[0] - y) + abs(coord[1] - x))
                    if dist <=3:
                        score += 4
                # For each commercial site with 2 squares, there is a penalty of 4 points
                for coord in c_coord:
                    dist = abs(abs(coord[0] - y) + abs(coord[1] - x))
                    if dist <=2:
                        score -= 4
                score -= 2 + orig_board[y][x]
            x += 1
        x = 0
        y += 1
    return score

def find_all_coordinates(building, board):
    coordinates = []
    y = 0
    x = 0
    for row in board:
        for plot in row:
            if plot == building:
                coordinates.append((y, x))
            x += 1
        x = 0
        y += 1
    return coordinates