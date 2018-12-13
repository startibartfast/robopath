'''
Created on Nov 29, 2018

@author: carlo
'''

#from tkinter import ttk
#To override the basic Tk widgets, the import should follow the Tk import:
from tkinter import *
from tkinter.ttk import *

#import math
from math import degrees, atan2

from patterns.observer import Subject
from model.datamodel import Obstacle, PassingPoint
from gui.obstacledialog import Dialog, ObstacleDialog

MAX_ARM_LENGTH = 5000 # 0..5000
MAX_UNREACHABLE_AREA_RADIUS = 500 # 0..500
ROUND_ANGLE = 360
X_COORD_IDX = 0
Y_COORD_IDX = 1
SECTOR_CENTER_ANGLE = 180
OBSTACLE_DEF_WIDTH = 50
OBSTACLE_DEF_HEIGHT = 30

class RoboPathWidget(Canvas):
    def __init__(self, container, width, height):
        super(RoboPathWidget, self).__init__(container, width=width, height=height)
        self.working_area_radius = min(width, height) / 2.
        self.center = (width/2., height/2.)

        self.passing_points = []
        self.obstacles = []
        self.working_area_id = None
        self.unreachable_area_id = None
        
        # Observer pattern
        self.point_subject = Subject()
        self.obstacle_subject = Subject()
        
    #def build(self, arm_length, unreachable_area_radius, action_angle, passing_points):
    def build(self, robot):
        self.clear()

        self.scale = self.working_area_radius / robot.arm_length #MAX_ARM_LENGTH
        # Compute normalized radiuses of the outer and inner circles
        self.arm_length = robot.arm_length * self.scale #self.working_area_radius * arm_length / MAX_ARM_LENGTH
        self.unreachable_area_radius = robot.unreachable_zone_radius * self.scale
        self.unreachable_sector_angle = ROUND_ANGLE - robot.action_angle
        
        x = self.center[X_COORD_IDX]
        y = self.center[Y_COORD_IDX]
        
        # Draw outer circle
        self.boundary_rect = x - self.arm_length, \
            y - self.arm_length, \
            x + self.arm_length, \
            y + self.arm_length
        self.starting_angle = (self.unreachable_sector_angle/2) - SECTOR_CENTER_ANGLE
        self.working_area_id = self.create_arc(self.boundary_rect, start=self.starting_angle, outline='', extent=ROUND_ANGLE-self.unreachable_sector_angle, fill="gray60")

        # Draw inner circle
        rect = x - self.unreachable_area_radius, \
            y - self.unreachable_area_radius, \
            x + self.unreachable_area_radius, \
            y + self.unreachable_area_radius
        self.unreachable_area_id = self.create_arc(rect, start=(self.unreachable_sector_angle/2) - SECTOR_CENTER_ANGLE, extent=ROUND_ANGLE-self.unreachable_sector_angle, fill="black")
        self.bind('<Button-1>', self.on_click)

        if not (robot.passing_points is None):         
            for pp in robot.passing_points:
                rppp = RoboPathPassingPoint(pp, self)
                self.passing_points.append(rppp)          

        if not (robot.obstacles is None):         
            for o in robot.obstacles:
                rpo = RoboPathObstacle(o, self)
                self.obstacles.append(rpo)          

        # Create context menu
        self.popup_menu = Menu(self, tearoff=0)
        self.popup_menu.add_command(label="Add point", command=self.on_add_point_click)
        self.popup_menu.add_command(label="Add obstacle", command=self.on_add_obstacle_click)
        self.bind("<Button-3>", self.popup) # Button-2 on Aqua
        
    def popup(self, event):
        try:
            self.popup_event = event
            self.popup_menu.tk_popup(event.x_root, event.y_root, 0)
        finally:
            self.popup_menu.grab_release()

    def clear(self):
        if not (self.working_area_id is None):
            self.delete(self.working_area_id)
            self.delete(self.unreachable_area_id)
            self.clear_points()
            self.clear_obstacles()

    def on_add_point_click(self):
        if self.is_within_bounds(self.popup_event):
            pid = self.get_new_point_id()
            s = 'P{}'.format(pid)
            pp = PassingPoint(name=s, x=self.popup_event.x, y=self.popup_event.y, z=0, point_id=pid)
            rppp = RoboPathPassingPoint(pp, self)
            self.passing_points.append(rppp)          
     
            # Notify observers
            self.point_subject.subject_state = pp
        else:
            messagebox.showwarning("Warning", "You're trying to add a point outside the working area!")
                
    def on_add_obstacle_click(self):
        if self.is_within_bounds(self.popup_event):
            x = self.popup_event.x
            y = self.popup_event.y
            oid = self.get_new_obstacle_id()
            s = 'O{}'.format(oid)
            o = Obstacle(name=s, x=x, y=y, z=0, width=OBSTACLE_DEF_WIDTH, height=OBSTACLE_DEF_HEIGHT, obstacle_id=oid)
    
            od = ObstacleDialog(self.winfo_toplevel(), title='Edit Obstacle:{}'.format(s), obstacle=o)
            if od.closing_status == Dialog.OK:
                #print(o)
                rpo = RoboPathObstacle(o, self)
                self.obstacles.append(rpo)          
                # Notify observers
                self.obstacle_subject.subject_state = o
        else:
            messagebox.showwarning("Warning", "You're trying to add an obstacle outside the working area!")
                        
    def on_click(self, event):   
        print("clicked at", event.x, event.y)
    
    def get_new_point_id(self):
        if len(self.passing_points) == 0:
            return 1
        
        # Get the last element
        p = self.passing_points[-1]
        
        # Remove the prefix 'P'
        s = p.passing_point.name[1:]
        pid = int(s)
        return pid + 1 
        
    def get_new_obstacle_id(self):
        if len(self.obstacles) == 0:
            return 1
        
        # Get the last element
        o = self.obstacles[-1]
        
        # Remove the prefix 'O'
        s = o.obstacle.name[1:]
        oid = int(s)
        return oid + 1 

    def is_within_bounds(self, event):
        # Check if point is inside the working area
        x = event.x - self.center[X_COORD_IDX]
        y = event.y - self.center[Y_COORD_IDX]
        #print('x:{},y:{}'.format(x, y))
        if not (x**2 + y**2 <= self.working_area_radius**2):
            print ('Touch down event out of bounds')
            return False
          
        # Check if point is inside the unreachable area
        if (x**2 + y**2 <= self.unreachable_area_radius**2):
            print ('Touch down event inside unreachable area')
            return False
        theta = atan2(y, x)
        theta = degrees(theta)

        if theta < 0 :
            theta = ROUND_ANGLE + theta
        
        alpha2 = ROUND_ANGLE + self.starting_angle
        alpha1 = alpha2 - self.unreachable_sector_angle

        #print('theta: {}, alpha1: {}, alpha2: {}'.format(theta, alpha1, alpha2))
        
        if theta >= alpha1 and theta <= alpha2:
            print ('Touch down event inside unreachable area (shadowed sector)')
            return False
           
        return True
    
    def clear_points(self):
        for rppp in self.passing_points:
            self.delete(rppp.text_object_id)
            self.delete(rppp.circle_object_id)
            
        self.passing_points.clear()

    def delete_point(self, point_name):
        for rppp in self.passing_points:
            if rppp.passing_point.name == point_name:
                self.delete(rppp.text_object_id)
                self.delete(rppp.circle_object_id)
                
        pps = []
        for pp in self.passing_points:
            if pp != point_name:
                pps.append(pp)
        self.passing_points = pps

    def clear_obstacles(self):
        for rpo in self.obstacles:
            self.delete(rpo.text_object_id)
            self.delete(rpo.rect_object_id)
            
        self.obstacles.clear()
                
    def delete_obstacle(self, obstacle_name):
        for rpo in self.obstacles:
            if rpo.obstacle.name == obstacle_name:
                self.delete(rpo.text_object_id)
                self.delete(rpo.rect_object_id)
                
        os = []
        for o in self.obstacles:
            if o != obstacle_name:
                os.append(o)
        self.obstacles = os

