import sys
import csv
import threading
import sqlite3
import logging
from employees import Casuals, Executives
from sqlalchemy.exc import IntegrityError

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
_thread_local = threading.local()

def get_db_conn():
    if not hasattr(_thread_local, 'db'):
        _thread_local.db = sqlite3.connect('Casuals.db', check_same_thread=False)
        _thread_local.cursor = _thread_local.db.cursor()
    return _thread_local.db, _thread_local.cursor
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

formatter = logging.Formatter("%(asctime)s: %(levelname)s: %(message)s")

f_handler = logging.FileHandler('executives.log')
f_handler.setFormatter(formatter)

logger.addHandler(f_handler)


    
conn = sqlite3.connect("Executives.db")
c = conn.cursor()

conn1 = sqlite3.connect("Casuals.db")
x = conn1.cursor()

'''
c.execute("""CREATE TABLE executives (
          first text,
          last text,
          position text,
          salary integer,
          communication text,
          years integer,
          j_role text
        )""")

x.execute("""CREATE TABLE casuals (
          first text,
          last text,
          position text,
          hours integer,
          salary integer,
          communication text,
          teamwork integer,
          years integer
        )""")
'''

# ------------------------------------------------------------------------------------------------- >>>
# ------------------------------------------------------------------------------------------------- >>>
#                                     [[ -- EXECUTIVE EMPLOYEE -- ]]

class e_database():
    def __init__(self, first, last, position, salary, communication, years, j_role):
        self.first = first
        self.last = last
        self.position = position
        self.salary = salary
        self._communication_ = communication
        self.years = years
        self.j_role = j_role

        logger.info("SUCCESSFULLY-- [[ MANIPULATED ]] {} {} in the Databse".format(self.first, self.last))


    def add(self):
        with conn:
            c.execute('''INSERT INTO executives VALUES(:f, :l, :p, :s, :c, :y, :j)''',{'f':self.first,
                                                                                   'l':self.last,
                                                                                   'p':self.position,
                                                                                   's':self.salary,
                                                                                   'c':self._communication_,
                                                                                   'y':self.years,
                                                                                   'j':self.j_role})
        conn.commit()    

    def retrieve(self):
        c.execute("SELECT * FROM executives")
        return c.fetchall()
        
    def retrieve0(self, first, position):
        with conn:
            c.execute("SELECT * FROM executives WHERE first=:f AND position=:p", {'f':first, 'p':position})
            return c.fetchone()
    
    def update_P(self, first, last, position):
        with conn:
            c.execute('''UPDATE executives SET position=:p
                      WHERE first=:f AND last=:l ''',{'f':first, 'l':last, 'p':position})
            
        logger.warning("SUCCESSFULLY UPDATED {}'s Postion in the Database".format(first)) 
        conn.commit()

    def update_C(self, first, position, communication):
        with conn:
            c.execute('''UPDATE executives SET communication=:c
                      WHERE first=:f AND position=:p ''',{'f':first, 'p':position, 'c':communication})
            
        logger.warning("SUCCESSFULLY UPDATED {}'s Communication skills in the Database".format(first)) 
        conn.commit()

    def update_S(self, first, last, salary):
        with conn:
            c.execute('''UPDATE executives SET salary=:s
                        WHERE first=:f AND last=:l ''',{'f':first, 'l':last, 's':salary})
            
        logger.warning("SUCCESSFULLY UPDATED {}'s Salary in the Database".format(first)) 
        conn.commit()
        
    def update_Y(self, first, last, years):
        with conn:
            c.execute('''UPDATE executives SET years=:y
                      WHERE first=:f AND last=:l ''',{'f':first, 'l':last, 'y':years})
            
        logger.warning("SUCCESSFULLY UPDATED {}'s Postion in the Database".format(first)) 
        conn.commit()
    
    def update_J(self, first, last, role):
        with conn:
            c.execute('''UPDATE executives SET j_role=:j
                      WHERE first=:f AND last=:l ''',{'f':first, 'l':last, 'j':role})
            
        logger.warning("SUCCESSFULLY UPDATED {}'s Postion in the Database".format(first)) 
        conn.commit()

    def delete(self):
        with conn:
            c.execute("DELETE FROM executives")
        conn. commit()

    def delete0(self, first, last):
        with conn:
            c.execute('''DELETE FROM executives WHERE first=:p AND last=:l''', {'p':first, 'l':last})

        logger.warning("SUCCESSFULLY DELETED {} {} in the Database".format(first, last))
        conn.commit()


