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
from compas.datastructures.mesh.algorithms.smoothing import mesh_smooth_centroid

#import utility as rhutil
import Rhino
import scriptcontext


def mesh_smooth_on_local_plane(mesh, k=1, d=0.5,boundary=None):
    """Smoothen the input mesh by moving each vertex to the centroid of its
    neighbours.

    Note:
        This is a node-per-node version of Laplacian smoothing with umbrella weights.

    Parameters:
        k (int): The number of smoothing iterations.
            Defaults to `1`.
        d (float): Scale factor for (i.e. damping of) the displacement vector.
            Defaults to `0.5`.

    Returns:
        None
    """
    def centroid(points):
        p = len(points)
        return [coord / p for coord in map(sum, zip(*points))]
    boundary = set(mesh.vertices_on_boundary())
    for _ in range(k):
        key_xyz = dict((key, (attr['x'], attr['y'], attr['z'])) for key, attr in mesh.vertices_iter(True))
        for key in key_xyz:
            if key in boundary:
                continue
            nbrs       = mesh.vertex_neighbours(key)
            points     = [key_xyz[nbr] for nbr in nbrs]
            cx, cy, cz = centroid(points)
            x, y, z    = key_xyz[key]
            tx, ty, tz = d * (cx - x), d * (cy - y), d * (cz - z)
            
            x += tx
            y += ty
            z += tz
            
            n = mesh.vertex_normal(key)
            x,y,z = closest_point_on_plane(key_xyz[key], n,(x,y,z))
            
            mesh.vertex[key]['x'] = x
            mesh.vertex[key]['y'] = y
            mesh.vertex[key]['z'] = z
            
            
            
def mesh_pull_to_surface(mesh,brep,max_srf_dis,tolerance):            
    pts = []
    key_index = {}
    count = 0
    for k, a in mesh.vertices_iter(True):
#         if k in fixed:
#             continue
        pts.append((a['x'], a['y'], a['z'])) 
        key_index[k] = count
        count += 1
    if pts:
        points = rs.coerce3dpointlist(pts, True)      
        points = brep.Faces[0].PullPointsToFace(points, tolerance)
        if len(pts) == len(points):
            #print "Yes"
            for key in key_index:
                index = key_index[key]
                
                if distance(points[index],pts[index])> max_srf_dis:
                    vec = subtract_vectors(pts[index],points[index])
                    vec = normalize(vec)
                    vec = scale(vec,max_srf_dis)
                    x,y,z = add_vectors(points[index],vec)
                    
                    
                    mesh.vertex[key]['x'] = x
                    mesh.vertex[key]['y'] = y
                    mesh.vertex[key]['z'] = z
        else:
            print "No" 
            pass            
            
            

def draw_light(mesh,temp = True):
    key_index = dict((key, index) for index, key in mesh.vertices_enum())
    xyz = mesh.xyz
    faces = []
    for fkey in mesh.faces_iter():
        face = mesh.face_vertices(fkey,True)
        face.append(face[-1])
        faces.append([key_index[k] for k in face])
    guid = rs.AddMesh(xyz, faces) 
    if temp:
        rs.EnableRedraw(True)
        rs.EnableRedraw(False)
        rs.DeleteObject(guid)
    return guid  


def space_points(pt1,pt2,trg_dis):
    mid_pt = midpoint(pt1,pt2)
    vec = subtract_vectors(pt1,pt2)
    vec = normalize(vec)
    vec = scale(vec,trg_dis*0.5)
    pt1 = add_vectors(mid_pt,vec)
    pt2 = add_vectors(mid_pt,scale(vec,-1))
    return pt1,pt2


def mesh_max_deviation(mesh):
    
    max_distances = []
    for fkey in mesh.faces_iter():
                   
        keys = mesh.face_vertices(fkey,ordered=True)
        points = [mesh.vertex_coordinates(key) for key in keys]
        
        points = rs.coerce3dpointlist(points, True)
        rc, plane = Rhino.Geometry.Plane.FitPlaneToPoints(points)
        points_planar = [plane.ClosestPoint(pt) for pt in points]
        
        distances = [distance(pt1,pt2) for pt1,pt2 in zip(points,points_planar)]
        max_distances.append(max(distances))
    return max(max_distances)

def color_mesh(mesh,dis_ub,dis_lb):
    
    max_distances = []
    mesh_faces = []
    for fkey in mesh.faces_iter():
                   
        keys = mesh.face_vertices(fkey,ordered=True)
        points = [mesh.vertex_coordinates(key) for key in keys]
        plane = rs.PlaneFitFromPoints(points)
        points_planar = [rs.PlaneClosestPoint(plane, pt) for pt in points] 
        distances = [distance(pt1,pt2) for pt1,pt2 in zip(points,points_planar)]
        max_distances.append(max(distances))
        mesh_faces.append(rs.AddMesh(points,[(0,1,2,3)]))
        
    values = normalize_values(max_distances,dis_ub,dis_lb,1,0)
    
    for i,face in enumerate(mesh_faces):
        rs.ObjectColor(face,i2rgb(values[i]))
    return mesh_faces

    
        
          
    
