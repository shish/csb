"""
Various library functions which are useful in curses programming

Taken from the ContextShift control panel (contextshift.net)
"""

import os
import curses
import curses.textpad

def curs_set(visibility):
    """
    Try to set the cursor visibility, and ignore any errors.

    (Errors happen under eg xterm-color, and can be safely ignored)
    """
    try:
        return curses.curs_set(visibility)
    except curses.error:
        return 1


def get_string(stdscr, prompt, maxlen=46):
    """
    Prompt for a string
    """
    (h, w) = stdscr.getmaxyx()
    win = curses.newwin(3, maxlen+4, (h-3)/2, (w-(maxlen+4))/2)
    draw_border(win, prompt)
    win.refresh()

    curses.echo()
    curs_set(2)
    string = win.getstr(1, 2, maxlen)
    curs_set(0)
    curses.noecho()

    return string


def get_text(stdscr, prompt, bw=70, bh=15):
    """
    Prompt for a large amount of text
    """
    (h, w) = stdscr.getmaxyx()
    win = curses.newwin(bh, bw, (h-bh)/2, (w-bw)/2)
    draw_border(win, prompt + " (Ctrl-G to finish)")
    win.refresh()

    editwin = curses.newwin(bh-2, bw-4, (h-bh)/2+1, (w-bw)/2+2)
    editwin.refresh()
    tb = curses.textpad.Textbox(editwin)
    curs_set(2)
    string = tb.edit()
    curs_set(0)

    return string


def confirm(stdscr, message):
    """
    Present a yes / no question, return true if the user presses y or false otherwise
    """
    if type(message) in (str, unicode):
        message = [message, ]
    (h, w) = stdscr.getmaxyx()
    width = max(map(len, message))+4
    height = 2+len(message)
    win = curses.newwin(height, width, (h-height)/2, (w-width)/2)
    draw_border(win, "Confirm")
    for n, line in enumerate(message):
        win.addstr(n+1, 2, line)
    win.addstr(height-1, width-7, " Y/N ")
    win.refresh()
    return (win.getch() in [ord('y'), ord('Y')])


def alert(stdscr, title, message):
    """
    Show an informational dialogue and wait for the user to say ok before continuing
    """
    if type(message) in (str, unicode):
        message = [message, ]
    (h, w) = stdscr.getmaxyx()
    pak = " Press any key to continue "
    width = max(max(map(len, message)), len(pak)) + 4
    height = 2+len(message)
    if width > w: width = w
    if height > h: height = h
    win = curses.newwin(height, width, (h-height)/2, (w-width)/2)
    draw_border(win, title)
    for n, line in enumerate(message[0:h-2]):
        win.addstr(n+1, 2, line[0:w-4])
    win.addstr(height-1, width-len(pak)-2, pak)
    win.refresh()
    return win.getch()


def submenu(stdscr, title, options):
    """
    Show a list of options, return the key which is pressed (the options
    should probably include some indication of which key is associated
    with which option...)
    """
    (h, w) = stdscr.getmaxyx()
    height = len(options) + 2
    width = max(map(len, options)) + 4
    win = curses.newwin(height, width, (h-height)/2, (w-width)/2)
    draw_border(win, title)
    for n in range(0, len(options)):
        win.addstr(n+1, 2, options[n])
    win.refresh()
    return win.getch()


def progress(stdscr, title, message):
    """
    Show an informational dialogue and continue running in the background
    """
    (h, w) = stdscr.getmaxyx()
    width = len(message) + 4
    curs_set(0)
    win = curses.newwin(3, width, (h-5)/2, (w-width)/2)
    draw_border(win, title)
    win.addstr(1, 2, message)
    win.refresh()


def draw_border(win, title=None):
    """
    Draw a border around a curses window, taking care to avoid using
    drawing characters on terminals which don't support them
    """
    if os.environ["TERM"] in ["xterm", "xterm-color"]:
        win.border()
    else:
        win.border('|', '|', '-', '-', '+', '+', '+', '+')
    if title:
        win.addstr(0, 2, " %s " % title)


def set_title(string):
    """
    Set the title of the terminal emulator, if supported
    """
    if os.environ["TERM"] in ["xterm", "xterm-color"]:
        print ("\033]2;%s\a" % (string, ))


def draw_base(stdscr, username):
    """
    Draw a simple header and footer
    """
    (h, w) = stdscr.getmaxyx()

    header = curses.newwin(1, w, 0, 0)
    header.bkgd(" ", curses.A_REVERSE)
    string = "User: %s" % username
    header.addstr(0, 2, "Contextshift Control Panel")
    header.addstr(0, max(0, w-2-len(string)), string)
    header.refresh()

    footer = curses.newwin(1, w, h-1, 0)
    footer.bkgd(" ", curses.A_REVERSE)
    footer.addnstr(0, 2, "Connection to database: OK", w-1)
    footer.refresh()

    return footer


def choose_option(stdscr, title, options):
    """
    Present the user with a list of options, return the index number
    of the one selected
    """
    option = 0
    option_count = len(options)
    text_width = max(max(map(len, options)), len(title)) + 6

    while True:
        #csui.draw_base(stdscr, self.session.user)

        (height, width) = stdscr.getmaxyx()
        win = curses.newwin(option_count+2, text_width, (height-(option_count+2))/2, (width-text_width)/2)
        draw_border(win, title)
        win.refresh()

        for n in range(0, option_count):
            win.addstr(1 + option, 2, "*")
            win.addstr(1 + n, 4, options[n])

        win.keypad(1)
        key = win.getch()
        if key == curses.KEY_UP:
            option = option - 1
        elif key == curses.KEY_DOWN:
            option = option + 1
        elif key in [10, curses.KEY_ENTER, ord(' ')]:
            break

        if option < 0:
            option = 0
        elif option > option_count-1:
            option = option_count-1

    return option

