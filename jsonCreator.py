import os
import numpy
import json
import webbrowser

# Vars
path = os.path.dirname(os.path.abspath(__file__))
data = {}

def createJSON(values, sudokuSize):
    sudokuData = numpy.empty((sudokuSize, sudokuSize), dtype=object)
    sudokuData = values
    squaresList = []

    for x in range(0, sudokuSize):
        for y in range(0, sudokuSize):
            if not values[x,y] == 0:
                data = {
                    'x': x,
                    'y': y,
                    'value': values[x,y]
                }
                squaresList.append(data)

    data = {
        'size': sudokuSize,
        'squares': squaresList
    }

    return data

def saveJSON(path, data):
    with open(path, 'w') as file:
        json.dump(data, file)
        print("JSON saved. Path:",path)

def openFolder():
    webbrowser.open('file:' + path)
