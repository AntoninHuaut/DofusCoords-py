import cv2
import easyocr
import mss
import win32gui
import win32con
import os
from timeit import default_timer as timer
from image import  read_coordinates, screenshot_and_process
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
        time_start = timer()

        path = screenshot_and_process(sct, {"top": 90, "left": 5, "width":120, "height":30})
        x, y, err = read_coordinates(ocr_reader, path)
        if err is not None:
            print(err)
            return
        
        time_end = timer()
        print(f"x: {x:.4}, y: {y:.4}, time: {time_end - time_start:.3f}s")