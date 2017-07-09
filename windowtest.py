import win32gui
 
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
