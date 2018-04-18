import os
import threading
import time

import sys
import glob
import serial

print("please wait")

def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

# gets serial ports and queries user for the action to be taken
x = serial_ports()
if(len(x) < 1):
    raise EnvironmentError('no USB devices connected')
print(x)
indx = input("Input the index (from zero) of the COM port to which the XBee is connected in the array above. ")
indx = int(indx)

# passes in the name of the COM array to the script files
with open('bin/workfile.txt', 'w+') as f:
    f.write(x[indx])

class myThread (threading.Thread):
    """
    Class of thread allowing the initialization of either the reciever or the display, depending on the counter.
    """
   def __init__(self, threadID, name, counter):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.counter = counter
   def run(self):
      if self.counter == 1:
          os.system('python bin/xbee.py')
      elif self.counter == 2:
          os.system('python bin/displayTabbed.py')

threads = []

# Create new threads
thread1 = myThread(1, "Thread-Receive", 1)
thread2 = myThread(2, "Thread-Display", 2)

# Start new Threads
thread1.start()
thread2.start()

# Add threads to thread list
threads.append(thread1)
threads.append(thread2)

# Wait for all threads to complete
for t in threads:
    t.join()

print("To close the program, close the data window and hit Ctrl-C")

while 1:
    pass
