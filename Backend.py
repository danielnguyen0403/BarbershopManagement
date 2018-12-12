import sqlite3

class Database():
    """docstring for Database."""
    def __init__(self):
        super(Database, self).__init__()
        #connect database and CREATE tables
        self.conn=sqlite3.connect("barbershop.db")
        self.cur=self.conn.cursor()
        customer = """CREATE TABLE IF NOT EXISTS Customer(
                    cId INTEGER PRIMARY KEY,
                    name TEXT,
                    phone TEXT,
                    address TEXT,
                    visit INTEGER,
                    reward NUMERIC)"""
        self.cur.execute(customer)

        employee = """CREATE TABLE IF NOT EXISTS Employee(
                    eId INTEGER PRIMARY KEY,
                    name TEXT,
                    phone TEXT,
                    address TEXT,
                    salary INTEGER)"""
        self.cur.execute(employee)

        service = """CREATE TABLE IF NOT EXISTS Service(
                    sId INTEGER PRIMARY KEY,
                    name TEXT,
                    cost REAL,
                    duration INTEGER)"""
        self.cur.execute(service)

        choose = """CREATE TABLE IF NOT EXISTS Choose(
                    cId INTEGER,
                    sId INTEGER,
                    eId INTEGER,
                    date TEXT,
                    PRIMARY KEY(cId, sId, eId),
                    FOREIGN KEY(cId) REFERENCES Customer(cId) ON UPDATE CASCADE,
                    FOREIGN KEY(sId) REFERENCES Service(sId) ON UPDATE CASCADE,
                    FOREIGN KEY(eId) REFERENCES Employee(eId) ON UPDATE CASCADE)"""
        self.cur.execute(choose)

        ability = """CREATE TABLE IF NOT EXISTS Ability(
                    sId INTEGER,
                    eId INTEGER,
                    PRIMARY KEY(sId, eId),
                    FOREIGN KEY(sId) REFERENCES Service(sId) ON UPDATE CASCADE,
                    FOREIGN KEY(eId) REFERENCES Employee(eId) ON UPDATE CASCADE)"""
        self.cur.execute(ability)

        # Trigger for update visit in Customer table
        trigg = """CREATE TRIGGER IF NOT EXISTS updateReward
                AFTER UPDATE OF visits ON Customer
                FOR EACH ROW
                WHEN (NEW.visits > 9)
                BEGIN
                    UPDATE Customer
                    SET visit = 0 AND reward = reward+1
                    WHERE cId = NEW.cId;
                    END;"""
        self.cur.execute(trigg)
        self.conn.commit()


    def __del__(self):
        self.conn.close()

    #Cusomer table
    def insert_Customer(self,name,phone,address):
        query = """INSERT INTO Customer(name, phone, address, visit, reward)
                    VALUES (?,?,?,0,0)"""
        self.cur.execute(query,(name,phone,address))
        self.conn.commit()

    def view_Customer(self):
        self.cur.execute("SELECT * FROM Customer")
        rows = self.cur.fetchall()
        return rows

    def search_Customer(self,name="",phone="",address=""):
        self.cur.execute("SELECT * FROM Customer WHERE name=? OR phone=? OR address=?",(name,phone,address))
        rows = self.cur.fetchall()
        return rows

    def update_Customer(self,cId):
        self.cur.execute("UPDATE Customer SET visit=visit+1 WHERE cId=?",(cId))
        self.conn.commit()

    #Employee table
    def insert_Employee(self,name,phone,address,salary):
        self.cur.execute("INSERT INTO Employee (name, phone, address, salary) VALUES (?,?,?,?)",(name,phone,address,salary))
        self.conn.commit()

    def view_Employee(self):
        self.cur.execute("SELECT * FROM Employee")
        rows = self.cur.fetchall()
        return rows

    def search_Employee(self,name="",phone="",address="",salary=""):
        self.cur.execute("SELECT * FROM Employee WHERE name=? OR phone=? OR address=? OR salary=?",(name,phone,address,salary))
        rows = self.cur.fetchall()
        return rows

    def update_Employee(self,eId,phone,salary):
        self.cur.execute("UPDATE Employee SET phone=?, salary=? WHERE eId=?",(phone,salary,eId))
        self.conn.commit()


    def delete_Employee(self,eId):
        self.cur.execute("DELETE FROM Employee WHERE eId=?",(eId,))
        self.conn.commit()


    #Service table
    def insert_Service(self,name,cost,duration):
        self.cur.execute("INSERT INTO Service (name, cost, duration) VALUES (?,?,?)",(name,cost,duration))
        self.conn.commit()


    def view_Service(self):
        self.cur.execute("SELECT * FROM Service")
        rows = self.cur.fetchall()
        return rows

    def search_Service(self,sid="",name="",cost="",duration=""):
        self.cur.execute("SELECT * FROM Service WHERE sId=? OR name=? OR cost=? OR duration=?",(sid,name,cost,duration))
        rows = self.cur.fetchall()
        return rows

    def update_Service(self,sId,cost,duration):
        self.cur.execute("UPDATE Service SET cost=?, duration=? WHERE sId=?",(cost,duration,sId))
        self.conn.commit()

    def delete_Service(self,sId):
        self.cur.execute("DELETE FROM Service WHERE sId=?",(sId,))
        self.conn.commit()


    #Choose table
    def insert_Choose(self,cId,sId,eId,date):
        self.cur.execute("INSERT INTO Choose (cId,sId,eId,date) VALUES (?,?,?,?)",(cId,sId,eId,date))
        self.conn.commit()

    def view_Choose(self):
        self.cur.execute("SELECT * FROM Choose")
        rows = self.cur.fetchall()
        return rows

    def search_Choose(self,cId="",sId="",eId="",date=""):
        self.cur.execute("SELECT * FROM Choose WHERE cId=? OR sId=? OR eId=? OR date=?",(cId,sId,eId,date))
        rows = self.cur.fetchall()
        return rows

        #no update contents in Choose table
        #no delete contents in Choose table

    #Ability table
    def insert_Ability(self,sId, eId):
        self.cur.execute("INSERT INTO Ability (sId,eId) VALUES (?,?)",(sId,eId))
        self.conn.commit()

    def view_Ability(self):
        self.cur.execute("SELECT * FROM Ability")
        rows = self.cur.fetchall()
        return rows

    def delete_Employee(self,sId,eId):
        self.cur.execute("DELETE FROM Employee WHERE sId=? OR eId=?",(sId,eId,))
        self.conn.commit()

    def update_Ability(self):
        return 1

    # Show employees can work for a service sId
    def employeesListForAService(self,sId):
        self.cur.execute("SELECT e.name FROM Employee e, Ability a WHERE e.eId=a.eId AND a.sId=?",(sId,))
        rows = self.cur.fetchall()
        return rows


    #Select employees who knows all skills
    def empoyeesOfAllSkills(self):
        self.cur.execute("SELECT e.name FROM Employee e WHERE NOT EXISTS (SELECT s.sId FROM Service s EXCEPT SELECT a.sId FROM Ability a WHERE a.eId = e.eId)")
        rows = self.cur.fetchall()
        return rows

    #Select employee with the most number of service order
    # def mostNumberOfService(self):
    #     self.cur.execute("SELECT e.name FROM Employee e WHERE e.eId = (SELECT c.eId FROM Choose c GROUP BY c.eId HAVING COUNT(c.sId) >= ALL (SELECT COUNT(c1.sId) FROM Choose c1 GROUP BY c1.eId))")
    #     rows = self.cur.fetchall()
    #     return rows


