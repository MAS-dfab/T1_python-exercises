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
    key_index = dict((key, index) for index, key in mesh.vertices_enum())
    xyz = mesh.xyz
    faces = []
    
    for fkey in mesh.faces_iter():
        face = mesh.face_vertices(fkey,True)
        
        
        #poly_pts = [xyz[key_index[k]] for k in face+[face[0]]]
        
        face.append(face[-1])
        faces.append([key_index[k] for k in face])
        
        
    
        #rs.AddPolyline(poly_pts)
        
    guid = rs.AddMesh(xyz, faces) 
    if temp:
        rs.EnableRedraw(True)
        rs.EnableRedraw(False)
        rs.DeleteObject(guid)
    return guid 

def draw(mesh,layer_1,layer_2):
    
    rs.EnableRedraw(False)
    
    rs.LayerVisible(layer_1, True)
    rs.LayerVisible(layer_2, True)

    objs = rs.ObjectsByLayer(layer_1)
    rs.DeleteObjects(objs)
    objs = rs.ObjectsByLayer(layer_2)
    rs.DeleteObjects(objs)    
    
    pts_objs = []
    for key, a in mesh.vertices_iter(True):
    
       pt = (a['x'], a['y'], a['z'])
       
       pts_objs.append(rs.AddPoint(pt))
       rs.ObjectColor(pts_objs[-1],a['color'] )
       
    rs.ObjectLayer(pts_objs,layer_1)
        
        
    key_index = dict((key, index) for index, key in mesh.vertices_enum())
    xyz = mesh.xyz    
    polylines = []
    for fkey in mesh.faces_iter():
        face = mesh.face_vertices(fkey,True)
        
        
        poly_pts = [xyz[key_index[k]] for k in face+[face[0]]]
        polylines.append(rs.AddPolyline(poly_pts))
        
    rs.ObjectLayer(polylines,layer_2)
    
        
        

    rs.EnableRedraw(True)
       




def wrapper(vis):
    
    def user_function(mesh,i):
     
        for key, a in mesh.vertices_iter(True):
        
           pt = (a['x'], a['y'], a['z'])
           
           if a['type'] == 'fixed' or a['type'] == 'free':
               continue
           if a['type'] == 'guide':
               point = rs.coerce3dpoint(pt)
               rc, t = a['guide_crv'].ClosestPoint(point)
               pt = a['guide_crv'].PointAt(t)
           elif a['type'] == 'surface':
               point = rs.coerce3dpoint(pt)
               pt = a['guide_srf'].ClosestPoint(point)
            
           mesh.vertex[key]['x'] = pt[0]
           mesh.vertex[key]['y'] = pt[1]
           mesh.vertex[key]['z'] = pt[2]    
        
        
        if vis:
            if i%vis==0:
                rs.Prompt(str(i))
                draw_light(mesh,temp = True) 
                Rhino.RhinoApp.Wait()

    return user_function


def relax_mesh_on_surface():
    
    srf = rs.ObjectsByLayer("re_01_trg_srf")[0]
    srf_id = rs.coerceguid(srf, True)
    brep = rs.coercebrep(srf_id, False)
    
    polylines = rs.ObjectsByLayer("re_02_polys")
    pts_objs = rs.ObjectsByLayer("re_03_points")
    guides = rs.ObjectsByLayer("re_04_guides")
    
    vis = 1
    
    rs.LayerVisible("re_02_polys", False)
    rs.LayerVisible("re_03_points", False)
    
    pts = get_points_coordinates(pts_objs)
    
    mesh = Mesh()
    
    for i,pt in enumerate(pts):
        color = rs.ObjectColor(pts_objs[i])
        type, guide_srf,guide_crv = None, None, None

        if [rs.ColorRedValue(color),rs.ColorGreenValue(color),rs.ColorBlueValue(color)] == [255,0,0]:
            type = 'fixed'
        elif [rs.ColorRedValue(color),rs.ColorGreenValue(color),rs.ColorBlueValue(color)] == [255,255,255]:
            type = 'free'
        elif [rs.ColorRedValue(color),rs.ColorGreenValue(color),rs.ColorBlueValue(color)] == [0,0,0]:
            type = 'surface'
            guide_srf = brep
        else:
            type = 'guide'
            for guide in guides:
                if rs.ObjectColor(guide) == color:
                    crv_id = rs.coerceguid(guide, True)
                    crv = rs.coercecurve(crv_id, False)
                    guide_crv = crv
                    break       
            
        mesh.add_vertex(str(i),{'x' : pt[0], 'y' : pt[1], 'z' : pt[2], 'color' : color, 'type' : type,'guide_srf' : guide_srf,'guide_crv' : guide_crv})
    

    
    polys = get_polyline_points(polylines)
    tris = get_faces_from_polylines(polys,pts)
    
    for tri in tris:
        mesh.add_face(tri)     
     
     
        
    user_function = wrapper(vis)    
    fixed = [key for key, a in mesh.vertices_iter(True) if a['type'] == 'fixed']
    
    mesh_smooth_centerofmass(mesh, fixed=fixed, kmax=150, d=1.0, ufunc=user_function)
    
    #mesh_smooth_angle(mesh, fixed=fixed, kmax=150, ufunc=user_function)
    
    #mesh_smooth_centroid(mesh, fixed=fixed, kmax=150, d=1.0, ufunc=user_function)
    
    #mesh_smooth_area(mesh, fixed=fixed, kmax=150, d=1.0, ufunc=user_function)
    
    
    #draw_light(mesh,temp = False)
    
    draw(mesh,"re_03_points","re_02_polys")
    

if __name__ == "__main__":
    
    
    relax_mesh_on_surface()