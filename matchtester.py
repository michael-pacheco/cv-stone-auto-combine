import cv2
import numpy as np
import argparse
from matplotlib import pyplot as plt
from PIL import ImageGrab
import win32gui
import msvcrt
 
 #first move and resize the image of our emulator
def windowEnumerationHandler(hwnd, top_windows):
    top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))
    
 
results = []
top_windows = []
win32gui.EnumWindows(windowEnumerationHandler, top_windows)
count=0
for i in top_windows:
    #for some reason there is more than one memu process, so get the 2nd one
    if "memu" == i[1].lower():
        count+=1
    if "memu" == i[1].lower() and count == 2:
        print(i)
        win32gui.ShowWindow(i[0],5)
        win32gui.SetForegroundWindow(i[0])
        win32gui.MoveWindow(i[0], 0, 0, 650, 1050, True)
        
        '''
        Getting the size/location of the window
        rect = win32gui.GetWindowRect(i[0])
        x = rect[0]
        y = rect[1]
        w = rect[2] - x
        h = rect[3] - y
        print("Window %s:" % win32gui.GetWindowText(i[0]))
        print("\tLocation: (%d, %d)" % (x, y))
        print("\t    Size: (%d, %d)" % (w, h))
        '''

img_rgb=np.array(ImageGrab.grab(bbox=(0,0,600,1000))) # X1,Y1,X2,Y2
img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
img_gray = img_gray[700:1000, 5:595]
cv2.imshow("roi", img_gray)
template = cv2.imread('stone.png',0)
w, h = template.shape[::-1]
res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
threshold = 0.7
loc = np.where( res >= threshold)

points = sorted(list(zip(*loc[::-1])))

points_to_remove = []
for x in range(len(points)):
    for y in range(x+1, len(points)):
        if (points[x][0] == points[y][0]+1 or points[x][0] == points[y][0]-1 or points[x][0] == points[y][0]) and (points[x][1] == points[y][1]+1 or points[x][1] == points[y][1]-1 or points[x][1] == points[y][1]):
            points_to_remove.append(points[y])

for pt in points_to_remove:
    if pt in points:
        points.remove(pt)

for pt in points:
    print(pt)
    #cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
    cv2.rectangle(img_rgb, (pt[0]+5, pt[1]+700), (pt[0] + w + 5 , pt[1] + h + 700), (0,0,255), 2)
cv2.imshow('PURGED.png',img_rgb)
cv2.waitKey(0)
#clover = 0.6