def normalize_values(values,old_max,old_min,new_max,new_min):
    old_range = (old_max - old_min)  
    new_range = (new_max - new_min)  
    return [(((old_value - old_min) * new_range) / old_range) + new_min for old_value in values]
    


def create_quad_mesh(srf,u_div,v_div):
    
  
    
    u_domain = rs.SurfaceDomain(srf, 0)
    v_domain = rs.SurfaceDomain(srf, 1)
    u = (u_domain[1] - u_domain[0]) / (u_div - 1)
    v = (v_domain[1] - v_domain[0]) / (v_div - 1)
    
    #pts =  [[None for i in range(v_div)] for j in range(u_div)]
    mesh_pts = []
    for i in xrange(u_div):
        for j in xrange(v_div):
            #pts[i][j] = rs.EvaluateSurface (srf, u_domain[0] + u * i, v_domain[0] + v * j)
            mesh_pts.append(rs.EvaluateSurface (srf, u_domain[0] + u * i, v_domain[0] + v * j))
            
    faces = []        
    for i in xrange(u_div-1):
         for j in xrange(v_div-1):       
             faces.append(((i*v_div)+j,((i+1)*v_div)+j,((i+1)*v_div)+j+1,(i*v_div)+j+1))

    mesh = Mesh()
    
    for i,pt in enumerate(mesh_pts):
        mesh.add_vertex(str(i),{'x' : pt[0], 'y' : pt[1], 'z' : pt[2]})
    
    for face in faces:
        mesh.add_face(face)  
    
    return mesh        

if __name__ == "__main__":
    
    srf = rs.GetObject("Select Surface",8)
    
#     srf_trg = rs.GetObject("Select Target Surface",8)
#     srf_id = rs.coerceguid(srf_trg, True)
#     brep = rs.coercebrep(srf_id, False)   
#     tolerance = rs.UnitAbsoluteTolerance()
    
    rs.EnableRedraw(False)
    
    rs.HideObject(srf)
    
    u_div = rs.GetInteger("Panel division in u direction",20)
    v_div = rs.GetInteger("Panel division in v direction",12)
    
    dev_threshold = rs.GetReal("Threshold in m",0.01)
    
    mesh = create_quad_mesh(srf,u_div,v_div)

    max_dev = mesh_max_deviation(mesh)
    mesh_faces = color_mesh(mesh,max_dev,0)
    rs.AddObjectsToGroup(mesh_faces,rs.AddGroup())
    rs.HideObjects(mesh_faces)
    
    kmax = 1000


    vis = 2


    diagonal_prop = 0.15
    edge_prop = 0.1
    
    edge_min = 1
    edge_max = 5
    max_srf_dis = 1
    
    

    
    
    boundary = mesh.vertices_on_boundary()
    boundary = []
    
    
