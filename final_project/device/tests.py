from django.test import TestCase
import sqlite3
# Create your tests here.
def GetInfoEndnode(link):

    con     = sqlite3.connect(link)
    c       = con.cursor()
    c.execute(''' SELECT NAME, IDNODE FROM MANAGE_ENDNODE  ''')
    row_data = c.fetchall()
#     print(row_data)
    c.close()

    data = {}
    RLACS = []
    RLTDS = []
    THL_SENSOR = []
    for i in row_data:
        if i[0] == 'RLACS': RLACS.append(i[1])
        elif i[0] == 'RLTDS': RLTDS.append(i[1])
        elif i[0] == 'THL_SENSOR' : THL_SENSOR.append(i[1])
    data = {'RLACS' : RLACS,
            'RLTDS' : RLTDS,
            'THL_SENSOR' : THL_SENSOR,
    }
    print(data)
    return data

def AddEndNode_(link, name, idnode):
    con     = sqlite3.connect(link)
    c       = con.cursor()
    ORDER_QUERY = ''' INSERT INTO MANAGE_ENDNODE(NAME, IDNODE) VALUES (?, ?);  '''
    c.execute(ORDER_QUERY, (name, idnode))
    con.commit()
    c.close()

def DeleteEndNode_(link, name, idnode):
    con     = sqlite3.connect(link)
    c       = con.cursor()
    ORDER_QUERY = ''' DELETE FROM MANAGE_ENDNODE WHERE IDNODE=?;  '''
    c.execute(ORDER_QUERY, (idnode,))
    con.commit()
    c.close()

def CheckIDNode(typenode, idnode):
    RLACS_id = ["RLACS%.2d" % i for i in range(100)]
    RLTDS_id = ["RLTDS%.2d" % i for i in range(100)]
    THL_SENSOR_id = ["THL%.2d" % i for i in range(100)]
    if typenode == 'RLACS':
        if idnode in RLACS_id:
            return True
        else:
            return False
    elif typenode ==  'RLTDS':
        if idnode in RLTDS_id:
            return True
        else:
            return False
    elif typenode == 'THL_SENSOR':
        if idnode in THL_SENSOR_id:
            return True
        else:
            return False
    else:
        return False
def CheckExist(link, idnode):
    con     = sqlite3.connect(link)
    c       = con.cursor()
    c.execute(''' SELECT IDNODE FROM MANAGE_ENDNODE  ''')
    row_data = c.fetchall()
    c.close()
    data    = [i[0] for i in row_data]
    if idnode in data:
        return True
    else:
        return False

def getdataCMpage(link):
    con     = sqlite3.connect(link)
    c       = con.cursor()
    c.execute(''' SELECT IDNODE,D1,A1,D2,A2 FROM RLACS  ''')
    data_RLACS = c.fetchall()
    c.execute(''' SELECT IDNODE,D,TDS FROM RLTDS  ''')
    data_RLTDS = c.fetchall()
    c.execute(''' SELECT IDNODE,T,H,L FROM THL_SENSOR  ''')
    data_THL = c.fetchall()
    c.close()
    data = {'RLACS' : data_RLACS,
            'RLTDS' : data_RLTDS,
            'THL'   : data_THL,}
    return data
    
def ControlRELAY(link, ORDER_QUERY):
    con     = sqlite3.connect(link)
    c       = con.cursor()
    c.execute(ORDER_QUERY)
    con.commit()
    c.close()
    # Gui lenh dieu khien relay qua lora

