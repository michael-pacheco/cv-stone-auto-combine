from PIL import ImageGrab
import cv2, numpy as np, pyautogui, time, win32gui, msvcrt, collections
from matplotlib import pyplot as plt

#filenames and manually found thresholds for template matching
thresholds = collections.OrderedDict([("stone.png", 0.7), ("pebble.png",0.48), ("big_stone.png", 0.6), ("rock.png", 0.8), ("shuriken.png", 0.75), ("cold_shuriken.png", 0.62), ("four_shuriken.png",0.61), ("clover.png", 0.6), ("four_clover.png", 0.57), ("hadouken.png", 0.58)])

#offsets for region of interest (our inventory)
x_offset = 5
y_offset = 700

#first move the emulator and resize it. i use memu
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
        
while True:
    for stone in thresholds.keys():
        print("Matching for: %s" % (stone.split('.')[0]))

        #grab the image of your android emulator. becuase this is a very simple method, you should fit your emulator to fit these settings
        img_rgb=np.array(ImageGrab.grab(bbox=(0,0,600,1000))) # X1,Y1,X2,Y2
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        img_gray = img_gray[y_offset:1000, x_offset:595]
        template = cv2.imread(stone,0)
        w, h = template.shape[::-1]
        res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
        threshold = thresholds[stone]
        loc = np.where( res >= threshold)

        #get the locations into a list so we can access its length later
        points = sorted(list(zip(*loc[::-1])))

        #iterate through the list of points that match the template and remove similar ones by appending to another list, since iteration will mess up if we remove it from the list while iterating
        points_to_remove = []
        for x in range(len(points)):
            for y in range(x+1, len(points)):
                if (points[x][0] == points[y][0]+1 or points[x][0] == points[y][0]-1 or points[x][0] == points[y][0]) and (points[x][1] == points[y][1]+1 or points[x][1] == points[y][1]-1 or points[x][1] == points[y][1]):
                    points_to_remove.append(points[y])
        #remove them here
        for pt in points_to_remove:
            if pt in points:
                points.remove(pt)
            
        #matching big stone is hard since its very similar to the regular stone. so we match the regular stone here and remove all the stones from the big stones found
        #this should definitely be a function
        if stone.split('.')[0] == "big_stone":
            #START OF STONE PURGE   
            template2 = cv2.imread('stone.png',0)
            w2, h2 = template2.shape[::-1]
            res2 = cv2.matchTemplate(img_gray,template2,cv2.TM_CCOEFF_NORMED)
            threshold2 = 0.7
            loc2 = np.where( res2 >= threshold2)

            points2 = sorted(list(zip(*loc2[::-1])))

            points_to_remove2 = []
            for x in range(len(points2)):
                for y in range(x+1, len(points2)):
                    if (points2[x][0] == points2[y][0]+1 or points2[x][0] == points2[y][0]-1 or points2[x][0] == points2[y][0]) and (points2[x][1] == points2[y][1]+1 or points2[x][1] == points2[y][1]-1 or points2[x][1] == points2[y][1]):
                        points_to_remove2.append(points2[y])

            for pt in points_to_remove2:
                if pt in points2:
                    points2.remove(pt)
                    
            points_to_remove = []
            for x in range(len(points2)):
                for pt in points:
                    if (points2[x][0] == pt[0]+1 or points2[x][0] == pt[0]-1 or points2[x][0] == pt[0]) and (points2[x][1] == pt[1]+1 or points2[x][1] == pt[1]-1 or points2[x][1] == pt[1]):
                        points_to_remove.append(pt)
            for pt in points_to_remove:
                if pt in points:
                    points.remove(pt)
            #END OF STONE PURGE
        
        #print out how many stones were found in the end
        print("Stones found: %d" % (len(points)))
        
        #this is where we use pyautogui to simulate mouse clicks/drags
        for pt in range(0, len(points)-1, 2):
            if pt+1 <= len(points):
                print("Starting at point: ", points[pt])
                pyautogui.moveTo(points[pt][0]+25+x_offset, points[pt][1]+25+y_offset)
                print("Moved to point: ", points[pt+1])
				#x coord + 25 (since the width of the inventory space is around 50px) + xoffset, same for y
                pyautogui.dragTo(points[pt+1][0]+25+x_offset,points[pt+1][1]+25+y_offset, 2, pyautogui.easeInQuad,button='left')
                pyautogui.moveTo(5,5)

                

        time.sleep(1.5)