# region USER INFO

# This script is used for viewing and modifying the sender database

# when "senders.csv" is imported as a dataframe, the columns are "Name", "Phone", "Email", and "List"

# TODO
# 1. Make main function to put all the functionality together
# 2. Add handling for duplicate values. As in, if the user tries to enter a value for an entry that is already present in another entry, it will block the action and allow the user to cancel the current task
# 3. maybe make some wrappers to clean up input loops and debug prints

# endregion

# region IMPORT STATEMENTS

import csv # currently not used but idk we'll see
import numpy as np # used for quickly searching through arrays
import pandas as pd  # used for creating a dataframe
import sys # used for closing the program
import tkinter as tk # used for making a gui, currently not used
from tkinter import filedialog, ttk # additional gui stuff, currently not use

# endregion

# region GLOBAL VARIABLES

buffer = [] # saves previous versions of the dataframe to allow for undo and redo functionality
buffer_location = 0 # keeps track of current position in the buffer
columns = ["", 'Name', 'Phone', 'Email', 'List'] # used to reference the columns in the dataframe

# endregion

# region BUFFER FUNCTIONS

# This group of functions is for working with the buffer

def buffer_reset() -> None: # void function
    """Clears the buffer and resets the buffer location"""

    # global buffer data
    global buffer
    global buffer_location
    print_brk()
    print("[LOG]: Clearing buffer...")
    buffer = [] # empty buffer
    buffer_location = 0 # set location to 0
    print("[LOG]: Done.")



def buffer_save(df : pd.DataFrame) -> None: # void function
    """Adds current dataframe state to buffer and advances buffer position"""

    # global buffer data
    global buffer
    global buffer_location

    print_brk()

    if buffer_location < (len(buffer) - 1): # checks to see if current position in buffer is not latest version
        # clears leading entries if so
        print("[LOG]: Current buffer position not end of buffer.")
        print("[LOG]: Removing leading entries...")
        x = buffer_location + 1 # index for start of deletion
        del buffer[x:] # delete from index to end
        print("[LOG]: Done.")
    
    print("[LOG]: Saving current state to buffer...")
    buffer.append(df.copy()) # add dataframe to buffer
    buffer_location += 1 # advance buffer location
    print("[LOG]: Done.")



def undo() -> pd.DataFrame: # returns previous version
    """Returns previous state in buffer"""

    # global buffer data
    global buffer
    global buffer_location

    if buffer_location == 0: # check if at bottom of buffer
        print("[ERROR]: Cannot undo, current buffer position is at the bottom of buffer.")
    else:
        buffer_location += -1 # regress buffer location

    df = pd.DataFrame(buffer[buffer_location]) # set working dataframe to one at buffer location
    return df # return



def redo() -> pd.DataFrame:
    """Returns next state in buffer"""

    # global buffer data
    global buffer
    global buffer_location

    if buffer_location == (len(buffer) - 1): # check if at top of buffer
        print("[ERROR]: Cannot redo, current buffer position is at end of buffer.")
    else:
        buffer_location += 1 # advance buffer location

    df = (buffer[buffer_location]).copy() # set working dataframe to one at buffer location
    return df # return

# endregion

# region FILE INTERACTION FUNCTIONS

# this group of functions is for interacting with the .csv file

def import_database(p : str = "senders.csv") -> pd.DataFrame:
    """Imports the database csv as a pandas dataframe"""

    buffer_reset()

    print(f"[LOG]: Importing database {p} as dataframe...")
    df = pd.read_csv(p, dtype = {'Phone' : str})
    print("[LOG]: Done.")

    print("[LOG]: Saving initial state to buffer...")
    buffer.append(df.copy())
    print("[LOG]: Done.")
    return df



def export_database(df : pd.DataFrame, p : str = "senders.csv") -> None:
    """Exports the dataframe to the database csv"""
    print(f"[LOG]: Exporting dataframe to {p}...")
    df.to_csv(str(p), index = False)
    print("[LOG]: Done.")

# endregion

# region DISPLAY FUNCTIONS

# this group of functions is for frequently used print statements

def print_brk() -> None: 
    """Prints a text break"""
    print("=========================")



