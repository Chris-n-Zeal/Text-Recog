#### ImageProcess.py
# Takes a jpg image and prints a version of the image with white 
# pixels as space and non-white pixels as characters.
#
# Authors: Chris Horan, Zeal Yim
####

from __future__ import print_function
from PIL import Image

THRESHOLD_MARGIN = 0.95 #Filters out near-white pixels
WHITE = 765 #RGB

def imgToArr(pic):
	nearWhite = WHITE * THRESHOLD_MARGIN

	pixels = []

	wid, hei = img.size

	i = 0
	tmp = []

	for pixel in iter(img.getdata()):
		r,g,b = pixel
		pixelVal = r + g + b
		if pixelVal < nearWhite:
			tmp.append("M ")
		else:
			tmp.append("  ")
		i += 1
		if i == wid:
			pixels.append(tmp)
			tmp = []
			i = 0
	return pixels

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




f = open('asciiArt.txt', 'w')

img = Image.open("cin.jpg")

pixArr = imgToArr(img)

while len(pixArr) > 400:
  pixArr = shrinkImgArr(pixArr)

for i in range(len(pixArr)):
	for j in range(len(pixArr[i])):
		f.write(pixArr[i][j])
	f.write('\n')
