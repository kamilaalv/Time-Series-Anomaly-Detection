import pandas as pd
import numpy as np
from . import scale

'''  window_size = 3, 
     overlap = 2
[1
 2     [[1,2,3] 
 3 ->   [3,4,5]]
 4
 5]
 
'''

def sliding_window_df(df, window_size, overlap=1, scale = '', delta = False):
    # Scaling part
    if scale.lower() == 'min max':
        df = scale.apply_min_max_scale(df)
    elif scale.lower() == 'robust':
        df = scale.apply_robust_scale(df)
        
    
    #Creating sliding window
    num_cols = len(df.columns) - 1  # Number of columns excluding the first column
    num_windows = (len(df) - window_size) // overlap + 1  # Calculate the number of windows
    window_data = np.zeros((num_windows, window_size * num_cols))  # Initialize an empty array to store window data

    # Extract window slices using NumPy indexing
    for i in range(num_windows):
        start_index = i * overlap
        end_index = start_index + window_size
        window_data[i] = df.iloc[start_index:end_index, 1:].values.reshape(-1)  # Extract values and flatten

    # Create column names for the DataFrame
    col_names = [f'{col}separator{i+1}' for i in range(window_size) for col in df.columns[1:]]

    # Create the DataFrame
    window_df = pd.DataFrame(window_data, columns=col_names)
    
    # Rearrange columns by alphabetical order of their names
    window_df = window_df.reindex(sorted(window_df.columns), axis=1)
    
    # Calculate delta values if delta=True
    if delta:
        for sensor in df.columns[1:]:
            cols = [col for col in window_df.columns if col.startswith(sensor)]
            window_df[f'{sensor}separatordelta'] = window_df[cols].diff(axis=1).sum(axis=1)
    
    return window_df


#is not finished
def add_delta_values(df):
   return True

def test():
    print("Hi")