def print_df(df : pd.DataFrame) -> None:
    """Prints the contents of a dataframe"""
    print("======CURRENT STATE======")
    with pd.option_context('display.max_rows', None, 'display.max_columns', None): # temporary formatting change to ensure the FULL dataframe is printed
        print(df) # prints out the dataframe

# endregion

# region DATAFRAME SEARCH FUNCTIONS

# This group of functions is used to select positions in the dataframe using indexes and search terms

def select_column(df : pd.DataFrame) -> str:
    """Input handler for column selection"""

    # global column header
    global columns

    while True:
        # take a column as input
        C = str(input("[INPUT]: Please select from the following columns by entering the corresponding number:\n1 - Name\n2 - Phone Number\n3 - Email Address\n\n"))
        try: 
            # try to convert input into an integer
            C = int(C)
            # if it works, check if the integer is in range
            if 0<C<4:
                # if it is, break out of loop
                print("[LOG]: Input taken.")
                print(f"[LOG]: Column \"{columns[C]}\" selected.")
                break
            else:
                # if not, continue loop
                print("[ERROR]: Invalid input value, try again.")
                continue
        except:
            # if it fails, continue loop
            print("[ERROR]: Invalid input type, try again.")
            continue

    return str(columns[C]) # return column header



def find_row(df : pd.DataFrame, C : str) -> int:
    """Finds the row index of an entry in a column"""

    while True:
        # input search term
        term = str(input(f"[INPUT]: Enter the corresponding {C} for the entry you are looking for, or enter nothing to select a different column.\n"))
        if term:
            # if a value is entered, search for it
            try:
                # try to get the index of the row the term shows up in
                row = int((np.where(df[C] == term))[0][0])
                print(f"[LOG]: Entry {row} selected.")
                print("[LOG]: Exiting row selection...")
                return row # return row index
            except:
                # if no row is found, retry
                print("[ERROR]: Entry not found, try again.")
                continue
        else:
            # if no value is entered, exit search
            print("[LOG]: Exiting row selection...")
            return None



def select_row(df : pd.DataFrame) -> int:
    """Finds the row index of an entry in the database"""

    while True:
        # select column
        C = select_column(df)
        # search for row
        R = find_row(df, C)
        if R:
            # if a row index is selected, return the index
            return R
        else:
            # if row search is exited, loop back to column selection
            print("[LOG]: Returning to column selection...")
            continue

# endregion

# region DATAFRAME MODIFICATION FUNCTIONS

# This group of functions is for adding, editing, and removing entries from the dataframe

def entry_editor(entry : list) -> list:
    """Edits an entry given in list form"""

    global columns

    print(f"[LOG]: Editing entry {entry}.")

    while True:
        print_brk()
        print(f"CURRENT STATE: {entry}")
        i = str(input("[INPUT]: Please select from the following columns by entering the corresponding number, or enter \'q\' to save and quit:\n1 - Name\n2 - Phone Number\n3 - Email Address\n4 - List\n\n"))
        if (i == "q") or (i == "Q"):
            if (entry[1] or entry[2]) and entry[0]:
                print("[LOG]: Saving and exiting...")
                break
            else:
                print(f"[ERROR]: Invalid state. Please enter a value for \'Name\' and at least one of the following columns:\n1. {columns[2]}\n2. {columns[3]}\n")
                continue
        else:
            try:
                C = int(i)

                if C == 1:

                    x = ''
                    x = str(input("[INPUT]: Please enter a value for \'Name\':\n"))
                    entry[0] = str(x)
                    print("[LOG]: Value entered.")
                
                elif C == 2:

                    x = ''
                    x = str(input("[INPUT]: Please enter a value for \'Phone Number\' as an unbroken string of numbers starting with \'+\' and the country code. Example: +155501234567\n"))
                    entry[1] = str(x)
                    print("[LOG]: Value entered.")

                elif C == 3:

                    x = ''
                    x = str(input("[INPUT]: Please enter a value for \'Email Address\' in standard email format:\n"))
                    entry[2] = str(x)
                    print("[LOG]: Value entered.")

                elif C == 4:

                    x = ''
                    x = str(input("[INPUT]: Plese enter a value for \'List\', either \'white\' or \'black\'.\n"))
                    entry[3] = str(x)
                    print("[LOG]: Value entered.")

                else:
                    print("[ERROR]: Invalid input, try again.")
                    continue

            except:
                print("[ERROR]: Invalid input, try again.")
                continue
    
    print("[LOG]: Exiting entry editor...")
    return entry



