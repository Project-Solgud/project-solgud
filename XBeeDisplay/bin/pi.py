import glob
import os
import serial
import csv

def parse_frame(frame_bytes): # TODO parse data from the arduino
    toBeReturned = [];



if __name__ == "__main__":
    port = "/dev/ttyACM0" # TODO port
    ser = serial.Serial(port, timeout=1)
    ser.flushInput()

    csvfile = open('origData.csv', 'a')
    writer = csv.writer(csvfile, delimiter=',')

    while True:
        list_of_files = glob.glob('/home/pi/camera/*') # TODO compress in folder
        latest_file = max(list_of_files, key=os.path.getctime)
        photo = open(latest_file, 'rb')
        ser.reset_input_buffer()
        ser.write('1'.encode())
        ser.write(photo.read(150))
        data = photo.read(150)
        while data:
            frame_bytes = bytearray(b'')
            start = False
            while True:
                sensorData = ser.read() # TODO packet size
                try:
                    print(str(ord(sensorData)) + " ")
                except TypeError:
                    pass
                if ord(sensorData) == 0xfd: # TODO start byte
                    start = True
                if start:
                    frame_bytes.append(ord(sensorData))
                if ord(sensorData) == 0xfe: # TODO end byte
                    break

            # writer.writerow(parse_frame(frame_bytes))
            # csvfile.flush()
            ser.write(b'0')
            ser.write(data)
            data = photo.read(150)
        break
