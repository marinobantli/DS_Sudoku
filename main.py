import imageProcessor
import ocrEngine
import numpy

#Vars
imgPath         = 'D:\\Private\\Juventus\\DataScience\\resources\\sudoku3.png'
img             = imageProcessor.processImage(imgPath)
sudokuSize      = 9

#X, Y
sudokuData      = numpy.empty((sudokuSize, sudokuSize), dtype=object)

for x in range(0, sudokuSize):
    for y in range(0, sudokuSize):
        image = imageProcessor.extractDigit(img,x,y)

        if image is not None:
            result = ocrEngine.getChar(image)
            print(result.strip())
            sudokuData[y, x] = result.strip()

print(sudokuData)

#print(ocrEngine.getChar(imageProcessor.getCell(imageProcessor.processImage(imgPath), 3, 0)))
