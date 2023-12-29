import pygetwindow as gw
import keyboard
import time
import pyperclip
import threading
import requests
from urllib.parse import urlparse
import tkinter as tk
from tkinter import messagebox



redirect = "127.0.0.1"
hosts_path = 'C:\\Windows\\System32\\drivers\\etc\\hosts'
backup_path = 'C:\\Windows\\System32\\drivers\\etc\\hosts.backup'
delay = 3
global blocked_sites
blocked_sites = []


def chrome():
    active = gw.getActiveWindow()
    if active and 'Google Chrome' in active.title:
        keyboard.press_and_release('ctrl+l')
        time.sleep(0.5)
        keyboard.press_and_release('ctrl+c')
        url = pyperclip.paste()
        if 'google.com/search?' in url or '.' not in url or " " in url:
            pass
        else:
            return url.strip()
    else:
        print('Chrome not active')
    return None


def check_url(url):
    try:
        if not (url.startswith('https://')):
            return False
        parsed_url = urlparse(url)
        domain = parsed_url.netloc or parsed_url.hostname
        if domain and domain != parsed_url.hostname:
            return False
        print('Visited domain:',domain )
        response = requests.get(url, verify=True)
        if response.status_code != 200:
            return False
        return True
    except Exception as e:
        return False
    

def block(curr_url):
    parsed_url = urlparse(curr_url)
    url = parsed_url.hostname or parsed_url.netloc
    if len(url)==0:
        url=curr_url
    try:
        global blocked_sites
        if url not in blocked_sites:    
            ans = messagebox.askquestion("SurfSafe", f"{url} is harmfull, do you want to block?", icon='warning')
            if ans == 'yes':    
                with open(hosts_path, 'r+') as hostfile:
                    hosts_content = hostfile.read()
                    if url not in hosts_content:
                        hostfile.write(redirect + ' ' + url + '\n')
                        print(url, 'blocked')
            else:
                pass
    except PermissionError:
        print("Need admin privileges to block websites")
    except Exception as e:
        print(e)
    finally:
        blocked_sites.append(url)
        active = gw.getActiveWindow()
        if active and 'Google Chrome' in active.title:
            time.sleep(2)
            keyboard.press_and_release('ctrl+r')


# to execute only reset() in cmd -> python -c "from app import reset; reset()"
    
def reset():
    try:     
        with open(backup_path, 'r') as backup_file:
            hosts_content = backup_file.read()
            with open(hosts_path, 'w') as hosts_file:
                hosts_file.write(hosts_content)
        print('Hosts file successfully restored.')
    except Exception as e:
        print(f'Error: {e}')
    finally:
        global blocked_sites
        blocked_sites.clear()
        time.sleep(2)
        active = gw.getActiveWindow()
        if active and 'Google Chrome' in active.title:
            keyboard.press_and_release('ctrl+r')

def stop():
    global running
    running = False

def main():
    global running
    running = True
    try:
        while running:
            url = chrome()
            if url:
                is_safe = check_url(url)
                if is_safe:
                    print(url," is safe to visit")
                else:
                    block(url)
            time.sleep(delay)
    except Exception as e:
        exit(0)
    
    
def start_main_thread():
    main_thread = threading.Thread(target=main)
    main_thread.start()


def window():
    window = tk.Tk()
    window.title("SurfSafe")
    window.geometry("400x400")
    window.configure(bg='black')
    window.resizable(False, False)
    label = tk.Label(window, text="SurfSafe", bg='black', fg='white', font=("Arial", 25))
    label.pack()
    button_start = tk.Button(window, text="Start", bg='black', fg='white', font=("Arial", 15), command=start_main_thread)
    button_start.pack()

    button_stop = tk.Button(window, text="Stop", bg='black', fg='white', font=("Arial", 15), command=stop)
    button_stop.pack()
    
    button_reset = tk.Button(window, text="Reset", bg='black', fg='white', font=("Arial", 15), command=reset)
    button_reset.pack()

    entry_label = tk.Label(window, text="Enter URL to block", bg='black', fg='white', font=("Arial", 15))
    entry_label.pack()
    entry = tk.Entry(window, width=30)
    entry.pack()
    button_entry = tk.Button(window, text="Block", bg='black', fg='white', font=("Arial", 15), command=lambda:block(entry.get()))
    button_entry.pack()
    button_clear = tk.Button(window, text="Clear", bg='black', fg='white', font=("Arial", 15), command=lambda:entry.delete(0, tk.END))
    button_clear.pack()

    button_exit = tk.Button(window, text="Exit", bg='black', fg='white', font=("Arial", 15), command=window.destroy)
    button_exit.pack()
    window.mainloop()


if __name__ == "__main__":
    window()