class RoboPathPassingPoint():
    _RADIUS = 5.
    _TEXT_OFFSET = 10
    def __init__(self, passing_point, canvas):
        self.passing_point = passing_point
#    def __init__(self, pid, x, y, canvas):
#         self.name = 'P{}'.format(pid)
#         self.x = x
#         self.y = y
#         self.point_id = pid
        self.text_object_id = canvas.create_text(self.passing_point.x + RoboPathPassingPoint._TEXT_OFFSET, self.passing_point.y + RoboPathPassingPoint._TEXT_OFFSET, text=self.passing_point.name)
        rect = self.passing_point.x - RoboPathPassingPoint._RADIUS, self.passing_point.y - RoboPathPassingPoint._RADIUS, self.passing_point.x + RoboPathPassingPoint._RADIUS, self.passing_point.y + RoboPathPassingPoint._RADIUS
        self.circle_object_id = canvas.create_oval(rect, fill="red")

    def __str__(self):
        return "%s" % (self.name)
     
    def __repr__(self):
        return "%s (%d, %d)" % (self.name, self.x, self.y)

class RoboPathObstacle():
    _TEXT_OFFSET = 10
    def __init__(self, obstacle, canvas):
        self.obstacle = obstacle 
        rect = obstacle.x, obstacle.y, obstacle.x + obstacle.width, obstacle.y + obstacle.height
        self.text_object_id = canvas.create_text(rect[0] + RoboPathObstacle._TEXT_OFFSET, rect[3] + RoboPathObstacle._TEXT_OFFSET, text=obstacle.name)
        self.rect_object_id = canvas.create_rectangle(rect, fill='blue')
        
    def __str__(self):
        return "%s" % (self.name)
     
    def __repr__(self):
        return "%s (%d, %d)" % (self.name, self.x, self.y)
    