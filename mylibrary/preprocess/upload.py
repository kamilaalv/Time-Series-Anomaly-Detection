#will work only in jupyter
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import pandas as pd
import os

def upload_csv():
    """Function to upload CSV file."""
    Tk().withdraw() 
    
    file_path = askopenfilename(filetypes=[("CSV files", "*.csv")])
    
    if file_path:  
        df = pd.read_csv(file_path)
        file_name = os.path.basename(file_path)
        return df, file_name
    else:
        print("No file selected.")

