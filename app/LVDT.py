import sys,os
import curses
import keyboard
import time

import serial.tools.list_ports

hardware_id = '10C4:EA60'

width = 0
con = False
con_dic = {True:'CONNECTED',False:'DISCONNECTED'}

state = 0
states = {'STOPPED':0,'RECORDING':1,'DOWNLOADING':2}
states_name = {0:'STOPPED',1:'RECORDING',2:'DOWNLOADING'}
last_action = 0

def scan_COM(p=True,d=True,id=True):
    global con
    devices = []
    ports = serial.tools.list_ports.comports()
    for port, desc, hwid in sorted(ports):
        if hardware_id in hwid:
            con = True
        else:
            con = False
        if not p: port = ''
        if not d: desc = ''
        if not id: hwid = ''
        devices.append("{}{}{}".format(port, desc, hwid))
    return devices

def center_str(str):
    global width
    return int((width // 2) - (len(str) // 2) - len(str) % 2)


def cmd_enter(stdscr):
    global state
    if state == states['STOPPED']:
        state = states['DOWNLOADING']
        refresh_screen(stdscr)
        # send the desired command
        # wait until download is finished
        time.sleep(2)
        state = states['STOPPED']
    slow_reset()

def cmd_space(stdscr):
    global state
    slow_reset()
    if state == states['STOPPED']:
        state = states['RECORDING']
        refresh_screen(stdscr)
        # send the desired command
    elif state == states['RECORDING']:
        state = states['STOPPED']
        refresh_screen(stdscr)
        # send the desired command
    elif state == states['DOWNLOADING']:
        pass


def slow():
    global last_action
    return last_action < time.time()*1000 - 500

def slow_reset():
    global last_action
    last_action = time.time()*1000

def refresh_screen(stdscr):
    global width
    global state
    global con

    # Initialization
    stdscr.clear()
    height, width = stdscr.getmaxyx()

    # Declaration of strings
    title = "--- High Precision LVDT Control ---"[:width-1]
    control1 = "Spacebar | to Start / Stop recording   "[:width-1]
    control2 = "Enter | to Download the .txt file"[:width-1]
    status = con_dic[con]
    statusbarstr = "Press 'ESC' to exit | "
    authorstr = "| https://github.com/Sven-J-Steinert/HighPrecisionLVDT"

    # Centering calculations
    start_x_title = center_str(title)
    start_y = 1 # int((height // 2) - 2)


    # Turning on attributes for title
    stdscr.attron(curses.A_BOLD)

    # Rendering title
    stdscr.addstr(start_y, start_x_title, title, curses.color_pair(1))
    # Logo
    stdscr.addstr(start_y+2, (width // 2) - 14, '████ █████', curses.color_pair(1))
    stdscr.addstr(start_y+3, (width // 2) - 14, ' █ █ █ █ █', curses.color_pair(1))
    stdscr.addstr(start_y+4, (width // 2) - 14, ' █ ███ █ █', curses.color_pair(1))
    

    # Turning off attributes for title
    stdscr.attroff(curses.A_BOLD)

    # Print rest of text
    stdscr.addstr(start_y + 6, center_str(control1), control1)
    stdscr.addstr(start_y + 7, center_str(control2), control2)
    if con: color_code = 4
    else: color_code = 2
    stdscr.addstr(start_y + 2, (width // 2), '┌───────────────┐',curses.color_pair(color_code))
    stdscr.addstr(start_y + 3, (width // 2), '│               │',curses.color_pair(color_code))
    stdscr.addstr(start_y + 4, (width // 2), '└───────────────┘',curses.color_pair(color_code))
    stdscr.addstr(start_y + 3, center_str(status) +9, status, curses.color_pair(color_code))
    
    

    stdscr.addstr(start_y + 9, (width // 2) - 6, '-' * 11)
    if state == states['RECORDING']: color_code = 5
    else: color_code = 6
    if not con:
        stdscr.addstr(start_y + 10, center_str('N/A'), 'N/A')
    else:
        stdscr.addstr(start_y + 10, center_str(states_name[state]), states_name[state],curses.color_pair(color_code))
    stdscr.addstr(start_y + 11, (width // 2) - 6, '-' * 11)

    # COM Port listing
    devices = scan_COM(p=True,d=False,id=False)
    for i, value in enumerate(devices):
        stdscr.addstr(start_y + i+13, center_str(value), value)


    # Render footer
    stdscr.attron(curses.color_pair(3))
    stdscr.addstr(height-1, 0, statusbarstr)
    stdscr.addstr(height-1, len(statusbarstr), " " * (width - len(statusbarstr) - 1))
    stdscr.addstr(height-1, int(width-len(authorstr)-2), authorstr)
    stdscr.attroff(curses.color_pair(3))

    # Refresh the screen
    stdscr.refresh()

def draw_menu(stdscr):
    
    global width
    global state

    # Clear and refresh the screen for a blank canvas
    stdscr.clear()
    stdscr.refresh()

    # Start colors in curses
    curses.start_color()
    curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_YELLOW, curses.COLOR_BLACK)
   
    # Main Loop
    while True:
        global con

        if con:
            if keyboard.is_pressed('space') and slow():
                cmd_space(stdscr)
            elif keyboard.is_pressed('enter') and slow():
                cmd_enter(stdscr)
        if keyboard.is_pressed('ESC'):
            exit(0)
        refresh_screen(stdscr)
        time.sleep(0.01)
        # creates some CPU load but necessary for COM realtime detection


def main():
    curses.wrapper(draw_menu)

if __name__ == "__main__":
    main()
