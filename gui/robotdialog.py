'''
Created on Dec 12, 2018

@author: carlo
'''
from tkinter import *
import tkinter as tk
from tkinter import ttk

from gui.simpledialog import Dialog
from model.datamodel import Robot

class RobotDialog(Dialog):
    def __init__(self, parent, title = None, **kwargs):
        if kwargs.get('robot') is None:
            self.is_new = True
            self.robot = Robot(name="Puppo", robot_type="XYZ", arm_length=4500, unreachable_zone_radius=450, action_angle=290)
        else:
            self.is_new = False
            self.robot = kwargs.get('robot')
        Dialog.__init__(self, parent, title)
        
    def body(self, master):
        Label(master, text="Name:").grid(row=0)
        Label(master, text="Type:").grid(row=1)
        Label(master, text="Length of the Arm:").grid(row=2)
        Label(master, text="Unreachable Zone:").grid(row=3)
        Label(master, text="Action Angle:").grid(row=4)

        self.txt_name = Entry(master)
        self.txt_name.insert(0, self.robot.name)
        self.txt_name.grid(row=0, column=1)
        
        self.txt_type = Entry(master)
        self.txt_type.insert(0, self.robot.robot_type)
        self.txt_type.grid(row=1, column=1)
        
        self.txt_arm_length = Entry(master)
        self.txt_arm_length.insert(0, self.robot.arm_length)
        self.txt_arm_length.grid(row=2, column=1)

        self.txt_unreachable_zone_radius = Entry(master)
        self.txt_unreachable_zone_radius.insert(0, self.robot.unreachable_zone_radius)
        self.txt_unreachable_zone_radius.grid(row=3, column=1)

        self.txt_action_angle = Entry(master)
        self.txt_action_angle.insert(0, self.robot.action_angle)
        self.txt_action_angle.grid(row=4, column=1)

        return self.txt_name # initial focus

    def validate(self):
        if len(self.txt_name.get()) == 0 or len(self.txt_type.get()) == 0:
            messagebox.showerror("Error", "Robot's name and type can't be empty!")
            return False

        if int(self.txt_arm_length.get()) <= 0 or int(self.txt_arm_length.get()) > 5000:
            messagebox.showerror("Error", "Robot's arm length must be in (0, 5000]!")
            return False

        if not self.is_new:                        
            if tk.messagebox.askquestion ('Save Changes', 'Saving any changes to the selected robot will overwrite the current set of points and obstacles.\nAre you sure?', icon = 'warning') == 'yes':
                return True
            else:
                return False
        else:
            return True
        
    def apply(self):
        try:
            self.robot.name = self.txt_name.get()
            self.robot.robot_type = self.txt_type.get()
            self.robot.arm_length = int(self.txt_arm_length.get())
            self.robot.unreachable_zone_radius = int(self.txt_unreachable_zone_radius.get())
            self.robot.action_angle = int(self.txt_action_angle.get())
        except ValueError as ve:
            messagebox.showerror("Error", "Invalid number.\nDescription:%s" % (ve))
            #print("Oops!  That was no valid number.  Try again...")        
