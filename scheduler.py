import os
import time
from timeit import default_timer as timer

import easyocr
import mss
import yaml

from image import read_coordinates, screenshot_and_process
from processus import get_pid_by_name

ocr_reader = easyocr.Reader(['en'], gpu=True)
if not os.path.exists("images/"):
    os.makedirs("images/")

latest_coordinates = {"x": None, "y": None, "timestamp": None}

with open("config.yaml") as f:
    cfg = yaml.load(f, Loader=yaml.FullLoader)


def scheduled_task(check_coordinates_change_func):
    global latest_coordinates

    cfg_screenshot = cfg["screenshot"]

    target_pid = get_pid_by_name("dofus")
    if not target_pid:
        print(f"No process ID found.")
        return

    with mss.mss() as sct:
        time_start = timer()

        path = screenshot_and_process(sct, cfg_screenshot)
        x, y, err = read_coordinates(ocr_reader, path)
        if err is not None:
            print(err)
            return

        time_end = timer()

        latest_coordinates["x"] = x
        latest_coordinates["y"] = y
        latest_coordinates["timestamp"] = time.time()

        print(f"x: {x:.4}, y: {y:.4}, time: {time_end - time_start:.3f}s")
        check_coordinates_change_func()
