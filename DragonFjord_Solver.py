#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  3 18:44:42 2021

@author: cubea
"""
import numpy as np
import time
import pdb


class Piece:
    """Class of piece. Defines shape and methods for rotating and flipping."""

    # Piece shape information stored for reference
    pieces_info = (('2x3-No Hole', np.array([[1, 1, 1],
                                             [1, 1, 1]]), 2, False),

                   ('2x3-Middle Hole', np.array([[1, 0, 1],
                                                 [1, 1, 1]]), 4, False),

                   ('2x3-End Hole', np.array([[1, 1, 0],
                                              [1, 1, 1]]), 4, True),

                   ('2x4-Zag', np.array([[0, 0, 1, 1],
                                         [1, 1, 1, 0]]), 4, True),

                   ('2x4-Tee', np.array([[0, 0, 1, 0],
                                         [1, 1, 1, 1]]), 4, True),

                   ('2x4-L', np.array([[0, 0, 0, 1],
                                       [1, 1, 1, 1]]), 4, True),

                   ('3x3-Zag', np.array([[1, 0, 0],
                                         [1, 1, 1],
                                         [0, 0, 1]]), 2, True),

                   ('3x3-L', np.array([[1, 0, 0],
                                       [1, 0, 0],
                                       [1, 1, 1]]), 4, False),
                   )

    def __init__(self, name, init_orientation, max_rotations, is_flippable):
        """Shape: numpy array where 0 is empty space and 1 is full space."""
        # Arguments
        self.name = name
        self.init_orientation = init_orientation
        self.current_orientation = init_orientation
        self.board_pos = None
        self.recursive_layer = []
        # Restrictions
        self.max_rotations = max_rotations
        self.is_flippable = is_flippable
        # Flags
        self.has_rotated = 1
        self.has_translated = 0
        self.has_flipped = False
        self.orientation_exhausted = False
        self.translation_exhausted = False
        self.is_used = False

    def rotate(self):
        """Rotate shop by 90 degrees."""
        self.current_orientation = np.rot90(self.current_orientation)
        self.has_rotated += 1

    def flip(self):
        """Flips shape on vertical axis."""
        self.current_orientation = np.flip(self.current_orientation, axis=0)
        self.has_flipped = True
        self.has_rotated = 1

    def reset(self):
        """Reset orientation back to initial."""
        self.current_orientation = self.init_orientation
        self.has_rotated = 1
        self.has_translated = 0
        self.has_flipped = False
        self.orientation_exhausted = False
        self.translation_exhausted = False

    def changeOrientation(self):
        """Change orientation of the shape."""
        # Check if max no. of rotations has been made
        if self.has_rotated == self.max_rotations:
            # Check if shape is flippable or has already been flipped
            if self.is_flippable and not self.has_flipped:
                # Shape is flippable and has not been flipped
                self.flip()
            else:
                # Shape is either not flippable or has already been flipped
                self.orientation_exhausted = True
        else:
            # Max no. of rotations hasn't been reached yet
            self.rotate()

    def translate(self):
        """Translate piece to the left of the board.

        If there are zero's in the top row of the piece, the piece will
        be translated until a value of 1 is at the board position.
        """
        # Extract top row of piece
        top_row = self.current_orientation[0]
        # Test if there is a 1 at the board position
        if top_row[self.has_translated] == 1:
            self.translation_exhausted = True
        else:
            self.has_translated += 1

    def translateAndRotate(self):
        """Translate and/or rotate piece."""
        if not self.translation_exhausted:
            self.translate()

        if self.translation_exhausted:
            self.changeOrientation()
            self.translation_exhausted = False
            self.has_translated = 0

    def addRecursiveLayer(self):
        """Save current state of piece at current function layer level."""
        current_state = (self.current_orientation,
                         self.has_rotated,
                         self.has_flipped,
                         self.orientation_exhausted)

        self.recursive_layer.append(current_state)

    def isUsed(self):
        """Set is_used flag to true."""
        self.is_used = True

    def noLongerUsed(self):
        """Set is_used flag to false."""
        self.is_used = False

    def saveBoardPosition(self, board_pos):
        """Set the board_pos property."""
        self.board_pos = board_pos

    def getPiecePlacement(self):
        """Return the board position and orientation of piece."""
        return (self.name, self.board_pos, self.current_orientation)


class Board:
    """Create instance of Board.

    Contains methods to get layout, calendar positions, add/remove
    pieces and other methods related to the management to the Board and its
    state.
    """

    @ staticmethod
    def getInitialLayout(day, month, empty_layout):
        """Create initial layout of Board for given day and month."""
        row, col = Board.getCalendarPos(day, 2, 6, 7)
        empty_layout[row][col] = 1

        row, col = Board.getCalendarPos(month, 0, 5, 6)
        empty_layout[row][col] = 1

        return empty_layout

    @ staticmethod
    def getCalendarPos(cal_obj, start_row, end_col, divisor):
        """Return (row, col) for day/month on calendar."""
        quotient = cal_obj // divisor
        remainder = cal_obj % divisor

        if remainder == 0:
            row = start_row + quotient - 1
            col = end_col
        else:
            row = start_row + quotient
            col = remainder - 1

        return (row, col)

    @ staticmethod
    def pieceToBoard(board_pos, piece_orientation):
        """Places piece onto board.

        Projects piece matrix onto the Board matrix at the given board
        position starting at (0, 0) of the piece matrix.
        """
        # Start out with an empty board
        piece_on_board = np.array([[0] * 7] * 7)
        row_B, col_B = board_pos
        # For each row in piece orientation
        for row_P in piece_orientation:
            # For each column in piece orientation = value
            for col_P in row_P:
                piece_on_board[row_B][col_B] = col_P
                col_B += 1
            col_B = board_pos[1]
            row_B += 1
        return piece_on_board
        # IndexError - piece doesn't fit and not a valid solution

    # Empty calendar layout stored for reference
    empty_layout = np.array([[0, 0, 0, 0, 0, 0, 1],
                             [0, 0, 0, 0, 0, 0, 1],
                             [0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 1, 1, 1, 1]])
    
    test_layout1 = np.array([[1, 1, 1, 1, 0, 1, 1],
                             [1, 1, 1, 1, 1, 1, 1],
                             [0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 1, 1, 1, 1]])
    
    test_layout2 = np.array([[1, 1, 1, 1, 1, 1, 1],
                             [1, 1, 1, 1, 1, 1, 1],
                             [1, 0, 1, 1, 1, 1, 0],
                             [1, 1, 1, 1, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 1, 1, 1, 1]])
    
    test_layout3 = np.array([[1, 1, 1, 1, 0, 0, 1],
                             [1, 1, 1, 1, 1, 1, 1],
                             [0, 0, 0, 0, 0, 1, 0],
                             [0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 1, 1, 1, 1]])
    
    test_layout4 = np.array([[1, 1, 1, 1, 1, 1, 1],
                             [1, 1, 1, 1, 1, 1, 1],
                             [1, 0, 0, 1, 0, 1, 0],
                             [1, 1, 1, 1, 0, 0, 0],
                             [1, 1, 0, 0, 0, 0, 0],
                             [0, 1, 0, 0, 0, 0, 0],
                             [0, 0, 0, 1, 1, 1, 1]])
    
    test_layout5 = np.array([[1, 1, 1, 1, 1, 1, 1],
                             [1, 1, 1, 1, 1, 1, 1],
                             [0, 0, 0, 1, 0, 1, 1],
                             [1, 1, 1, 1, 0, 0, 1],
                             [0, 0, 0, 0, 0, 0, 1],
                             [0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 1, 1, 1, 1]])
    
    test_layout6 = np.array([[0, 1, 0, 0, 0, 0, 1],
                             [0, 1, 0, 0, 0, 0, 1],
                             [0, 1, 0, 0, 0, 0, 0],
                             [1, 1, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 1, 1, 1, 1]])
    
    test_layout7 = np.array([[1, 1, 1, 1, 1, 1, 1],
                             [1, 1, 1, 1, 1, 1, 1],
                             [1, 0, 0, 0, 1, 1, 0],
                             [1, 1, 1, 1, 0, 1, 0],
                             [0, 0, 0, 0, 0, 1, 0],
                             [0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 1, 1, 1, 1]])
    
    test_layout8 = np.array([[1, 1, 1, 1, 1, 1, 1],
                             [1, 1, 1, 1, 1, 0, 1],
                             [0, 0, 0, 0, 1, 0, 0],
                             [0, 0, 0, 0, 1, 1, 1],
                             [0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 1, 1, 1, 1]])
    
    test_layout9 = np.array([[1, 1, 1, 1, 1, 1, 1],
                             [1, 1, 1, 1, 1, 1, 1],
                             [1, 1, 0, 1, 1, 1, 1],
                             [1, 0, 0, 1, 0, 0, 1],
                             [1, 1, 1, 1, 0, 0, 1],
                             [0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 1, 1, 1, 1]])

    test_layout10 = np.array([[1, 1, 1, 1, 1, 1, 1],
                              [1, 1, 1, 1, 1, 1, 1],
                              [0, 0, 1, 1, 1, 1, 0],
                              [0, 0, 1, 1, 0, 0, 0],
                              [1, 1, 1, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 1, 1, 1, 1]])

    test_layout11 = np.array([[0, 0, 1, 0, 0, 0, 1],
                              [0, 0, 1, 0, 0, 0, 1],
                              [1, 1, 1, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 1, 1, 1, 1]])
    
    test_layout12 = np.array([[1, 1, 1, 1, 1, 1, 1],
                              [1, 1, 1, 1, 1, 1, 1],
                              [1, 0, 0, 1, 1, 1, 0],
                              [1, 0, 0, 1, 0, 0, 0],
                              [1, 1, 1, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 1, 1, 1, 1]])

    test_layout13 = np.array([[1, 1, 1, 1, 1, 1, 1],
                              [1, 1, 1, 1, 1, 1, 1],
                              [1, 0, 0, 0, 0, 1, 0],
                              [1, 1, 1, 1, 1, 1, 0],
                              [0, 0, 0, 0, 0, 1, 0],
                              [0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 1, 1, 1, 1]])

    def __init__(self, day, month):
        """Initialise instance of Board."""
        self.current_layout = Board.getInitialLayout(day, month,
                                                     Board.empty_layout.copy())
        self.old_layout = self.current_layout
        self.recursive_layer = []

    def getNextBoardPos(self):
        """Get next Board position to place the next piece on."""
        for row_index, row in enumerate(self.current_layout):
            for col_index, col in enumerate(row):
                if col == 0:
                    return (row_index, col_index)

    def addPiece(self, piece_on_board):
        """Add piece to the Board and retain a copy of the old board layout."""
        self.old_layout = self.current_layout
        self.current_layout = self.current_layout + piece_on_board

    def removePiece(self):
        """Remove piece that was added to the Board."""
        self.current_layout = self.old_layout

    def changeDate(self, day, month):
        """Change initial layout of Board."""
        self.current_layout = Board.getInitialLayout(day, month,
                                                     Board.empty_layout.copy())
        self.old_layout = self.current_layout

    def setTestLayout(self):
        """Set current board layout to a test layout."""
        self.current_layout = Board.empty_layout

    # TODO
    def isUnreachableHole(self):
        """Determine if current layout is invalid."""       
        # Test if there are any holes first
        if 0 not in self.current_layout:
            # Board is complete. Piece is valid
            return False
        
        # Get the next board position
        next_board_pos = self.getNextBoardPos()
        tested_board_pos = [next_board_pos]
        neighbour_info = self.getNeighbours(next_board_pos)
        other_holes = self.evaluateNeighbours(neighbour_info, next_board_pos)
        
        while len(tested_board_pos) < 5:
            for hole in other_holes:
                if hole not in tested_board_pos:
                    neighbour_info = self.getNeighbours(hole)
                    more_holes = self.evaluateNeighbours(neighbour_info, hole)
                    
                    tested_board_pos.append(hole)
                    other_holes += more_holes
                    break
            
            # For loop break
            # Tested all holes which is less than 5. Hole is unreachable
            else:
                return True
        
        # While loop break
        # Exceeded 5 holes which means hole isn't unreachable
        else:
            return False


    # TODO
    def getNeighbours(self, board_pos):
        """Return adjacent neighbours.

        Returns a matrix of the adjacent neighbours at the specified
        board position.
        """

        row, col = board_pos
        board_layout = self.current_layout.copy()

        # Check if board position is on top or bottom of board
        if row in (0, 6):
            extra_row = np.array([[1]*7])
            # Check if board position is on top row
            if row == 0:
                board_layout = np.append(extra_row, board_layout, axis=0)
                row += 1
            else:
                board_layout = np.append(board_layout, extra_row, axis=0)

        # Check if board position is on left or right side of board
        if col in (0, 6):
            extra_col = np.array([[1]]*len(board_layout))
            # Check if board positions is on left side
            if col == 0:
                board_layout = np.append(extra_col, board_layout, axis=1)
                col += 1
            else:
                board_layout = np.append(board_layout, extra_col, axis=1)

        neighbours = board_layout[row-1:row+2, col-1:col+2]

        return neighbours

    # TODO
    def evaluateNeighbours(self, neighbours, current_board_pos):
        """Return adjacent holes

        neighbour_info = [neighbours, row_index_shifted, col_index_shifted]
        neighbours = [np.array of neighbours of board position]
        """
        row, col = current_board_pos
        
        other_holes = []

        for row_index, row_value in enumerate(neighbours):
            for col_index, col_value in enumerate(row_value):
                if (row_index + col_index) % 2 != 0:
                    if col_value == 0:
                        new_row = row + (row_index - 1)
                        new_col = col + (col_index - 1)
                        other_holes.append((new_row, new_col))
        
        return other_holes

    def isPieceValid(self, board_pos, piece_current_orientation):
        """Confirm if piece can be placed onto Board.

        Checks if piece is within board boundary and doesn't overlap with
        other pieces which have already been placed.
        """
        # Check if board position is within bounds (0, 0)
        for axis in board_pos:
            if axis < 0:
                return False

        # Place piece on board at current board position
        try:
            piece_on_board = Board.pieceToBoard(board_pos,
                                                piece_current_orientation)
        except IndexError:
            return False

        # Piece is within board boundary. Add piece to board
        self.addPiece(piece_on_board)
        # Check if piece overlaps with other pieces
        if 2 in self.current_layout:
            # Piece overlaps and not valid solutions
            self.removePiece()
            return False

        # Piece can be placed
        # Check if piece leaves any holes
        if self.isUnreachableHole():
            self.removePiece()  # Need to remove piece which was placed
            return False
        
        # Piece is placed in valid position
        return True

    def isBoardComplete(self):
        """Check if board is complete.

        If complete, array should only contain 1(s).
        An incomplete board will contain 0(s).
        """
        if 0 in self.current_layout:
            return False
        else:
            return True

    def addRecursiveLayer(self):
        """Save current layout of board for current recursion layer."""
        self.recursive_layer.append(self.current_layout)

    def removeRecursiveLayer(self):
        """Remove a saved state of board layout for exited recursion layer."""
        _ = self.recursive_layer.pop()

    def getCurrentBoardState(self):
        """Return board layout to current layout for recursive layer."""
        self.current_layout = self.recursive_layer[-1]


class Solver:
    """Contains methods for solving puzzle."""

    def __init__(self, day, month):
        """Initialise instance of Solver."""
        self.day = day
        self.month = month
        self.pieces = [Piece(*piece) for piece in Piece.pieces_info]
        self.board = Board(day, month)
        self.solution_set = []

    def getSolutionSet(self):
        """Return solution set.

        Iterates through all possible combinations and appends solutions
        to a solution set array.
        """
        # Save current configuration of board
        self.board.addRecursiveLayer()
        # Get the next available board position
        row, col = self.board.getNextBoardPos()

        # Get next eligible piece to be placed
        for piece in self.pieces:
            if not piece.is_used:
                while not piece.orientation_exhausted:
                    # Adjust column for translation
                    col_new = col - piece.has_translated
                    board_pos = (row, col_new)
                    # Determine if piece is valid
                    valid_pos = (self.board.
                                 isPieceValid(board_pos,
                                              piece.current_orientation))

                    if valid_pos:
                        piece.saveBoardPosition(board_pos)
                        piece.isUsed()

                        # Check if solution has been found
                        if self.board.isBoardComplete():
                            # Record state of all pieces
                            solution = []
                            for piece_placement in self.pieces:
                                solution.append(piece_placement
                                                .getPiecePlacement())
                            self.solution_set.append(solution)
                        else:
                            # Save current state of piece & call function again
                            # piece.addRecursiveLayer()
                            self.getSolutionSet()
                            # Exited layer of function & remove recursive layer
                            self.board.removeRecursiveLayer()

                        # Reset board state to current layer state
                        self.board.getCurrentBoardState()
                        # Remove flag indicating piece is used
                        piece.noLongerUsed()
                        # change piece orientation
                        piece.translateAndRotate()

                    # If valid_pos else block - Change orientation
                    else:
                        piece.translateAndRotate()

                # While loop else block. Orientations exhausted - reset piece.
                else:
                    piece.reset()

    def updateDate(self, day, month):
        """Update date of board."""
        self.day = day
        self.month = month
        self.board.changeDate(day, month)

    def resetPieces(self):
        """Reset piece state."""
        for piece in self.pieces:
            piece.reset()


def removeDuplicates(solution_set):
    """Remove duplicate solutions from solution set."""
    unique_solution_set = []
    for solution in solution_set:
        outer_bool_array = []
        for unique_solution in unique_solution_set:
            # Will be 8 booleans each representing a piece
            inner_bool_array = []
            for index in range(8):
                name_outer = solution[index][0]
                name_inner = unique_solution[index][0]
                name = name_outer == name_inner

                pos_outer = solution[index][1]
                pos_inner = unique_solution[index][1]
                pos = pos_outer == pos_inner

                piece_outer = solution[index][2]
                piece_inner = unique_solution[index][2]
                piece = np.array_equal(piece_outer, piece_inner)

                if name and pos and piece:
                    inner_bool_array.append(True)
                else:
                    inner_bool_array.append(False)
            
            # If false present in inner array, then solution is unique
            if False in inner_bool_array:
                outer_bool_array.append(False)
            else:
                outer_bool_array.append(True)
        
        # Inner for-loop else block
        else:
            # If true in outer_bool_array solution is already in unique set
            # First solution will always be added as True is not in empty array
            if True not in outer_bool_array:
                unique_solution_set.append(solution)

    return unique_solution_set # [String name, tuple position, int[] orient]


def run(day, month):
    """Find solutions for puzzle for given day and month."""
    start_time = time.time()
    Dragon = Solver(day, month)
    Dragon.getSolutionSet()
    end_time = time.time()
    print("Program took {} seconds to execute.".format(end_time - start_time))
    print("{} solution(s) were found".format(len(Dragon.solution_set)))
    unique_solution_set = removeDuplicates(Dragon.solution_set)
    print("{} unique solution(s) were found.".format(len(unique_solution_set)))
    printSolution(unique_solution_set, 1)
    return Dragon


def printSolution(solution_set, index):
    """Print out the specified solution from the solution set."""
    print("Solution {} is shown below:".format(index))
    solution = solution_set[index]
    for piece in solution:
        print("Place {} at position (row, col) = {} with the following "
              "orientation:".format(piece[0], piece[1]))
        print(piece[-1])
        print("\n")


def test():
    """Run through all combinations of days and months."""
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    failed = []
    passed = []

    for index, month in enumerate(months):
        for day in range(1, 32):
            print("Finding solution for {} of {}".format(day, month))
            start_time = time.time()
            puzzle = Solver(day, index + 1)
            puzzle.getSolutionSet()
            end_time = time.time()

            seconds = end_time - start_time
            solution_set = puzzle.solution_set
            unique_solution_set = removeDuplicates(solution_set)

            if solution_set:
                no_solutions = len(solution_set)
                no_unique_solutions = len(unique_solution_set)
                print("{} solution(s) were found".format(no_solutions))
                print("{} unique solution(s) were found.".format(no_unique_solutions))
                passed.append((str(day),
                               str(month),
                               str(no_solutions),
                               str(no_unique_solutions),
                               str(seconds),
                               ))
            else:
                print("No solutions were found.")
                failed.append((str(day),
                               str(month),
                               "None",
                               "None",
                               str(seconds),
                               ))

            print("\n")

    return passed, failed


def writeToFile(results, fname):
    """Write results to text file."""
    # Check file extension has been added
    if not fname.endswith(".txt"):
        fname = fname + ".txt"

    # Defining file name
    file_dir = "test_results/" + fname

    # Start writing to file
    with open(file_dir, 'w') as file:
        file.write("Day, Month, No. Solutions, No. Unique Solutions, Seconds to Solve\n")
        for row in results:
            line = ",".join(row) + "\n"
            file.write(line)


if __name__ == "__main__":
    # passed, failed = test()
    # writeToFile(passed, "rev4_optimised_passed")
    # writeToFile(failed, "rev4_optimised_failed")

    dragon = run(31, 1)
    # unique_solution_set = removeDuplicates(dragon.solution_set)
    # print(len(dragon.solution_set))
    # print(len(unique_solution_set))
    
    # Experimenting with summing of neighbours
    # test_board = Board(21, 5)
    # test_board.setTestLayout()
    # is_unreachable_hole = test_board.isUnreachableHole()
    # print(is_unreachable_hole)
    

