import tkinter as tk
import tkinter.ttk as ttk
from vidstream import *
import threading as th
import ctypes as ct
import socket as soc

stop_threads = False

t1 = None
t2 = None
t3 = None
t4 = None
t5 = None

def discon_all():
    global stop_threads
    stop_threads = True

# getting local ip
def getLocalIPV4():
    local_ip_addres = soc.gethostbyname(soc.gethostname())
    return local_ip_addres

local_ip = getLocalIPV4()

# getting local IP for Streaming and Receiving
locIPV4 = soc.gethostbyname(soc.gethostname())
server = StreamingServer(locIPV4, 13333)
receiver = AudioReceiver(locIPV4, 16666)

# creating the listening, streaming and receiveing functions
def listen_init():
    global stop_threads, t1, t2
    stop_threads = False
    t1 = th.Thread(target=server.start_server)
    t2 = th.Thread(target=receiver.start_server)
    t1.start()
    t2.start()

def camstream_init():
    global stop_threads, t3
    stop_threads = False
    camera_client = CameraClient(TargetIPV4.get(1.0, 'end-1c'), 14444)
    t3 = th.Thread(target=camera_client.start_stream)
    t3.start()

def screenshare_init():
    global stop_threads, t4
    stop_threads = False
    screen_client = ScreenShareClient(TargetIPV4.get(1.0, 'end-1c'), 14444)
    t4 = th.Thread(target=screen_client.start_stream)
    t4.start()

def audiostream_init():
    global stop_threads, t5
    stop_threads = False
    audio_sender = AudioSender(TargetIPV4.get(1.0, 'end-1c'), 18888)
    t5 = th.Thread(target=audio_sender.start_stream)
    t5.start()

def discon_all():
    global t1, t2, t3, t4, t5, stop_threads
    stop_threads = True

    if t1 is not None:
        t1.join()
        t1 = None

    if t2 is not None:
        t2.join()
        t2 = None
    
    if t3 is not None:
        t3.join()
        t3 = None
    
    if t4 is not None:
        t4.join()
        t4 = None
    
    if t5 is not None:
        t5.join()
        t5 = None

    # Also stop and destroy the servers here if needed
    if server is not None:
        server.stop_server()
        t1 = None

    if receiver is not None:
        receiver.stop_server()
        receiver = None

# Define Window style via DWM (Desktop Windows Manager API)

def night_mode_title_bar(window):
    window.update()
    set_window_attribute = ct.windll.dwmapi.DwmSetWindowAttribute
    get_parent = ct.windll.user32.GetParent
    hwnd = get_parent(window.winfo_id())
    value = 2
    value = ct.c_int(value)
    set_window_attribute(hwnd, 20, ct.byref(value), 4)

# Updating the window's height dynamically every 1000 milliseconds
def winupdateheight():
    WINheight = winproc.winfo_height()
    userList.config(height=WINheight)
    winproc.after(1000, winupdateheight)

# start of main window loop
winproc = tk.Tk()

# Window properties
winproc.title('ViperWire')
winproc.geometry('1200x800')
winproc.minsize(1000, 600)
winproc.config(bg = '#13023e')

# Element style
sto = ttk.Style()

sto.theme_use('alt')
sto.configure('TButton', foreground='#0d012d', background='#440bdd', font = ('Arial', 10, 'underline'))
sto.map('TButton', background=[('active', '#2a0789')])

# Window elements
clientIP = tk.Label(winproc, text="Local IPV4: " + local_ip, font = ("Helvetica", 16), bg='#1f192f', borderwidth = 0.5)
TargetIPV4 = tk.Text(winproc, height = 1, width = 30)
userList = tk.Listbox(winproc, height = 600, width = 15, bg= '#08011c', activestyle = 'dotbox', font = "Helvetica", fg = "yellow", justify = 'right')
scrshr = ttk.Button(winproc, text="Share Screen", style='TButton', command=screenshare_init)
listn = ttk.Button(winproc, text="Listen", style='TButton', command=listen_init)
discon = ttk.Button(winproc, text="Disconnect", style='TButton', command=discon_all)
conn = ttk.Button(winproc, text="Connect", style='TButton', command=audiostream_init)
cam_init = ttk.Button(winproc, text="Camera", style='TButton', command=camstream_init)

# Packing and placing Elements
userList.pack(anchor = 'ne')
clientIP.place(anchor = 'nw')
discon.place(relx = 0.05, rely = 0.9)
conn.place(relx = 0.2, rely = 0.9)
listn.place(relx = 0.35, rely = 0.9)
scrshr.place(relx = 0.5, rely = 0.9)
cam_init.place(relx = 0.65, rely = 0.9)
TargetIPV4.place(relx = 0.0, rely = 0.05)


night_mode_title_bar(winproc)
winupdateheight()

# end of main loop for window
winproc.mainloop()