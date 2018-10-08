#from PIL import ImageGrab, ImageOps
#import os
import time
import win32api, win32con
from numpy import *
import win32clipboard
 
if __name__ == '__main__':
    main()
    
def screenGrab():
    box = ()
    im = ImageGrab.grab()
    print(os.getcwd())
    #im.save(os.getcwd() + '\\full_snap__' + str(int(time.time())) + '.png', 'PNG')
    return im
 
def main():
    time.sleep(1)
 
def mousePos(x=(0,0)):
    win32api.SetCursorPos(x)
    
def leftClick():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
    print("Click.")          #completely optional. But nice for debugging purposes.

def ctrlA():
    win32api.keybd_event(0x11, 0,0,0)
    win32api.keybd_event(0x41, 0,0,0)
    win32api.keybd_event(0x11,0 ,win32con.KEYEVENTF_KEYUP ,0)
    win32api.keybd_event(0x41,0 ,win32con.KEYEVENTF_KEYUP ,0)
    print("Selected all.")
    
def ctrlC():
    win32api.keybd_event(0x11, 0,0,0)
    win32api.keybd_event(0x43, 0,0,0)
    win32api.keybd_event(0x11,0 ,win32con.KEYEVENTF_KEYUP ,0)
    win32api.keybd_event(0x43,0 ,win32con.KEYEVENTF_KEYUP ,0)
    print("Copied.")
    
def get_clipboard():
    win32clipboard.OpenClipboard()
    text = win32clipboard.GetClipboardData()
    win32clipboard.CloseClipboard()
    return text

def get_cords():
    x,y = win32api.GetCursorPos()
    x = x - x_pad
    y = y - y_pad
    print(x,y)
    
def get_data():
    text= get_clipboard()
    data_dic = {}
    
    paperclip_index = text.find("Paperclips: ")
    business_index = text.find("Business")
    paperclip_num = text[paperclip_index+12 : business_index-6]
    
    available_funds_index = text.find("Available Funds: $ ")
    avg_letter_index = text.find("Avg. ")
    if avg_letter_index == -1:
        avg_letter_index = text.find("Unsold")
    fund_num = text[available_funds_index+19 : avg_letter_index-2]
    #print(fund_num)
    data_dic["fund_num"] = float(fund_num)
    
    mrkt_level_index = text.find("Cost: $ ")
    manufacturing_index = text.find("\r\n\r\nManufacturing")
    marketing_cost = text[mrkt_level_index+8 : manufacturing_index]
    data_dic["marketing_cost"] = float(marketing_cost)
    
    clips_per_sec_index = text.find("Second: ")
    clips_end_index = text.find("\r", clips_per_sec_index)
    clips_per_sec = text[clips_per_sec_index+8 : clips_end_index]
    data_dic["clips_per_sec"] = float(clips_per_sec)
    
    # TODO
    # wire cost check below average (below 20 for exmample)
    
    return data_dic
    
ctrlA()
ctrlC()
#leftClick()
data_dic = get_data()
print(data_dic)
# mousePos((30,320)) lower!!!
mousePos((30,570))
leftClick()

event_count = 0
while event_count < 60:
    time.sleep(1)
    ctrlA()
    ctrlC()
    data_dic = get_data()
    if data_dic["clips_per_sec"] == 0:
        mousePos((30,520))
        leftClick()
        event_count += 1
        continue
    mousePos((30,390))
    leftClick()
    mousePos((30,570))
    leftClick()
    event_count += 1
    
    
    
# TODO
# Use if statement to click less.
# Use best algorithm to reach marketing in less time (under 10 minutes?)
# basically buys enough autoclippers to keep wait time for marketing button
# press under 10 minutes
    
# also use price per clip in algorithm