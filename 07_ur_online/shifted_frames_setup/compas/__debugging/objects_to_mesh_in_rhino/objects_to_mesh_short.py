__author__     = ['Matthias Rippmann <rippmann@ethz.ch>', ]
__copyright__  = 'Copyright 2016, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__version__    = '0.1'
__date__       = 'Nov 11, 2016'


import time
import math
import copy

from compas.datastructures.mesh.mesh import Mesh
from compas.datastructures.mesh.algorithms.smoothing import mesh_smooth_centroid
from compas.datastructures.mesh.algorithms.tri.topology import remesh
from compas.datastructures.mesh.algorithms.tri.delaunay import delaunay

import compas_rhino.utilities as rhino

import Rhino
import scriptcontext
import rhinoscriptsyntax as rs  



def get_boundary_points(crvs_bound,trg_len):
    crvs = rs.ExplodeCurves(crvs_bound,True)
    if not crvs:  crvs = [crvs_bound]
    div_pts = []
    for crv in crvs:
        div = round(rs.CurveLength(crv)/trg_len,0)
        if div < 1: div = 1
        pts = rs.DivideCurve(crv,div)
        div_pts += pts
        
    div_pts = rs.CullDuplicatePoints(div_pts)
    if crvs: rs.DeleteObjects(crvs)
    return div_pts    
        
def get_boundary_indecies(bound_pts,all_pts): 
    keys = []
    for bound_pt in bound_pts:
        for i,pt in enumerate(all_pts):
            if rs.PointCompare(pt,bound_pt):
                keys.append(str(i))
    return keys   

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

def convert_to_uv_space(srf,pts):
    
    tol = rs.UnitAbsoluteTolerance()
    uv_pts = []
    for pt in pts:
        #need for issues in cases points lie on a seam
        if not rs.IsPointOnSurface (srf, pt):
            pts_dis = []
            pts_dis.append((pt[0]+tol,pt[1],pt[2]))
            pts_dis.append((pt[0]-tol,pt[1],pt[2]))
            pts_dis.append((pt[0],pt[1]+tol,pt[2]))
            pts_dis.append((pt[0],pt[1]-tol,pt[2]))
            pts_dis.append((pt[0],pt[1],pt[2]+tol))
            pts_dis.append((pt[0],pt[1],pt[2]-tol))    
            for pt_dis in pts_dis:
                data= rs.BrepClosestPoint(srf,pt_dis)
                if rs.IsPointOnSurface(srf,data[0]):
                    pt = data[0]
                    break
        u,v = rs.SurfaceClosestPoint(srf,pt)             
        uv_pts.append((u,v,0))
        
        #rs.AddTextDot(str(data[2] ) + " / " + str(rs.IsPointOnSurface (srf, pt)) + " / " + str(u) + " / " + str(v),pt)
    return uv_pts

def wrapper(brep,tolerance,fixed,vis):
    def user_func(mesh,i):
        
        
   
        #dict((k, i) for i, k in self.vertices_enum())
        
        pts = []
        key_index = {}
        count = 0
        for k, a in mesh.vertices_iter(True):
            if k in fixed:
                continue
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
                    mesh.vertex[key]['x'] = points[index][0]
                    mesh.vertex[key]['y'] = points[index][1]
                    mesh.vertex[key]['z'] = points[index][2]
            else:
                print "No"
                pass
            
        
        
        
        if vis:
            if i%vis==0:
                rs.Prompt(str(i))
                draw_light(mesh,temp = True) 
                Rhino.RhinoApp.Wait()
            

        
        
        
            
    return user_func
        
def wrapper_2(crvs,mesh_rhino_obj,fixed,boundary,vis):
  
    def user_func(mesh,i):
        
        
        
        
        pts = []
        key_index = {}
        count = 0
        for k, a in mesh.vertices_iter(True):
            if k in boundary:
                continue
            pts.append((a['x'], a['y'], a['z'])) 
            key_index[k] = count
            count += 1
        if pts:
            points = rs.coerce3dpointlist(pts, True)      
            points = mesh_rhino_obj.PullPointsToMesh(points)
            if len(pts) == len(points):
                #print "Yes"
                for key in key_index:
                    index = key_index[key]
                    mesh.vertex[key]['x'] = points[index][0]
                    mesh.vertex[key]['y'] = points[index][1]
                    mesh.vertex[key]['z'] = points[index][2]
            else:
                print "No"
                pass
        
        
        
        
        
        
        
        mesh_smooth_boundary(mesh,fixed,crvs, k=1, d=0.5)
        
        if vis:
            if i%vis==0:
                rs.Prompt(str(i))
                draw_light(mesh,temp = True) 
                Rhino.RhinoApp.Wait()
    return user_func


def mesh_smooth_boundary(mesh,fixed,crvs, k=1, d=0.5):
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
            if (key in boundary) and (key not in fixed):
                nbrs       = mesh.vertex_neighbours(key)
                points     = [key_xyz[nbr] for nbr in nbrs]
                cx, cy, cz = centroid(points)
                x, y, z    = key_xyz[key]
                tx, ty, tz = d * (cx - x), d * (cy - y), d * (cz - z)
                mesh.vertex[key]['x'] += tx
                mesh.vertex[key]['y'] += ty
                mesh.vertex[key]['z'] += tz
                
                pt = mesh.vertex[key]['x'],mesh.vertex[key]['y'],mesh.vertex[key]['z']
                pt = rs.PointClosestObject(pt,crvs)[1]
                mesh.vertex[key]['x'] = pt[0]
                mesh.vertex[key]['y'] = pt[1]
                mesh.vertex[key]['z'] = pt[2]
                
                

