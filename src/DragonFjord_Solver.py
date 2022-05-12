#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  3 18:44:42 2021

@author: cubea
"""
from typing import Tuple
import unittest
import numpy as np
import time
import pdb


class RecursiveBoardHistory:
    def __init__(self):
        self.history = []

    def add_memento(self, memento):
        self.history.append(memento)

    def get_memento(self):
        return self.history.pop()


class Piece:
    """Class of piece. Defines shape and methods for rotating and flipping."""
    
    # @ staticmethod
    # def createPieces():
    # # Piece shape information stored for reference
    #     return (Piece('2x3-No Hole', np.array([[1, 1, 1],
    #                                            [1, 1, 1]]), 1, False),

    #                Piece('2x3-Middle Hole', np.array([[1, 0, 1],
    #                                                   [1, 1, 1]]), 3, False),

    #                Piece('2x3-End Hole', np.array([[1, 1, 0],
    #                                                [1, 1, 1]]), 3, True),

    #                Piece('2x4-Zag', np.array([[0, 0, 1, 1],
    #                                           [1, 1, 1, 0]]), 3, True),

    #                Piece('2x4-Tee', np.array([[0, 0, 1, 0],
    #                                           [1, 1, 1, 1]]), 3, True),

    #                Piece('2x4-L', np.array([[0, 0, 0, 1],
    #                                         [1, 1, 1, 1]]), 3, True),

    #                Piece('3x3-Zag', np.array([[1, 0, 0],
    #                                           [1, 1, 1],
    #                                           [0, 0, 1]]), 1, True),

    #                Piece('3x3-L', np.array([[1, 0, 0],
    #                                         [1, 0, 0],
    #                                         [1, 1, 1]]), 3, False),
                   # )
    
    @ staticmethod
    def createPieces():
    # Piece shape information stored for reference
        return (Piece('2x3-No Hole', np.array([[1, 1, 1],
                                               [1, 1, 1]]), 1, False),

                Piece('2x3-End Hole', np.array([[1, 1],
                                                [1, 1], 
                                                [1, 0]]), 3, True),   
                
                
                Piece('3x3-Zag', np.array([[1, 0, 0],
                                              [1, 1, 1],
                                              [0, 0, 1]]), 1, True),
                
                Piece('2x3-Middle Hole', np.array([[1, 0, 1],
                                                      [1, 1, 1]]), 3, False),


                   Piece('2x4-Tee', np.array([[0, 1],
                                              [0, 1],
                                              [1, 1],
                                              [0, 1]]), 3, True),

                   
                   Piece('2x4-L', np.array([[1, 1],
                                            [1, 0],
                                            [1, 0],
                                            [1, 0]]), 3, True),

                   
                   Piece('3x3-L', np.array([[1, 0, 0],
                                            [1, 0, 0],
                                            [1, 1, 1]]), 3, False),
                   
                   Piece('2x4-Zag', np.array([[1, 1, 1, 0],
                                              [0, 0, 1, 1]]), 3, True),
                         
                   
                   )

    def __init__(self, name, init_orientation, max_rotations, is_flippable):
        """Shape: numpy array where 0 is empty space and 1 is full space."""
        # Arguments
        self.name = name
        self.init_orientation = init_orientation
        self.current_orientation = init_orientation.copy()
        self.board_pos = None

        # Restrictions
        self.max_rotations = max_rotations
        self.is_flippable = is_flippable

        # Flags
        self.has_rotated = 0
        self.has_translated = 0
        self.has_flipped = False
        self.orientation_exhausted = False
        self.is_used = False

    def rotate(self):
        """Rotate shop by 90 degrees."""
        self.current_orientation = np.rot90(self.current_orientation)
        self.has_rotated += 1

    def flip(self):
        """Flips shape on vertical axis."""
        self.current_orientation = np.flip(self.current_orientation, axis=1)
        self.has_flipped = True
        self.has_rotated = 0

    def reset(self):
        """Reset orientation back to initial."""
        self.current_orientation = self.init_orientation.copy()
        self.has_rotated = 0
        self.has_translated = 0
        self.has_flipped = False
        self.orientation_exhausted = False

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
        if not self.isTranslationExhausted():
            self.has_translated += 1

    def translateAndRotate(self):
        """Translate and/or rotate piece."""
        if self.isTranslationExhausted():
            self.changeOrientation()
            self.has_translated = 0
        else:
            self.translate()

    def isTranslationExhausted(self):
        return self.current_orientation[0][self.has_translated]

    def isUsed(self):
        """Set is_used flag to true."""
        self.is_used = True

    def noLongerUsed(self):
        """Set is_used flag to false."""
        self.is_used = False

    def setBoardPosition(self, board_pos):
        """Set the board_pos property."""
        row, col = board_pos

        # Adjust for translation
        col = col - self.has_translated

        self.board_pos = (row, col)

    def getBoardPosition(self):
        return self.board_pos

    def getPiecePlacement(self):
        """Return the board position and orientation of piece."""
        return (self.name, self.board_pos, self.current_orientation)


class TestPieceMethods(unittest.TestCase):

    def test_translate_once(self):
        # Arrange
        piece = Piece('2x4-Zag', np.array([[0, 0, 1, 1],
                                           [1, 1, 1, 0]]), 3, True)

        # Act
        piece.translateAndRotate()

        # Assert
        self.assertEqual(1, piece.has_translated)

    def test_translate_max_times(self):
        # Arrange
        piece = Piece('2x4-Zag', np.array([[0, 0, 1, 1],
                                           [1, 1, 1, 0]]), 3, True)

        # Act
        count = 0
        while count < 2:
            piece.translateAndRotate()
            count += 1

        # Assert
        self.assertEqual(2, piece.has_translated)
        self.assertEqual(1, piece.isTranslationExhausted())

    def test_Rotate_once(self):
        # Arrange
        piece = Piece('2x4-Zag', np.array([[0, 0, 1, 1],
                                           [1, 1, 1, 0]]), 3, True)

        # Act
        count = 0
        while count < 3:
            piece.translateAndRotate()
            count += 1

        # Assert
        self.assertEqual(1, piece.has_rotated)
        self.assertTrue(np.array_equal(
            np.array([[1, 0], [1, 1], [0, 1], [0, 1]]), piece.current_orientation))

    def test_rotate_max(self):
        # Arrange
        piece = Piece('2x4-Zag', np.array([[0, 0, 1, 1],
                                           [1, 1, 1, 0]]), 3, True)

        # Act
        count = 0
        while count < 6:
            piece.translateAndRotate()
            count += 1

        # Assert
        self.assertEqual(3, piece.has_rotated)
        self.assertEqual(False, piece.has_flipped)
        self.assertTrue(np.array_equal(
            np.array([[1, 0], [1, 0], [1, 1], [0, 1]]), piece.current_orientation))

    def test_flip_once(self):
        # Arrange
        piece = Piece('2x4-Zag', np.array([[0, 0, 1, 1],
                                           [1, 1, 1, 0]]), 3, True)

        # Act
        count = 0
        while count < 7:
            piece.translateAndRotate()
            count += 1

        # Assert
        self.assertEqual(0, piece.has_rotated)
        self.assertEqual(True, piece.has_flipped)
        self.assertTrue(np.array_equal(
            np.array([[0, 1], [0, 1], [1, 1], [1, 0]]), piece.current_orientation))

    def test_flip_max(self):
        # Arrange
        piece = Piece('2x4-Zag', np.array([[0, 0, 1, 1],
                                           [1, 1, 1, 0]]), 3, True)

        # Act
        count = 0
        while count < 14:
            piece.translateAndRotate()
            count += 1

        # Assert
        self.assertEqual(3, piece.has_rotated)
        self.assertEqual(True, piece.has_flipped)
        self.assertEqual(True, piece.orientation_exhausted)
        self.assertTrue(np.array_equal(
            np.array([[1, 1, 0, 0], [0, 1, 1, 1]]), piece.current_orientation))


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
    def pieceToBoard(piece: Piece):
        """Places piece onto board.

        Projects piece matrix onto the Board matrix at the given board
        position starting at (0, 0) of the piece matrix.
        """
        # Start out with an empty board
        piece_on_board = np.array([[0] * 7] * 7)
        row_B, col_B = piece.getBoardPosition()
        # For each row in piece orientation
        for row_P in piece.current_orientation:
            # For each column in piece orientation = value
            for col_P in row_P:
                piece_on_board[row_B][col_B] = col_P
                col_B += 1
            _, col_B = piece.getBoardPosition()
            row_B += 1
        return piece_on_board
        # IndexError - piece doesn't fit and not a valid solution

    @ staticmethod
    def getNextBoardPos(board_layout):
        """Get next Board position to place the next piece on."""
        for row_index, row in enumerate(board_layout):
            for col_index, col in enumerate(row):
                if col == 0:
                    return (row_index, col_index)

    @ staticmethod
    def isBoardComplete(board_layout):
        """Check if board is complete.

        If complete, array should only contain 1(s).
        An incomplete board will contain 0(s).
        """
        if 0 in board_layout:
            return False
        else:
            return True

    @ staticmethod
    def isUnreachableHole(board_layout) -> bool:
        """Determine if current layout is invalid."""
        # Test if there are any holes first
        if Board.isBoardComplete(board_layout):
            return False

        empty_positions = Board.getAllEmptyPositions(board_layout)

        for board_position in empty_positions:
            tested_holes = []
            other_holes = []
            other_holes.append(board_position)

            while True:
                more_holes = []

                for hole in other_holes:
                    if hole not in tested_holes:
                        neighbours = Board.getNeighbours(board_layout, hole)
                        more_holes.extend(Board.evaluateNeighbours(
                            neighbours, hole))
                        tested_holes.append(hole)

                other_holes.extend(more_holes)
                unique_holes = []
                [unique_holes.append(x)
                 for x in other_holes if x not in unique_holes]
                other_holes = unique_holes

                if len(tested_holes) > 4:
                    # Tested more than 4 adjacnent holes which means hole isnt reachable
                    break
                elif len(tested_holes) == len(other_holes):
                    # Current position is unreachable. Piece is invalid - no need to keep testing
                    return True

        # All empty board positions were tested and nor unreachable
        return False

    @ staticmethod
    def getNeighbours(board_layout, board_pos: Tuple[int, int]):
        """Return adjacent neighbours.

        Returns a matrix of the adjacent neighbours at the specified
        board position.
        """

        row, col = board_pos
        board_layout = board_layout.copy()

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

    @ staticmethod
    def evaluateNeighbours(neighbours, current_board_pos):
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

    @ staticmethod
    def getAllEmptyPositions(board_layout):
        empty_positions = []

        for (row_index, row) in enumerate(board_layout):
            for (col_index, element) in enumerate(row):
                if element == 0:
                    empty_positions.append((row_index, col_index))

        return empty_positions

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
        self.history = RecursiveBoardHistory()

    def addPiece(self, piece):
        """Add piece to the Board and retain a copy of the old board layout."""
        self.current_layout = self.current_layout + \
            Board.pieceToBoard(piece)

    def changeDate(self, day, month):
        """Change initial layout of Board."""
        self.current_layout = Board.getInitialLayout(day, month,
                                                     Board.empty_layout.copy())
        self.old_layout = self.current_layout

    def setTestLayout(self):
        """Set current board layout to a test layout."""
        self.current_layout = Board.empty_layout

    def isPieceValid(self, board_pos, piece):
        """Confirm if piece can be placed onto Board.

        Checks if piece is within board boundary and doesn't overlap with
        other pieces which have already been placed.
        """
        # Check if translated board position is within bounds of the board
        row, col = board_pos
        if piece.has_translated > col:
            return False
        else:
            # Adjust board position to take into account translation
            piece.setBoardPosition(board_pos)
            _, col = piece.getBoardPosition()

        # Check if piece is within bounds of the board if placed
        if row + piece.current_orientation.shape[0] - 1 > self.current_layout.shape[0] - 1 or \
                col + piece.current_orientation.shape[1] - 1 > self.current_layout.shape[1] - 1:
            return False

        # Check if piece overlaps with an existing piece
        new_layout = self.current_layout.copy()
        new_layout += Board.pieceToBoard(piece)
        if 2 in new_layout:
            return False

        # Piece can be placed
        # Check if piece leaves any holes
        if Board.isUnreachableHole(new_layout):
            return False

        # Piece is placed in valid position
        return True

    def generate_memento(self):
        self.history.add_memento(self.current_layout.copy())

    def restore_from_memento(self):
        memento = self.history.get_memento()
        self.current_layout = memento


class TestPieceMethods(unittest.TestCase):

    def test_calendar_position_month(self):
        # Arrange & Act
        position = Board.getCalendarPos(5, 0, 5, 6)

        # Assert
        self.assertEqual((0, 4), position)

    def test_calendar_position_day(self):
        # Arrange & Act
        position = Board.getCalendarPos(21, 2, 6, 7)

        # Assert
        self.assertEqual((4, 6), position)

    def test_get_initial_layout(self):
        # Arrange & Act
        initial_board_layout = Board.getInitialLayout(
            21, 5, Board.empty_layout)

        expected_result = np.array([[0, 0, 0, 0, 1, 0, 1],
                                    [0, 0, 0, 0, 0, 0, 1],
                                    [0, 0, 0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0, 0, 1],
                                    [0, 0, 0, 0, 0, 0, 0],
                                    [0, 0, 0, 1, 1, 1, 1]])

        # Assert
        self.assertTrue(np.array_equal(expected_result, initial_board_layout))

    def test_get_next_board_position(self):
        # Arrange
        board = np.array([[1, 1, 1, 1, 1, 1, 1],
                          [1, 1, 1, 1, 1, 1, 1],
                          [1, 1, 1, 1, 1, 1, 1],
                          [0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 1, 1, 1, 1]])

        # Act
        next_position = Board.getNextBoardPos(board)

        # Assert
        self.assertEqual((3, 0), next_position)

    def test_get_next_board_position_completed(self):
        # Arrange
        board = np.array([[1, 1, 1, 1, 1, 1, 1],
                          [1, 1, 1, 1, 1, 1, 1],
                          [1, 1, 1, 1, 1, 1, 1],
                          [1, 1, 1, 1, 1, 1, 1],
                          [1, 1, 1, 1, 1, 1, 1],
                          [1, 1, 1, 1, 1, 1, 1],
                          [1, 1, 1, 1, 1, 1, 1]])

        # Act
        next_position = Board.getNextBoardPos(board)

        # Assert
        self.assertIsNone(next_position)

    def test_board_complete(self):
        # Arrange
        board = np.array([[1, 1, 1, 1, 1, 1, 1],
                          [1, 1, 1, 1, 1, 1, 1],
                          [1, 1, 1, 1, 1, 1, 1],
                          [1, 1, 1, 1, 1, 1, 1],
                          [1, 1, 1, 1, 1, 1, 1],
                          [1, 1, 1, 1, 1, 1, 1],
                          [1, 1, 1, 1, 1, 1, 1]])

        # Act
        is_complete = Board.isBoardComplete(board)

        # Assert
        self.assertTrue(is_complete)

    def test_board_incomplete(self):
        # Arrange
        board = np.array([[1, 1, 1, 1, 1, 1, 1],
                          [1, 1, 1, 1, 1, 1, 1],
                          [1, 1, 1, 1, 1, 1, 1],
                          [1, 1, 1, 1, 1, 1, 1],
                          [1, 1, 1, 1, 0, 1, 1],
                          [1, 1, 1, 1, 1, 1, 1],
                          [1, 1, 1, 1, 1, 1, 1]])

        # Act
        is_complete = Board.isBoardComplete(board)

        # Assert
        self.assertFalse(is_complete)

    def test_piece_to_board(self):
        # Arrange
        puzzle_piece = Piece(
            '2x4-Zag', np.array([[0, 0, 1, 1],
                                 [1, 1, 1, 0]]), 3, True)

        board_position = (2, 3)
        expected_result = np.array([[0, 0, 0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0, 1, 1],
                                    [0, 0, 0, 1, 1, 1, 0],
                                    [0, 0, 0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0, 0, 0]])
        puzzle_piece.setBoardPosition(board_position)

        # Act
        piece_on_board = Board.pieceToBoard(puzzle_piece)

    def test_get_neighbours_centre(self):
        # Arrange
        board_position = (3, 2)
        board_layout = np.array([[0, 1, 1, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0],
                                 [0, 1, 1, 0, 0, 1, 1],
                                 [0, 0, 5, 1, 1, 1, 0],
                                 [0, 0, 1, 0, 0, 0, 0],
                                 [0, 1, 1, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0]])

        expected_result = np.array([[1, 1, 0],
                                    [0, 5, 1],
                                    [0, 1, 0]])

        # Act
        neighbours = Board.getNeighbours(board_layout, board_position)

        # Assert
        self.assertTrue(np.array_equal(expected_result, neighbours))

    def test_get_neighbours_top_lhcorner(self):
        # Arrange
        board_position = (0, 0)
        board_layout = np.array([[5, 1, 1, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0],
                                 [0, 1, 1, 0, 0, 1, 1],
                                 [0, 0, 0, 1, 1, 1, 0],
                                 [0, 0, 1, 0, 0, 0, 0],
                                 [0, 1, 1, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0]])

        expected_result = np.array([[1, 1, 1],
                                    [1, 5, 1],
                                    [1, 0, 0]])

        # Act
        neighbours = Board.getNeighbours(board_layout, board_position)

        # Assert
        self.assertTrue(np.array_equal(expected_result, neighbours))

    def test_get_neighbours_top_rhcorner(self):
        # Arrange
        board_position = (6, 6)
        board_layout = np.array([[5, 1, 1, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0],
                                 [0, 1, 1, 0, 0, 1, 1],
                                 [0, 0, 0, 1, 1, 1, 0],
                                 [0, 0, 1, 0, 0, 0, 0],
                                 [0, 1, 1, 0, 0, 2, 1],
                                 [0, 0, 0, 0, 0, 1, 5]])

        expected_result = np.array([[2, 1, 1],
                                    [1, 5, 1],
                                    [1, 1, 1]])

        # Act
        neighbours = Board.getNeighbours(board_layout, board_position)

        # Assert
        self.assertTrue(np.array_equal(expected_result, neighbours))

    def test_evaluate_neighbours(self):
        # Arrange
        board_position = (3, 2)
        neighbours = np.array([[0, 0, 0],
                               [1, 5, 0],
                               [0, 0, 0]])
        expected_results = [(2, 2), (3, 3), (4, 2)]

        # Act
        other_holes = Board.evaluateNeighbours(neighbours, board_position)

        # Assert
        self.assertEqual(expected_results, other_holes)


class Solver:
    """Contains methods for solving puzzle."""

    def __init__(self, day, month):
        """Initialise instance of Solver."""
        self.day = day
        self.month = month
        self.pieces = Piece.createPieces()
        self.board = Board(day, month)
        self.solution_set = []

    def getSolutionSet(self, start_index):
        """Return solution set.

        Iterates through all possible combinations and appends solutions
        to a solution set array.
        """
        # Create memento to handle state
        solver_history = []

        while True:
            # Flag to determine when to go back to previous state
            restore_last_state = True

            # Flag to determine when to break out of for loop
            is_looping = True

            # Get next available board position
            board_pos = Board.getNextBoardPos(self.board.current_layout)

            # Get next eligible piece to be placed
            for index in range(start_index, len(self.pieces)):
                piece = self.pieces[index]

                if not piece.is_used:
                    while not piece.orientation_exhausted:
                        if self.board.isPieceValid(board_pos, piece):
                            # Set flag to indicate piece is used
                            piece.isUsed()

                            # Save current board state
                            self.board.generate_memento()

                            # Update board state
                            self.board.addPiece(piece)

                            # Save current state of solver
                            solver_history.append(index)

                            # Set loop flag
                            restore_last_state = False

                            # Reset start_index
                            start_index = 0

                            # Set loop flag
                            is_looping = False
                            break
                        else:
                            piece.translateAndRotate()

                    # while else block
                    else:
                        # Orientations exhausted - reset piece
                        piece.reset()

                if not is_looping:
                    break

            # Check if board is complete. Add solution set if it is complete
            if Board.isBoardComplete(self.board.current_layout):
                # Record state of all pieces
                solution = []
                for piece_placement in self.pieces:
                    solution.append(piece_placement
                                    .getPiecePlacement())

                # Append solution to solution set
                self.solution_set.append(solution)

                # Change flag to indicate to undo last move
                restore_last_state = True

            # If hasn't broken out, has exhausted all possibilities for current loop.
            # Return to previous solver state or break from loop if finished searching
            if restore_last_state:
                if len(solver_history) > 0:
                    start_index = solver_history.pop()

                    # Return to previous board position
                    self.board.restore_from_memento()

                    # Remove flag indicating piece is used
                    self.pieces[start_index].noLongerUsed()

                    # change piece orientation
                    self.pieces[start_index].translateAndRotate()
                else:
                    # Completed search, break from outer loop
                    break

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

    return unique_solution_set  # [String name, tuple position, int[] orient]


def run(day, month):
    """Find solutions for puzzle for given day and month."""
    start_time = time.time()
    Dragon = Solver(day, month)
    Dragon.getSolutionSet(0)
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
                print("{} unique solution(s) were found.".format(
                    no_unique_solutions))
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
        file.write(
            "Day, Month, No. Solutions, No. Unique Solutions, Seconds to Solve\n")
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

# if __name__ == '__main__':
#     unittest.main()
