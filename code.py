from PIL import ImageGrab, ImageOps
import os
import time
import win32api, win32con
from numpy import *
import win32clipboard
 
def screenGrab():
    box = ()
    im = ImageGrab.grab()
    print(os.getcwd())
    #im.save(os.getcwd() + '\\full_snap__' + str(int(time.time())) + '.png', 'PNG')
    return im
 
def main():
    time.sleep(1)
    screenGrab()
 
if __name__ == '__main__':
    main()
    
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

def mousePos(cord):
    win32api.SetCursorPos((x_pad + cord[0], y_pad + cord[1]))
     
def get_cords():
    x,y = win32api.GetCursorPos()
    x = x - x_pad
    y = y - y_pad
    print(x,y)
    
def divide_clipboard():
    text= get_clipboard()
    paperclip_index = text.find("Paperclips: ")
    business_index = text.find("Business")
    paperclip_num = text[paperclip_index+12 : business_index-6]
    
    available_funds_index = text.find("Available Funds: $ ")
    avg_letter_index = text.find("Avg. ")
    if avg_letter_index == -1:
        avg_letter_index = text.find("Unsold")
    fund_num = text[available_funds_index+19 : avg_letter_index-2]
    #print(fund_num)
    
    
ctrlA()
ctrlC()
leftClick()
divide_clipboard()