import time

# The explainer states this program will demonstrate how persistent recursive calls can lead to a stack overflow.

# Times we have encountered the maximum recursion depth.
timesExcept = 0

try:
    # Wait for user input before starting the crash.
    input('Press ENTER to start the recursion or CTRL+C to exit.')
    print('This program will demonstrate a stack overflow in 3 seconds. You still have time to abort (see above)')
    time.sleep(3)
except KeyboardInterrupt:
    # Graceful shutdown on user interruption.
    print("Interrupted. Exiting now...")
    exit(0)

# Informative print before starting the crashing process.
print('Starting the recursive loop now')

# Function to recursively call itself until stack overflow occurs.
def loop():
    loop()  # This line will lead to RecursionError.

# Function that allows the program to restart instead of terminating on RecursionError.
def realloop():  # Manage RecursionError handling.
    try:
        loop()  # Begin the recursive loop.
    except RecursionError:
        # This block executes after hitting the maximum recursion depth, instead of crashing.
        print('Encountered recursion depth error. This has happened ' + str(timesExcept) + ' times.')
        timesExcept += 1  # Increment our exception count.
        realloop()  # Restart the recursive loop after handling the exception.

# Start the recursive crashing loop for the first time.
realloop()
# This line will ideally never be reached unless the crashing loop is somehow stopped.
print('The program should continue to demonstrate a stack overflow')