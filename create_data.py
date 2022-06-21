import json
import os
import random
import sqlite3
from itertools import cycle

import numpy as np
import pandas as pd
from datetime import datetime


def generate_data_files():
    labeling_files = ['labeling1.json', 'labeling2.json', 'labeling.json']
    for file in labeling_files:
        size = 500
        labels = ['car', 'truck', 'road_sign', 'traffic_sign', 'pedestrian', 'animal', 'unknown']
        countries = ['germany', 'austria', 'hungary', 'france']
        timestamp_list = list(pd.date_range(datetime.now(), periods=size, freq='us').astype(str))
        speed_asc = np.logspace(-2, 6, num=int(size / 2) - 1, base=2)
        speed_desc = np.logspace(6, -2, num=int(size / 2) - 1, base=2)
        speed = np.concatenate((np.array([0]), speed_asc, speed_desc, np.array([0])))
        distance_km = list(np.linspace(100, 104, num=size).astype(float))
        confidence = np.random.uniform(0, 1, size=size)

        timestamp_list = [datetime.timestamp(datetime.strptime(str(x), "%Y-%m-%d  %H:%M:%S.%f")) for x in
                          timestamp_list]
        json_labels_list = list(zip(timestamp_list, cycle(labels), cycle(countries), confidence))
        json_labels = {x[0]: {'time_stamp': x[1][0], 'label': x[1][1], "confidence": x[1][3]} for x in
                       enumerate(json_labels_list)}
        with open(file, 'w') as labels_file:
            json.dump(json_labels, labels_file)

        data_dict = {timestamp_list.index(x): {"time_stamp": x, "speed": speed[timestamp_list.index(x)],
                                               "distance_km": distance_km[timestamp_list.index(x)],
                                               "country": json_labels_list[timestamp_list.index(x)][2],
                                               "image": f'image{random.randint(0, 1000)}.jpg'} for x in
                     timestamp_list}
    with open('recording.json', 'w') as records_file:
        json.dump(data_dict, records_file)


def clear_database():
    try:
        os.remove('example.db')
    except FileNotFoundError:
        pass


def create_database():
    with sqlite3.connect('example.db') as conn:
        cur = conn.cursor()
        cur.execute('''CREATE TABLE labeling (time timestamp, label varchar(50), confidence float)''')
        cur.execute('''CREATE TABLE recording (time_stamp timestamp,
        speed float, distance_km float, country varchar(50), image varchar(50))''')

        conn.commit()


def populate_database():
    with open('labeling.json', 'r') as labels:
        with sqlite3.connect('example.db') as conn:
            cur = conn.cursor()
            data = json.loads(labels.read())
            for row in data.values():
                cur.execute('INSERT INTO labeling values (?, ?, ?)',
                            (row['time_stamp'], row['label'], row['confidence']))
            conn.commit()

    with open('recording.json', 'r') as labels:
        with sqlite3.connect('example.db') as conn:
            cur = conn.cursor()
            data = json.loads(labels.read())
            for row in data.values():
                cur.execute('INSERT INTO recording values (?, ?, ?, ?, ?)',
                            (row['time_stamp'], row['speed'], row['distance_km'], row['country'], row['image']))
            conn.commit()


if __name__ == '__main__':
    clear_database()
    generate_data_files()
    create_database()
    populate_database()
