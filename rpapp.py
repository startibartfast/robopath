'''
Created on Dec 7, 2018

@author: carlo
'''
from model.datamodel import DatabaseManager, Robot
from gui.rpmainwindow import RoboPathMainWindow

class RobotPathApp():
    def __init__(self):
        self.dm = DatabaseManager()

    def run(self):
        RoboPathMainWindow(self.dm.session).run()
        
    def updateDatabase(self):
        self.dm.dropStructure()
        self.dm.createStructure()
        robot0 = Robot(name="Raffaello", robot_type="ABB-001-XYZ", arm_length=4500, unreachable_zone_radius=500, action_angle=270)
        robot1 = Robot(name="Leonardo", robot_type="ABB-002-XYZ", arm_length=2500, unreachable_zone_radius=200, action_angle=300)
        robot2 = Robot(name="Giotto", robot_type="ABB-003-XYZ", arm_length=1500, unreachable_zone_radius=100, action_angle=320)
        self.dm.session.add(robot0)
        self.dm.session.add(robot1)
        self.dm.session.add(robot2)
        self.dm.session.commit()    
        
if __name__ == "__main__":
    rpa = RobotPathApp()
    #rpa.updateDatabase()
    rpa.run()
