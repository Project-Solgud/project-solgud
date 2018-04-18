import glob
import os
import serial
import csv

def parse_frame(frame_bytes): # TODO parse data from the arduino
    toBeReturned = [];

if __name__ == "__main__":
    port = "/dev/ttyACM1" # TODO port
    ser = serial.Serial(port, timeout=1)
    ser.flushInput()

    id = 0

    csvfile = open('origData.csv', 'a')
    writer = csv.writer(csvfile, delimiter=',')

    imgFile = open(str(id) + ".jpg", 'ab')

    frame_bytes = bytearray(b'')

    while True:
        count = 0
        start = False
        while True:
            sensorData = ser.read() # TODO packet size
            if sensorData == b'':
                continue
            if ord(sensorData) == 253: # TODO start byte
                start = True
            if count >= 15:
                print(str(ord(sensorData)) + " ")
                imgFile.write(sensorData)
            if ord(sensorData) == 240:
                count += 1
                print(count)
            if start:
                frame_bytes.append(ord(sensorData))
            if ord(sensorData) == 254: # TODO end byte
                break

        # writer.writerow(parse_frame(frame_bytes))
        # csvfile.flush()
