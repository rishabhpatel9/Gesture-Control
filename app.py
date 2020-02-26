import sys
import os
import subprocess
import re
import cv2
def get_active_window_title():
    root = subprocess.Popen(['xprop', '-root', '_NET_ACTIVE_WINDOW'], stdout=subprocess.PIPE)
    stdout, stderr = root.communicate()

    m = re.search(b'^_NET_ACTIVE_WINDOW.* ([\w]+)$', stdout)
    if m != None:
        window_id = m.group(1)
        window = subprocess.Popen(['xprop', '-id', window_id, 'WM_CLASS'], stdout=subprocess.PIPE)
        stdout, stderr = window.communicate()
    else:
        return None

    match = re.match(b'WM_CLASS\(\w+\) = ".*", (?P<name>.+)$', stdout)
    if match != None:
        return match.group("name").strip(b'"')

    return None

if __name__ == "__main__":
	while True:
		k = cv2.waitKey(1) & 0xFF
		if k == ord('q'):
			break
		else:
			print(get_active_window_title())
#b'Google-chrome'
#b'Gnome-terminal
#b'Spotify'
