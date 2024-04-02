from sklearn.preprocessing import RobustScaler
import pandas as pd

def min_max_scale(column):
    min_val = column.min()
    max_val = column.max()
    return (column - min_val) / (max_val - min_val)

def apply_min_max_scale(df):
    return df.apply(lambda col: min_max_scale(col) if col.name != 'DateTime' else col, axis=0)

def apply_robust_scale(df):
    scaler = RobustScaler()
    scaled_columns = pd.DataFrame(scaler.fit_transform(df.drop(columns=['DateTime'])), columns=df.drop(columns=['DateTime']).columns)
    scaled_df = pd.concat([df[['DateTime']], scaled_columns], axis=1)
    return scaled_df