#     diagonal = {}
#     for fkey in mesh.faces_iter():
#         keys = mesh.face_vertices(fkey, ordered=True)
#         if len(keys) == 4:
#             dis1 = distance(mesh.vertex_coordinates(keys[0]),mesh.vertex_coordinates(keys[2]))
#             dis1_min, dis1_max = dis1*(1-diagonal_fac),dis1*(1+diagonal_fac)
#             dis2 = distance(mesh.vertex_coordinates(keys[1]),mesh.vertex_coordinates(keys[3]))
#             dis2_min, dis2_max = dis2*(1-diagonal_fac),dis2*(1+diagonal_fac)
#             diagonal[fkey] = dis1_min,dis1_max,dis2_min,dis2_max
#             
#     edges_dis = {}
#     for uv in mesh.edges():
#         dis = mesh.edge_length(uv[0], uv[1])
#         dis_min, dis_max = dis*(1-edge_fac),dis*(1+edge_fac)
#         edges_dis[uv] = dis_min, dis_max
    
    for k in range(kmax):
        
        if 1 == 1:
        
        
            max_dev_step = mesh_max_deviation(mesh)
        
            nodes_dict = {key: [] for key in mesh.vertices()}
            dots = []
            for fkey in mesh.faces_iter():
                
                keys = mesh.face_vertices(fkey,ordered=True)
                points = [mesh.vertex_coordinates(key) for key in keys]
                
                points = rs.coerce3dpointlist(points, True)
                rc, plane = Rhino.Geometry.Plane.FitPlaneToPoints(points)
                points = [plane.ClosestPoint(pt) for pt in points]
    
    #             dis1_min, dis1_max,dis2_min,dis2_max= diagonal[fkey] 
                
                if 1==1:
                    dis1_step = distance(points[0],points[2])
                    dis2_step = distance(points[1],points[3])
                    
                    if dis1_step > dis2_step:
                        if (dis1_step-dis2_step)/dis1_step > diagonal_prop:
                            trg_dis = -dis2_step/(diagonal_prop-1)
                            points[0],points[2] = space_points(points[0],points[2],trg_dis)
                            #rs.AddLine(points[0],points[2])
                    else:
                        if (dis2_step-dis1_step)/dis2_step > diagonal_prop:
                            trg_dis = -dis1_step/(diagonal_prop-1)
                            points[1],points[3] = space_points(points[1],points[3],trg_dis)
                            #rs.AddLine(points[1],points[3])    
                
                
    #             if dis1_step < dis1_min:
    #                 trg_dis = dis1_min
    #             elif dis1_step > dis1_max:
    #                 trg_dis = dis1_max
    #             else:
    #                 trg_dis = None
    #             if trg_dis:
    #                 space_points(points[0],points[2],trg_dis)
    #                 rs.AddLine(points[0],points[2])
    #                 
    #                 
    #             if dis2_step < dis2_min:
    #                 trg_dis = dis2_min
    #             elif dis2_step > dis2_max:
    #                 trg_dis = dis2_max
    #             else:
    #                 trg_dis = None
    #             if trg_dis:
    #                 space_points(points[1],points[3],trg_dis)
    #                 rs.AddLine(points[1],points[3])            
                dis1_step = distance(points[0],points[1])
                dis2_step = distance(points[2],points[3])
                if dis1_step > dis2_step:
                    if (dis1_step-dis2_step)/dis1_step > edge_prop:
                        trg_dis = -dis2_step/(edge_prop-1)
                        points[0],points[1] = space_points(points[0],points[1],trg_dis)
                        #rs.AddLine(points[0],points[1])
                else:
                    if (dis2_step-dis1_step)/dis2_step > edge_prop:
                        trg_dis = -dis1_step/(edge_prop-1)
                        points[2],points[3] = space_points(points[2],points[3],trg_dis)
                        #rs.AddLine(points[2],points[3])     
                                
                dis1_step = distance(points[1],points[2])
                dis2_step = distance(points[3],points[0])            
                if dis1_step > dis2_step:
                    if (dis1_step-dis2_step)/dis1_step > edge_prop:
                        trg_dis = -dis2_step/(edge_prop-1)
                        points[1],points[2] = space_points(points[1],points[2],trg_dis)
                        #rs.AddLine(points[1],points[2])
                else:
                    if (dis2_step-dis1_step)/dis2_step > edge_prop:
                        trg_dis = -dis1_step/(edge_prop-1)
                        points[3],points[0] = space_points(points[3],points[0],trg_dis)
                        #rs.AddLine(points[3],points[0])             
                
                
                
                
                for i,key in enumerate(keys):
                    nodes_dict[key].append(points[i])
            
            
            
                    
            for key in mesh.vertices():
                if key in boundary:
                    continue
                cent = centroid(nodes_dict[key])
                mesh.vertex[key]['x'] = cent[0]
                mesh.vertex[key]['y'] = cent[1]
                mesh.vertex[key]['z'] = cent[2]   
                
                
            nodes_dict = {key: [] for key in mesh.vertices()}    
            for uv in mesh.edges():
                dis_step = mesh.edge_length(uv[0], uv[1])
                        
                if dis_step < edge_min:
                    trg_dis = edge_min
                elif dis_step > edge_max:
                    trg_dis = edge_max
                else:
                    trg_dis = None
                if trg_dis:
                    pt1 = mesh.vertex_coordinates(uv[0])
                    pt2 = mesh.vertex_coordinates(uv[1])
                    pt1,pt2 = space_points(pt1,pt2,trg_dis)
                    
                    nodes_dict[uv[0]].append(pt1)
                    nodes_dict[uv[1]].append(pt2)
                    
                    #rs.AddLine(pt1,pt2) 
            
            for key in nodes_dict:
                if key in boundary:
                    continue
                cent = centroid(nodes_dict[key])
                if cent:
                    mesh.vertex[key]['x'] = cent[0]
                    mesh.vertex[key]['y'] = cent[1]
                    mesh.vertex[key]['z'] = cent[2] 
            #rs.AddPoints(points)
            
            #rhino_mesh = draw_light(mesh,temp = False)   
        
        mesh_smooth_on_local_plane(mesh, k=1, d=0.01)
        
        #mesh_pull_to_surface(mesh,brep,max_srf_dis,tolerance)
        
        if k%vis==0:  
            rs.Prompt("Iteration {0} of {1} with a maximum deviation of {2}".format(k,kmax,round(max_dev_step,4)))
            #draw_light(mesh,temp = True)  
            mesh_faces = color_mesh(mesh,max_dev,0)
            rs.Redraw()
            Rhino.RhinoApp.Wait()
            rs.DeleteObjects(mesh_faces)
        if max_dev_step < dev_threshold or k == kmax:
            print"Iteration {0} of {1} with a maximum deviation of {2}".format(k,kmax,round(max_dev_step,4))
            break
    
    #draw_light(mesh,temp = False)  
    mesh_faces = color_mesh(mesh,max_dev,0)
    rs.AddObjectsToGroup(mesh_faces,rs.AddGroup())

