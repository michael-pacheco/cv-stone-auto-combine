import cv2
import numpy as np
import argparse
from matplotlib import pyplot as plt
from PIL import ImageGrab
'''
img_rgb = cv2.imread('Untitled.png')
img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
'''
while True:
	img_rgb=np.array(ImageGrab.grab(bbox=(0,0,600,1000))) # X1,Y1,X2,Y2
	img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
	template = cv2.imread('rain2.png',0)
	w, h = template.shape[::-1]
	res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
	threshold = 0.5
	loc = np.where( res >= threshold)

	points = sorted(list(zip(*loc[::-1])))
	print(points)
	points_to_remove = []
	for x in range(len(points)):
		for y in range(x+1, len(points)):
			if (points[x][0] == points[y][0]+1 or points[x][0] == points[y][0]-1 or points[x][0] == points[y][0]) and (points[x][1] == points[y][1]+1 or points[x][1] == points[y][1]-1 or points[x][1] == points[y][1]):
				points_to_remove.append(points[y])

	for pt in points_to_remove:
		if pt in points:
			points.remove(pt)
	if points:
		for pt in points:
			print(pt)
			cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)

			cv2.imshow('PURGED.png',img_rgb)
			cv2.waitKey(0)
