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
    fig = plt.figure(figsize = (15, 21))
    measure = ['mAcc', 'mGps', 'mGyr', 'mMag']
    feature_map = {'mAcc' : ['timestamp','x','y','z'], 'mGps' : ['timestamp', 'lat', 'lon', 'accuracy'], 
                   'mGyr' : ['timestamp', 'x', 'y', 'z', 'roll', 'pitch', 'yaw'], 'mMag' : ['timestamp','x','y','z']}
    color_map = ['r', 'g', 'b', 'purple', 'pink', 'grey']
    activity_color = {'work' : 'red', 'study' : 'red', 'travel' : 'yellow', 'meal' : 'green', 'recreation_etc' : 'blue', 'recreation_media' : 'blue',
                      'outdoor_act' : 'purple', 'household' : 'grey', 'personal_care' : 'pink', 'sleep' : 'black', 'socialising' : 'blue'}
    pos = [611, 612, 613, 614, 615, 616]
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
        
        ax = fig.add_subplot(pos[i])
        for j, feature in enumerate(feature_map[measure[i]][1:]):
            ax.scatter(df['timestamp']/60, df[feature], s = 2, marker = '_', alpha = 0.5, color = color_map[j], label = feature)
        ax.set_title(measure[i])
        ax.legend(loc="best")

    ax = fig.add_subplot(pos[-2])
    label_path = path + path.split("/")[3] + "_label.csv"
    init_date = pd.to_datetime(int(directory.split("/")[3]), unit = 's')
    df = pd.read_csv(label_path)
    df["ts"] = pd.to_datetime(df["ts"], unit = 's').apply(lambda x : (x - init_date).total_seconds()/60 if True else x)
    used_labels = set()
    if (t_start != 0 and t_end != 0):
        df = df[df['ts'] >= t_start]
        df = df[df['ts'] <= t_end]
    for i in range(1, len(df)):
        ax.fill_between([df.iloc[i-1, 0], df.iloc[i, 0]], 0, 1, color=activity_color[df.iloc[i-1, 1]], label=df.iloc[i-1, 1] if df.iloc[i-1, 1] not in used_labels else "")
        used_labels.add(df.iloc[i-1,1])
    ax.set_title('action')
    ax.legend(loc="best")

    ax = fig.add_subplot(pos[-1])
    ax.plot(df['ts'], df['emotionPositive'], label = 'emotionPositive')
    ax.plot(df['ts'], df['emotionTension'], label = 'emotionTension')
    ax.plot(df['ts'], df['activity'], label = 'activity')
    ax.set_title('survey')
    ax.legend(loc="best")
    
    plt.show()