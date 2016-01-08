# RPiEOS

Take and serve pics from a Canon EOS 450D via Raspberry Pi.

Raspberry Pi GPIO xx -> shutter release
Raspberry Pi GPIO yy -> autofocus

# Working notes

* need to get simple UI sorted to take + serve the pics
* confirm we can connect to the camera via USB while it's still taking pics

# Python REPL session

    [sean@mokpo ~]$ sudo pip install RPi.GPIO
    [sean@mokpo ~]$ sudo python
    Python 2.7.9 (default, Mar  1 2015, 13:48:22) 
    [GCC 4.9.2] on linux2
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import RPi.GPIO as GPIO
    >>> GPIO.setmode(GPIO.BOARD)
    >>> GPIO.setup(12, GPIO.OUT)
    >>> import time
    >>> GPIO.output(12, GPIO.HIGH)
    >>> time.sleep(0.1)
    >>> GPIO.output(12, GPIO.LOW)

