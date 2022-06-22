import json
import operator

import pandas as pd
import sqlite3

with sqlite3.connect('example.db') as conn:
    df_labeling = pd.read_sql_query("SELECT * from labeling", conn)
    df_recording = pd.read_sql_query("SELECT * from recording", conn)

"""
• statistics
    o Number of images in the system with cars on them
    o Number of overall driven kilometers in Germany
"""
print("Number of images with cars: ", df_labeling['label'].value_counts()['car'])

df_recording['distance_km'] = df_recording['distance_km'] - df_recording['distance_km'][0]
df_recording['distance_diff'] = df_recording['distance_km'].diff()
df_filter = df_recording['country'] == 'germany'
last_recorded = df_recording.where(df_filter).dropna()
print("Distance taken in Germany (km): ", last_recorded['distance_diff'].sum())

"""
• ad-hoc requests:
    o Collect all the images of a “recording” where the test car’s speed is less than 1 m/s and
    pedestrians can be found on the front camera images.
    o Front camera images with animals in Austria.
"""
with sqlite3.connect('example.db') as conn:
    pedestrian_slow_images = pd.read_sql_query("SELECT r.image FROM recording r LEFT JOIN labeling l ON "
                                               "r.id = l.id  WHERE  r.speed < 1 AND l.label = 'car' ", conn)
    animal_austria_images = pd.read_sql_query("SELECT r.image FROM recording r LEFT JOIN labeling l ON r.id = "
                                              "l.id  WHERE  r.country = 'austria' AND l.label = 'animal'", conn)

print("Images where car is slower than 1m/s", pedestrian_slow_images)
print("Images where recording has image of animals in austria: ", animal_austria_images)

"""
Load data into the created database and answer the following questions:
• for each recfile list the 5 label classes with the highest confidence
• find the recfile which has the most labels with at least 0.6 confidence
"""

rec_files = ['labeling.json', 'labeling1.json', 'labeling2.json']
recfile_confidences = dict()

for recfile in rec_files:
    with open(recfile, 'r') as file:
        data = json.loads(file.read())
    sorted_dict = dict(sorted(data.items(), key=lambda item: item[1]['confidence']))

    five_highest_confidence = dict()
    for k, v in sorted_dict.items():
        if not five_highest_confidence.get(v['label']):
            five_highest_confidence[v['label']] = 1
        if len(five_highest_confidence) == 5:
            break

    print(f"Five highest confidence labels are - {', '.join(five_highest_confidence.keys())} - in recfile: {recfile}")

    for val in data.values():
        if val['confidence'] >= 0.6:
            if not recfile_confidences.get(recfile):
                recfile_confidences[recfile] = 1
            else:
                recfile_confidences[recfile] += 1

    print(recfile_confidences)
print("\nrecfile with most confident labels: ", max(recfile_confidences.items(), key=operator.itemgetter(1))[0])
