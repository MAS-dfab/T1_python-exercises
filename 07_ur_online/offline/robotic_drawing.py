"""
MAS ROBOTIC DRAWING
04.10.2017

Author: David Jenny
"""


import simple_ur_script as ur
import simple_comm as c

import math as m
import random as r

import rhinoscriptsyntax as rs
import Rhino.Geometry as rg

ROBOT_IP = '.xxx.xx.xx'


#how to move the robot to a vertical position
def move_robot_vertical(move_to):
    script = ""
    script += ur.set_tcp_by_angles(0.0,0.0,0.0,m.radians(0.0),m.radians(180.0),m.radians(0))

    velocity = 0.05
    acceleration = 0.02
    robot_ip = ROBOT_IP

    plane = rg.Plane(move_to,rg.Vector3d.ZAxis)
    script += ur.move_l(plane,acceleration,velocity)

    script = c.concatenate_script(script)
    c.send_script(script,robot_ip)
    print script

#how to get the robot's position
def get_robot_position():
    robot_ip = ROBOT_IP
    data = c.listen_to_robot(robot_ip)

#how to set a base plane
def set_robot_base_plane():
    robot_ip = ROBOT_IP
    #robot_ip = "192.168.10.43"

    rs.MessageBox("move robot to base plane origin, press OK when there",0)
    data = c.listen_to_robot(robot_ip)
    pose = data['pose']
    pt_1 = rg.Point3d(pose[0]*1000,pose[1]*1000,pose[2]*1000)
    print pt_1
    rs.MessageBox("move robot to base plane positive x direction, press OK when there",0)
    data = c.listen_to_robot(robot_ip)
    pose = data['pose']
    pt_2 = rg.Point3d(pose[0]*1000,pose[1]*1000,pose[2]*1000)
    print pt_2
    rs.MessageBox("move robot to base plane positive y direction, press OK when there",0)
    data = c.listen_to_robot(robot_ip)
    pose = data['pose']
    pt_3 = rg.Point3d(pose[0]*1000,pose[1]*1000,pose[2]*1000)
    print pt_3

    robot_base = rg.Plane(pt_1,pt_2-pt_1,pt_3-pt_1)
    text_file = open("robot_base.txt", "w")
    text_file.write(str(robot_base.Origin)+","+str(robot_base.XAxis)+","+str(robot_base.YAxis))
    text_file.close()

#how to load a base plane
def load_robot_base_plane():
    text_file = open("robot_base.txt", "r")
    string = text_file.read()
    values = string.split(",")
    values = [float(value) for value in values]

    base_origin = rg.Point3d(values[0],values[1],values[2])
    base_x_axis = rg.Vector3d(values[3],values[4],values[5])
    base_y_axis = rg.Vector3d(values[6],values[7],values[8])

    base_plane = rg.Plane(base_origin,base_x_axis,base_y_axis)
    return base_plane

#how to transform rhino to robot base coordinates
def rhino_to_robot_space(_plane,_robot_base):
    _r_matrix = rg.Transform.PlaneToPlane(rg.Plane.WorldXY,_robot_base)
    _plane.Transform(_r_matrix)
    return _plane

#how to randomly draw
def random_walk_draw(_robot_base,pen_height,_no_pts,vel,accel):
    way_pts = []
    for i in range(_no_pts):
        x_r = r.randint(50,247)
        y_r = r.randint(50,370)
        r_pt = rg.Point3d(50+5*i,y_r,pen_height)
        way_pts.append(r_pt)

    #way_pts.append(way_pts[-1]+rg.Point3d(0,0,150))
    #way_pts.insert(0,way_pts[0]+rg.Point3d(0,0,150))

    for i,pt in enumerate(way_pts):
        if i>0:
            rs.AddLine(way_pts[i-1],pt)

    way_planes = [rg.Plane(pt,rg.Vector3d.ZAxis) for pt in way_pts]
    way_planes = [rhino_to_robot_space(plane,_robot_base) for plane in way_planes]

    velocity = vel
    acceleration = accel
    robot_ip = ROBOT_IP

    script = ""
    script += ur.set_tcp_by_angles(0.0,0.0,pen_height,m.radians(0.0),m.radians(180.0),m.radians(0))

    for plane in way_planes:
        script += ur. move_l(plane,acceleration,velocity)

    script = c.concatenate_script(script)
    c.send_script(script,robot_ip)
    print script

#how to nicely draw
def nice_walk(_robot_base,pen_height,_no_pts,vel,accel):
    way_pts = []
    step_x = 150/_no_pts
    step_y = 237/_no_pts
    for i in range(_no_pts):
        if i%2 == 0:
            x_r = 30+step_x*i
            y_r = 30+step_y*i
            r_pt = rg.Point3d(x_r,y_r,pen_height)
            way_pts.append(r_pt)
        else:
            x_r = 30+step_x*i
            y_r = 150+60*m.sin(i)*-1
            r_pt = rg.Point3d(x_r,y_r,pen_height)
            way_pts.append(r_pt)

    #way_pts.append(way_pts[-1]+rg.Point3d(0,0,150))
    #way_pts.insert(0,way_pts[0]+rg.Point3d(0,0,150))

    for i,pt in enumerate(way_pts):
        if i>0:
            rs.AddLine(way_pts[i-1],pt)

    way_planes = [rg.Plane(pt,rg.Vector3d.ZAxis) for pt in way_pts]
    way_planes = [rhino_to_robot_space(plane,_robot_base) for plane in way_planes]

    velocity = vel
    acceleration = accel
    robot_ip = ROBOT_IP

    script = ""
    script += ur.set_tcp_by_angles(0.0,0.0,pen_height,m.radians(0.0),m.radians(180.0),m.radians(0))

    for plane in way_planes:
        script += ur. move_l(plane,acceleration,velocity)

    script = c.concatenate_script(script)
    c.send_script(script,robot_ip)
    print script


if __name__ == "__main__":
    #set_robot_base_plane()
    #robot_base = load_robot_base_plane()
    #print robot_base

    #random_walk_draw(robot_base,5.0,50,0.3,0.3)

    """
    robot_ip = ROBOT_IP
    script = ur.popup("tada","tada")
    script = c.concatenate_script(script)
    print script
    c.send_script(script,robot_ip)
    """

    #robot_base = load_robot_base_plane()
    #move_along_crv(robot_base,0.2,0.2)
    #nice_walk(robot_base,150,300,1.5,1.8)
    #random_circles(robot_base,150,20,2.5,1.5)
