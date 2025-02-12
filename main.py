import cv2
import easyocr
import mss
import numpy
import psutil
import win32gui
import win32process
from PIL import Image, ImageEnhance, ImageFilter

def find_window_by_pid(pid):
    def callback(hwnd, extra):
        _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
        if found_pid == pid:
            extra.append(hwnd)
    
    hwnds = []
    win32gui.EnumWindows(callback, hwnds)
    return hwnds

def get_pid_by_name(process_name):
    for proc in psutil.process_iter(attrs=['pid', 'name']):
        if process_name.lower() in proc.info['name'].lower():
            return proc.info['pid']
    return None

def preprocess_image(image_path):
    img = cv2.imread(image_path, cv2.COLOR_BGR2GRAY)
    _, img = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY_INV)
    img = cv2.resize(img, None, fx=4, fy=4, interpolation=cv2.INTER_CUBIC) # Scale image first (4x upscaling)   
    # img = cv2.bilateralFilter(img, 100, 100, 100) # Apply bilateral filter to reduce noise while preserving edges
    # img = cv2.convertScaleAbs(img, alpha=1.5, beta=0) # Enhance contrast
    # img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 9, 3)  # Apply adaptive thresholding
    # img = cv2.dilate(img, numpy.ones((2,2), numpy.uint8), iterations=1) # Dilate slightly to enhance connectivity
    # img = cv2.medianBlur(img, 7) # Remove small noise
    # img = cv2.bitwise_not(img) # Invert back
    return img

def ocr(image_path):
    result = reader.readtext(
        image_path,
        paragraph=True,
        min_size=20,
        # contrast_ths=0.3,
        text_threshold=0.35,  # Lower threshold for better number recognition
        # width_ths=2.0,  # Increased width threshold for connected digits
        mag_ratio=2.0  # Additional magnification
    )
    return result

target_pid = get_pid_by_name("dofus")
hwnds = find_window_by_pid(target_pid)
reader = easyocr.Reader(['en'])

if hwnds:
    hwnd = hwnds[0]

    # win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
    # win32gui.SetForegroundWindow(hwnd)
    
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)

    with mss.mss() as sct:
        screenshot = sct.grab({"top": 90, "left": 5, "width":120, "height":30})
        mss.tools.to_png(screenshot.rgb, screenshot.size, output="app_screenshot.png")

        processed_img = preprocess_image('app_screenshot.png')
        processed_path = 'processed_screenshot.png'
        cv2.imwrite(processed_path, processed_img)

        raw_result = ocr(processed_path)
        while isinstance(raw_result, list):
            if len(raw_result) == 0:
                print("No coordinates extracted.")
                exit()  
            raw_result = raw_result[len(raw_result) - 1]

        if "," in raw_result:
            raw_result = raw_result.replace(",", " ")
        raw_result = raw_result.split()

        if len(raw_result) < 2:
            print("No coordinates found.")
            exit()

        x = ''.join(c for c in raw_result[0] if c in "0123456789-")
        y = ''.join(c for c in raw_result[1] if c in "0123456789-")
        print("x:", x, "y:", y)
        
    print("Screenshot saved!")
else:
    print(f"No window found for process ID {target_pid}.")