def mesh_to_mesh(rhino_mesh,trg_len,vis):
    
    print rhino_mesh
    crvs = rs.DuplicateMeshBorder(rhino_mesh)
    
    
    
    vertices = [map(float, vertex) for vertex in rs.MeshVertices(rhino_mesh)]
    faces = map(list, rs.MeshFaceVertices(rhino_mesh))
    
    mesh  = Mesh.from_vertices_and_faces(vertices, faces)
    
    
    pts_objs = rs.GetObjects("Fixed Points",1)
    rs.EnableRedraw(False)
    if pts_objs:
        pts_fixed = [rs.PointCoordinates(obj) for obj in pts_objs]
        
        pts = []
        index_key = {}
        count = 0
        for k, a in mesh.vertices_iter(True):
            pts.append((a['x'], a['y'], a['z'])) 
            index_key[count] = k
            count += 1
        
        fixed = [] 
        for pt_fix in pts_fixed:
            index = rs.PointArrayClosestPoint(pts,pt_fix)
            fixed.append(index_key[index])
    
    

      
    edge_lengths = []
    for u, v in mesh.edges():
        edge_lengths.append(mesh.edge_length(u, v))
    target_start = max(edge_lengths)/2  
     
    id = rs.coerceguid(rhino_mesh, True)
    mesh_rhino_obj = rs.coercemesh(id, False)
    
    boundary = set(mesh.vertices_on_boundary())
    user_func = wrapper_2(crvs,mesh_rhino_obj,fixed,boundary,vis)
        
    rs.HideObject(rhino_mesh)
        
    remesh(mesh,trg_len,
       tol=0.1, divergence=0.01, kmax=400,
       target_start=target_start, kmax_approach=200,
       verbose=False, allow_boundary=True,
       ufunc=user_func)  
        
    rs.DeleteObject(rhino_mesh)
    return draw_light(mesh,temp = False) 
    
    
    
    




def nurbs_to_mesh(srf,trg_len,vis):
    
    crvs = rs.DuplicateEdgeCurves(srf) 
    
    if len(crvs)>1:
        joint = rs.JoinCurves(crvs,True)
        if joint:
            if len(joint) > 2:
                print "hole" 
    else:
        if rs.IsCurveClosed(crvs[0]):
            joint = [crvs[0]]
            print "closed"#e.g. if it is a disk
        else:
            print "Surface need to be split"#e.g. if it is a sphere
            return None
         

    
    #sort curves (this is cheating: the longer curve is not necessarily the outer boundary!) 
    #todo: an inside outside comparison in uv space
    crvs_len = [rs.CurveLength(crv) for crv in joint] 
    crvs  = [x for (_,x) in sorted(zip(crvs_len,joint))]
    
    outer_crv =  crvs[-1]
    inner_crvs = crvs[:-1]
    
    outer_bound_pts = get_boundary_points(outer_crv,trg_len)
    if inner_crvs: inner_bounds_pts = [get_boundary_points(crvs,trg_len) for crvs in inner_crvs]
    
    all_pts = copy.copy(outer_bound_pts)
    if inner_crvs: 
        for pts in inner_bounds_pts:
            all_pts += pts
    
    outbound_keys = get_boundary_indecies(outer_bound_pts,all_pts)

    inbounds_keys = []
    if inner_crvs:
        for inner_bound_pts in inner_bounds_pts:
            inbounds_keys.append(get_boundary_indecies(inner_bound_pts,all_pts))   
     

    rs.DeleteObjects(crvs)        

    all_pts_uv = convert_to_uv_space(srf,all_pts) 
    tris = delaunay(all_pts_uv,outbound_keys,inbounds_keys)
    
    mesh = Mesh()
    
    for i,pt in enumerate(all_pts):
        mesh.add_vertex(str(i),{'x' : pt[0], 'y' : pt[1], 'z' : pt[2]})
    for tri in tris:
        mesh.add_face(tri)  
    
    edge_lengths = []
    for u, v in mesh.edges():
        edge_lengths.append(mesh.edge_length(u, v))
    
    target_start = max(edge_lengths)/2

    rs.EnableRedraw(False)
    
    srf_id = rs.coerceguid(srf, True)
    brep = rs.coercebrep(srf_id, False)   
    tolerance = rs.UnitAbsoluteTolerance()
    
    fixed = outbound_keys+[item for sublist in inbounds_keys for item in sublist]
    user_func = wrapper(brep,tolerance,fixed,vis)
    

    remesh(mesh,trg_len,
       tol=0.1, divergence=0.01, kmax=300,
       target_start=target_start, kmax_approach=150,
       verbose=False, allow_boundary=False,
       ufunc=user_func)
 
    for k in xrange(10):
        mesh_smooth_centroid(mesh,fixed=fixed,kmax=1) 
        user_func(mesh,k)
    
    return draw_light(mesh,temp = False) 
    

    
    
    


    