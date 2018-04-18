import glob
import os
import serial
import csv

def parse_frame(frame_bytes): # TODO parse data from the arduino
    toBeReturned = [];

if __name__ == "__main__":
    port = "" # TODO port
    ser = serial.Serial(port, timeout=1)
    ser.flushInput()

    id = 0

    csvfile = open('origData.csv', 'a')
    writer = csv.writer(csvfile, delimiter=',')

    imgFile = open(str(id) + ".jpg", 'a')

    frame_bytes = bytearray(b'')

    while True:
        packetData = ser.read() # TODO packet size
        if sensorData = 0xff: # TODO start byte
            start = True
        if start:
            frame_bytes.append(sensorData)
        if sensorData = 0xe0: # TODO end byte
            break

        writer.writerow(parse_frame(frame_bytes))
        csvfile.flush()
        ser.write('0')
        ser.write(data)
