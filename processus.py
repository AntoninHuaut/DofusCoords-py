import psutil
import win32gui
import win32process

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