'''
Created on Dec 13, 2018

@author: carlo
'''
from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
from gui.rpwidget import RoboPathWidget
from gui.robotdialog import RobotDialog, Dialog
from gui.obstacledialog import ObstacleDialog
from gui.pointdialog import PassingPointDialog
from patterns.observer import Observer #, Subject

from model.datamodel import PassingPoint, Obstacle
from controller.robot import RobotController
from tkinter import filedialog

import os
import csv
 
GRAPH_EDITOR_WIDTH = 500
GRAPH_EDITOR_HEIGHT = 500

class RoboPathMainWindow():
    def __init__(self, session):
        self.session = session
        
    def run(self):
        self.root = tk.Tk()
        self.root.title('RoboPath Configuration Editor v0.1')
        self.root.resizable(0, 0)
        self.build()
        self.root.mainloop()    

    def build(self):
        self.mainframe = ttk.Frame(self.root, padding='5 5 5 5')
        self.mainframe.grid(row=0, column=0, sticky=(E, W, N, S))
        
        self.build_robot_frame()
        
        self.geditorframe = ttk.LabelFrame(self.mainframe, text='Selected Robot: none', padding='5 5 5 5')
        self.geditorframe.grid(row=1, column=0, rowspan=3, sticky=(N, S, E, W), padx=5)
        
        self.robopathwidget = RoboPathWidget(self.geditorframe, GRAPH_EDITOR_WIDTH, GRAPH_EDITOR_HEIGHT)
        self.robopathwidget.grid(row=0, column=0, sticky=(E, W, N, S), padx=5, pady=5)

        self.build_points_frame()
        self.build_obstacles_frame()  
        self.build_paths_frame()
        
        # Observer setting for passing-point editor
        self.point_observer = RoboPathPassingPointObserver(self, RoboPathMainWindow.on_passing_point_add)
        self.robopathwidget.point_subject.attach(self.point_observer)

        # Observer setting for obstacle editor
        self.obstacle_observer = RoboPathPassingPointObserver(self, RoboPathMainWindow.on_obstacle_add)
        self.robopathwidget.obstacle_subject.attach(self.obstacle_observer)

    def build_robot_frame(self):
        self.robotframe = ttk.LabelFrame(self.mainframe, text='Robot', padding='5 5 5 5')
        self.robotframe.grid(row=0, column=0, columnspan=4, sticky=(W, E, N, S), padx=5)

        #self.cbo_robot = ttk.Combobox(self.robotframe, state='readonly', values=list(rs))
        self.cbo_robot = ttk.Combobox(self.robotframe, state='readonly', postcommand=self.on_populate_robot_list)
        self.cbo_robot.grid(row=0, column=0, columnspan=4, sticky=(E, W, N), padx=5, pady=5)
        #self.cbo_robot.current(1)
        self.cbo_robot.bind("<<ComboboxSelected>>", self.on_robot_selection_change)
        
        self.btn_new_robot = ttk.Button(self.robotframe, text="New", command=self.on_new_robot_click)
        self.btn_new_robot.grid(row=1, column=0, sticky=(N, W, E), padx=5, pady=5)

        self.btn_edit_robot = ttk.Button(self.robotframe, text="Edit", command=self.on_edit_robot_click)
        self.btn_edit_robot.grid(row=1, column=1, sticky=(N, W, E), padx=5, pady=5)
        self.btn_edit_robot.state(["disabled"]) 

        self.btn_del_robot = ttk.Button(self.robotframe, text="Delete", command=self.on_del_robot_click)
        self.btn_del_robot.grid(row=1, column=2, sticky=(N, W, E), padx=5, pady=5)
        self.btn_del_robot.state(["disabled"]) 

        self.btn_run_robot = ttk.Button(self.robotframe, text="Export", command=self.on_export_robot_click)
        self.btn_run_robot.grid(row=1, column=3, sticky=(N, W, E), padx=5, pady=5)
        self.btn_run_robot.state(["disabled"]) 
        
        self.lbl_robot_info = Label(self.robotframe, text='Type: <none>\nArm Length: <none>\nUnreachable Zone: <none>\nAction Angle: <none>', anchor=W, relief=SUNKEN, justify=LEFT)
        self.lbl_robot_info.grid(row=0, column=4, rowspan=2, sticky=(W, E, N, S), padx=5, pady=5)
    
    def on_populate_robot_list(self):
        self.robots = RobotController().get_robots(self.session)
        rs = map(lambda r: r.name, self.robots)
        self.cbo_robot['values'] = list(rs)
        #print(list(rs))
        
    def on_new_robot_click(self):
        rd = RobotDialog(self.root, title='New Robot', robot=None)
        if rd.closing_status == Dialog.OK:
            r = rd.robot
            self.session.add(r)
            self.session.commit()
    
    def on_edit_robot_click(self):
        rd = RobotDialog(self.root, title='Edit Robot', robot=self.robot)
        if rd.closing_status == Dialog.OK:
            self.cbo_robot.set(self.robot.name)
            self.robot.passing_points.clear()
            self.clear_points()
            self.clear_obstacles()
            self.refresh_children()
            #print(self.robot)

    def on_del_robot_click(self):
        if tk.messagebox.askquestion ('Delete Robot', 'The selected robot and its related data will be deleted.\nAre you sure?', icon = 'warning') == 'yes':
            self.clear_children()
            self.session.delete(self.robot)
            self.session.commit()
            self.robot = None
            self.cbo_robot.set('')
                        
    def on_export_robot_click(self):
        cwd = os.getcwd()
        export_filename =  filedialog.asksaveasfilename(initialdir = cwd, title = "Select file", filetypes = (("text files","*.txt"), ("all files","*.*")))
        if len(export_filename) > 0:
            #print("Exporting file:{}".format(export_filename))
            rc = RobotController()
            rc.export_robot_file(self.robot, export_filename)

    def build_points_frame(self):
        self.pointsframe = ttk.LabelFrame(self.mainframe, text='Passing Points', padding='5 5 5 5')
        self.pointsframe.grid(row=1, column=1, sticky=(W, E, N, S), padx=5)
    
        self.lb_points = Listbox(self.pointsframe, width=20, height=10)
        self.lb_points.grid(row=0, column=0, columnspan=3, sticky=(E, W, N, S), padx=5)
        self.lb_points.bind('<<ListboxSelect>>', self.on_list_points_change)
        
        self.btn_edit_point = ttk.Button(self.pointsframe, text="Edit", command=self.on_edit_point_click)
        self.btn_edit_point.grid(row=1, column=0, sticky=(N, W, E), padx=5, pady=5)
        self.btn_edit_point.state(["disabled"]) 
        
        self.btn_del_point = ttk.Button(self.pointsframe, text="Delete", command=self.on_delete_point_click)
        self.btn_del_point.grid(row=1, column=1, sticky=(N, W, E), padx=5, pady=5)
        self.btn_del_point.state(["disabled"]) 

        self.btn_clear_points = ttk.Button(self.pointsframe, text="Clear", command=self.on_clear_points_click)
        self.btn_clear_points.grid(row=1, column=2, sticky=(N, W, E), padx=5, pady=5)
        
    def build_obstacles_frame(self):
        self.obstaclesframe = ttk.LabelFrame(self.mainframe, text='Obstacles', padding='5 5 5 5')
        self.obstaclesframe.grid(row=2, column=1, sticky=(W, E, S, N), padx=5)
        
        self.lb_obstacles = Listbox(self.obstaclesframe, width=20, height=10)
        self.lb_obstacles.grid(row=0,column=0, columnspan=3, sticky=(E, W, N, S), padx=5)
        self.lb_obstacles.bind('<<ListboxSelect>>', self.on_list_obstacles_change)

        self.btn_edit_obstacle = ttk.Button(self.obstaclesframe, text="Edit", command=self.on_edit_obstacle_click)
        self.btn_edit_obstacle.grid(row=1, column=0, sticky=(N, W, E), padx=5, pady=5)
        self.btn_edit_obstacle.state(["disabled"]) 
        
        self.btn_del_obstacle = ttk.Button(self.obstaclesframe, text="Delete", command=self.on_delete_obstacle_click)
        self.btn_del_obstacle.grid(row=1, column=1, sticky=(N, W, E), padx=5, pady=5)
        self.btn_del_obstacle.state(["disabled"]) 

        self.btn_clear_obstacles = ttk.Button(self.obstaclesframe, text="Clear", command=self.on_clear_obstacles_click)
        self.btn_clear_obstacles.grid(row=1, column=2, sticky=(N, W, E), padx=5, pady=5)
    
    def build_paths_frame(self):
        self.pathsframe = ttk.LabelFrame(self.mainframe, text='Paths', padding='5 5 5 5')
        self.pathsframe.grid(row=3, column=1, sticky=(W, E, S, N), padx=5)
        
        self.lb_paths = Listbox(self.pathsframe, width=20, height=10)
        self.lb_paths.grid(row=0,column=0, columnspan=3, sticky=(E, W, N, S), padx=5)
        self.lb_paths.bind('<<ListboxSelect>>', self.on_list_paths_change)

        self.btn_open_path = ttk.Button(self.pathsframe, text="Open", command=self.on_open_path_click)
        self.btn_open_path.grid(row=1, column=0, sticky=(N, W, E), padx=5, pady=5)
        self.btn_open_path.state(["disabled"]) 
        
        self.btn_show_path = ttk.Button(self.pathsframe, text="Show", command=self.on_show_path_click)
        self.btn_show_path.grid(row=1, column=1, sticky=(N, W, E), padx=5, pady=5)
        self.btn_show_path.state(["disabled"]) 

        self.btn_clear_path = ttk.Button(self.pathsframe, text="Clear", command=self.on_clear_path_click)
        self.btn_clear_path.grid(row=1, column=2, sticky=(N, W, E), padx=5, pady=5)
        self.btn_clear_path.state(["disabled"]) 

    def on_robot_selection_change(self, event):
        self.robot = self.robots[self.cbo_robot.current()]
        self.refresh_children()
    
    def refresh_children(self):
        r = self.robot
        self.lbl_robot_info['text'] = 'Id: %d\nType: %s\nArm Length: %d\nUnreachable Zone: %d\nAction Angle: %d' % (r.id, r.robot_type, r.arm_length, r.unreachable_zone_radius, r.action_angle)
        self.geditorframe['text'] = 'Robot: %s %s' % (r.name, r.robot_type)
        self.btn_edit_robot.state(["!disabled"])
        self.btn_del_robot.state(["!disabled"])
        self.btn_run_robot.state(["!disabled"])
        self.btn_open_path.state(["!disabled"]) 

        self.refresh_points()
        self.refresh_obstacles()
        self.clear_paths()
        
    def refresh_points(self):
        self.robopathwidget.clear_points() 
        self.lb_points.delete(0, END) # clear
        r = self.robot
        if not r.passing_points is None:
            r.passing_points.sort(key=lambda x: x.point_id)
            pps = map(lambda pp: pp.name, r.passing_points)
            self.lb_points.insert(END, *pps)
            self.robopathwidget.build(r)
        
    def refresh_obstacles(self):
        self.robopathwidget.clear_obstacles() 
        self.lb_obstacles.delete(0, END) # clear
        r = self.robot
        if not r.obstacles is None:
            r.obstacles.sort(key=lambda x: x.obstacle_id)
            os = map(lambda o: o.name, r.obstacles)
            self.lb_obstacles.insert(END, *os)
            self.robopathwidget.build(r)
                    
    def clear_paths(self):
        self.robopathwidget.path.clear() 
        self.lb_paths.delete(0, END) # clear
        self.btn_show_path.state(["disabled"]) 
        self.btn_clear_path.state(["disabled"]) 

    def clear_children(self):
        self.geditorframe['text'] = 'Robot: none selected'
        self.btn_edit_robot.state(["!disabled"])
        self.btn_del_robot.state(["!disabled"])
        self.btn_run_robot.state(["!disabled"])
        self.robopathwidget.clear()
        self.lb_points.delete(0, END) # clear

    def on_list_points_change(self, event):
        w = event.widget
        if len(w.curselection()) == 0:
            return
        index = int(w.curselection()[0])
        self.selected_point = w.get(index)
        #print('You selected item %d: "%s"' % (index, self.selected_point))
        self.btn_edit_point.state(["!disabled"]) 
        self.btn_del_point.state(["!disabled"]) 
     
    def on_edit_point_click(self):
        pp = [pp for pp in self.robot.passing_points if pp.name == self.selected_point][0] 
        ppd = PassingPointDialog(self.root, title='Edit Passing Point', passing_point=pp)
        if ppd.closing_status == Dialog.OK:
            p = self.robopathwidget.working_area.robot2tkinter_coordinates([pp.x1, pp.y1])
            pp.x = p[0]
            pp.y = p[1]
            self.session.commit()
            self.refresh_points()
    
    def on_delete_point_click(self):
        if messagebox.askyesno("Delete", "The selected point will be deleted. Are you sure?", icon=messagebox.WARNING):
            self.lb_points.delete(ANCHOR)
            self.robopathwidget.delete_point(self.selected_point)
            self.session.query(PassingPoint).filter(PassingPoint.name==self.selected_point).delete()
            self.session.commit()
            self.selected_point = None

    def on_clear_points_click(self):
        if messagebox.askyesno("Clear", "All points will be deleted. Are you sure?", icon=messagebox.WARNING):
            self.clear_points()
            
    def clear_points(self):
        self.robopathwidget.clear_points() 
        self.lb_points.delete(0, END) # clear
        self.session.query(PassingPoint).filter(PassingPoint.robot_id==self.robot.id).delete()
        self.session.commit()
                
    def on_list_obstacles_change(self, event):
        w = event.widget
        if len(w.curselection()) == 0:
            return
        index = int(w.curselection()[0])
        self.selected_obstacle = w.get(index)
        self.btn_edit_obstacle.state(["!disabled"]) 
        self.btn_del_obstacle.state(["!disabled"]) 
        
    def on_edit_obstacle_click(self):
        o = [o for o in self.robot.obstacles if o.name == self.selected_obstacle][0]
        od = ObstacleDialog(self.root, title='Edit Obstacle', obstacle=o)
        if od.closing_status == Dialog.OK:
            p = self.robopathwidget.working_area.robot2tkinter_coordinates([o.x1, o.y1])
            o.x = p[0]
            o.y = p[1]
            o.width = self.robopathwidget.working_area.robot2tkinter_scale(o.width1)
            o.height = self.robopathwidget.working_area.robot2tkinter_scale(o.height1)
            self.session.commit()
            self.refresh_obstacles()
            
    def on_delete_obstacle_click(self):
        if messagebox.askyesno("Delete", "The selected obstacle will be deleted. Are you sure?", icon=messagebox.WARNING):
            self.lb_obstacles.delete(ANCHOR)
            self.robopathwidget.delete_obstacle(self.selected_obstacle)
            self.session.query(Obstacle).filter(Obstacle.name==self.selected_obstacle).delete()
            self.session.commit()
            self.selected_obstacle = None

    def on_clear_obstacles_click(self):
        if messagebox.askyesno("Clear", "All obstacles will be deleted. Are you sure?", icon=messagebox.WARNING):
            self.clear_obstacles()
            
    def clear_obstacles(self):
        self.robopathwidget.clear_obstacles() 
        self.lb_obstacles.delete(0, END) # clear
        self.session.query(Obstacle).filter(Obstacle.robot_id==self.robot.id).delete()
        self.session.commit()
    
    def on_passing_point_add(self, passing_point):
        self.lb_points.insert(END, passing_point.name)
        passing_point.robot_id = self.robot.id
        self.session.add(passing_point)
        self.session.commit()
        
    def on_obstacle_add(self, obstacle):
        self.lb_obstacles.insert(END, obstacle.name)
        obstacle.robot_id = self.robot.id
        self.session.add(obstacle)
        self.session.commit()

    def on_list_paths_change(self, event):
        w = event.widget
        if len(w.curselection()) == 0:
            return
        index = int(w.curselection()[0])
        self.selected_path = w.get(index)
        self.btn_show_path.state(["!disabled"]) 
        self.btn_clear_path.state(["!disabled"]) 
        
    def on_open_path_click(self):
        cwd = os.getcwd()
        #export_filename =  filedialog.asksaveasfilename(initialdir = cwd, title = "Select file", filetypes = (("text files","*.txt"), ("all files","*.*")))
        filename =  filedialog.askopenfilename(initialdir = cwd, title = "Select file", filetypes = (("CSV files","*.csv"),("all files","*.*")))
        if len(filename) > 0:
            with open(filename) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                self.populate_path_list(csv_reader)
                #print("Exporting file:{}".format(filename))
    
    def on_show_path_click(self):
        try:
            self.robopathwidget.draw_path(self.selected_path)
        except Exception as e:
            messagebox.showerror("Error", "%s\nCheck if the output file corresponds to the robot." % (e))
            
    def on_clear_path_click(self):
#         if messagebox.askyesno("Clear", "All obstacles will be deleted. Are you sure?", icon=messagebox.WARNING):
#             self.clear_obstacles()
        pass

    def populate_path_list(self, csv_reader):
        self.lb_paths.delete(0, END) # clear
        self.paths = list(map(lambda r: r[0], csv_reader))
        self.lb_paths.insert(END, *self.paths)

class RoboPathPassingPointObserver(Observer):
    def __init__(self, obj, callback):
        self.notify_object = obj
        self.callback = callback
         
    def update(self, passing_point):
        self.callback(self.notify_object, passing_point)

class RoboPathObstacleObserver(Observer):
    def __init__(self, obj, callback):
        self.notify_object = obj
        self.callback = callback
         
    def update(self, obstacle):
        self.callback(self.notify_object, obstacle)
        
