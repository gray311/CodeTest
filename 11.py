def parse_startup_packet(packet_stream):
    """
    Processes startup packets by concatenating incoming packet data into a string buffer.

    :param packet_stream: An iterable of packet data (e.g., a list of strings or bytes).
    :return: A single string containing all concatenated packet data.
    """
    buffer = ""
    for packet in packet_stream:
        buffer += packet.decode('utf-8') if isinstance(packet, bytes) else packet
    return buffer

# Example usage:
packets = [
    b"STARTUP_SEQUENCE_1_",
    "CONTINUATION_2_",
    b"DATA_3_",
    "FINAL_PART_4"
]

result = parse_startup_packet(packets)
print(result)