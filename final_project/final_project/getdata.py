import time
import serial, sqlite3
linkDB = "/home/pi/Desktop/final_project/final_project/db.sqlite3"
ser = serial.Serial(
    port = '/dev/ttyAMA0',
    baudrate = 9600,
    parity = serial.PARITY_NONE,
    stopbits = serial.STOPBITS_ONE,
    bytesize = serial.EIGHTBITS,
    timeout = 1
)
def connectDB(linkDB):
    con     = sqlite3.connect(linkDB)
    c       = con.cursor()
    c.execute(''' SELECT IDNODE FROM MANAGE_ENDNODE  ''')
    row_data = c.fetchall()
    c.close()
    return row_data

def getNameEndnode(list_endnode):
    LIST_RLACS = []
    LIST_RLTDS = []
    LIST_THL = []
    
    for i in list_endnode:
        print(i[0][:len(i[0])-2])
        if i[0][:len(i[0])-2] == 'RLACS':
            LIST_RLACS.append(i[0])
        elif i[0][:len(i[0])-2] == 'RLTDS':
            LIST_RLTDS.append(i[0])
        elif i[0][:len(i[0])-2] == 'THL':
            LIST_THL.append(i[0])
    return LIST_RLACS, LIST_RLTDS, LIST_THL

def getDataRLACS(RLACS):
    rlacs_data = []
    for i in RLACS:
        str_getdata = "{}_GETDATA\n".format(i)
        bytes_getdata = str.encode(str_)
        ser.write(bytes_getdata)
        ser.flush()
        time.sleep(3)
        try:
            s = ser.readline()
            data = s.decode()
            data = data.rstrip()
            print(data)
            rlacs_data.append([i,data])
        except:
            rlacs_data.append([i,'Not connect'])
    return rlacs_data
def getDataRLTDS(RLTDS):
    rltds_data = []
    for i in RLTDS:
        str_getdata = "{}_GETDATA\n".format(i)
        bytes_getdata = str.encode(str_)
        ser.write(bytes_getdata)
        ser.flush()
        time.sleep(3)
        try:
            s = ser.readline()
            data = s.decode()
            data = data.rstrip()
            print(data)
            rltds_data.append([i,data])
        except:
            rltds_data.append([i,'Not connect'])
    return rltds_data
def getDataTHL(THL):
    thl_data = []
    for i in RLTDS:
        str_getdata = "{}_GETDATA\n".format(i)
        bytes_getdata = str.encode(str_)
        ser.write(bytes_getdata)
        ser.flush()
        time.sleep(3)
        try:
            s = ser.readline()
            data = s.decode()
            data = data.rstrip()
            print(data)
            thl_data.append([i,data])
        except:
            thl_data.append([i,'Not connect'])

        return thl_data
endnode = connectDB(linkDB)
print(endnode)

rlacs, rltds, thl = getNameEndnode(endnode)
print(rlacs, rltds, thl)

data_rlacs = getDataRLACS(rlacs)
data_rltds = getDataRLTDS(rltds)
data_thl = getDataTHLthl)
print(data_rlacs)
print(data_rltds)
print(data_thl)

    
    


