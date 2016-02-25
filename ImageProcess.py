#### ImageProcess.py
# Takes a jpg image in white background and prints a version of the image 
# with white pixels as space and non-white pixels as characters.
#
# Authors: Chris Horan, Zeal Yim
# Created: Feb 23 2016
# Last modified: Feb 24 2016 by Zeal
####

from __future__ import print_function
from PIL import Image

THRESHOLD_MARGIN = 0.95 #Filters out near-white pixels
WHITE = 765 #RGB
MAX_HEIGHT_OUTPUT = 200
MAX_WIDTH_OUTPUT = 200

def imgToArr(img):
	nearWhite = WHITE * THRESHOLD_MARGIN
	pixelsArr = []
	imgWidth, imgHeight = img.size

	if imgWidth > MAX_WIDTH_OUTPUT or imgHeight > MAX_HEIGHT_OUTPUT: #check if img needs to be compressed
		imgArr = []
		compressedImgArr = []
		tmp = []
		pixelCounter = 0
		#convert img's pixel into a 2D array
		for pixel in iter(img.getdata()):
			tmp.append(pixel)
			pixelCounter += 1
			if pixelCounter >= imgWidth:
				imgArr.append(tmp)
				tmp = [] #still looking at how python handles reassignment regarding memory management
				pixelCounter = 0
		#calculate the ratio the img needs to be compressed at
		compressRatio = int(round(max(imgWidth/MAX_HEIGHT_OUTPUT, imgHeight/MAX_HEIGHT_OUTPUT)))
		#compress imgArr and put in to compressedImgArr for later process
		topLeftPixelRow = 0
		topLeftPixelCol = 0
		btnRightPixelRow = topLeftPixelRow + compressRatio
		btnRightPixelCol = topLeftPixelCol + compressRatio
		nextBtnRightPixelCol = btnRightPixelCol
		averageRGB = 0,0,0
		while nextBtnRightPixelCol <= imgHeight:
			averageRGB = ()
*************************************************************************************************************
	else: #img does not need to be compressed
		tmp = []
		pixelCounter = 0
		for pixel in iter(img.getdata()):
			r,g,b = pixel
			pixelVal = r + g + b
			if pixelVal < nearWhite:
				tmp.append("M ")
			else:
				tmp.append("  ")
			pixelCounter += 1
			if pixelCounter == imgWidth:
				pixelsArr.append(tmp)
				tmp = []
				pixelCounter = 0
	return pixelsArr

def printImgArr(imgArr):
	for i in range(len(imgArr)):
		for j in range(len(imgArr[i])):
			print(imgArr[i][j], end="")
		print("")

def shrinkImgArr(imgArr):
	newArr = []
	k = 0
	i = 0
	while i < len(imgArr) - 1:
		newArr.append([])
		j = 0
		while j < len(imgArr[i]) - 1:
			newArr[k].append(imgArr[i][j])
			j += 2
		i += 2
		k += 1
	return newArr
def average(list):
	return sum(list)/list.len

#main
f = open('asciiArt.txt', 'w')

img = Image.open("logo.jpg")

pixArr = imgToArr(img)

while len(pixArr) > 400:
  pixArr = shrinkImgArr(pixArr)

for i in range(len(pixArr)):
	for j in range(len(pixArr[i])):
		f.write(pixArr[i][j])
	f.write('\n')
