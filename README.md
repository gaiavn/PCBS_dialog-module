
# GENERAL PURPOSE OF THE DIALOG MODULE

The goal of this dialog module is to display an interactive dialog from a well-syntactically-formed text file.



# STRUCTURE OF A DIALOG

A dialog is consituted by a set of cells, sorted in a dictionary via their index.
Cells are inseparable dialog units - i.e. the dialog bits in a single cell will always be displayed together. Typically, a dialog part will need to be divided into different cells when the user has to choose between different choices.
A cell have two components: a list of elements (text boxes and instructions), that will be read in order, and a 'next object', that specifies how to move from this cell to the next cell.

A text box is either a 'simple box', either a 'choice box'.
A simple box contains few string lines that will be displayed simultaneously at the screen, and informations about the speaker (currently, only the name, but that could also contain the speaker's picture).
A choice box contains two short string lines, that are the two options between which the user must choose.

An instruction can - at least for now - only be a variable assignment. That is, either 'simply assign' a value to a variable or increment a variable (called an 'adding assignement').
Note that the only variables that can be modified are the ones from a 'variables dictionnary', defined at the beginning of the dialog (this is so for reasons of having a well-delimited domain of action, especially if this dialog module is used in a broader programm - e.g. a game).

A 'next object' can either be simple - by direclty giving the index of the next cell - either conditional. If it is conditonal, the condition for the next cell can either depend on a previous choice, either depend on values of some variables from the 'variables dictionary'.



# CURRENT STATE

All the relevant information about the current state of the dialog, variables, etc, are stored in CurrentState object. That is, the dialog file we are reading, in which cell we are currently, which is the current element of the cell, the current value of variables, but also more 'local' information like the position of the user's pointer during a choice.
Note that the current state can only remember the user's last choice; otherwise important older choices should to be stored in variables.



# MAIN LOOP

The main loop's principal job is to look out for keyboard from the user, and update the current state accordingly.
The only keys used are 'A', up arrow and down arrow buttons.
The other thing the main loop can do is to update variables if the current element is an instruction.



# SYNTAX OF A DIALOG TEXT FILE

The idea of the text file is to be as simple as possible and as close as possible to the implemented structure of a dialog. That is, cells, boxes and instructions are clearly delimited.

See one of the examples text files if you want to have a look at the syntax.

For helping the writer not to get lost, the 'variables dictionnary' can be written at the very beginning of the text file, as a memo for the person writing the file, but will not be considered by the program). Cell indexes can be followed by an indicative cell name, neither considered.



# NOTES ABOUT THE IMPLEMENTATION

I have coded this module using a lot of object classes, especially classes that "don't do anything". Their main use here is to organize information in a hierachical structure and to discriminate between objects by using the 'isinstance' function.
I know that this is not very parcimonious, but that was what I was the most confortable with. As I am probably going to improve this code in the future, I will think of a better way (I would be glad to take any suggestion).

Also, I made several comments on functions using regex. I know it is better not to comment too much, but since regex is quite technical, and understanding what I am doing implies being familiar with the text syntax I created, I thought it could be useful.


# IN CASE OF PROBLEMS

If the program does not want to read the text file, try putting the entire path name rather than the mere file name.

If the window size doesn't fit your computer, you can modify its size by changing the value of the 'zoom' variable.