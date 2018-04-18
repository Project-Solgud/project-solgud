import csv
import serial
import time

current_milli_time = lambda: time.time()*1000

"""
    Program continuously taking data from an XBee and saving it to a disk, where other programs can interact with it.
"""


def channel_name(n):
    """
        Convert channel bit number to its actual name
    """
    return {
        0: "na",
        1: "A5",
        2: "A4",
        3: "A3",
        4: "A2",
        5: "A1",
        6: "A0",
        7: "D8",
        8: "D7",
        9: "D6",
        10: "D5",
        11: "D4",
        12: "D3",
        13: "D2",
        14: "D1",
        15: "D0",
    }.get(n, "na")


def parse_frame(private_frame):
    """
        Parses one frame of hex data from the XBee into a dictionary.

        Frames have a very specific format specified by the API linked here:
        https://www.sparkfun.com/datasheets/Wireless/Zigbee/XBee-Datasheet.pdf

        Pages 13, 14, 57, and 63 are particularly useful to understand this format.
        This code assumes 0x83 is the packet received on only analog channels.

        Returns negative integers if basic API checksums fail
        Behavior is unpredictable if the packet type is not 0x83
    """

    # TODO change code to be dynamic based on packet type
    frame_bytes = private_frame.split(" ")

    # ensures the length of the packet received is the same as the length specified in the packet
    if int(frame_bytes[2], 16) - int(frame_bytes[1], 16) != len(frame_bytes) - 4:
        return -2

    # runs checksum
    total = 0
    for a in range(3, len(frame_bytes)):
        total += int(frame_bytes[a], 16)
    if total % 256 != 255:
        return -1

    # initial declaration
    dict_frame = {"address": frame_bytes[4] + " " + frame_bytes[5], "startDelimit": frame_bytes[0],
                  "dataLength": len(frame_bytes) - 4, "type": frame_bytes[3],
                  "signalStrength": "-" + str(int(frame_bytes[6], 16)) + " dBm", "options": frame_bytes[7]}

    # most packets contain multiple samples (5 seems to be default)
    num_samples = int(frame_bytes[8], 16)
    dict_frame["numSamples"] = str(num_samples)

    # converts channel bytes into binary and looks at each bit to determine which channels are being sent
    first_channels = bin(int(frame_bytes[9], 16))[2:].zfill(8)
    second_channels = bin(int(frame_bytes[10], 16))[2:].zfill(8)
    channels_open = []
    for a in range(0, 8):
        if first_channels[a] == '1':
            channels_open.append(channel_name(a))
        if second_channels[a] == '1':
            channels_open.append(channel_name(a + 8))

    # TODO allow for processing of digital channels as well
    measurements = {}
    for itr in range(0, num_samples):
        sample_measurements = {}
        for j in range(0, len(channels_open)):
            # each measurement consists of two bytes, which must be recombined into one decimal number
            byte1 = frame_bytes[11 + 2 * itr * len(channels_open) + j * 2]
            byte2 = frame_bytes[11 + 2 * itr * len(channels_open) + j * 2 + 1]
            byte1 = bin(int(byte1, 16))[2:].zfill(8)
            byte2 = bin(int(byte2, 16))[2:].zfill(8)
            sample_measurements[channels_open[j]] = int(byte1 + byte2, 2)
        measurements[str(itr)] = sample_measurements

    # finalizes dict_frame and returns
    dict_frame["channelsOpen"] = channels_open
    dict_frame["measurements"] = measurements
    dict_frame["checkSum"] = frame_bytes[len(frame_bytes) - 1]
    return dict_frame


"""
    This code opens the XBee on COM7 and reads one byte at a time until it hits the start delimiter
    byte "7E" (decimal 126) at which point it attempts to parse everything it has in its buffer so far
    before clearing the buffer.

    It writes its info (including packet number, address, and signal strength as well as its data) to a CSV.
    Other applications should make a copy of this whenever they want to interact with the data/whenever they
    want to refresh their data as the file may have a write lock on it.
"""

if __name__ == "__main__":
    # open the serial port
    port = ""
    with open("bin/workfile.txt", "r") as f:
        port  = f.read()
    ser = serial.Serial(port, timeout=1)
    ser.flushInput()
    frameBuffer = "7e"
    data = [[], [], [], [], []]
    packet = 0
    with open('origData.csv', 'a') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        # TODO make dynamic column headers
        while True:
            try:
                # reads a byte and converts it to an int
                char = ser.read(1)
                charInt = char[0]
                print(charInt)
                # TODO make dynamic start delimiter an option
                # checks for the start delimiter, parsing and saving the data
                if charInt == 126:
                    # parse the frame and clear the buffer
                    frame = parse_frame(frameBuffer)
                    print(frameBuffer)
                    frameBuffer = "7e"
                    # as long as there were no parsing errors, we write the data
                    if not (type(frame) is int):
                        # assumes packet is recieved about the same time it is transmitted
                        toBeWritten = [current_milli_time(), frame["address"], frame["signalStrength"]]

                        # writes each sample separately
                        for i in range(0, int(frame["numSamples"])):
                            writer.writerow(toBeWritten + [v for v in frame["measurements"][str(i)].values()])
                            print(toBeWritten)
                        packet += 1

                        # this line is KEY! it makes sure that the data gets sent to the display in "real-time"
                        csvfile.flush()
                else:
                    # just add the next byte to the buffer after a space
                    frameBuffer += " "
                    frameBuffer += hex(charInt)[2:].zfill(2)
            except IndexError:
                pass
