__author__     = ['Matthias Rippmann <rippmann@ethz.ch>', ]
__copyright__  = 'Copyright 2016, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__version__    = '0.1'
__date__       = 'Nov 11, 2016'


import time
import rhinoscriptsyntax as rs  
import math
import copy
import Rhino
from compas.datastructures.mesh.mesh import Mesh
from compas.geometry.functions import centroid
from compas.geometry.functions import distance
from compas.geometry.functions import midpoint
from compas.geometry.functions import vector_component
from compas.geometry.functions import angle_smallest

from compas.geometry.arithmetic import add_vectors
from compas.geometry.arithmetic import subtract_vectors

from compas.geometry.transformations import normalize
from compas.geometry.transformations import scale
from compas.utilities.colors import i2rgb
from compas.geometry.spatial import closest_point_on_plane

import compas_rhino.utilities as rhino
from compas.datastructures.mesh.algorithms.smoothing import mesh_smooth_centerofmass
from compas.datastructures.mesh.algorithms.smoothing import mesh_smooth_angle
from compas.datastructures.mesh.algorithms.smoothing import mesh_smooth_centroid
from compas.datastructures.mesh.algorithms.smoothing import  mesh_smooth_area


from compas.datastructures.mesh.algorithms.orientation import mesh_unify_cycle_directions

from compas_rhino.conduits.lines import LinesConduit

#import utility as rhutil
import Rhino
import scriptcontext





def get_faces_from_polylines(polys,points):
    faces = []
    for key in polys:
        poly_points = polys[key]['points']
        indices = []
        for point in poly_points:
            indices.append(str(rs.PointArrayClosestPoint(points,point)))
        faces.append(indices)
    return faces



def get_points_coordinates(objs):
    return [rs.PointCoordinates(obj) for obj in objs]


def get_polyline_points(polylines):
    polys = {}
    for key,id in enumerate(polylines):
        polys[key] = {}
        if not rs.IsCurveClosed(id):
            print str(id) + " is an open curve"
            rs.MessageBox(str(id) + " is an open curve")
            return None
        polys[key]['points'] = rs.PolylineVertices(id)[:-1]
        polys[key]['id'] = id
    return polys


def draw_light(mesh,temp = True):
    
    
    pts = []
    faces = []
    count = 0
    for u,v in mesh.edges():
        pts.append(mesh.vertex_coordinates(u))
        pts.append(mesh.vertex_coordinates(v))
        pts.append((mesh.vertex[u]['x2'],mesh.vertex[u]['y2'],mesh.vertex[u]['z2']))
        pts.append((mesh.vertex[v]['x2'],mesh.vertex[v]['y2'],mesh.vertex[v]['z2']))
        faces.append([count,count+1,count+3,count+2])
        count += 4
        
    guid = rs.AddMesh(pts, faces) 
    if temp:
        Rhino.RhinoApp.Wait()
        rs.Redraw()
#         rs.EnableRedraw(True)
#         rs.EnableRedraw(False)
        rs.DeleteObject(guid)
    return guid 

       
def draw(mesh,dev_threshold):
    srfs = []
    for u,v in mesh.edges():
        pts = []
        pts.append(mesh.vertex_coordinates(u))
        pts.append(mesh.vertex_coordinates(v))
        pts.append((mesh.vertex[u]['x2'],mesh.vertex[u]['y2'],mesh.vertex[u]['z2']))
        pts.append((mesh.vertex[v]['x2'],mesh.vertex[v]['y2'],mesh.vertex[v]['z2']))
        srfs.append(rs.AddSrfPt(pts))
          
        points = rs.coerce3dpointlist(pts, True)
        rc, plane = Rhino.Geometry.Plane.FitPlaneToPoints(points)
        pt3,pt4 = [plane.ClosestPoint(pt) for pt in points[2:]]
            
        distance_max = max([distance(pt1,pt2) for pt1,pt2 in zip(points[2:],[pt3,pt4])])
       
        if distance_max > dev_threshold:
            rs.ObjectColor(srfs[-1],[255,0,0])
            
        

    rs.AddObjectsToGroup(srfs,rs.AddGroup())
    return srfs




