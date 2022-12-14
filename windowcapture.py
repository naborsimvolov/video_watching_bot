import win32gui
from win32api import GetSystemMetrics
import mss
import numpy as np

def callback(hwnd, strings):
    if win32gui.IsWindowVisible(hwnd):
        window_title = win32gui.GetWindowText(hwnd)
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        if window_title and right-left and bottom-top:
            strings.append('0x{:08x}: "{}"'.format(hwnd, window_title))
    return True

#this function finds window which starts with name, we gave it.
def update_win_name(callback, st_window_name):
    win_list = []
    win32gui.EnumWindows(callback, win_list)  # populate list

    for window in win_list:
        full_name = window.split(' ', 1)[1]
        bot_part = window.split(' ', 2)[1]
        if st_window_name == bot_part:
            full_name = full_name.replace('"', '')
            window_name = full_name
            return(window_name)
            

class Capture:

    window_name = None
    st_window_name = None

    x_pr = int(round(GetSystemMetrics(0) / 100, 0))
    y_pr = int(round(GetSystemMetrics(1) / 100, 0))
    #set crop
    crop_x1 = 10
    crop_y1 = 100
    crop_x2 = 18
    crop_y2 = 15

    from_x_text1 = 12 * x_pr
    from_x_text2 = 26 * x_pr
    from_y = 24 * y_pr
    
    text_w = 3 * x_pr
    text_h = 2 * y_pr
    
    def __init__(self, st_window_name):
        self.st_window_name = '"' + st_window_name
        self.window_name = update_win_name(callback, self.st_window_name)

    def get_screenshot(self):
        #find window and get parameters  
        self.window_name = update_win_name(callback, self.st_window_name)
        mn_wnd = win32gui.FindWindow(None, self.window_name)
        mn_rect = win32gui.GetWindowRect(mn_wnd)
        
        mn_pos_x1 = mn_rect[0] + self.crop_x1
        mn_pos_y1 = mn_rect[1] + self.crop_y1
        mn_pos_x2 = mn_rect[2]
        mn_pos_y2 = mn_rect[3]

        win_w = mn_pos_x2 - mn_pos_x1 - self.crop_x2
        win_h = mn_pos_y2 - mn_pos_y1 - self.crop_y2

        win_range = {"top": mn_pos_y1, "left": mn_pos_x1, "width": win_w, "height": win_h}

        #get screenshot 
        with mss.mss() as sct:
            img_array = np.array(sct.grab(win_range))
        
        #drop alpha channel for correct work cv2.matchtemplate
        img_array = img_array[...,:3]
        return img_array

    def get_win_pos(self):
        #find window and get params
        self.window_name = update_win_name(callback, self.st_window_name)
        mn_wnd = win32gui.FindWindow(None, self.window_name)
        mn_rect = win32gui.GetWindowRect(mn_wnd)
        
        return mn_rect[0], mn_rect[1]

    def get_text_part(self):
        #find window and get parameters
        self.window_name = update_win_name(callback, self.st_window_name)
        mn_wnd = win32gui.FindWindow(None, self.window_name)
        mn_rect = win32gui.GetWindowRect(mn_wnd)

        text1_x = mn_rect[0] + self.from_x_text1
        text2_x = mn_rect[0] + self.from_x_text2
        text_y = mn_rect[1] + self.from_y

        text1_range = {"top": text_y, "left": text1_x, "width": self.text_w, "height": self.text_h}
        text2_range = {"top": text_y, "left": text2_x, "width": self.text_w, "height": self.text_h}

        #get screenshot 
        with mss.mss() as sct:  # Create a new mss.mss instance
            text1_sc = np.array(sct.grab(text1_range))
            text2_sc = np.array(sct.grab(text2_range))
        
        return text1_sc, text2_sc, text1_x, text2_x, text_y