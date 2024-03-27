import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s: %(levelname)s: %(message)s")

f_handler = logging.FileHandler('employee.log')
f_handler.setFormatter(formatter)

logger.addHandler(f_handler)


class Employees:
    def __init__(self, first, last, position, salary):
        self.first = first
        self.last = last
        self.position = position
        self.salary = salary

        logger.info("Hey Qazy, {}  {} has been added to our COMPANY database and Co.".format(self.first, self.last))

    @property
    def fullname(self):
        return "{} {}".format(self.first, self.last)
    
    @property
    def email(self):
        return "Their mail: {}.{}@email.com".format(self.first, self.last)
    
    @property
    def p_position(self):
        return "Sir {} position at the company is {}".format(self.first, self.position)
    
    @property
    def payday(self):
        return "The Cheque reflects: ${}".format(self.salary)
    
class Executives(Employees):
    def __init__(self, first, last, position, salary, communication, years, s_role):
        self._communication = communication
        self.years = years
        self.s_role = s_role
        super().__init__(first, last, position, salary)

        logger.info("PRIMUS Qazy, {}  {} has been added to our EXECUTIVE database and Co.".format(self.first, self.last))

    @property
    def comms(self):
        return "{} has a {} review on the communication category towards other employees.".format(self.first, self._communication)
    @property
    def experience(self):
        return "For {} year(s), the executive has held this role as a {}".format(self.years, self.position)
    
    @property
    def secondary(self):
        return "Since {} is an Executive, his Secondary role is: {}".format(self.first, self.s_role)
    
class Casuals(Employees):
    def __init__(self, first, last, position, hours, salary, communication, teamwork, years):
        self.hours = hours
        self.communication_ = communication
        self.teamwork = teamwork
        self.years = years
        super().__init__(first, last, position, salary)

        logger.info("PRIMUS Qazy, {}  {} has been added to our Casual database and Co.".format(self.first, self.last))

    @property
    def comm(self):
        return "{} has a {} review on the communication category towards other employees.".format(self.first, self.communication_)
    @property
    def experience(self):
        return "For {} year(s), the employee has held this role as a {}".format(self.years, self.position)
    
    @property
    def team(self):
        return "As an employee, {}'s teamwork score is a solid: {}".format(self.first, self.teamwork)


#emp1 = Executives("Jane", "Doe", "Chairman", 190000, 5, "CSec")
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

c.execute("""CREATE TABLE casuals (
          first text,
          last text,
          position text,
          salary integer,
          communication text,
          teamwork integer,
          years integer
        )""")
'''
