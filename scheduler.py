import cv2
import easyocr
import mss
import win32gui
import win32con
import os
from timeit import default_timer as timer
from image import cleanCoordinate, preprocess_image, readtext, screenshot
from processus import find_window_by_pid, get_pid_by_name

ocr_reader = easyocr.Reader(['en'], gpu = True)
if not os.path.exists("images/"):
    os.makedirs("images/")

def scheduled_task():
    target_pid = get_pid_by_name("dofus")
    hwnds = find_window_by_pid(target_pid)
    if not hwnds:
        print(f"No window found for process ID {target_pid}.")
        return
    
    hwnd = hwnds[0]
    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
    try:
        win32gui.SetForegroundWindow(hwnd)
    except Exception as e:
        pass
    
    with mss.mss() as sct:
        timeStart = timer()

        screenshot(sct, {"top": 90, "left": 5, "width":120, "height":30}, "images/app_screenshot.png")
        processed_img = preprocess_image("images/app_screenshot.png")
        cv2.imwrite('images/processed_screenshot.png', processed_img)
        raw_result = readtext(ocr_reader, 'images/processed_screenshot.png')

        x,y,err = handleRawResult(raw_result)
        if err is not None:
            print(err)
            return
        
        timeEnd = timer()
        print(f"x: {x:.4}, y: {y:.4}, time: {timeEnd - timeStart:.3f}s")

def handleRawResult(raw_result):
    while isinstance(raw_result, list):
        if len(raw_result) == 0:
            return None, None, "no coordinates extracted"
        raw_result = raw_result[len(raw_result) - 1]

    if "," in raw_result:
        raw_result = raw_result.replace(",", " ")
   
    raw_result = raw_result.split()

    if len(raw_result) < 2:
        return None, None, "no coordinates found"

    x, y = cleanCoordinate(raw_result[0]), cleanCoordinate(raw_result[1])
    return x,y,None