import cv2
import imutils
import numpy as np
from skimage.segmentation import clear_border
from imutils.perspective import four_point_transform

#Read, Blur, Threshold and invert the Picture for better Puzzle recognizion
def processImage(imgPath, debug=False):
    rawimg = cv2.imread(imgPath)
    img = rawimg.copy()
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.GaussianBlur(img, (5, 5), 1)
    img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    img = cv2.bitwise_not(img)
    puzzleCnt = findOutline(img)
    croppedImg = cropImage(rawimg, puzzleCnt)

    processedImage = cv2.resize(croppedImg, dsize=(225,225))

    #Vizualize the outline and cropped Image for debugging
    if debug:
        outlinedImg = cv2.drawContours(rawimg, [puzzleCnt], -1, (0, 255, 0), 2)
        cv2.imshow("Puzzle Outline", outlinedImg)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        cv2.imshow("Puzzle cropped", cropImage(outlinedImg, puzzleCnt))
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        cv2.imshow("Processed Image", processedImage)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return processedImage

#Find contours in the thresholded image and sort them by size
def findOutline(img):
    cnts = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

    puzzleCnt = None

    for c in cnts:
        # approximate the contour
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        # if our approximated contour has four points, then we can assume we have found the outline of the puzzle
        if len(approx) == 4:
            puzzleCnt = approx
            break

    return puzzleCnt

#Crop image to achieve a "Top-Down" view of the Puzzle
def cropImage(img, puzzleCnt):
    return four_point_transform(img, puzzleCnt.reshape(4, 2))

#Extract the digit from the cell
def extractDigit(inputImage, x, y, debug=False):

    cell = inputImage[(25 * y):((25 * y) + 25 + 4), (25 * x):((25 * x) + 25 + 4)]

    img = cv2.resize(cell, dsize=(50,50))
    # apply automatic thresholding to the cell and then clear any
    # connected borders that touch the border of the cell
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    img = clear_border(img)

    # find contours in the thresholded cell
    cnts = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    # if no contours were found than this is an empty cell
    if len(cnts) == 0:
        print("Nothing here")
        return None

    # otherwise, find the largest contour in the cell and create a
    # mask for the contour
    c = max(cnts, key=cv2.contourArea)
    mask = np.zeros(img.shape, dtype="uint8")
    cv2.drawContours(mask, [c], -1, 255, -1)

    # compute the percentage of masked pixels relative to the total
    # area of the image
    (h, w) = img.shape
    percentFilled = cv2.countNonZero(mask) / float(w * h)

    img = cv2.medianBlur(img, 3)
    img = cv2.bitwise_not(img)
    # if less than 2% of the mask is filled then we are looking at
    # noise and can safely ignore the contour
    if percentFilled < 0.02:
        print("Only noise")
        return None

    # check to see if we should visualize the masking step
    if debug:
        cv2.imshow("Digit", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    # return the digit to the calling function
    return img