class e_specific(e_database):
    def __init__(self, first=None, last=None, position=None, salary=None, communication=None, years=None, j_role=None):
        super().__init__(first, last, position, salary, communication, years, j_role)

    @property
    def secondary(self):
        usr = self.retrieve0(self.first, self.position)
        if usr:
            return "Since {} is an Executive, his Secondary role is: {}".format(usr.first, usr.j_role)
        else:
            return "No executive found with the provided criteria."
    
    def add_one_user(self, first, last, position, salary, _communication_, years, j_role):
        new_user = e_database(first, last, position, salary, _communication_, years, j_role)
        new_user.add()
        conn.commit()
        logger.warning("SUCCESSFULLY ADDED {} {} in the Database".format(first, last))

    def add_multiple_users(self, users):
        for user in users:
            new_user = e_database(*user)
            new_user.add()
            conn.commit()
            logger.warning("SUCCESSFULLY ADDED {} in the Database".format(user))
    
    def fetch(self):
        global users
        users = super().retrieve()  
        logger.warning("SUCCESSFULLY RETRIEVED info of all executives from the Database")
        return users
    
    def fetch_one(self, first, position):
        global usr
        usr = super().retrieve0(first, position)
        logger.warning("SUCCESSFULLY RETRIEVED {}'s info from the Database".format(first))
        return usr

    @property
    def fullname(self):
        return "{} {}".format(self.first, self.last)
    

    @property
    def email(self):
        return "Their mail: {}.{}@email.com".format(usr[0], usr[1])
    

    @property
    def p_position(self):
        return "Sir {}'s position at the company is {}".format(usr[0], usr[2])
    

    @property
    def payday(self):
        return "The Cheque reflects: ${}".format(usr[3])
    
    @property
    def c_skills(self):
        return "{}'s communication skills reflects as: {}: ${}".format(usr[0], usr[4])

    @property
    def secondary(self):
        return "Since {} is an Executive, his Secondary role is: {}".format(usr[0], usr[-1])

    
    @property
    def experience(self):
        return "For {} year(s), the executive has held this role as a {}".format(usr[4], usr[2]) 
        
    
    def fetch_many(self, first, last):
        global manyy
        manyy = super.retrieve()
        logger.warning("SUCCESSFULLY RETRIEVED info of name {} or {} from the Database".format(first, last))
        return manyy


# ------------------------------------------------------------------------------------------------- >>>
# ------------------------------------------------------------------------------------------------- >>>
#                                     [[ -- CASUAL EMPLOYEE -- ]]
        

