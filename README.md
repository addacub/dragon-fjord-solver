# dragon-fjord-solver
Solver for the Dragon Fjord A-Puzzle-A-Day

Uses a recursive function to find all solutions for the
specified day and month using a "brute force" method. The backend
will return a solution set (an array of all possible solutions) to the GUI
which is then displayed to the user.

The solver contains piece information to prevent the solver from flipping
or rotating pieces which have symmetry i.e. flipping / rotating piece results in
the same shape being placed. This information prevents solver from placing and checking
redundent pieces.

Additional checks are used to prevent the solver checking dead end solutions
(i.e. when placing a piece results in unreachable holes) in
an attempt to increase the speed at which a solution set is found.