# def drop():
#     conn=sqlite3.connect("barbershop.db")
#     cur=conn.cursor()
#     cur.execute("DROP TABLE Ability")
#     conn.commit()
#
# drop()

# insert_Customer("Chastity Daniels","(829)-819-0244","454-1296 Cursus St.",1,0)
# insert_Customer("Abraham Brooks","(945)-216-7073","288-8787 Gravida. Ave",2,1)

# insert_Employee("Angelina Person","(575)618-8314","94 Harrison St. ,Bolingbrook, IL 60440",12)
# insert_Employee("Iosif Farrow","(412)344-5218","9504 Lafayette Street,Dallas, GA 30132",16)
# insert_Employee("Mohamed Burton","(414)283-5738","29 Evergreen Drive, Perkasie, PA 18944",27)
# insert_Employee("Cecil Gardiner","(810)410-7035","246 Country Club Ave., Bozeman, MT 59715",21)
# insert_Employee("Kaiya Villanueva","(518)860-7508","771 Golf Ave., Muscatine, IA 52761",15)
# insert_Employee("Shona Goodman","(719)592-7142","72 East Griffin Drive, Evans, GA 30809",30)

# db.insert_Service("Shampoo, Cut, Style, Blow-dry",38,30)
# db.insert_Service("Hair and Scalp Treatments",20,50)
# db.insert_Service("Colour Blending or Highlights",40,120)
# db.insert_Service("Moustache and Beard Trim",7,10)
# db.insert_Service("Moustache Trim",5,5)
# db.insert_Service("Stately Shave (Hot towels, Balm)",30,30)
# db.insert_Service("Hair Style and Stately Shave",60,21)

# db.insert_Ability(2,1)
# db.insert_Ability(2,2)
# db.insert_Ability(2,3)
# db.insert_Ability(2,4)
# db.insert_Ability(2,5)
# db.insert_Ability(2,6)
# db.insert_Ability(2,7)
# db.insert_Ability(1,5)
# db.insert_Ability(3,4)
# db.insert_Ability(1,3)
# db.insert_Ability(3,3)
# db.insert_Ability(4,3)
# db.insert_Ability(5,3)
# db.insert_Ability(6,3)
# db.insert_Ability(7,3)

# db.insert_Choose(1,1,1,"11/5/18 9:00")
# db.insert_Choose(1,2,2,"11/5/18 9:00")
# db.insert_Choose(2,4,1,"11/5/18 9:40")
# db.insert_Choose(3,6,1,"11/5/18 10:10")
# db.insert_Choose(4,1,4,"11/5/18 9:40")
# db.insert_Choose(5,2,1,"11/5/18 13:10")


# db = Database()
# print(db.empoyeesOfAllSkills())
