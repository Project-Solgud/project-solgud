This program was built against Python 3.6.1 and should be compatible with all other versions of Python 3,
although that has not been tested. Python should be in your path. To test this, open an instance of
Terminal and enter 'python'. If python responds, then this program should work.

This program requires:
* numpy
* PyQt5
* pyqtgraph
* pyserial

To install a certain package <package>, use:
'python -m pip install <package>' (Windows CMD)
'sudo pip install <package>' (Shell)

To run:
Change directory to the root of the zip file, which should contain this file as well as 'runXBee.py' and
the 'bin' folder. Then, run:

'python runXBee.py'

After a brief pause, the command should prompt you for your choice of serial port. Input the index of your
desired port. For example, if the command displays the array:

['COM1', 'COM2', 'COM3']

For 'COM1', you would input 0, for 'COM2' you would input 1, etc.

This program assumes that the XBee is configured to send packets of 5 samples from AD0, AD1, AD2, AD3,
and AD4 each at a rate of around one second per packet.

When the resistance measured is -1, that denotes that the resistance is too high to be measured.
When the resistance measured is -5 and the signal strength measured is 5, that denotes a discontinuity
in the data in terms of recording time.
