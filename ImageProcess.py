#### ImageProcess.py
# Takes a jpg image in white background and prints a version of the image 
# with white pixels as space and non-white pixels as characters.
#
# Authors: Chris Horan, Zeal Yim
# Created: Feb 23 2016
# Last modified: Mar 22 2016 by Chris
####

from __future__ import print_function
from PIL import Image
from Tkinter import Tk
from tkFileDialog import askopenfilename
import os
from subprocess import call
from sys import platform
from time import sleep
import _winreg

THRESHOLD_MARGIN = 0.95 #Filters out near-white pixels
WHITE = 765 #RGB
MAX_HEIGHT_OUTPUT = 300
MAX_WIDTH_OUTPUT = 300

# Takes the sum of RGB values and returns a corresponding character
def colourToChar(rgbSum, min=1):
	cRange = WHITE - min
	if rgbSum > min + cRange * 0.9:
		return "  "
	elif rgbSum <= min + cRange * 0.9 and rgbSum > min + cRange * 0.8:
		return ". "
	elif rgbSum <= min + cRange * 0.8 and rgbSum > min + cRange * 0.7:
		return "` "
	elif rgbSum <= min + cRange * 0.7 and rgbSum > min + cRange * 0.6:
		return "; "
	elif rgbSum <= min + cRange * 0.6 and rgbSum > min + cRange * 0.5:
		return "/ "
	elif rgbSum <= min + cRange * 0.5 and rgbSum > min + cRange * 0.4:
		return "j "
	elif rgbSum <= min + cRange * 0.4 and rgbSum > min + cRange * 0.3:
		return "@ "
	elif rgbSum <= min + cRange * 0.3 and rgbSum > min + cRange * 0.2:
		return "% "
	elif rgbSum <= min + cRange * 0.2 and rgbSum > min + cRange * 0.1:
		return "y "
	else:
		return "$ "

# Takes an image and returns the sum of the RGB values of the darkest pixel
def getDarkest(pic):
	darkest = 765
	for pixel in iter(pic.getdata()):
		r,g,b = pixel
		pixelVal = r + g + b
		if pixelVal < darkest:
			darkest = pixelVal
	return darkest

# Takes an image and returns a 1D array of RGB values by pixel
def imgToArr(img, imgWidth):
	rgbMapArray = []

	#convert img's pixel into a 2D array
	for pixel in iter(img.getdata()):
		rgbMapArray.append(pixel)

	return rgbMapArray

# Takes an image and returns a 2D array of RGB values by pixel with the same width and height as the image
def imgTo2DArr(img, imgWidth):
	rgbMapArray = []
	tmp = []
	pixelCounter = 0

	#convert img's pixel into a 2D array
	for pixel in iter(img.getdata()):
		tmp.append(pixel)
		pixelCounter += 1
		if pixelCounter >= imgWidth:
			rgbMapArray.append(tmp)
			tmp = [] #need to look at how python handles reassignment regarding memory management
			pixelCounter = 0

	return rgbMapArray

# Compresses an image based on compressRatio and returns a 2D array of the compressed image
def compressImg(imgArr, compressRatio):
	compressedImgArr = [] #store the pixel of img after compression
	tmp = [] # temp array to store pixel temporary
	imgWidth, imgHeight = img.size
	#calculate the ratio the img needs to be compressed at

	#compress imgArr and put in to compressedImgArr for later process
	topLeftPixelRow = 0 #start from the first row
	btnRightPixelRow = topLeftPixelRow + compressRatio - 1
	nextBtnRightPixelRow = btnRightPixelRow
	while nextBtnRightPixelRow < imgHeight: #Goes through every pixel within the same row until exceeding the height of image
		topLeftPixelCol = 0 #always start from the first column
		btnRightPixelCol = topLeftPixelCol + compressRatio - 1
		nextBtnRightPixelCol = btnRightPixelCol
		while nextBtnRightPixelCol < imgWidth: #Goes through every pixel within the same column until exceeding the width of image
			currentRow = topLeftPixelRow
			currentCol = topLeftPixelCol
			#get every pixel within the group of pixels needs to be compress into one pixel
			while currentRow <= btnRightPixelRow: #goes through every pixel in row within this group
				while currentCol <= btnRightPixelCol: #goes through every pixel in column within this group
					tmp.append(imgArr[currentRow][currentCol])
					currentCol += 1
				currentCol = topLeftPixelCol
				currentRow += 1
			# print("GROUP!!!!!!!!!!!")
			# print("tmpList: ", tmp)
			#compress the grouped pixels into one pixel
			compressedImgArr.append(averageRGB(tmp)) #put compressed pixel in the compressedImgArr
			tmp = [] #clear tmp. need to look at how python handles reassignment regarding memory management
			#update to the next group on the right
			topLeftPixelCol += compressRatio
			btnRightPixelCol += compressRatio
			nextBtnRightPixelCol = btnRightPixelCol
			# print("Row Compressed!!!!!!!!!!!!")
		#all the groups in one single row is compress at this point

		#get the rest of the pixels on the right that are not enough to form one group
		currentRow = topLeftPixelRow
		currentCol = topLeftPixelCol
		while currentRow < btnRightPixelRow:
			while currentCol < imgWidth: #do until the currentCol is no longer with in the image's width
				tmp.append(imgArr[currentRow][currentCol])
				currentCol += 1
			currentCol = topLeftPixelCol
			currentRow += 1
		# print("tmpList: ", tmp)
		if (imgWidth/compressRatio) != int(imgWidth/compressRatio):
			#compress the last grouped pixels into one pixel
			compressedImgArr.append(averageRGB(tmp))
			tmp = [] #clear tmp
		#next row of groups
		topLeftPixelRow += compressRatio
		btnRightPixelRow = topLeftPixelRow + compressRatio
		nextBtnRightPixelRow = btnRightPixelRow
		#print("LeftOver Compressed!!!!!!!!!!!!")
		# print("tmpList: ", tmp)
	return compressedImgArr

