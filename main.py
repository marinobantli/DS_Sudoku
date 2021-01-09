import imageProcessor
import ocrEngine
import numpy

#Vars
imgPath         = 'D:\\Private\\Juventus\\DataScience\\resources\\sudoku2.PNG'
img             = imageProcessor.processImage(imgPath)
sudokuSize      = 9

#X, Y
sudokuData      = numpy.empty((sudokuSize, sudokuSize), dtype=object)

for x in range(0, sudokuSize):
    for y in range(0, sudokuSize):
        image = imageProcessor.extractDigit(img,x,y)

        if image is not None:
            result = ocrEngine.getChar(image)
            print(result)
            if not result.strip():
                result = 0

            sudokuData[y, x] = int(result)

print(sudokuData)

#print(ocrEngine.getChar(imageProcessor.getCell(imageProcessor.processImage(imgPath), 3, 0)))
