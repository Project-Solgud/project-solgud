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

    csvfile = open('origData.csv', 'a')
    writer = csv.writer(csvfile, delimiter=',')

    while True:
        list_of_files = glob.glob('/home/pi/camera/*') # TODO compress in folder
        latest_file = max(list_of_files, key=os.path.getctime)
        photo = open(latest_file, 'rb')
        ser.write('1')
        ser.write(f.read(200))
        data = f.read(200)
        while data:
            frame_bytes = bytearray(b'')
            start = False
            while True:
                sensorData = ser.read() # TODO packet size
                print(str(int(sensorData)) + " ")
                if sensorData = 0xff: # TODO start byte
                    start = True
                if start:
                    frame_bytes.append(sensorData)
                if sensorData = 0xfe: # TODO end byte
                    break

            writer.writerow(parse_frame(frame_bytes))
            csvfile.flush()
            ser.write('0')
            ser.write(data)
            data = f.read(200)
