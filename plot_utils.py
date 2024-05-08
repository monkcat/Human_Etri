import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import plot_utils
import os

m_measure = ['mAcc', 'mGps', 'mGyr', 'mMag']
w_measure = ['e4Acc', 'e4Bvp', 'e4Eda', 'e4Hr', 'e4Temp']
feature_map = {'mAcc' : ['timestamp','x','y','z'], 'mGps' : ['timestamp', 'lat', 'lon', 'accuracy'], 
               'mGyr' : ['timestamp', 'x', 'y', 'z', 'roll', 'pitch', 'yaw'], 'mMag' : ['timestamp','x','y','z'],
               'e4Acc' : ['timestamp','x','y','z'], 'e4Bvp' : ['timestamp','value'], 'e4Eda' : ['timestamp','eda'], 
               'e4Hr' : ['timestamp','hr'], 'e4Temp' : ['timestamp','temp']}
color_map = ['r', 'g', 'b', 'purple', 'pink', 'grey']
activity_color = {'work' : 'red', 'study' : 'red', 'travel' : 'yellow', 'meal' : 'green', 'recreation_etc' : 'blue', 'recreation_media' : 'blue',
                  'outdoor_act' : 'purple', 'household' : 'grey', 'personal_care' : 'pink', 'sleep' : 'black', 'socialising' : 'blue'}

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


def plot_HAR_m(path, integrated = 1, t_start = 0, t_end = 0):
    fig = plt.figure(figsize = (15, 14))
    pos = [411, 412, 413, 414]
    for i in range(4):
        if (integrated):
            directory = path + m_measure[i]+'.csv'
            df = pd.read_csv(directory)
        else:
            directory = path + m_measure[i]+'/'
            files = os.listdir(directory)
            files = [file for file in files if "csv" in file]
            files.sort()
            df = pd.read_csv(directory+files[0])
            
            for filename in files[1:]:
                filepath = os.path.join(directory, filename)
                if os.path.isfile(filepath):
                    date = pd.to_datetime(int(filename.split(".")[0]), unit='s') + datetime.timedelta(hours = 9)
                    temp_df = pd.read_csv(directory+filename)
                    temp_df['timestamp'] = temp_df['timestamp'].apply(lambda x : date + datetime.timedelta(seconds = x) if True else x)
                    df = pd.concat([df, temp_df])
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df[df['timestamp'] >= datetime.datetime(2000, 1, 1, 12, 0, 0)]
        if (t_start != 0 and t_end != 0):
            df = df[df['timestamp'] >= t_start]
            df = df[df['timestamp'] <= t_end]
        
        ax = fig.add_subplot(pos[i])
        for j, feature in enumerate(feature_map[m_measure[i]][1:]):
            ax.scatter(df['timestamp'], df[feature], s = 2, marker = '_', alpha = 0.5, color = color_map[j], label = feature)
        if (t_start != 0 and t_end != 0):
            plt.xlim(t_start, t_end)
        ax.set_title(m_measure[i])
        ax.legend(loc="best")
    print(" End? ")
    plt.show()


def plot_HAR_w(path, integrated = 1, t_start = 0, t_end = 0):
    fig = plt.figure(figsize = (15, 17))
    pos = [511, 512, 513, 514, 515]
    for i in range(5):
        if (integrated):
            directory = path + w_measure[i]+'.csv'
            df = pd.read_csv(directory)
        else:
            directory = path + w_measure[i]+'/'
            files = os.listdir(directory)
            files = [file for file in files if "csv" in file]
            files.sort()
            df = pd.read_csv(directory+files[0])
            
            for filename in files[1:]:
                filepath = os.path.join(directory, filename)
                if os.path.isfile(filepath):
                    date = pd.to_datetime(int(filename.split(".")[0]), unit='s') + datetime.timedelta(hours = 9)
                    temp_df = pd.read_csv(directory+filename)
                    temp_df['timestamp'] = temp_df['timestamp'].apply(lambda x : date + datetime.timedelta(seconds = x) if True else x)
                    df = pd.concat([df, temp_df])
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df[df['timestamp'] >= datetime.datetime(2000, 1, 1, 12, 0, 0)]
        if (t_start != 0 and t_end != 0):
            df = df[df['timestamp'] >= t_start]
            df = df[df['timestamp'] <= t_end]
        
        ax = fig.add_subplot(pos[i])
        for j, feature in enumerate(feature_map[w_measure[i]][1:]):
            ax.scatter(df['timestamp'], df[feature], s = 2, marker = '_', alpha = 0.5, color = color_map[j], label = feature)
        if (t_start != 0 and t_end != 0):
            plt.xlim(t_start, t_end)
        ax.set_title(w_measure[i])
        ax.legend(loc="best")
    plt.show()
        

def plot_HAR_label(path, integrated = 1, t_start = 0, t_end = 0):
    fig = plt.figure(figsize = (15, 7))
    pos = [211, 212]
    ax = fig.add_subplot(pos[-2])
    if (integrated):
        label_path = 'data' + path[15:] + path.split("/")[3] + "_label.csv"
    else:
        label_path = path + path.split("/")[3] + "_label.csv"
    df = pd.read_csv(label_path)
    df["ts"] = pd.to_datetime(df["ts"], unit = 's') + datetime.timedelta(hours = 9)
    used_labels = set()
    df = df[df['ts'] >= datetime.datetime(2000, 1, 1, 12, 0, 0)]
    if (t_start != 0 and t_end != 0):
        df = df[df['ts'] >= t_start]
        df = df[df['ts'] <= t_end]
    for i in range(1, len(df)):
        ax.fill_between([df.iloc[i-1, 0], df.iloc[i, 0]], 0, 1, color=activity_color[df.iloc[i-1, 1]], label=df.iloc[i-1, 1] if df.iloc[i-1, 1] not in used_labels else "")
        used_labels.add(df.iloc[i-1,1])
    if (t_start != 0 and t_end != 0):
        plt.xlim(t_start, t_end)
    ax.set_title('action')
    ax.legend(loc="best")

    ax = fig.add_subplot(pos[-1])
    ax.plot(df['ts'], df['emotionPositive'], label = 'emotionPositive')
    ax.plot(df['ts'], df['emotionTension'], label = 'emotionTension')
    ax.plot(df['ts'], df['activity'], label = 'activity')
    if (t_start != 0 and t_end != 0):
        plt.xlim(t_start, t_end)
    ax.set_title('survey')
    ax.legend(loc="best")
    plt.show()
