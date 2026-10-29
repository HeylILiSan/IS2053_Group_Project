import csv
import numpy as np
import pandas as pd 
import tkinter as tk
from tkinter import filedialog, ttk

# WHEN "senders.csv" IS IMPORTED AS A DATAFRAME, THE COLUMNS ARE "Name", "Phone", "Email", AND "List"

changes = {}

def import_database(p = "senders.csv") -> pd.DataFrame:
    """Imports the database csv as a pandas dataframe"""
    print(f"Importing database {p}...")
    df = pd.readcsv(p)
    print("Done.")
    return df

def export_database(df : pd.DataFrame, p : str = "senders.csv"):
    """Exports the dataframe to the database csv"""
    print(f"Writing dataframe to {p}...")
    df.to_csv(p)
    print("Done.")

def print_df(df):
    """Prints the contents of a dataframe"""
    print(df)

def add_entry(df):
    """Adds a new entry to the dataframe"""

    raise NotImplementedError

def edit_entry(df):
    """Edits an existing entry in the dataframe"""

    raise NotImplementedError

def select_column(df) -> str:
    """Returns the name of the column selected by the user"""
    done = False
    while not done:
        C = str(input("Please select from the following identifiers by entering the corresponding number:\n1 - Name\n2 - Phone Number\n3 - Email Address\n\n"))
        try: 
            C = int(C)
            if 0<C<4:
                done = True
            else:
                print("Invalid input/")
        except:
            print("Invalid type.")
    columns = ["", 'Name', 'Phone', 'Email']
    return columns[C]

def find_row(df, C):
    """Finds the row of an entry in a column"""
    while True:
        entry = str(input(f"Enter the corresponding {C} for the entry you are looking for\n"))
        try:
            row = np.where(df[C] == entry)[0]
            return row
        except:
            print("Entry not found, try again")



def del_entry(df):
    """Deletes an entry in the dataframe"""
    C = select_column(df)
    R = find_row(df, C)
    print(f"Entry {R} selected.")
    print(f"Contents:\n{df.iloc[[R]]}")
    done = False
    y_list = ["y", "Y"]
    n_list = ["n", "N"]
    while not done:
        proceed = str(input("Delete this entry? [y/n]"))
        if (proceed in y_list) or (proceed in n_list):
            done = True
        else:
            print("Invalid input.")
    if proceed in y_list:
        df.drop(df.index[R])
        print("Entry deleted, exiting...")
    elif proceed in n_list:
        print("Exiting...")

    


