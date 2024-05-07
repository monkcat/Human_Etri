import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_label_dist(input_label):
    fig = plt.figure(figsize = (12,5))
    
    label = ["avg_up", "avg_down"]
    index = ["Q1", "Q2", "Q3", "S1", "S2", "S3", "S4"]
    pos = [241, 242, 243, 245, 246, 247, 248]
    title = ["Sleep Quality", "Emotion", "Stress", "Sleep Time", "Sleep Efficiency", "Sleep Latency", "WASO"]
    
    for i in range(7):
        ratio = [int(input_label[index[i]].sum()/508*100), int((508-input_label[index[i]].sum())/508*100)]
        ax1 = fig.add_subplot(pos[i])
        ax1.pie(ratio, labels = label, autopct='%.1f%%')
        ax1.set_title(title[i])


def plot_HAR(path, t_start = 0, t_end = 0):
    measure = ['mAcc', 'mGps', 'mGyr', 'mMag']
    feature_map = {'mAcc' : ['timestamp','x','y','z'], 'mGps' : ['timestamp', 'lat', 'lon', 'accuracy'], 
                   'mGyr' : ['timestamp', 'x', 'y', 'z', 'roll', 'pitch', 'yaw'], 'mMag' : ['timestamp','x','y','z']}
    color_map = ['r', 'g', 'b']
    for i in range(4):
        directory = path + measure[i]+'/'
        files = os.listdir(directory)
        files = [file for file in files if "csv" in file]
        files.sort()
        init_date = pd.to_datetime(int(directory.split("/")[3]), unit = 's')
        df = pd.read_csv(directory+files[0])
        
        for filename in files[1:]:
            filepath = os.path.join(directory, filename)
            if os.path.isfile(filepath):
                date = pd.to_datetime(int(filename.split(".")[0]), unit='s')
                temp_df = pd.read_csv(directory+filename)
                temp_df['timestamp'] += (date - init_date).total_seconds()
                df = pd.concat([df, temp_df])
        if (t_start != 0 and t_end != 0):
            df = df[df['timestamp'] >= t_start*60]
            df = df[df['timestamp'] <= t_end*60]
        
        plt.figure(figsize = (15, 3))
        for j, feature in enumerate(feature_map[measure[i]][1:4]):
            plt.scatter(df['timestamp']/60, df[feature], s = 2, marker = '_', alpha = 0.5, color = color_map[j])
        plt.title(measure[i])
    plt.show()