class c_database():
    def __init__(self, first, last, position, hours, salary, communication, teamwork, years):
        self.first = first
        self.last = last
        self.position = position
        self.hours = hours
        self.salary = salary
        self.communication = communication
        self.teamwork = teamwork
        self.years = years

        logger.info("SUCCESSFULLY-- [[ MANIPULATED ]] {} {} in the Databse".format(self.first, self.last))


    def add(self):
        with conn1:
            x.execute('''INSERT INTO casuals VALUES(:f, :l, :p, :h, :s, :c, :t, :y)''',{'f':self.first,
                                                                                   'l':self.last,
                                                                                   'p':self.position,
                                                                                   'h':self.hours,
                                                                                   's':self.salary,
                                                                                   'c':self.communication,
                                                                                   't':self.teamwork,
                                                                                   'y':self.years
                                                                                   })
        conn.commit()    

    def retrieve(self):
        try:
            x.execute("SELECT * FROM casuals")
            return x.fetchall()
        finally:
            x.close()
        
        
    def retrieve0(self, first, position):
        with conn1:
            x.execute("SELECT * FROM casuals WHERE first=:f AND position=:p", {'f':first, 'p':position})
            return x.fetchone()
    
    def update_P(self, first, last, position):
        with conn1:
            x.execute('''UPDATE casuals SET position=:p
                      WHERE first=:f AND last=:l ''',{'f':first, 'l':last, 'p':position})
            
        logger.warning("SUCCESSFULLY UPDATED {}'s position in the Database".format(first)) 
        conn1.commit()

    def update_C(self, first, position, communication):
        with conn1:
            x.execute('''UPDATE casuals SET communication=:c
                      WHERE first=:f AND position=:p ''',{'f':first, 'p':position, 'c':communication})
            
        logger.warning("SUCCESSFULLY UPDATED {}'s Communication skills in the Database".format(first)) 
        conn1.commit()

    def update_S(self, first, last, salary):
        with conn1:
            x.execute('''UPDATE casuals SET salary=:s
                        WHERE first=:f AND last=:l ''',{'f':first, 'l':last, 's':salary})
            
        logger.warning("SUCCESSFULLY UPDATED {}'s Salary in the Database".format(first)) 
        conn1.commit()

    def update_H(self, first, last, hours):
        with conn1:
            x.execute('''UPDATE casuals SET hours=:h
                        WHERE first=:f AND last=:l ''',{'f':first, 'l':last, 'h':hours})
            
        logger.warning("SUCCESSFULLY UPDATED {}'s Salary in the Database".format(first)) 
        conn1.commit()
    
    def update_T(self, first, last, teamwork):
        with conn1:
            x.execute('''UPDATE casuals SET teamwork=:t
                        WHERE first=:f AND last=:l ''',{'f':first, 'l':last, 't':teamwork})
            
        logger.warning("SUCCESSFULLY UPDATED {}'s Salary in the Database".format(first)) 
        conn1.commit()
        
    def update_Y(self, first, last, years):
        with conn1:
            x.execute('''UPDATE casuals SET years=:y
                      WHERE first=:f AND last=:l ''',{'f':first, 'l':last, 'y':years})
            
        logger.warning("SUCCESSFULLY UPDATED {}'s Postion in the Database".format(first)) 
        conn1.commit()
    


    def delete(self):
        with conn1:
            x.execute("DELETE FROM casuals")
        conn1. commit()

    def delete0(self, first, last):
        with conn1:
            x.execute('''DELETE FROM casuals WHERE first=:p AND last=:l''', {'p':first, 'l':last})

        logger.warning("SUCCESSFULLY DELETED {} {} in the Database".format(first, last))
        conn1.commit()