def edit_entry(df : pd.DataFrame) -> pd.DataFrame:
    """Edits an entry in the dataframe"""

    print_brk()
    print("[LOG]: Entering dataframe editor...")
    R = int(select_row(df))
    entry = df.iloc[R].tolist()
    new_entry = entry_editor(entry)
    df.iloc[R] = new_entry
    print("[LOG]: Dataframe entry edited.")
    buffer_save(df)
    print("[LOG]: Exiting dataframe editor...")
    print_brk()
    return df



def add_entry(df : pd.DataFrame) -> pd.DataFrame:
    """Adds a new entry to the dataframe"""

    print_brk()
    print("[LOG]: Creating an empty entry to be added...")
    empty_entry = ['', '', '', '']
    print("[LOG]: Done.")
    print("[LOG]: Entering entry editor...")
    new_entry = entry_editor(empty_entry)
    print("[LOG]: Done.")
    print("[LOG]: Saving new entry to dataframe...")
    df.loc[len(df)] = new_entry
    print("[LOG]: Done.")
    buffer_save(df)

    return df



def del_entry(df : pd.DataFrame) -> pd.DataFrame:
    """Deletes an entry in the dataframe"""

    print_brk()
    R = select_row(df)
    print(f"Contents:\n{df.iloc[[R]]}")
    done = False
    y_list = ["y", "Y"]
    n_list = ["n", "N"]
    while not done:
        proceed = str(input("[INPUT]: Delete this entry? [y/n]"))
        if (proceed in y_list) or (proceed in n_list):
            done = True
        else:
            print("[ERROR]: Invalid input, try again.")
    if proceed in y_list:
        print(f"[LOG]: Deleting entry {R}.")
        df = df.drop(index = int(R))
        print("[LOG]: Done.")
        buffer_save(df.copy())
        return df
    elif proceed in n_list:
        print("[LOG]: Exiting...")
        return df

# endregion

# region MAIN

# This region is just for the main function and any additional code i want to test for a sec

def main():
    """Putting everything together"""

    global buffer
    global buffer_location

    print("====== DATABSE CONFIGURATOR ======")
    df = import_database()
    print_df(df)

    while True:
        print_brk()
        choice = ""
        x = ""
        choice = str(input("[INPUT]: Please choose from the following options:\n[P]rint dataframe\n[E]dit an entry\n[A]dd an entry\n[D]elete an entry\n[U]ndo\n[R]edo\n[S]ave and exit\n[Q]uit without saving\n\n"))
        if (choice == "P") or (choice == "p"):
            print_df(df)

        if (choice == "E") or (choice == "e"):
            df = edit_entry(df.copy())

        if (choice == "A") or (choice == "a"):
            df = add_entry(df.copy())

        if (choice == "D") or (choice == "d"):
            df = del_entry(df.copy())

        if (choice == "U") or (choice == "u"):
            df = undo()

        if (choice == "R") or (choice == "r"):
            df = redo()

        if (choice == "S") or (choice == "s"):
            x = str(input("[INPUT]: Confirm save and exit [Y/n]:\n"))
            while True:
                if (x == "Y") or (x == "y") or (not x):
                    export_database(df.copy())
                    print("[LOG]: Exiting...")
                    sys.exit()
                elif (x == "N") or (x == "n"):
                    break
                else:
                    print("[ERROR]: Invalid input, try again.")
            continue

        if (choice == "Q") or (choice == "q"):
            x = str(input("[INPUT]: Confirm quit without saving [Y/n]:\n"))
            while True:
                if (x == "Y") or (x == "y") or (not x):
                    print("[LOG]: Exiting...")
                    sys.exit()
                elif (x == "N") or (x == "n"):
                    break
                else:
                    print("[ERROR]: Invalid input, try again.")
            continue


if __name__ == "__main__":
    main()

#endregion