import imageProcessor
import jsonCreator
import ocrEngine
import numpy
import tkinter
from tkinter import filedialog

#Vars
sudokuSize  = 9
sudokuData  = numpy.empty((sudokuSize, sudokuSize), dtype=object)
jsonData = None

#Prerequisites
root        = tkinter.Tk().withdraw() #Don't show tkinter root window
imgPath     = filedialog.askopenfilename()
img         = imageProcessor.processImage(imgPath)

print("Sudoku puzzle path:",imgPath)
print("Processing puzzle...")

#Process the Puzzle
for x in range(0, sudokuSize):
    for y in range(0, sudokuSize):
        result  = ''
        image   = imageProcessor.extractDigit(img, x, y)

        if image is not None:
            result = ocrEngine.getChar(image)
            # print(result.strip())

        if result.strip() == '':
            result = 0

        sudokuData[x, y] = int(result)

print("Processing done.")
print("Results:")
print("---------------------")
print(sudokuData)
print("---------------------")
print("Generating JSON file")
jsonData = jsonCreator.createJSON(sudokuData, sudokuSize)
print("JSON generated.")
jsonCreator.saveJSON(filedialog.asksaveasfilename(), jsonData)
