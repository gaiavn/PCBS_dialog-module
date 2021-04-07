# PCBS_dialog-module
Python module for dealing with dialog in a game, a simulation, etc. Dialog information are stored in a syntactically-specified text file and are displayed using pygame.

More precisely, the user can make choices at some point, which will influence the dialog.
Each bit of dialog that always come together is called a cell. A cell is constituted by (i) list of dialog boxes and (ii) a condition for determining the next cell to display.
A box is a portion of text that is displayed at the same time on the screen. A simple box display sentences, up to 3 lines, and optionnally the name of the speaker and its image. A choice box display two alternative actions.

Each possible cell of the dialog are stored in a single dictionary, which takes their id as a key. There is also a dictionary for the variables that can be modified during the dialog and displayed.
The text file that is used for creating the dialog dictionary will follow a syntax as close as possible to the structure of the object classes used in the code.
TEST

