#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  3 18:44:42 2021

@author: cubea
"""

import random

try:
    import tkinter
except ImportError:  # python 2
    import Tkinter as tkinter

from functools import partial
import DragonFjord_Solver as DFS
import time

# Global variable for background colour
bkg_col = '#19232D'
shuffle = False  # Turn shuffle on and off


class mainWindow:
    """Create a GUI window."""

    @ staticmethod
    def setWindowGeometry(window, window_width, window_height):
        """Set initial window geometry."""
        # Obtain screen width and height
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        # Centre window in centre of 1 window (allowing for dual montitors)
        common_aspect_ratios = [1.25, 1.33, 1.6, 1.78]
        screen_ratio = round((screen_width / screen_height), 2)
        if screen_ratio in common_aspect_ratios:
            swd = 2  # swd = screen width divisor
        else:
            swd = 4

        x_coord = int((screen_width / swd) - (window_width / 2))
        y_coord = int((screen_height / 2) - (window_height / 2))

        window.geometry('{}x{}+{}+{}'.format(window_width, window_height,
                                             x_coord, y_coord))

    def __init__(self):
        """Initiate instance of GUI window."""
        # creating main window
        self.window = tkinter.Tk()
        self.window.title('Dragon Fjord Solution Finder')

        # Set window geometry
        window_width = 1000
        window_height = 1100
        self.setWindowGeometry(self.window, window_width, window_height)
        self.window.minsize(window_width, window_height)

        # Set background colour of window
        self.window.config(bg=bkg_col)

        # Keep main window ontop of other windows
        self.window.wm_attributes('-topmost', 1)

        # Update window
        self.window.update()
        
    def run(self):
        """Exceuctes mainloop."""
        self.window.mainloop()


class headerFrame:
    """Create title frame and lables to be placed."""

    @ staticmethod
    def createLabel(parent, row, col, label_text, label_font, label_colour):
        """Create label widget."""
        label = tkinter.Label(parent, text=label_text,
                              fg=label_colour, bg=bkg_col, font=label_font)

        label.grid(row=row, column=col, sticky='')
        return label

    def __init__(self, parent, row, col):
        """Create instance of header frame."""
        # Create frame & position
        self.frame = tkinter.Frame(parent, relief='flat',
                                   pady=20, bg=bkg_col)

        self.frame.grid(row=row, column=col, sticky='')

        # Create title label
        title_text = "Dragon Fjord: A-Puzzle-A-Day"
        title_font = 'TkHeadingFont 20'
        self.title = self.createLabel(self.frame, 0, 0, title_text,
                                      title_font, 'white')

        # Create info label
        info_text = "Solution finder coded by: Adrian Cubelic"
        info_font = 'TkTextFont 14'
        self.info = self.createLabel(self.frame, 1, 0, info_text,
                                     info_font, 'white')


class Calendar:
    """Create calendar frame and calendar."""

    @ staticmethod
    def getCalendarPos(position, start_row, end_col, divisor):
        """Return (row, col) for day/month on calendar."""
        quotient = position // divisor
        remainder = position % divisor

        if remainder == 0:
            row = start_row + quotient - 1
            col = end_col
        else:
            row = start_row + quotient
            col = remainder - 1

        return (row, col)

    @ staticmethod
    def createButton(parent, row, col, text):
        """Create a button at specified (row, col)."""
        # Static options which are the same for all buttons
        width = 80
        height = 80
        font = 'TkIconFont 14'

        # Create frame to put button in
        frame = tkinter.Frame(parent, width=width, height=height)
        frame.grid_propagate(False)  # disables resizing of frame
        frame.columnconfigure(0, weight=1)  # enables button to fill frame
        frame.rowconfigure(0, weight=1)  # enables button to fill frame
        frame.grid(row=row, column=col)  # position frame where button is

        # Create button
        button = tkinter.Button(frame, text=text, font=font)
        button.grid(sticky='nsew')

        return button

    # static variables
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    def __init__(self, parent, outer_class, row, col):
        """Create instance of calendar frame and populate with buttons."""
        # Reference to outer class
        self.outer_class = outer_class
        
        # Create the calendar frame
        self.frame = tkinter.Frame(parent, relief='flat',
                                   pady=20, bg='#19232D')
        # sticky defaults to center
        self.frame.grid(row=row, column=col, sticky='')

        # Create array of calendar to store buttons in
        self.calendar = [[None]*7 for i in range(7)]  # list comprehension                 

        # Tkinter variables passed in
        self.month_var = outer_class.month_var
        self.day_var = outer_class.day_var

        # Calendar Objects selected
        self.month_selected = None
        self.day_selected = None
        self.default_button_colour = None

    def selectMonth(self, button, month):
        """Is called when a month button is pressed."""
        # Check if month is already selected
        if self.month_selected:
            self.month_selected.config(relief='raised')

        # Sink selected month
        button.config(relief='sunken')
        self.month_selected = button

        # Change variable
        self.month_var.set(month)
        
        # Is solution found
        self.outer_class.isSolutionFound()

    def selectDay(self, button, day):
        """Is called when a day button is pressed."""
        # Check if day is already selected
        if self.day_selected:
            self.day_selected.config(relief='raised')

        # Sink selected day
        button.config(relief='sunken')
        self.day_selected = button

        # Change variable
        self.day_var.set(day)
        
        # Is solution found
        self.outer_class.isSolutionFound()
        
    def getDay(self):
        """Return selected day."""
        return self.day_var.get()
    
    def getMonth(self):
        """Return selected month"""
        return self.month_var.get()

    def saveDefaultColour(self):
        """Save the default colour of button. System specific."""
        self.default_button_colour = self.calendar[0][0]['bg']

    def createCalendarObjs(self):
        """Create calendar and matrix of buttons."""
        for index, month in enumerate(self.months):
            row, col = self.getCalendarPos(index+1, 0, 5, 6)
            button = self.createButton(self.frame, row, col,
                                       text=month)

            # Add command
            button_action = partial(self.selectMonth, button, index+1)
            button.config(command=button_action)

            # Add button to calendar
            self.calendar[row][col] = button

        for index, day in enumerate(range(1, 32)):
            row, col = self.getCalendarPos(index+1, 2, 6, 7)
            button = self.createButton(self.frame, row, col,
                                       text=str(day))

            # Add command
            button_action = partial(self.selectDay, button, day)
            button.config(command=button_action)

            # Add button to calendar
            self.calendar[row][col] = button
        
        # Save default button colour
        self.saveDefaultColour()

    def addPieces(self):
        """Colours the calendar objects appropirately to show pieces"""
        no_pieces = self.outer_class.no_pieces.get()
        colours = self.outer_class.colours
        # Solution is in the form [String name, tuple position, int[] orient]
        solution = self.outer_class.selected_solution
        # Get individual elements

        
        for index in range(no_pieces):
            colour = colours[index]
            row_start, col_start = solution[index][1]
            piece_orientation = solution[index][2]
            
            for row_delta, row in enumerate(piece_orientation):
                for col_delta, col in enumerate(row):
                    if col == 1:
                        row_index = row_start + row_delta
                        col_index = col_start + col_delta
                        calendar_object = self.calendar[row_index][col_index]
                        calendar_object.config(bg=colour)

    def removePieves(self):
        """Set the colour of calendar widegts to grey."""
        for row in self.calendar:
            for widget in row:
                if widget:
                    widget.config(bg=self.default_button_colour)

    def showSolution(self):
        """Show the solution on board."""
        self.removePieves()
        self.addPieces()
            

class Frame:
    """Creates menu frame."""

    def __init__(self, parent, row, col):
        """Create instance of menu frame."""

        self.frame = tkinter.Frame(parent, relief='flat', pady=20)
        self.frame.grid(row=row, column=col, sticky='')
        
     
class SolveButton:
    """Creates solve button and associated methods."""
    
    font = 'TkIconFont 13'
    
    def __init__(self, parent, row, col):
        # Create frame
        self.frame = tkinter.Frame(parent, padx=40)
        self.frame.grid(row=row, column=col, sticky='')
        self.dark_bg = '#486684'
        self.light_bg = '#7b99b7'

        # Create button widget
        
        self.button = tkinter.Button(self.frame,
                                     text="Find Solution(s)",
                                     font=SolveButton.font,
                                     fg='white', bg=self.dark_bg,
                                     activebackground=self.light_bg,
                                     activeforeground='white')
        
        self.button.grid(row=0, column=0, sticky='')


    def pressButton(self):
        self.button.config(relief='sunken', bg=self.light_bg)

    def releaseButton(self):
        self.button.config(relief='raised', bg=self.dark_bg)


class SlideBar:
    """Create instance of slide bar and defines methods."""
    
    font = 'TkIconFont 12'

    def __init__(self, parent, outer_class, row, col):
        # Outer class reference
        self.outer_class = outer_class
        
        # Add slide bar frame
        self.frame = tkinter.Frame(parent, padx=35)
        self.frame.grid(row=row, column=col, sticky='')

        # Add slide bar label
        self.label = tkinter.Label(self.frame,
                                   text='Select how many pieces to show:',
                                   font=SlideBar.font)
        self.label.grid(row=0, column=0, sticky="w")

        # Add slide bar widget
        self.scale = tkinter.Scale(self.frame,
                                   from_=0, to=8,
                                   tickinterval=1,
                                   length=300,
                                   orient=tkinter.HORIZONTAL)
        self.scale.set(0)
        self.scale.grid(row=1, column=0, sticky='')

    def scaleMoved(self, scale_value):
        """Save the scale value to a tkinter variable."""
        self.outer_class.no_pieces.set(scale_value)
        if self.outer_class.is_solution_found:
            self.addRemovePiece()

    def addRemovePiece(self):
        """Add or remove a piece from the board."""       
        self.outer_class.calendar.showSolution()
        

    def addCommand(self):
        """Assign command to slide bar."""
        self.scale.config(command=self.scaleMoved)


class SpinBox:
    """Create instance of spin box."""
    
    font = 'TkIconFont 13'
    dark_bg = '#486684'
    light_bg = '#7b99b7'
    DEFAULT_SOLUTION = 1
    WIDTH = 30

    def __init__(self, parent, outer_class, row, col):
        
        # Outer class refernece
        self.outer_class = outer_class
        
        # Variables
        self.solution_index = outer_class.solution_index  # Tkinter var
        self.no_solutions = outer_class.len_solution_set # Tkinter variable
        self.prev_selected_solution = None
        
        # Add spin box frame
        self.frame = tkinter.Frame(parent, padx=35)
        self.frame.grid(row=0, column=2, sticky='')

        # Add spin box label
        self.label = tkinter.Label(self.frame,
                                   text='Select solution to show',
                                   font=SpinBox.font)
        self.label.grid(row=0, column=0, sticky='')

        # Add spin box widget
        self.spinner = tkinter.Spinbox(self.frame,
                                        from_=0, to=0,
                                        textvariable=self.solution_index,
                                        font=SpinBox.font,
                                        width=15,
                                        buttonbackground=SpinBox.dark_bg)

        self.spinner.grid(row=1, column=0, sticky='')
        
        # Add text frame
        self.text_frame = tkinter.Frame(self.frame, width=210, height=30)
        self.text_frame.grid(row=2, column=0, sticky='')
        self.text_frame.grid_propagate(False)
        
        # Add text
        text = "No solutions to select from"
        text_info = '{: <{width}}'.format(text, width=SpinBox.WIDTH)
        self.text = tkinter.Label(self.text_frame, text=text_info,
                                  font=SpinBox.font, justify="center")
        self.text.grid(row=2, column=0, sticky='w')

    def updateRange(self):
        """Update value of tkinter variable everytime spinbox value changed."""
        to = self.no_solutions.get()
        self.spinner.config(from_=1, to=to)

    def updateText(self):
        text = "{} solution(s) were found".format(self.no_solutions.get())
        text_info = '{: <{width}}'.format(text, width=SpinBox.WIDTH)
        self.text.config(text=text_info)

    def updateSolutionSet(self):
        """Update spin box to reflect new solution set found."""
        self.updateRange()
        self.updateText()

    def updateValue(self):
        """Update value of the spin box."""
        solution_set = self.outer_class.solution_set
        index = self.solution_index.get()
        self.outer_class.old_solution_index = index
        self.outer_class.selected_solution = solution_set[index - 1]
        
        if self.outer_class.is_solution_found:
            if shuffle:
                if index > 2 and index < self.no_solutions.get() - 1:
                    # Shuffle colours and solution set
                    random.shuffle(self.outer_class.colours)
                    random.shuffle(self.outer_class.selected_solution)
            
            self.outer_class.slide_bar.addRemovePiece()
        
    def setDefaultValue(self):
        """Set the spin box to default value of 1."""
        self.solution_index.set(SpinBox.DEFAULT_SOLUTION)

    def invalidSolution(self):
        text = "No solutions to select from"
        text_info = '{: ^{width}}'.format(text, width=SpinBox.WIDTH)
        self.text.config(text=text_info)
        self.spinner.config(from_=0, to=0)
        self.solution_index.set(0)

    def addCommand(self):
        """Add add command to spin box when value is changed."""
        self.spinner.config(command=self.updateValue)
               

class Console:
    """Create instance of text box which is read only."""

    def __init__(self, parent, row, col, colspan):
        greeting1 = "Welcome to the Dragon Fjord Puzzle Solver.\n"
        greeting2 = "Please select a day and a month to find solutions for.\n"
        self.messages = [greeting1, greeting2]
        self.height = 10
        
        # Create frame
        self.frame = tkinter.Frame(parent, pady=40)
        self.frame.grid(row=row, column=col, columnspan=colspan)
        
        # Create Label
        self.label = tkinter.Label(self.frame, text="Console")
        self.label.grid(row=0, column=0, sticky='W')
        
        # Create text box widget
        self.text_box = tkinter.Text(self.frame, height=self.height,
                                     wrap="word")
        self.text_box.grid(row=1, column=0, sticky='WE')
        self.text_box.insert('1.0', greeting1)
        self.text_box.insert('2.0', greeting2)
        self.text_box['state'] = 'disabled'
    
    def addMessage(self, message):
        """Print message to the text box."""

        line_count = self.text_box.count('1.0', 'end', "displaylines")[0] + 1
        # Write to text_box
        self.text_box['state'] = 'normal'
        self.text_box.insert('end-1c', message)
        if line_count > 10:
            self.text_box.delete('1.0', '2.0')
        self.text_box['state'] = 'disabled'
            

class GUIHandler:
    """GUI Instance handler"""
    
    # Static variables
    colours = ['red', 'green', 'blue', 'cyan', 'yellow', 'magenta',
               '#ff8c1a', '#9966ff']

    def __init__(self):
        """Initialise GUI and logic"""
        ######### Tkinter window
        self.main_window = mainWindow()

        ######### Tkinter variables
        self.no_pieces = tkinter.IntVar(self.main_window.window,
                                        name="number_pieces")
        self.solution_index = tkinter.IntVar(self.main_window.window,
                                                name="selected_solution")
        self.len_solution_set = tkinter.IntVar(self.main_window.window,
                                                name="number_solutions")
        self.month_var = tkinter.IntVar(self.main_window.window, name="month")
        self.day_var = tkinter.IntVar(self.main_window.window, name="day")


        ######### Tkinter widgets
        self.header_frame = headerFrame(self.main_window.window, 0, 1)

        self.calendar = Calendar(self.main_window.window, self, 1, 1)
        self.calendar.createCalendarObjs()

        self.menu_frame = Frame(self.main_window.window, 2, 1)
        
        self.solver_button = SolveButton(self.menu_frame.frame, 0, 0)

        # Add slide bar
        self.slide_bar = SlideBar(self.menu_frame.frame, self, 0, 1)
        self.slide_bar.addCommand()

        # Add spin box
        self.spin_box = SpinBox(self.menu_frame.frame, self, 0, 2)
        self.spin_box.addCommand()
        #self.spin_box.addCommand()
        
        # Add Console
        self.console = Console(self.menu_frame.frame, 1, 0, 3)
        
        # Adjust weights of columns
        self.main_window.window.columnconfigure(0, weight=5)
        self.main_window.window.columnconfigure(1, weight=0)
        self.main_window.window.columnconfigure(2, weight=5)
        
        
        ######## Variables and Flags
        self.solution_set = None
        self.selected_solution = None
        
        self.day_solved_for = None
        self.month_solved_for = None
        self.old_solution_index = None
        self.is_solution_found = None
        
        
    def runGUI(self):
        self.main_window.run()
        
    def runSolver(self):
        """Run solver when button is clicked"""
        day = self.calendar.getDay()
        month_int = self.calendar.getMonth()
        month_str = self.calendar.months[month_int - 1]
        self.console.addMessage("Solving for the {} of {}." 
                                " Please wait...\n"
                                .format(day, month_str))
        self.main_window.window.update_idletasks()
        
        start_time = time.time()
        Dragon = DFS.Solver(day, month_int)
        Dragon.getSolutionSet()
        end_time = time.time()
        
        text = ("Program took {:.2f} seconds to execute.\n"
                .format(end_time - start_time))
        self.console.addMessage(text)


        solution_set = Dragon.solution_set
        length = len(solution_set)

        # Removing duplicate solutions
        self.solution_set = DFS.removeDuplicates(solution_set)
        self.len_solution_set.set(len(self.solution_set))
        
        # Add message to console
        text = ("Successfully found {} solution(s) of which {} solution(s)" +
                " are unique.\n").format(length, self.len_solution_set.get())
        self.console.addMessage(text)
        
    
    def clickSolveButton(self):
        """Run logic associated with solve button."""
        
        # Depress the button
        self.solver_button.pressButton()
        
        # Check if day and month has been selected
        if not (self.calendar.day_selected
                and self.calendar.month_selected):
            self.console.addMessage("No day or month selected. Please select "
                                    "a day and month before attempting to "
                                    "find a solution.\n")
            self.main_window.window.update_idletasks()

        else:
            # Run solver and find solutions
            self.runSolver()
                   
            # Update the spinBox
            self.spin_box.updateSolutionSet()
            # Set default solution to 1
            if not self.old_solution_index:
                self.spin_box.setDefaultValue()
                self.recordSolutionIndex()

        self.is_solution_found = True
        self.spin_box.updateValue()
        self.recordDayMonth()
        
        self.solver_button.releaseButton()

    def addCommands(self):
        self.solver_button.button.config(command=self.clickSolveButton)

    def recordDayMonth(self):
        """Save the day and month solution solved for."""
        self.day_solved_for = self.day_var.get()
        self.month_solved_for = self.month_var.get()

    def recordSolutionIndex(self):
        """Record last solution index selected."""
        self.old_solution_index = self.solution_index.get()

    def restoreSolutionIndex(self):
        """Set solution index to last selected index."""
        self.solution_index.set(self.old_solution_index)

    def isSolutionFound(self):
        """Test if solution for selected day and month has already been found."""
        # Has a solution been run?
        if self.old_solution_index:
            days_match = self.day_solved_for == self.day_var.get()
            months_match = self.month_solved_for == self.month_var.get()
            if days_match and months_match:
                self.is_solution_found = True
                self.spin_box.updateSolutionSet()
                self.restoreSolutionIndex()
                self.spin_box.updateValue()
            else:
                self.is_solution_found = False
                self.spin_box.invalidSolution()
                self.calendar.removePieves()
                
        
            
# Code in chain of command
# Calendar - Select Day/Month
# Compare to previously selected day/month
# If different - remove shapes and disable spin box
# If same - add shapes and enable spin box
#           |
#           V
# Find Solutions Button clicked
# Run solver, get solution set and store solution set
# Record Day/Month Solution found for
# To save computing time should solution come back to same day
#           |
#           V
# Select Solution
# Update to/from and store selected solution
# Select the solution from solution set to store
# If select different solution set, update (call chained commands)
# Pass on a shuffled solution and colour array
#           |
#           V
# How many pieces
# Determines how many pieces to select
# If changed, pass on info (call chained commands)
#           |
#           v
# Calendar objects
# Colour the calendar objects appropriately to show pieces
#           |
#           v
# Displayed on GUI
# End result

# =============================================================================
#     def solve():
#         Dragon = DragonFjord_Solver.Solver(day_var.get(), month_var.get())
#         Dragon.getSolutionSet()
#         number_of_solutions.set(len(Dragon.solution_set))
#         print("{} solution(s) were found".format(len(Dragon.solution_set)))
#         print("The first solution is shown below:")
#         solution = Dragon.solution_set[0]
#         for piece in solution:
#             print("Place {} at position (row, col) = {} with the following"
#                   "orientation:".format(piece[0], piece[1]))
#             print(piece[-1])
#             print("")
# 
#     menu_font = 'TkIconFont 14'
#     solve_button = tkinter.Button(menu_frame, text="Find Solution(s)",
#                                    font=menu_font, command=solve)
#     solve_button.grid(row=0, column=0, sticky='we')
# =============================================================================

if __name__ == "__main__":
    GUI = GUIHandler()
    GUI.addCommands()   
    GUI.runGUI()
