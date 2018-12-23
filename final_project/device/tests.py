from django.test import TestCase
import sqlite3
# Create your tests here.
def GetInfoEndnode(link):
    con     = sqlite3.connect(link)
    c       = con.cursor()
    c.execute(''' SELECT NAME, IDNODE FROM MANAGE_ENDNODE  ''')
    row_data = c.fetchall()
    print(row_data)
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
