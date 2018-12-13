'''
Created on Dec 11, 2018

@author: carlo
'''

from model.datamodel import Robot

# def getCustomers():
#     session = config.Session()
#     q = session.query(Customer)
#     
#     for c in q:
#         print(c.id, c.first_name, c.last_name)    

class RobotController():
    def get_robots(self, session):
        return session.query(Robot).order_by(Robot.name)
