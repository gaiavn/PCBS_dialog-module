#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Created on Wed Mar  3 10:19:01 2021

@author: gaia
'''

# for a pygame font problem on my computer -
# basically reset all variables at each execution
# can be removed if it triggers issues
from IPython import get_ipython
if get_ipython() is not None:
    get_ipython().magic('reset -sf')



'''_________________CLASSES_________________________________________________'''

class CurrentState:
    def __init__(self, dialog_dict, variables_dict, current_cell_index = 1,
                 current_element_index = 0, pointer_position = 1,
                 choice_of_current_cell = None):
        self.dialog_dict = dialog_dict
        self.variables_dict = variables_dict
        self.current_cell_index = current_cell_index
        self.current_element_index = current_element_index
        self.pointer_position = pointer_position # corresponds to line 1 or 2,
                                                               # for choices
        self.choice_of_current_cell = choice_of_current_cell
        
    def get_current_cell(self):
        return self.dialog_dict[self.current_cell_index]
    
    def get_current_element(self):
        return self.get_current_cell().elements[self.current_element_index]
    
    def set_current_cell_index_and_reset_element_index(self, new_index):
        if new_index not in self.dialog_dict:
            if isinstance(new_index, str):
                raise IndexError("new index '"+ new_index + "' not in the dictionary")
        else:
            self.current_cell_index = new_index
            self.current_element_index = 0
        
    def increment_current_element_index(self):
        if self.current_element_index + 1 >= len(self.get_current_cell().elements):
            raise IndexError("cannot increment element index anymore")
        else:
            self.current_element_index += 1
            
    def switch_pointer_position(self):
        self.pointer_position = self.pointer_position % 2 + 1
        
    def set_choice_and_reset_pointer_position(self, position):
        self.choice_of_current_cell = position
        self.pointer_position = 1


class Cell:
    def __init__(self, list_of_elements, next_object):
        self.elements = list_of_elements
        self.next_object = next_object


class Element:
    pass


class Box(Element):
    pass

class SimpleBox(Box):
    def __init__(self, speaker_name, list_of_textlines):
        self.speaker_name = speaker_name
        if len(list_of_textlines) > LINES_PER_BOX:
            raise ValueError("there should be no more than 4 text lines")
        else:
            self.list_of_textlines = list_of_textlines
        
class ChoiceBox(Box):
    def __init__(self, choice1_text, choice2_text):
        self.choice1_text = choice1_text
        self.choice2_text = choice2_text


class Instruction(Element):
    pass

class SimpleAssignment(Instruction):
    def __init__(self, variable, value):
        self.variable = variable
        self.value = value
        
class AddingAssignment(Instruction):
    def __init__(self, variable, value):
        if not(isinstance(value, int)):
            raise TypeError("added value must be of integer type")
        else:
            self.variable = variable
            self.value = value


class Next: 
    pass
    
class NextSimple(Next):
    def __init__(self, next_cell_index):
        self.index = next_cell_index
    
class NextCond(Next):
    def __init__(self, condition, index1, index2):
        self.condition = condition
        self.index1 = index1
        self.index2 = index2
        
class NextChoice(Next):
    def __init__(self, index1, index2):
        self.index1 = index1
        self.index2 = index2
        
class NextEnd(Next):
    def __init__(self):
        pass


class Evaluate:
    pass

class IsEqual(Evaluate):
    def __init__(self, a, b):
        self.a = a
        self.b = b
        
class IsGreater(Evaluate): #strictly greater
    def __init__(self, a, b):
        self.a = a
        self.b = b
        
        
class VariableName:
    def __init__(self, var_name):
        if type(var_name) != str:
            raise TypeError("var_name must be of type string.")
        self.var_name = var_name
           
        
            
'''________FUNCTIONS:_TXT_INTERPRETATION_PART_______________________________'''

def file_to_dict(filename):
    file = open(filename, 'r')
    text = file.read()
    cells = text_to_cells(text)
    dict = create_dict_from_cells_list(cells)
    return dict

def create_dict_from_cells_list(L):
    D = {}
    for i, cell in L:
        D[i] = cell
    return D

def text_to_cells(text):
    cell_indexes = re.findall('\#(\d+)', text)
    str_cells = re.split('\#\d+.*\n', text)      
    try:
        str_cells.remove('') #artefact if the variable_dict is written at the                                               
    except ValueError:                          # beginning of the text file
        pass     
    if re.search("\{.+\}", str_cells[0]): #remove the variable_dict
        str_cells.remove(str_cells[0])                                  
    cells = []
    for i in range(len(str_cells)):
        str_cell = str_cells[i]
        cells += [(int(cell_indexes[i]), Cell(text_to_elements(str_cell),
                                               text_to_next(str_cell)))]
    return cells

def text_to_elements(str_cell):
    clean_str = re.sub('NEXT\w*(\(.+\))*', '', str_cell) #remove the "next" part       
    split_str_elements = re.split("(BOX\(.*\)|CHOICE\(\)|SIMPLEASSIGNMENT|ADDINGASSIGNMENT)", clean_str)
    split_str_elements.remove(split_str_elements[0]) #artefact, either '' or '\n'
    
    # combine each box name with its text (e.g. 'BOX()' with the text in the box)
    str_elements = [split_str_elements[i*2] + split_str_elements[i*2+1] for i in range(len(split_str_elements)//2)]

    elements = []                                          
    for str in str_elements:
        lines = re.split('\n', str)
        if re.search('BOX\(', str):
            speaker_name = re.match('BOX\((.*)\)', lines[0]).groups()[0]
            lines.remove(lines[0])
            elements.extend(name_and_lines_to_boxes(speaker_name, lines))
        elif re.search('CHOICE\(\)', str):
            elements.append(ChoiceBox(lines[1], lines[2]))
        elif re.match('SIMPLEASSIGNMENT', str):
            matched = re.match('SIMPLEASSIGNMENT\((.+),\s{0,1}(.+)\)', str).groups()
            elements.append(SimpleAssignment(fix_type(matched[0]),
                                             fix_type(matched[1])))
        elif re.match('ADDINGASSIGNMENT', str):
            matched = re.match('ADDINGASSIGNMENT\((.+),\s{0,1}(.+)\)', str).groups()
            elements.append(AddingAssignment(fix_type(matched[0]),
                                             fix_type(matched[1])))
        else:
            raise ValueError("Unidentified element type in the cell: " + str + "!")
    return elements

def name_and_lines_to_boxes(name, lines):
    final_lines = []
    for line in lines:
        if line_length(line) < SCREEN_WIDTH - RIGHT_MARGIN:
            final_lines.append(line)
        else: #line too long
            good_lines = long_line_to_good_lines(line, SCREEN_WIDTH - RIGHT_MARGIN)
            final_lines.extend(good_lines)
    return lines_to_boxes(name, final_lines)

def line_length(line):
    return font.render(line, False, (0, 0, 0)).get_rect().size[0]

def long_line_to_good_lines(longline, length_max):
    final_lines = []
    words_left = re.split(' ', longline) # words not processed yet
    while words_left != []:
        sub_line = '' # a line of the right length
        while words_left != [] and line_length(sub_line + ' ' + words_left[0]) < length_max:
            sub_line += ' ' + words_left[0]
            words_left.remove(words_left[0])
        final_lines.append(sub_line)
    return final_lines  

def lines_to_boxes(name, lines):
    lines_left = list(lines)
    final_boxes = []
    while lines_left != []:
        counter = 0
        new_box = []
        while counter < LINES_PER_BOX and lines_left != []:
            if lines_left[0] == '': #means a new box is asked for
                if counter == 0: # we have already an empty box
                    lines_left.remove(lines_left[0])
                    counter = LINES_PER_BOX # allows new box
            else:
                new_box.append(lines_left[0])
                lines_left.remove(lines_left[0])
                counter += 1
        if new_box != []:
            final_boxes.append(SimpleBox(name, new_box))
    return final_boxes       

def text_to_next(text_cell):
    if re.search('NEXT\(', text_cell):
        return NextSimple(int(re.search('NEXT\((\d+)\)', text_cell).groups()[0]))
    elif re.search('NEXTEND', text_cell):
        return NextEnd()
    elif re.search('NEXTCOND', text_cell):
        matched = re.search('NEXTCOND\((.+),\s{0,1}(\d+), (\d+)\)',
                            text_cell).groups()
        #condition = re.sub('VAL\((.+)\)', strval_to_val, matched[0])
        return NextCond(str_to_condition(matched[0]), int(matched[1]),
                                                    int(matched[2]))
    elif re.search('NEXTCHOICE', text_cell):
        matched = re.search('NEXTCHOICE\((\d+),\s{0,1}(\d+)\)',
                                            text_cell).groups()
        return NextChoice(int(matched[0]), int(matched[1]))
    else:
        raise ValueError("Next object missing in the cell: " + text_cell)
    
def str_to_condition(str):
    if re.search('ISEQUAL|ISGREATER', str):
        matched = list(re.search('(ISEQUAL|ISGREATER)\((.+),\s{0,1}(.+)\)',
                                                             str).groups())
        for i in range(1, 3):
            matched[i] = fix_type(matched[i])
        if re.search('ISEQUAL', str):
            return IsEqual(matched[1], matched[2])
        elif re.search('ISGREATER', str):
            return IsGreater(matched[1], matched[2])
    else:
        raise ValueError("The condition miss an Evaluate object.")
        
def fix_type(str):
    if re.search('\'', str): #if str represents a str value
        string = re.search('\'(.*)\'', str).groups()[0]
        return string
    else:
        try:
            return int(str) #if str represents an integer
        except ValueError:
            return VariableName(str) #otherwise, it's the name of a variable
        


'''________FUNCTIONS:_VARIABLES_UPDATE_PART_________________________________'''
    
def update_current_state():
    global end
    still_unread_elements_in_current_cell = current_state.current_element_index\
                        < len(current_state.get_current_cell().elements) - 1
    if still_unread_elements_in_current_cell:
        current_state.increment_current_element_index()
    else:
        next_object = current_state.get_current_cell().next_object
        if isinstance(next_object, NextSimple):
            current_state.set_current_cell_index_and_reset_element_index(next_object.index)
        elif isinstance(next_object, NextCond):
            if condition_to_bool(next_object.condition):
                current_state.set_current_cell_index_and_reset_element_index(next_object.index1)
            else:
                current_state.set_current_cell_index_and_reset_element_index(next_object.index2)
        elif isinstance(next_object, NextChoice):
            if current_state.choice_of_current_cell == 1:
                current_state.set_current_cell_index_and_reset_element_index(next_object.index1)
            else:
                current_state.set_current_cell_index_and_reset_element_index(next_object.index2)
        elif isinstance(next_object, NextEnd):
            end = True
            
def update_variables():
    element = current_state.get_current_element()
    if isinstance(element, SimpleAssignment):
        try:
            current_state.variables_dict[element.variable.var_name] = element.value
        except KeyError: 
            raise KeyError("VARIABLES_DICT doesn't have the corresponding key")
    elif isinstance(element, AddingAssignment):
        try:
            current_state.variables_dict[element.variable.var_name] += element.value
        except KeyError: 
            raise KeyError("VARIABLES_DICT doesn't have the corresponding key")

def condition_to_bool(cond):
    #transforms objects into evaluable expressions
    v1, v2 = cond.a, cond.b
    if isinstance(v1, VariableName):
        v1 = current_state.variables_dict[v1.var_name]
    if isinstance(v2, VariableName):
        v2 = current_state.variables_dict[v2.var_name]
    if isinstance(cond, IsEqual):
        return v1 == v2
    elif isinstance(cond, IsGreater):
        return v1 > v2



'''________FUNCTIONS:_DISPLAY_PART__________________________________________'''

def display_box(box):
    if isinstance(box, SimpleBox):
        screen.blit(font.render(box.speaker_name, False, (0, 0, 0)), (LEFT_MARGIN, 5))
        for line, line_index in tuple(zip(box.list_of_textlines, list(range(1,
                                            len(box.list_of_textlines) + 1)))):
            screen.blit(font.render(line.format(**current_state.variables_dict),
                                            False, (0, 0, 0)), (LEFT_MARGIN,
                        UP_MARGIN + (line_index - 1) * SPACE_BETWEEN_LINES))
    elif isinstance(box, ChoiceBox):
        screen.blit(font.render(box.choice1_text, False, (0, 0, 0)),
                                    (LEFT_MARGIN + POINTER_SPACE, UP_MARGIN))
        screen.blit(font.render(box.choice2_text, False, (0, 0, 0)),
                (LEFT_MARGIN + POINTER_SPACE, UP_MARGIN + SPACE_BETWEEN_LINES))
        if current_state.pointer_position == 1:
            screen.blit(font.render(">", False, (0, 0, 0)),
                        (LEFT_MARGIN - POINTER_SPACE, UP_MARGIN))
        else:
            screen.blit(font.render(">", False, (0, 0, 0)),
                 (LEFT_MARGIN - POINTER_SPACE, UP_MARGIN + SPACE_BETWEEN_LINES))

def redraw_window():
    pyg.draw.rect(screen, SCREEN_COLOR, pyg.Rect(0,0, SCREEN_WIDTH, SCREEN_HEIGHT))
    pyg.draw.rect(screen, BANNER_COLOR, pyg.Rect(0,0, SCREEN_WIDTH, BANNER_HEIGHT))
    display_box(current_state.get_current_element())   
    pyg.display.update()
    


if __name__ == '__main__':

    '''_______CREATION_OF_VARIABLES_________________________________________'''

    import pygame as pyg
    import re
    
    pyg.mixer.pre_init(44100, -16, 1, 512)
    pyg.init()  
    
    zoom = 1.2 # multiply the window size by zoom factor
    SCREEN_WIDTH = int(600 * zoom)
    SCREEN_HEIGHT = int(200 * zoom)
    LEFT_MARGIN = 20 * zoom
    RIGHT_MARGIN = 35 * zoom
    UP_MARGIN = 50 * zoom
    SPACE_BETWEEN_LINES = 30 * zoom
    POINTER_SPACE = 10 * zoom
    LINES_PER_BOX = 3
    BANNER_HEIGHT = 25 * zoom

    screen = pyg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    font = pyg.font.SysFont(pyg.font.get_default_font(), int(24 * zoom)) 
    pyg.display.set_caption("Dialog Module")
    
    SCREEN_COLOR = pyg.Color(150, 150, 250)
    BANNER_COLOR = pyg.Color(150, 150, 150)
    BLACK = pyg.Color(0, 0, 0)
    
    beep_sound = pyg.mixer.Sound("sfx-bip.wav")
    beep_sound.set_volume(0.3)
    move_sound = pyg.mixer.Sound("sfx-blink.wav")
    move_sound.set_volume(0.3)
    
    DIALOG_DICT = file_to_dict("escape.md")
    VARIABLES_DICT = {'key': 0}
    current_state = CurrentState(DIALOG_DICT, VARIABLES_DICT)
    
    '''__________________MAIN_LOOP__________________________________________'''
     
    end = False    
    clock = pyg.time.Clock()
               
    while not(end):
        clock.tick(30)
        current_element = current_state.get_current_element()
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                end = True
            elif isinstance(current_element, Instruction):
                update_variables()
                update_current_state()
            elif event.type == pyg.KEYDOWN and isinstance(current_element, SimpleBox):
                if event.key == pyg.K_a:
                    pyg.mixer.Sound.play(beep_sound)
                    update_current_state()
            elif event.type == pyg.KEYDOWN and isinstance(current_element, ChoiceBox):
                if event.key == pyg.K_DOWN and current_state.pointer_position == 1:
                    pyg.mixer.Sound.play(move_sound)
                    current_state.switch_pointer_position()
                elif event.key == pyg.K_UP and current_state.pointer_position == 2:
                    pyg.mixer.Sound.play(move_sound)
                    current_state.switch_pointer_position()
                elif event.key == pyg.K_a:
                    pyg.mixer.Sound.play(beep_sound)
                    current_state.set_choice_and_reset_pointer_position(current_state.pointer_position)
                    update_current_state()                                      
        redraw_window()       
        
    pyg.quit()