class c_specific(c_database):
    def __init__(self, first=None, last=None, position=None, hours=None, salary=None, communication=None, teamwork= None, years=None):
        super().__init__(first, last, position, hours, salary, communication, teamwork, years)

    @property
    def secondary(self):
        usr = self.retrieve0()
        if usr:
            return "{}'s role in the company is: {}".format(usr.first, usr.j_role)
        else:
            return "No executive found with the provided criteria."
        
    def fetch(self):
        try:
            conn = sqlite3.connect('Casuals.db', check_same_thread=False)
            x = conn.cursor()
            x.execute("SELECT * FROM casuals")
            users = x.fetchall()

            users = super().retrieve()  
            logger.warning("SUCCESSFULLY RETRIEVED info of casuals from the Database")
            
        finally:
            x.close()
            conn.close()

        return users
        
    
    def add_one_user(self, first, last, position, hours, salary, communication, teamwork, years):
        new_user = c_database(first, last, position, hours, salary, communication, teamwork, years)
        new_user.add()
        conn1.commit()
        logger.warning("SUCCESSFULLY ADDED {} {} in the Database".format(first, last))

    def add_multiple_users(self, users):
        for user in users:
            new_user = c_database(*user)
            new_user.add()
            conn1.commit()
            logger.warning("SUCCESSFULLY ADDED {} in the Database".format(user))

    
    def fetch_one(self, first, position):
        global usr
        usr = super().retrieve0(first, position)
        logger.warning("SUCCESSFULLY RETRIEVED {}'s info from the Database".format(first))
        return usr

    @property
    def fullname(self):
        return "{} {}".format(self.first, self.last)
    

    @property
    def email(self):
        return "Their mail: {}.{}@email.com".format(usr[0], usr[1])
    

    @property
    def p_position(self):
        return "Sir {}'s position at the company is {}".format(usr[0], usr[2])
    

    @property
    def payday(self):
        return "The Cheque reflects: ${}".format(usr[4])
    
    @property
    def c_skills(self):
        return "{}'s communication skills reflects as: {}: ${}".format(usr[0], usr[5])

    @property
    def longevity(self):
        return "{}'s work hours for the week is: {}".format(usr[0], usr[3])

    
    @property
    def experience(self):
        return "For {} year(s), the executive has held this role as a {}".format(usr[4], usr[2]) 
        
    
    def fetch_many(self, first, last):
        global many
        many = super.retrieve()
        logger.warning("SUCCESSFULLY RETRIEVED info of name {} or {} from the Database".format(first, last))
        return many


#                                 [[ --- TESTS --- ]]
        
sp_i = e_specific()
sp_x = c_specific()

exec1 = Executives("John", "McClean", "CEO", 1000000, 'awesome', 4, "chairman")
cas1 = Casuals("Janet", "Smith", "Administrator", 60, 1000000, 'great', 7, 3)
cas2 = Casuals("Lorra", "Smith", "Junior ddministrator", 55, 900000, 'awesome', 7, 3)
cas3 = Casuals("Montana", "Smith", "CFO", 60, 9800000, 'cool', 8, 3)
cas4 = Casuals("Lisa", "Ann", "CTO", 60, 1000000, 'nice', 7, 3)
cas5 = Casuals("Avil", "Reiner", "CIO", 60, 1000000, 'good', 9, 3)
cas6 = Casuals("Moon", "Shadow", "COO", 60, 9900000, 'sensational', 10, 3)

"""
sp_i.add_one_user(exec1.first, exec1.last, exec1.position, exec1.salary, exec1._communication, exec1.years, exec1.s_role)  
sp_x.add_one_user(cas2.first, cas2.last, cas2.position, cas2.hours, cas2.salary, cas2.communication_, cas2.teamwork, cas2.years)
sp_x.add_one_user(cas3.first, cas3.last, cas3.position, cas3.hours, cas3.salary, cas3.communication_, cas3.teamwork, cas3.years)
sp_x.add_one_user(cas4.first, cas4.last, cas4.position, cas4.hours, cas4.salary, cas4.communication_, cas4.teamwork, cas4.years)
sp_x.add_one_user(cas5.first, cas5.last, cas5.position, cas5.hours, cas5.salary, cas5.communication_, cas5.teamwork, cas5.years)
sp_x.add_one_user(cas6.first, cas6.last, cas6.position, cas6.hours, cas6.salary, cas6.communication_, cas6.teamwork, cas6.years)
"""
#print(sp_x.fetch())

#                   [[  CREATION OF A CSV FILE FOR AN ALTERNATION TO THREADING  ]]


data = sp_x.fetch()

csv_file_path = 'employees.csv'
headers = ['First Name', 'Last Name', 'Position', 'Hours', 'Salary', 'Communication', 'Team Score', 'Years']

# Write data to CSV file
with open(csv_file_path, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(headers)
    csv_writer.writerows(data)

print("CSV file created successfully!")