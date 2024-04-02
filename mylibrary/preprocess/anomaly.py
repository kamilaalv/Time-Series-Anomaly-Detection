import random
import copy
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D


def add_percentage_anomaly(
    arr,
    anomaly_normal_ratio=0.01,
    noise=0.05,
    wave=False,
    noise_direction="p",
    wave_length=0,
    random_state=None,  # Added parameter for random state
):
    random.seed(random_state)  # Set random seed

    anomaly_count = int(arr.shape[0] * anomaly_normal_ratio)
    print(anomaly_count, "ANOMALIES")

    anomaly_points = list()
    if wave and wave_length != 0:
        anomaly_waves = list()
        for _ in range(anomaly_count):
            max_starting_point = arr.shape[0] - wave_length
            starting_point = random.randrange(0, max_starting_point)
            anomaly_points = list(range(starting_point, starting_point + wave_length))
            anomaly_waves.append(anomaly_points)
    else:
        anomaly_points = random.sample(range(arr.shape[0]), anomaly_count)

    ano_arr = copy.deepcopy(arr)
    if wave and wave_length != 0:
        for wave in anomaly_waves:
            for j in range(arr.shape[1]):
                for i in range(arr.shape[0]):
                    if i in wave:
                        if noise_direction == "p":
                            ano_arr[i][j] += noise * arr[i][j]
                        elif noise_direction == "n":
                            ano_arr[i][j] -= noise * arr[i][j]
                        elif noise_direction == "random":
                            if random.choice([True, False]):
                                ano_arr[i][j] += noise * arr[i][j]
                            else:
                                ano_arr[i][j] -= noise * arr[i][j]
    elif not wave:
        for j in range(arr.shape[1]):
            choice = random.choice([True, False])
            for i in range(arr.shape[0]):
                if i in anomaly_points:
                    if noise_direction == "p":
                        ano_arr[i][j] += noise * arr[i][j]
                    elif noise_direction == "n":
                        ano_arr[i][j] -= noise * arr[i][j]
                    elif noise_direction == "random":
                        if choice:
                            ano_arr[i][j] += noise * arr[i][j]
                        else:
                            ano_arr[i][j] -= noise * arr[i][j]

    if wave and wave_length != 0:
        return ano_arr.reshape(-1), anomaly_waves
    else:
        return ano_arr.reshape(-1), anomaly_points

""" Adds anomalies to the data.
    Args:
        arr: Wanted values at the given columns.
        anomaly_normal_ratio: The ratio of the number of anomalies to the number of normal values. ,
        noise: Noise to be added to the values.,
        wave: True if you want to add waves of anomalies. False otherwise. ,
        noise_direction:'p' for positive noise and 'n' for negative noise. ,
        wave_length: Wave length of the anomaly wave. ,

    Returns: Anomaly array and the anomaly points.
    """

def apply_anomaly(
    df,
    anomaly_normal_ratio=0.01,
    noise=0.05,
    wave=False,
    noise_direction="n",
    wave_length=0,
    random_state=None,  
    nsensors=1
):
    
    # Show to Sevde
    sensors = [col for col in df.columns if col != 'DateTime']
    anomaly_points = {}

    random.seed(random_state)
    selected_sensors = random.sample(list(sensors), nsensors)

    for sensor in selected_sensors:
        print(sensor)
        df.loc[:, sensor], anomaly_points[sensor] = add_percentage_anomaly(
            df.loc[:, sensor].values.reshape(-1,1), 
            anomaly_normal_ratio = anomaly_normal_ratio, 
            noise = noise,
            wave = wave,
            noise_direction = noise_direction,
            wave_length = wave_length,
            random_state=random_state  
        )
    return df, anomaly_points

def plot_anomaly(df, anomaly_points):
    sensors = [col for col in df.columns if col != 'DateTime']
    anomaly_sensors = [key for key in anomaly_points.keys()]
    
    num_subplots = len(sensors)
    fig, axes = plt.subplots(num_subplots, 1, figsize=(10, 5*num_subplots)) 

    for i, sensor in enumerate(sensors):
        ax = axes[i] if num_subplots > 1 else axes  
        ax.plot(df.index, df[sensor])  
        
        if sensor in anomaly_sensors:
            anomaly_indexes = anomaly_points[sensor]
            for index in anomaly_indexes:
                ax.plot(df.index[index], df[sensor].iloc[index], 'ro')  
        
        ax.set_title(sensor)  

    plt.tight_layout()
    plt.show()