# Takes a 2D array of pixel RGB values of an image, the image width, and the lowest combined RGB value of a pixel 
# on the image. Returns a 2D array filled with ASCII character that draw out the image 
def imgToASCII(imgArr, imgWidth, darkestPixel):
	pixelsArr = []
	tmp = []
	pixelCounter = 0
	for pixel in imgArr:
		r,g,b = pixel
		pixelVal = r + g + b
		tmp.append(colourToChar(pixelVal, darkestPixel))
		pixelCounter += 1
		if pixelCounter == imgWidth:
			pixelsArr.append(tmp)
			tmp = []
			pixelCounter = 0
	return pixelsArr

# Turns an image into a 2D array. If the image's size is larger than MAX_HEIGHT_OUTPUT or MAX_WIDTH_OUTPUT, the 
# image will be compressed proportionally
def imgToText(img):
	nearWhite = WHITE * THRESHOLD_MARGIN
	pixelsArr = []
	imgWidth, imgHeight = img.size
	newImgWidth = 0
	
	if imgWidth > MAX_WIDTH_OUTPUT or imgHeight > MAX_HEIGHT_OUTPUT: #check if img needs to be compressed
		#Imgae needs to turn into a 2D array in order to do the compressing on groups of pixels
		imgArr = imgTo2DArr(img, imgWidth)
		compressRatio = int(round(max(imgWidth/MAX_WIDTH_OUTPUT, imgHeight/MAX_HEIGHT_OUTPUT))) + 1 #the plus one is to account for the last group that gather the left over pixels
		compressedImgArr = compressImg(imgArr, compressRatio)
		#print("nextBtnRightPixelRow: ", nextBtnRightPixelRow, "nextBtnRightPixelCol: ", nextBtnRightPixelCol)
		newImgWidth = (int(imgWidth/compressRatio))
	else: #img does not need to be compressed
		newImgWidth = imgWidth
		compressedImgArr = imgToArr(img, imgWidth)

	#tranform img to ASCII map
	pixelsArr = imgToASCII(compressedImgArr, newImgWidth, getDarkest(img))
	return pixelsArr

# Saves the ASCII character array to a text file
def writeImgArr(imgArr, outputFile):
	if len(imgArr) != 0:
		for i in range(len(pixArr)):
			for j in range(len(pixArr[i])):
				outputFile.write(pixArr[i][j])
			outputFile.write("\n")
		outputFile.write("/")

# Takes an array of RGB tuples and returns a tuple that contains the average of all the RGB values
def averageRGB(pixelList):
	if len(pixelList) < 1:
		return pixelList
	sumPixel = sumRGB(pixelList)
	averagePixel = sumPixel[0] / len(pixelList), sumPixel[1] / len(pixelList), sumPixel[2] / len(pixelList)
	return averagePixel

# Takes an array of RGB tuples and returns the sum of all of the RGB values as a tuple
def sumRGB(pixelList):
	sumRed, sumGreen, sumBlue = 0, 0, 0
	red, green, blue = 0, 0, 0

	for pixel in pixelList:
		red, green, blue = pixel
		sumRed += red 
		sumGreen += green
		sumBlue += blue
	
	sumPixel = sumRed, sumGreen, sumBlue
	return sumPixel

# Opens a dialog box that allows the user to select an image file
def getFileName():
	Tk().withdraw()
	filename = askopenfilename()
	return filename

# Opens the AsciiArt.txt file for preview
def openFile(filepath):
	os.startfile(filepath)

# Main
# Works best with square images. As the ratio between the sides gets bigger, the output image will be more distorted
f = open('asciiArt.txt', 'w')
fileName = getFileName()
img = Image.open(fileName)
pixArr = imgToText(img)
writeImgArr(pixArr, f)
openFile('asciiArt.txt')
f.close()

# Deletes the file after
while(os.path.isfile('asciiArt.txt')):
	sleep(0.5)
	os.remove('asciiArt.txt')
