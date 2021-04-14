#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  3 10:19:01 2021

@author: gaia
"""

'''TO DO: transformer les int en vrai int et enlever les guillemets aux string'''


from IPython import get_ipython
get_ipython().magic('reset -sf')
# for the font problem, reset variables
import pygame as pyg
import re
pyg.init()

pyg.font.init()
myfont = pyg.font.SysFont('arial', 18)

WINX = 500
WINY = 500
win = pyg.display.set_mode((WINX, WINY))
pyg.display.set_caption("Simple Dialog")


'''_________________CLASSES_________________________________________________'''

#(Je fais des vérifications dans les classes, mais normalement ces vérifications
# devraient être assurées ailleurs)

class StoreValue:
    pass

class AssignValue(StoreValue):
    def __init__(self, var_name, val):
        self.var_name = var_name
        self.val = val
        
class AssignValueFromChoice(StoreValue):
    def __init__(self, var_name, val1, val2):
        self.var_name = var_name
        self.val1 = val1
        self.val2 = val2
        
class AddValue(StoreValue):
    def __init__(self, var_name, val):
        if not(isinstance(val, int)):
            raise TypeError("added value must be of integer type")
        else:
            self.var_name = var_name
            self.val = val
            
class AddValueFromChoice(StoreValue):
    def __init__(self, var_name, val1, val2):
        if not(isinstance(val1, int)) or not(isinstance(val2, int)):
            raise TypeError("added values " + val1 + ' and ' + val2 + " must be of integer type")
        else:
            self.var_name = var_name
            self.val1 = val1
            self.val2 = val2


class Box:
    pass

class SimpleBox(Box):
    def __init__(self, locutor_name, list_of_textlines):
        self.loc_name = locutor_name
        if len(list_of_textlines) > 4:
            raise ValueError("there should be no more than 4 text lines")
        else:
            self.list_of_textlines = list_of_textlines
        
class ChoiceBox(Box):
    def __init__(self, choice1_text, choice2_text, store_value=None):
        self.choice1_text = choice1_text
        self.choice2_text = choice2_text
        if store_value == None:
            self.store_value = []
        else:
            self.store_value = store_value


class NextCell: 
    pass
        
class NextEnd(NextCell):
    def __init__(self):
        pass
    
class NextSimple(NextCell):
    def __init__(self, next_cell_index):
        self.index = next_cell_index
    
class NextCond(NextCell):
    def __init__(self, condition, index1, index2):
        self.condition = condition
        self.index1 = index1
        self.index2 = index2
        
class NextChoice(NextCell):
    def __init__(self, index1, index2):
        self.index1 = index1
        self.index2 = index2
  
    
class Cell:
    def __init__(self, list_of_boxes, nextcell_object):
        self.boxes = list_of_boxes
        self.nextcell_object = nextcell_object 
        
class CurrentState:
    def __init__(self, dialog_dict, variables_dict, current_cell_index = 1, current_box_index = 0, pointed_choice = True, choice_of_current_cell = None):
        self.dialog_dict = dialog_dict
        self.variables_dict = variables_dict
        self.current_cell_index = current_cell_index
        self.current_box_index = current_box_index
        self.pointed_choice = pointed_choice
        self.choice_of_current_cell = choice_of_current_cell
        
    def get_current_cell(self):
        return self.dialog_dict[self.current_cell_index]
    
    def get_current_box(self):
        return self.get_current_cell().boxes[self.current_box_index]
    
    def set_current_cell_index_and_reset_box_index(self, new_index):
        if new_index not in self.dialog_dict:
            if isinstance(new_index, str):
                print("new index is a str")
            raise IndexError("new index '"+ new_index + "' not in the dictionary")
        else:
            self.current_cell_index = new_index
            self.current_box_index = 0
        
    def increment_current_box_index(self):
        if self.current_box_index + 1 >= len(self.get_current_cell().boxes):
            raise IndexError("cannot increment box index anymore")
        else:
            self.current_box_index += 1
            
    def switch_pointed_choice(self):
        self.pointed_choice = not(self.pointed_choice)
        
    def set_choice(self, boolean):
        self.choice_of_current_cell = boolean
    
    

'''________FUNCTIONS:_TXT_INTERPRETATION_PART_______________________________'''
                    
def remove_noise(str_list):
    new_list = list(str_list)
    for string in str_list:
        if string == '' or string == '\n' or string == ' \n' or string == ' ':
            new_list.remove(string)
    return new_list

def file_to_dict(pathname):
    file = open(pathname, 'r')
    text = file.read()
    cells = text_to_cells(text)
    dict = create_dict_from_list(cells)
    return dict

def create_dict_from_list(L):
    '''only for int keys, starting at 1'''
    D = {}
    for i in range(len(L)):
        D[i+1] = L[i]
    return D

def text_to_cells(text):
    text_cells = remove_noise(re.split('\#\d+', text))
    cells = []
    for el in text_cells:
        cells += [Cell(text_to_boxes(el), text_to_next(el))]
    return cells

def text_to_boxes(str_cell):
    clean_str = re.sub('\#\#NEXT\w*(\(.+\))*', '', str_cell) #remove the "next" part        
    list_of_box_type_str = remove_noise(re.split('\#\#', clean_str)) #list of str boxes
    final_boxes = []                                             
    for string in list_of_box_type_str:
        lines = remove_noise(re.split('\n', string))
        if re.search('NAME\(', string):
            name = re.match('NAME\((.*)\)', lines[0]).groups()[0]
            lines.remove(lines[0])
            final_boxes.extend(str_and_name_to_boxes_list(name, lines))
        elif re.search('CHOICE', string):
            if re.search('ASSIGNVALUE|ADDVALUE', string):
                print(lines)
                matched = re.findall('(ASSIGNVALUE[FROMCHOICE]*|ADDVALUE[FROMCHOICE]*)\((.+)\)', string)
                final_boxes.append(ChoiceBox(lines[1], lines[2], str_to_store_values(matched)))
            else:
                final_boxes.append(ChoiceBox(lines[1], lines[2]))
        elif re.search('ASSIGNVAL', string):
            matched = re.match('ASSIGNVAL\((.+), (.+)\))').groups()
            final_boxes.append(AssignValue(matched[0], matched[1]))
        elif re.search('ADDVAL', string):
            matched = re.match('ADDVAL\((.+), (.+)\))').groups()
            final_boxes.append(AddValue(matched[0], matched[1]))
        else:
            raise ValueError("Unidentified box types in the cell: " + string)
    return final_boxes

def str_and_name_to_boxes_list(name, str_lines):
    # for simplebox only
    final_lines = []
    for line in str_lines:
        if line_length(line) < WINX - 10:
            final_lines.append(line)
        else: #line too long
            final_lines.extend(divide_line(line, WINX - 10))
    return lines_to_boxes(name, final_lines)
        
    return [SimpleBox(name, ['Everything', 'is']), SimpleBox(name, ['fine'])]

def line_length(line):
    return myfont.render(line, False, (0, 0, 0)).get_rect().size[0]

def divide_line(longline, length_max):
    ''' takes a line, cuts it into sub lines of a smaller length and return them
    as a list'''
    final_lines = []
    words_left = re.split(' ', longline) # words not processed
    while words_left != []:
        sub_line = '' # a line of the right length
        while line_length(sub_line + ' ' + words_left[0]) < length_max and words_left != []:
            sub_line += ' ' + words_left[0]
            words_left.remove(words_left[0])
        final_lines.append(sub_line)
    return final_lines  

def lines_to_boxes(name, lines):
    lines_left = list(lines)
    boxes = []
    while lines_left != []:
        if len(lines_left) >= lines_per_box:
            boxes.append(SimpleBox(name, [lines_left[i] for i in range(lines_per_box)]))
            for i in range(lines_per_box):
                lines_left.remove(lines_left[i])
        else:
            boxes.append(SimpleBox(name, lines_left))
            lines_left = []
    return boxes

def text_to_next(text_cell):
    if re.search('NEXT\(', text_cell):
        return NextSimple(int(re.search('NEXT\((\d+)\)', text_cell).groups()[0]))
    elif re.search('NEXTEND', text_cell):
        return NextEnd()
    elif re.search('NEXTCOND', text_cell):
        matched = re.search('NEXTCOND\(ASSERT\((.+)\), (\d+), (\d+)\)', text_cell).groups()
        condition = re.sub('VAL\((.+)\)', strval_to_val, matched[0])
        return NextCond(condition, int(matched[1]), int(matched[2]))
    elif re.search('NEXTCHOICE', text_cell):
        matched = re.search('NEXTCHOICE\((\d+), (\d+)\)', text_cell).groups()
        return NextChoice(int(matched[0]), int(matched[1]))
    else:
        raise ValueError("Next object missing in the cell: " + text_cell)
    
def strval_to_val(val_str):
        bare_str = re.match('VAL\((.+)\)', val_str.group()).groups()[0]
        if bare_str in VARIABLES_DICT:
            return str(VARIABLES_DICT[bare_str])
        else:
            raise ValueError(bare_str + " not in the dict")
            
def str_to_store_values(list):
    store_values = []
    for el in list:
        matched = re.split(',', el[1])
        matched[1] = re.sub('VAL\((.+)\)', strval_to_val, matched[1])
        try:
            matched[2] = re.sub('VAL\((.+)\)', strval_to_val, matched[2])
        except IndexError:
            pass          
        if el[0] == 'ASSIGNVALUE':
            store_values.append(AssignValue(matched[0], matched[1]))
        elif el[0] == 'ADDVALUE':
            store_values.append(AddValue(matched[0], matched[1]))
        elif el[0] == 'ASSIGNVALUEFROMCHOICE':
            store_values.append(AssignValueFromChoice(matched[0], matched[1], matched[2]))
        elif el[0] == 'ADDVALUEFROMCHOICE':
            store_values.append(AddValueFromChoice(matched[0], matched[1], matched[2]))
    return store_values



'''________FUNCTIONS:_VARIABLES_UPDATE_PART_________________________________'''
    
def update_variables():
    #for choice box only
    if current_state.get_current_box().store_value == []:
        print('no store value')
        current_state.set_choice(current_state.pointed_choice)
    else:
        print('store value')
        for action in current_state.get_current_box().store_value:
            if isinstance(action, AssignValue):
                try:
                    current_state.variables_dict[action.var_name] = action.val
                except KeyError: 
                    raise KeyError("VARIABLES_DICT doesn't have the corresponding key")
            elif isinstance(action, AddValue):
                try:
                    current_state.variables_dict[action.var_name] += action.val
                except KeyError: 
                    raise KeyError("VARIABLES_DICT doesn't have the corresponding key")
            elif isinstance(action, AssignValueFromChoice):
                if action.var_name not in current_state.variables_dict:
                    raise KeyError("VARIABLES_DICT doesn't have the corresponding key")
                else:
                    if current_state.pointed_choice == True:           
                        current_state.variables_dict[action.var_name] = action.val1
                    else:
                        current_state.variables_dict[action.var_name] = action.val2
            elif isinstance(action, AddValueFromChoice):
                if action.var_name not in current_state.variables_dict:
                    raise KeyError("VARIABLES_DICT doesn't have the corresponding key")
                else:
                    if current_state.pointed_choice == True:           
                        current_state.variables_dict[action.var_name] += action.val1
                    else:
                        current_state.variables_dict[action.var_name] += action.val2

def update_state():
    global end
    still_unread_boxes_in_current_cell = current_state.current_box_index < len(current_state.get_current_cell().boxes) - 1
    if still_unread_boxes_in_current_cell:
        current_state.increment_current_box_index()
    else:
        next_object = current_state.get_current_cell().nextcell_object
        if isinstance(next_object, NextSimple):
            current_state.set_current_cell_index_and_reset_box_index(next_object.index)
        elif isinstance(next_object, NextCond):
            if eval(next_object.condition):
                current_state.set_current_cell_index_and_reset_box_index(next_object.index1)
            else:
                current_state.set_current_cell_index_and_reset_box_index(next_object.index2)
        elif isinstance(next_object, NextChoice):
            if current_state.choice_of_current_cell == True: #choice 1
                current_state.set_current_cell_index_and_reset_box_index(next_object.index1)
            else:
                current_state.set_current_cell_index_and_reset_box_index(next_object.index2)
        elif isinstance(next_object, NextEnd):
            end = True



'''________FUNCTIONS:_DISPLAY_PART__________________________________________'''

def display_box(box):
    if not(isinstance(box, Box)):
        raise TypeError("box is not a Box object")
    elif isinstance(box, SimpleBox):
        win.blit(myfont.render(box.loc_name, False, (0, 0, 0)), (left_margin, 10))
        for line, line_index in tuple(zip(box.list_of_textlines, list(range(1, len(box.list_of_textlines) + 1)))):
            win.blit(myfont.render(line.format(**VARIABLES_DICT), False, (0, 0, 0)), (left_margin, 10 + line_index*50))
    elif isinstance(box, ChoiceBox):
        win.blit(myfont.render(box.choice1_text, False, (0, 0, 0)), (left_margin + 10, 10))
        win.blit(myfont.render(box.choice2_text, False, (0, 0, 0)), (left_margin + 10, 60))
        if current_state.pointed_choice == True:
            win.blit(myfont.render(">", False, (0, 0, 0)), (left_margin - 10, 10))
        else:
            win.blit(myfont.render(">", False, (0, 0, 0)), (left_margin - 10, 60))
        

def redraw_window():
    pyg.draw.rect(win, pyg.Color(250, 250, 250), pyg.Rect(0,0, WINX, WINY))
    display_box(current_state.get_current_box())
    
    pyg.display.update()



'''_______CREATION_OF_VARIABLES_AND_MAIN_LOOP_______________________________'''

DIALOG_DICT2 = {1: Cell([SimpleBox("Aki", ["Hello!", "How are u?"]), SimpleBox("Aki", ["Are you okay?"])], NextSimple(2)), 2: Cell([SimpleBox("", ["Replay?"]), ChoiceBox("yes", "no")], NextCond("current_state.choice_of_current_cell == True", 1, 3)), 3: Cell([SimpleBox("", ["Bye!"])], NextEnd())}   
DIALOG_DICT1 = {1: Cell([SimpleBox("", ["What's your name? I asked you {loops} times."]), ChoiceBox("Dana", "Danny", [AssignValueFromChoice("name", "Dana", "Danny"), AddValue("loops", 1)]), SimpleBox("", ["Your name is {name}?"]), ChoiceBox("Yeah", "Not really...")], NextCond("current_state.choice_of_current_cell == True", 2, 1)), 2: Cell([SimpleBox("", ["Awesome!"])], NextEnd())}
VARIABLES_DICT1 = {"name": None, "loops": 0}
VARIABLES_DICT = {'player': 'Hazel', 'money': 10, 'friend': None}
#mettre le var_dict dans le dialog_dict ?

left_margin = 20
lines_per_box = 3
    
clock = pyg.time.Clock()
end = False

DIALOG_DICT = file_to_dict("prototype.txt")
current_state = CurrentState(DIALOG_DICT, VARIABLES_DICT)
                
while not(end):
    clock.tick(30)   
    for event in pyg.event.get():
        if event.type == pyg.QUIT:
            end = True
        if event.type == pyg.KEYDOWN:
            if isinstance(current_state.get_current_box(), SimpleBox) and event.key == pyg.K_a:
                update_state()
            elif isinstance(current_state.get_current_box(), ChoiceBox):
                if event.key == pyg.K_DOWN:
                    if current_state.pointed_choice == True:
                        current_state.switch_pointed_choice()
                if event.key == pyg.K_UP:
                    if current_state.pointed_choice == False:
                        current_state.switch_pointed_choice()
                if event.key == pyg.K_a:
                    update_variables()
                    current_state.pointed_choice = True #reset
                    update_state()
                
    redraw_window()
    
    
pyg.quit()