def relax_mesh_on_surface():
    
    polylines = rs.ObjectsByLayer("re_02_polys")
    pts_objs = rs.ObjectsByLayer("re_03_points")
   
    
    vis = 5
    kmax = 2000
    dis = 0.3
    dev_threshold = 0.003
    angle_max = 30

    pts = get_points_coordinates(pts_objs)
    
    mesh = Mesh()
    
    for i,pt in enumerate(pts):         
        mesh.add_vertex(str(i),{'x' : pt[0], 'y' : pt[1], 'z' : pt[2]})
    

    
    polys = get_polyline_points(polylines)
    tris = get_faces_from_polylines(polys,pts)
    
    for tri in tris:
        mesh.add_face(tri)     

    
    
    rs.EnableRedraw(False)

    pts = []
    for key, a in mesh.vertices_iter(True):
        
        
        pt1 = (a['x'], a['y'], a['z'])
        pts.append(pt1)
        vec = mesh.vertex_normal(key) 
        vec = scale(normalize(vec),dis)
        pt2 = add_vectors(pt1,vec)
        
        pt2 = add_vectors(pt1,vec)
        a['x2'] = pt2[0]
        a['y2'] = pt2[1]
        a['z2'] = pt2[2]
        
        a['normal'] = vec
        #rs.AddLine(pt1,pt2)
    
    
    faces_1 = draw(mesh,dev_threshold)
    rs.HideObjects(faces_1)
    
    
    for k in range(kmax):
        nodes_top_dict = {key: [] for key in mesh.vertices()}
        polys = []
        max_distances = []
        for u,v in mesh.edges():
            pt1 = mesh.vertex_coordinates(u)
            pt2 = mesh.vertex_coordinates(v)
            pt3 = mesh.vertex[u]['x2'],mesh.vertex[u]['y2'],mesh.vertex[u]['z2']
            pt4 = mesh.vertex[v]['x2'],mesh.vertex[v]['y2'],mesh.vertex[v]['z2']
            points = [pt1,pt2,pt3,pt4]
        
          
            
            points = rs.coerce3dpointlist(points, True)
            rc, plane = Rhino.Geometry.Plane.FitPlaneToPoints(points)
            pt3,pt4 = [plane.ClosestPoint(pt) for pt in points[2:]]
            
            
            vec = scale(normalize(subtract_vectors(pt3,pt1)),dis)
            pt3 = add_vectors(pt1,vec)
            
            vec = scale(normalize(subtract_vectors(pt4,pt2)),dis)
            pt4 = add_vectors(pt2,vec)

            
                        
            nodes_top_dict[u].append(pt3)
            nodes_top_dict[v].append(pt4)
               
            distances = [distance(pt1,pt2) for pt1,pt2 in zip(points[2:],[pt3,pt4])]
            max_distances.append(max(distances))    
                    
        for key, a in mesh.vertices_iter(True):
            cent = centroid(nodes_top_dict[key])
            pt = mesh.vertex_coordinates(key)
            vec = subtract_vectors(cent,pt)  
            norm = a['normal']
            
            if angle_smallest(vec,norm) < angle_max:
                a['x2'] = cent[0]
                a['y2'] = cent[1]
                a['z2'] = cent[2] 
    

    
        if k%vis==0:  
            rs.Prompt("Iteration {0} of {1} with with deviation sum {2}".format(k,kmax,round(sum(max_distances),4)))
            draw_light(mesh,temp = True)  
        if max(max_distances) < dev_threshold or k == kmax:
            print"Iteration {0} of {1} with deviation sum {2}".format(k,kmax,round(sum(max_distances),4))
            break
       

    dfaces_2 = draw(mesh,dev_threshold) 
    rs.ShowObjects(faces_1)  
    rs.EnableRedraw(True)
    print max(max_distances)
    #draw(mesh,"re_03_points","re_02_polys")
    

if __name__ == "__main__":
    
    
    relax_mesh_on_surface()