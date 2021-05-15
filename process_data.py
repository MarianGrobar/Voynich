import math
from datetime import datetime
from PIL import Image, ImageDraw

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


def GetDistance(x1,y1,x2,y2):
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)



data_dictionary = dict()

# exported classification.csv
data = pandas.read_csv('D:\\Downloads\\voynich-manuscript-classifications (2).csv')
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
    if key == "f082v.jpg":
        groups = []
        done = []
        for c1 in range(len(values)):
            print(values[c1])
            c1x0 = values[c1].x
            c1y0 = values[c1].y
            c1x1 = c1x0 + values[c1].width
            c1y1 = c1y0 + values[c1].height
            avgx0 = 0
            avgy0 = 0
            avgx1 = 0
            avgy1 = 0
            group = []
            avgCoordinates = []
            for c2 in range(c1, len(values)):
                if c1 != c2:
                    c2x0 = values[c2].x
                    c2y0 = values[c2].y
                    c2x1 = c2x0 + values[c2].width
                    c2y1 = c2y0 + values[c2].height

                    euc1 = GetDistance(c1x0,c1y0,c2x0,c2y0)
                    euc2 = GetDistance(c1x1,c1y1,c2x1,c2y1)

                    if euc1 < 10 and euc2 < 10:
                        avgx0 = avgx0 + c2x0
                        avgy0 = avgy0 + c2y0
                        avgx1 = avgx1 + c2x1
                        avgy1 = avgy1 + c2y1

                        group.append(c2)
                        done.append(c2)

            if c1 not in done:
                avgx0 = avgx0 + c1x0
                avgy0 = avgy0 + c1y0
                avgx1 = avgx1 + c1x1
                avgy1 = avgy1 + c1y1
                group.append(c1)

                avgCoordinates = [avgx0/len(group),avgy0/len(group),avgx1/len(group),avgy1/len(group)]


                group.append(avgCoordinates)
                done.append(c1)

            if len(group) != 0:
                groups.append(group)

        with Image.open("f082v.jpg") as im:
            draw = ImageDraw.Draw(im)
            for gr in groups:
                x0 = gr[-1][0]
                y0 = gr[-1][1]
                x1 = gr[-1][2]
                y1 = gr[-1][3]
                draw.rectangle([(x0, y0), (x1, y1)], width=2, outline='red')
            im.show()

