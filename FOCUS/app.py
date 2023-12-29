import time, tkinter as tk
from urllib.parse import urlparse
import threading
import time, keyboard, pygetwindow as gw
from tkinter import messagebox

global running
running = True
delay=3
global blocked_win, blocked_sites
blocked_sites = []
blocked_win = []
backup_path = 'C:\\Windows\\System32\\drivers\\etc\\hosts.backup'
hosts_path = 'C:\\Windows\\System32\\drivers\\etc\\hosts'
redirect = "127.0.0.1"    


def get_browser_info():
    try:
        active_window = gw.getWindowsWithTitle(gw.getActiveWindow().title)
        if active_window:
            return active_window[0].title

    except Exception as e:
        print(f"Error: {e}")

    return None

def block_websites(curr_url):
    parsed_url = urlparse(curr_url)
    url = parsed_url.hostname or parsed_url.netloc
    if len(url)==0:
        url=curr_url
    try:
        global blocked_sites
        if url not in blocked_sites:    
            ans = messagebox.askquestion("FOCUS", f"Do you want to focus by not visiting {url}", icon='warning')
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
        active = gw.getActiveWindow()
        if active and 'Google Chrome' in active.title:
            time.sleep(2)
            keyboard.press_and_release('ctrl+r')



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
    global blocked_win, blocked_sites, running
    blocked_sites.clear()
    blocked_win.clear()
    running = False
    reset()
    exit(0)


def website(url):
    block_websites(url)    

def window():
    global running
    running = True
    try:
        while running:
            win = get_browser_info()
            print('Active window: ',win)
            win=win.split()
            global blocked_win
            for i in blocked_win:
                if i in win:
                    print('Blocked window: ',i)
                    keyboard.press_and_release('alt+f4')
            time.sleep(delay)
    except Exception as e:
        exit(0)


def window_thread(win):
    global blocked_win
    blocked_win.append(win)
    wind = threading.Thread(target=window)
    wind.start()


def gui():
    gui = tk.Tk()
    gui.geometry('300x400')
    gui.configure(bg='skyblue')
    gui.resizable(False, False)
    tk.Label(gui, text="FOCUS", bg='skyblue', fg='black', font=("Arial", 25)).pack()
    tk.Label(gui, text="concentrate on you self \nby not allowing you device control you", bg='skyblue', fg='black', font=("Arial", 13)).pack()
    tk.Label(gui, text="\n\n", bg='skyblue').pack()
    entry1 = tk.Entry(gui, width=25)
    entry1.pack()

    button_entry1 = tk.Button(gui, text="Block website", bg='skyblue', fg='black', font=("Arial", 15), command=lambda:block_websites(entry1.get()))
    button_entry1.pack()
    tk.Label(gui, text="\n", bg='skyblue').pack()

    entry2 = tk.Entry(gui, width=25)
    entry2.pack()

    button_entry2 = tk.Button(gui, text="Block window", bg='skyblue', fg='black', font=("Arial", 15), command=lambda:window_thread(entry2.get()))
    button_entry2.pack()
    
    tk.Label(gui, text="\n", bg='skyblue').pack()
    tk.Button(gui, text="Exit", bg='skyblue', fg='black', font=("Arial", 15), command=stop).pack()
    gui.mainloop()


if __name__ == '__main__':
    gui()


#flush dns cache -> ipconfig /flushdns
    
