####
# David Parker
# 2017
# Screen Capture script
#
# Usage: Run script then hold CTRL anywhere on screen to drag a box around desired screen capture area.
#
# TODO: Change box to inverted colors to allow erasing of lines on screen
# TODO: Create another GUI to save image to desired location

import win32gui
import win32api
import win32con
from ctypes import windll
from time import sleep
from PIL import ImageGrab, ImageTk, Image, ImageChops, ImageOps
import Tkinter as Tk


####
# grab_screen()
# Purpose: Save a PIL image of the appropriate area of the screen
# Arguments: None
# Returns: PIL image
####
def grab_screen():
    while True:                                                         # Loop until return
        cursor_current_x, cursor_current_y = 0, 0                       # Declare variable for future cursor
        crop_im = False                                                 # Declare boolean for cropping later

        win_DC = win32gui.GetDC(0)                                      # Get device context
        cursor_origin_x, cursor_origin_y = win32gui.GetCursorPos()      # Get cursor position
        full_image = ImageGrab.grab(bbox=(0,                            # Capture entire screen
                                          0,
                                          win32api.GetSystemMetrics(0),
                                          win32api.GetSystemMetrics(1)))

        while win32api.GetAsyncKeyState(win32con.VK_CONTROL) < 0:       # While CTRL key is pressed
            if not crop_im:
                crop_im = True                                          # Set crop bool so crop branch is entered after

            cursor_current_x, cursor_current_y = win32gui.GetCursorPos()  # Get current cursor position
            win32gui.MoveToEx(win_DC, cursor_origin_x, cursor_origin_y)   # Draw a box with original cursor
            win32gui.LineTo(win_DC, cursor_origin_x, cursor_current_y)    # and current cursor as opposite corners
            win32gui.MoveToEx(win_DC, cursor_origin_x, cursor_current_y)
            win32gui.LineTo(win_DC, cursor_current_x, cursor_current_y)
            win32gui.MoveToEx(win_DC, cursor_current_x, cursor_current_y)
            win32gui.LineTo(win_DC, cursor_current_x, cursor_origin_y)
            win32gui.MoveToEx(win_DC, cursor_current_x, cursor_origin_y)
            win32gui.LineTo(win_DC, cursor_origin_x, cursor_origin_y)

        if crop_im:                                                     # Enter crop branch, crop to box size
            cropped_image = full_image.crop((min(cursor_current_x, cursor_origin_x),
                                             min(cursor_current_y, cursor_origin_y),
                                             max(cursor_current_x, cursor_origin_x),
                                             max(cursor_current_y, cursor_origin_y)))
            return cropped_image                                        # RETURN: cropped image
        sleep(.01)                                                      # Sleep so it doesn't waste resources


####
# prompt_image(im)
# Purpose: Displays GUI with PIL Image allowing user to approve of captured image
# Arguments: PIL image (im)
# Returns: integer
####
def prompt_image(im):
    width, height = im.size                                 # Get width and height of image
    window = Tk.Tk()                                        # Initialize Tkinter window and dimensions
    window.title("")
    window.geometry(str(width) + 'x' + str(height))
    window.configure(background='grey')

    # Creates a Tkinter-compatible photo image, which can be used everywhere Tkinter expects an image object.
    img = ImageTk.PhotoImage(im)

    # The Label widget is a standard Tkinter widget used to display a text or image on the screen.
    panel = Tk.Label(window, image=img)

    # The Pack geometry manager packs widgets in rows or columns.
    panel.pack(side="bottom", fill="both", expand="yes")

    # Start the GUI
    window.lift()
    window.attributes('-topmost', True)
    window.after_idle(window.attributes, '-topmost', False)
    window.update()
    ret = windll.user32.MessageBoxA(window.winfo_id(),      # Prompt user to verify image
                                    "Use this picture?",
                                    "",
                                    6)
    window.destroy()
    return ret                                              # RETURN: MessageBox prompt returned value


#####################################
#
#   Main
#
#####################################
if __name__ == '__main__':
    condition, process = True, True                         # Declare Booleans outside of loop
    image = None                                            # Declare variable for image
    while condition:
        image = grab_screen()                               # CALL: grab_screen() and store image
        reply_continue, reply_try_again = 11, 10            # Store variables corresponding to later GUI button feedback
        selection = prompt_image(image)                     # CALL: prompt_image() and store GUI button pressed
        process = selection == reply_continue               # If continue, process = True
        condition = selection == reply_try_again            # If try again, condition = True (loop again)
    if process:
        print 'Yes'
