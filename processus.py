import psutil


def get_pid_by_name(process_name):
    for proc in psutil.process_iter(attrs=['pid', 'name']):
        if process_name.lower() in proc.info['name'].lower():
            return proc.info['pid']
    return None
