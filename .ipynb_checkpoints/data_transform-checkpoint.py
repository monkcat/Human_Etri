import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import plot_utils
import os

def save_HAR_m(path, t_start = 0, t_end = 0):
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
        df = pd.read_csv(directory+files[0])
        
        for filename in files[1:]:
            filepath = os.path.join(directory, filename)
            if os.path.isfile(filepath):
                date = pd.to_datetime(int(filename.split(".")[0]), unit='s') + datetime.timedelta(hours = 9)
                temp_df = pd.read_csv(directory+filename)
                temp_df['timestamp'] = temp_df['timestamp'].apply(lambda x : date + datetime.timedelta(seconds = x) if True else x)
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                df = pd.concat([df, temp_df])
        if not os.path.exists('./data_integrated/' + path[4:]):
            os.makedirs('./data_integrated/' + path[4:])
        df.to_csv('./data_integrated/' + path[4:] + measure[i] + '.csv')


def save_HAR_w(path, t_start = 0, t_end = 0):
    fig = plt.figure(figsize = (15, 17))
    measure = ['e4Acc', 'e4Bvp', 'e4Eda', 'e4Hr', 'e4Temp']
    feature_map = {'e4Acc' : ['timestamp','x','y','z'], 'e4Bvp' : ['timestamp','value'], 
                   'e4Eda' : ['timestamp','eda'], 'e4Hr' : ['timestamp','hr'], 'e4Temp' : ['timestamp','temp']}
    color_map = ['r', 'g', 'b', 'purple']
    pos = [511, 512, 513, 514, 515]
    for i in range(5):
        directory = path + measure[i]+'/'
        files = os.listdir(directory)
        files = [file for file in files if "csv" in file]
        files.sort()
        # init_date = pd.to_datetime(int(directory.split("/")[3]), unit = 's')
        df = pd.read_csv(directory+files[0])
        
        for filename in files[1:]:
            filepath = os.path.join(directory, filename)
            if os.path.isfile(filepath):
                date = pd.to_datetime(int(filename.split(".")[0]), unit='s') + datetime.timedelta(hours = 9)
                temp_df = pd.read_csv(directory+filename)
                temp_df['timestamp'] = temp_df['timestamp'].apply(lambda x : date + datetime.timedelta(seconds = x) if True else x)
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                df = pd.concat([df, temp_df])

        if not os.path.exists('./data_integrated/' + path[4:]):
            os.makedirs('./data_integrated/' + path[4:])
        df.to_csv('./data_integrated/' + path[4:] + measure[i] + '.csv')