MAX_EXCEPTIONS = 10  # The maximum number of allowed RecursionError occurrences

def realloop():
    global timesExcept
    try:
        loop()  # Begin the recursive loop.
    except RecursionError:
        print('Python tried to give an exception. This has happened ' + str(timesExcept) + ' times.')
        timesExcept += 1
        if timesExcept > MAX_EXCEPTIONS:
            print("Maximum recursion errors exceeded. Exiting.")
            exit(0)
        realloop()  # Restart the recursive crashing loop.

# Start the recursive crashing loop for the first time.
realloop()