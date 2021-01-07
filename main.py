import imageProcessor
import imga
import ocrEngine
import numpy

#Vars
imgPath         = '/Users/marinobantli/Documents/Coding/DS_Sudoku/resources/sudoku.jpg'
img             = imageProcessor.processImage(imgPath)
sudokuSize      = 9

#X, Y
sudokuData      = numpy.empty((sudokuSize, sudokuSize), dtype=object)

for x in range(0, sudokuSize):
    for y in range(0, sudokuSize):
        result = ocrEngine.getChar(imageProcessor.extract_digit(imageProcessor.getCell(img,x,y)))
        print(result)
        if not result.strip():
            result = 0

        sudokuData[y, x] = int(result)

print(sudokuData)

#print(ocrEngine.getChar(imageProcessor.getCell(imageProcessor.processImage(imgPath), 3, 0)))
