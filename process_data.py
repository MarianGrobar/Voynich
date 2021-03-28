from datetime import datetime

import pandas
import json


class Identification:
    def __init__(self, x, y, width, height, description):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.description = description

    def __str__(self):
        return f'X: {self.x} Y: {self.y} width: {self.width} height: {self.height} description: {self.description}'

data_dictionary = dict()

# exported classification.csv
data = pandas.read_csv('C:/Users/AnetaOpletalova/Desktop/VoynichExports/voynich-manuscript-classifications.csv')
for index, row in data.iterrows():

    # filter out dates before selected date
    created = row['created_at']
    parsed_created_at = datetime.strptime(created[0:10], "%Y-%m-%d")
    filter_datetime = datetime(2021, 2, 28)
    if parsed_created_at < filter_datetime:
        continue

    annotations = pandas.read_json(row['annotations'])
    an_data = json.loads(annotations.to_json())

    file = pandas.read_json(row['subject_data'])
    file_data = json.loads(file.to_json())
    filename = pandas.DataFrame(file_data.values())['Filename'][0]

    # '0' for task 0 , '1' for task 1
    if len(pandas.DataFrame(an_data['value']['0'])) > 0:
        classifications = an_data['value']['0']
        for classification in classifications:
            ident = Identification(classification['x'], classification['y'], classification['width'],
                                   classification['height'], list(classification['details'][0].values())[0])

            if filename in data_dictionary:
                data_dictionary[filename].append(ident)
            else:
                data_dictionary[filename] = [ident]

for key, values in data_dictionary.items():
    print(key)
    for value in values:
        print(value)

