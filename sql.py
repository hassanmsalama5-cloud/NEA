import sqlite3
con = sqlite3.connect('mydatabase.db')
cur = con.cursor()
cur.execute('''CREATE  TABLE employes 
            (empID INTEGER  NOT NULL PRIMARY KEY, 
            empName VARCHAR(20) NOT NULL,
             hireDate DATE NOT NULL,
             salary CURRENCY )
            ''')