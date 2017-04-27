import win32gui

def get_hwnd(playerName):	
	toplist, winlist = [], []
	def enum_cb(hwnd, results):
		winlist.append((hwnd, win32gui.GetWindowText(hwnd)))

	win32gui.EnumWindows(enum_cb, toplist)
	ts = [(hwnd, title) for hwnd, title in winlist if playerName.lower() in title.lower()]
	if len(ts) == 0:
		return -1
	else:
		return ts[0][0]
	

