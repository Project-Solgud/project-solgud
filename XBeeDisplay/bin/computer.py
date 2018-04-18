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
        count = 0
        packetData = ser.read() # TODO packet size
        if sensorData = 0xfd: # TODO start byte
            start = True
        if sensorData = 0xf0:
            count++
        if count > 16:
            print(str(ord(sensorData)) + " ")
            imgFile.write(sensorData)
        if start:
            frame_bytes.append(sensorData)
        if sensorData = 0xfe: # TODO end byte
            break

        writer.writerow(parse_frame(frame_bytes))
        csvfile.flush()
        ser.write('0')
        ser.write(data)
