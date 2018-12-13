'''
Created on Dec 12, 2018

@author: carlo
'''
from tkinter import *
import tkinter as tk
from tkinter import ttk

from gui.simpledialog import Dialog
from model.datamodel import Robot

class PassingPointDialog(Dialog):
    def __init__(self, parent, title = None, **kwargs):
        self.is_new = False
        self.passing_point = kwargs.get('passing_point')
        Dialog.__init__(self, parent, title)
        
    def body(self, master):
        Label(master, text="X:").grid(row=0)
        Label(master, text="Y:").grid(row=1)

        self.txt_x = Entry(master)
        self.txt_x.insert(0, self.passing_point.x)
        self.txt_x.grid(row=0, column=1)
        
        self.txt_y = Entry(master)
        self.txt_y.insert(0, self.passing_point.y)
        self.txt_y.grid(row=1, column=1)
        
        return self.txt_x # initial focus

    def validate(self):
#         if int(self.txt_width.get()) <= 0 or int(self.txt_width.get()) > 10000:
#             messagebox.showerror("Error", "Obstacle's width must be in (0, 10000]!")
#             return False
# 
#         if int(self.txt_height.get()) <= 0 or int(self.txt_height.get()) > 10000:
#             messagebox.showerror("Error", "Obstacle's height must be in (0, 10000]!")
#             return False

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
            self.passing_point.x = int(self.txt_x.get())
            self.passing_point.y = int(self.txt_y.get())
        except ValueError as ve:
            messagebox.showerror("Error", "Invalid number.\nDescription:%s" % (ve))
            #print("Oops!  That was no valid number.  Try again...")        
