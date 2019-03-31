import numpy as np

'''
Utility functions for data labels. 

Our data labels are in Forsyth–Edwards Notation (FEN). 
This module converts them into numpy ndarrays which will be used as output 
tensors.

See this wikipedia page for more info:
https://en.wikipedia.org/wiki/Forsyth%E2%80%93Edwards_Notation
'''

def convert_FEN_to_2d_char_array(string_rep: str, 
                             delimiter: str='-') -> np.array:

    board_2d_arr = np.zeros((8,8)).astype(str)
    for i,row in enumerate(string_rep.split(delimiter)):
        j=0
        for c in row:
            if str.isalpha(c):
                board_2d_arr[i][j] = c
                j+=1
            elif str.isdigit(c):
                for k in range(j,j+int(c)):
                    j=k
                    board_2d_arr[i][j] = delimiter
                    j+=1
            else:
                raise ValueError('Bad Forsyth-Edwards Notation')
        assert j==8, f'Not enough characters in row {i}, string: "{row}"'
    assert i==7, f'Not enough rows on board: "{string_rep}"'
    return board_2d_arr

def convert_to_3d_one_hot_array(board_2d_arr: np.array, 
                                null_char: str='-') -> np.array:
    '''
    Returns an 8x8x13 ndarray. Every vector in the third dimension is a one hot 
    encoded representation of a space on the chessboard.
    '''
    board_3d_arr = np.zeros((8,8,13))

    POSSIBLE_PIECES_LIST = ['Q','q','K','k','R','r',
                        'B','b','N','n','P','p', null_char]
    POSSIBLE_PIECES_DICT = { piece_char: i for i, piece_char in 
                                        enumerate(POSSIBLE_PIECES_LIST) }

    for i,row in enumerate(board_2d_arr):
        for j,item in enumerate(row):
            board_3d_arr[i, j, POSSIBLE_PIECES_DICT[item]] = 1

    return board_3d_arr

def convert_one_hot_array_to_3d(board_3d_arr: np.array, 
                                null_char: str='-') -> np.array:
    '''
    Takes an 8x8x13 ndarray and converts it into a 2d representation.
    '''
    board_2d_arr = np.zeros((8,8)).astype(str)

    POSSIBLE_PIECES_LIST = ['Q','q','K','k','R','r',
                        'B','b','N','n','P','p', null_char]
    POSSIBLE_PIECES_DICT = { i: piece_char for i, piece_char in 
                                        enumerate(POSSIBLE_PIECES_LIST) }

    for i,matrix in enumerate(board_3d_arr):
        for j,row in enumerate(matrix):
            piece_num = np.where(row==1)[0][0]
            board_2d_arr[i, j] = POSSIBLE_PIECES_DICT[piece_num]

    return board_2d_arr

def convert_2d_char_array_to_FEN(board_2d_arr: np.array, 
                                             null_char: str='-') -> str:

    string_rep = ''
    for i,row in enumerate(board_2d_arr):
        blank_counter = 0
        for j,c in enumerate(row):
            if str.isalpha(c):
                if blank_counter > 0:
                    string_rep += str(blank_counter)
                blank_counter = 0
                string_rep += c
            elif c == null_char:
                blank_counter += 1
            else:
                raise ValueError(f'Illegal Character: {c}')
        if blank_counter > 0:
                string_rep += str(blank_counter)
        if i < 7:
            string_rep += null_char
        assert j==7, f'Not enough pieces in row {j} {i}, string: "{row}"'
    assert i==7, f'Not enough rows on board.'
    return string_rep

