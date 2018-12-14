'''
Created on Dec 12, 2018

@author: carlo
'''
from tkinter import *
import tkinter as tk
from tkinter import ttk

from gui.simpledialog import Dialog
from model.datamodel import Robot

class ObstacleDialog(Dialog):
    def __init__(self, parent, title = None, **kwargs):
        self.is_new = False
        self.obstacle = kwargs.get('obstacle')
        Dialog.__init__(self, parent, title)
        
    def body(self, master):
        Label(master, text="Name:").grid(row=0)
        Label(master, text=self.obstacle.name, anchor=W, relief=SUNKEN).grid(row=0, column=1, sticky=(E, W))

        Label(master, text="X:").grid(row=1)
        Label(master, text="Y:").grid(row=2)
        Label(master, text="Width:").grid(row=3)
        Label(master, text="Height:").grid(row=4)

        self.txt_x = Entry(master)
        self.txt_x.insert(0, self.obstacle.x1)
        self.txt_x.grid(row=1, column=1)
        
        self.txt_y = Entry(master)
        self.txt_y.insert(0, self.obstacle.y1)
        self.txt_y.grid(row=2, column=1)
        
        self.txt_width = Entry(master)
        self.txt_width.insert(0, self.obstacle.width1)
        self.txt_width.grid(row=3, column=1)

        self.txt_height = Entry(master)
        self.txt_height.insert(0, self.obstacle.height1)
        self.txt_height.grid(row=4, column=1)

        return self.txt_x # initial focus

    def validate(self):
        if int(self.txt_width.get()) <= 0 or int(self.txt_width.get()) > 10000:
            messagebox.showerror("Error", "Obstacle's width must be in (0, 10000]!")
            return False

        if int(self.txt_height.get()) <= 0 or int(self.txt_height.get()) > 10000:
            messagebox.showerror("Error", "Obstacle's height must be in (0, 10000]!")
            return False

#         if not self.is_new:                        
#             if tk.messagebox.askquestion ('Save Changes', 'Saving any changes to the selected robot will overwrite the current set of points and obstacles.\nAre you sure?', icon = 'warning') == 'yes':
#                 return True
#             else:
#                 return False
#         else:
#             return True
        return True
    
    def apply(self):
        try:
            #self.robot.name = self.txt_name.get()
            self.obstacle.x1 = float(self.txt_x.get())
            self.obstacle.y1 = float(self.txt_y.get())
            self.obstacle.width1 = float(self.txt_width.get())
            self.obstacle.height1 = float(self.txt_height.get())
        except ValueError as ve:
            messagebox.showerror("Error", "Invalid number.\nDescription:%s" % (ve))
            #print("Oops!  That was no valid number.  Try again...")        
