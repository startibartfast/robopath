'''
Created on Dec 11, 2018

@author: carlo

[x,y,z] = [0,0,0] #Robot's position. Here is always [0,0,0]
r = 900 #is the length of the arm 
sr = 100 #is the unreachable zone around the robot (small circle in the center)
angle = 135 #is the angle of the unreachable zone.

VAR robtarget p10 := [ [0, 400, 0], [0.0, -0.707106,   0.707106,  0.0] ,[ 0, 0, 0, 0 ], [ 0, 0, 0, 9E9, 9E9, 9E9]];
VAR robtarget p20 := [ [400, 0, 0], [0.0, -0.707106,   0.707106,  0.0] ,[ 0, 0, 0, 0 ], [ 0, 0, 0, 9E9, 9E9, 9E9]];
VAR robtarget p30 := [ [200, 200, 0], [0.0, -0.707106,   0.707106,  0.0] ,[ 0, 0, 0, 0 ], [ 0, 0, 0, 9E9, 9E9, 9E9]];

VAR robobstacle o1 := [[x,y,z], [width, height, depth]]

VAR robot r :=[<id>,<name>,<type>]
'''

from model.datamodel import Robot

class RobotController():
    ROUND_ANGLE = 360
    ROBOT_TEMPLATE_LINE = "VAR robot r := [%d, %s, %s]\n"
    POINT_TEMPLATE_LINE = "VAR robtarget p%d := [ [%d, %d, 0], [0.0, -0.707106,   0.707106,  0.0] ,[ 0, 0, 0, 0 ], [ 0, 0, 0, 9E9, 9E9, 9E9]];\n"
    OBSTACLE_TEMPLATE_LINE = "VAR robobstacle o%d := [ [%d, %d, 0], [%d, %d, 0]];\n"

    def get_robots(self, session):
        return session.query(Robot).order_by(Robot.name)

    def export_robot_file(self, robot, dest_filename):
        with open("%s" % (dest_filename), "w+") as f:
            f.write("[x,y,z] = [0,0,0]\n")
            f.write("r=%d\n" % (robot.arm_length))
            f.write("angle=%d\n" % (self.ROUND_ANGLE - robot.action_angle))
            # Points
            for p in robot.passing_points:
                f.write(self.POINT_TEMPLATE_LINE % (p.point_id, p.x1, p.y1))
            # Obstacle
            for o in robot.obstacles:
                f.write(self.OBSTACLE_TEMPLATE_LINE % (o.obstacle_id, o.x1, o.y1, o.width1, o.height1))

            # Robot's data            
            f.write(self.ROBOT_TEMPLATE_LINE % (robot.id, robot.name, robot.robot_type))
