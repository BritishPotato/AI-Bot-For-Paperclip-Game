#from PIL import ImageGrab, ImageOps
#import os
import time
import win32api, win32con
from numpy import *
import win32clipboard
 
def main():
    time.sleep(1)
    

if __name__ == '__main__':
    main()
    
def screenGrab():
    box = ()
    im = ImageGrab.grab()
    print(os.getcwd())
    #im.save(os.getcwd() + '\\full_snap__' + str(int(time.time())) + '.png', 'PNG')
    return im
 
 
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
    print(x,y)
    
def wireClick(y=0):
    """
    Click on "Wire" at position (30,520)
    """
    mousePos((30,520+y))
    leftClick()
    
def marketingClick(y=0):
    """
    Click on "Marketing" at position (30,390)
    """
    mousePos((30,390+y))
    leftClick()
    
def autoclippersClick(y=0):
    """
    Click on "AutoClippers" at position (30, 570)
    """
    mousePos((30,570+y))
    leftClick()
    
def get_data():
    """
    Select all, copy, get clipboard, use indexes to create dic
    Returns dictionary with keys "paperclip_num", "fund_num", 
    "marketing_cost", "wire_length", "wire_cost", 
    """
    ctrlA()
    ctrlC()
    time.sleep(.1)
    text = get_clipboard()
    data_dic = {}
    
    paperclip_index = text.find("Paperclips: ")
    business_index = text.find("Business")
    paperclip_num = text[paperclip_index+12 : business_index-6]
    data_dic["paperclip_num"] = int(paperclip_num.replace(",",""))
    
    available_funds_index = text.find("Available Funds: $ ")
    avg_letter_index = text.find("Avg. ")
    if avg_letter_index == -1:
        avg_letter_index = text.find("Unsold")
    fund_num = text[available_funds_index+19 : avg_letter_index-2]
    #print(fund_num)
    data_dic["fund_num"] = float(fund_num.replace(",", ""))
    
    mrkt_level_index = text.find("Cost: $ ")
    manufacturing_index = text.find("\r\n\r\nManufacturing")
    marketing_cost = text[mrkt_level_index+8 : manufacturing_index]
    data_dic["marketing_cost"] = float(marketing_cost.replace(",", ""))
    
    clips_per_sec_index = text.find("Second: ")
    before_inch_empline_index = text.find("\r", clips_per_sec_index)
    inches_index = text.find(" inches")
    wire_length = text[before_inch_empline_index+4 : inches_index]
    data_dic["wire_length"] = int(''.join(c for c in wire_length if c.isdigit()))
    #wire_length.replace(",", ""))
    
    wire_cost_index = text.find("$ ", inches_index)
    wire_end_index = text.find("\r\n\r\n", wire_cost_index)
    wire_cost = text[wire_cost_index+2 : wire_end_index]
    data_dic["wire_cost"] = int(wire_cost.replace(",", ""))
    
    autoclippers_cost_index = text.find("$ ", wire_end_index)
    autoclippers_end_index = text.find("\r\n\r\n", autoclippers_cost_index)
    autoclippers_cost = text[autoclippers_cost_index+2 : autoclippers_end_index]
    data_dic["autoclippers_cost"] = float(autoclippers_cost.replace(",", ""))
#    clips_end_index = text.find("\r", clips_per_sec_index)
#    clips_per_sec = text[clips_per_sec_index+8 : clips_end_index]
#    data_dic["clips_per_sec"] = float(clips_per_sec)
    
    
    
    # TODO
    # wire cost check below average (below 20 for exmample)
    
    print(data_dic)
    return data_dic


def bot():
    global r,w
    event_count = 0
    autoclippers_event = 0
    while event_count < 100 or 1==1:
        try:
            time.sleep(2)
            dic = get_data()
            
            #print(data_dic["wire_length"])
            if dic["wire_length"] <= 500 or dic["wire_cost"] < 21:
                wireClick(r+w)
                event_count += 1
                continue
            if dic["marketing_cost"] < dic["fund_num"]:
                marketingClick(r)
            
            if autoclippers_event >= 50 and dic["autoclippers_cost"] < dic["fund_num"]:
                autoclippersClick(r+w)
                autoclippers_event = -1
            autoclippers_event += 1
            event_count += 1
        
        except win32api.error:
            continue
    
def init():
    global r, w
    revtracker_check = input("Is the RevTracker Project complete?(y/n): ")
    if revtracker_check == "y":
        r = 40
    wirebuyer_check = input("Is the WireBuyer Project complete?(y/n): ")
    if wirebuyer_check == "y":
        w = 20
    for i in reversed(range(6)):
        print(i)
        time.sleep(1)
    print("ONLINE!")
    bot()
        
        

init()
    
# TODO
# Use if statement to click less.
# Use best algorithm to reach marketing in less time (under 10 minutes?)
# basically buys enough autoclippers to keep wait time for marketing button
# press under 10 minutes
    
# also use price per clip in algorithm