import time
import serial
 
ser = serial.Serial(
    port = '/dev/ttyAMA0',
    baudrate = 9600,
    parity = serial.PARITY_NONE,
    stopbits = serial.STOPBITS_ONE,
    bytesize = serial.EIGHTBITS,
    timeout = 4
)
 
print("Raspberry's receiving : ")
 
try:
    while True:
                    # print string
        ser.write(b'RLTDS27_GETDATA\n')
        ser.flush()
        time.sleep(1)
        s = ser.readline()
        data = s.decode()           # decode s
        data = data.rstrip()            # cut "\r\n" at last of string
        print(data) 
 
except KeyboardInterrupt:
    ser.close()


 
