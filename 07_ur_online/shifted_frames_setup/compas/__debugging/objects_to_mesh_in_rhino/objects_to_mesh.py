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
from compas.geometry.functions import distance
from compas.geometry.spatial import closest_point_on_plane

import compas_rhino.utilities as rhino

import Rhino
import scriptcontext
import rhinoscriptsyntax as rs  


from compas.datastructures.mesh.operations.tri.split import split_edge
from compas.datastructures.mesh.operations.tri.collapse import collapse_edge
from compas.datastructures.mesh.operations.tri.swap import swap_edge

def remesh_ani(srf,mesh,trg_len_min,trg_len_max,gauss_min,gauss_max,
           tol=0.1, divergence=0.01, kmax=100,
           target_start=None, kmax_approach=None,
           verbose=False, allow_boundary=False,
           ufunc=None):
    """Remesh until all edges have a specified target length.

    This involves three operations:

        * split edges that are shorter than a minimum length,
        * collapse edges that are longer than a maximum length,
        * swap edges if this improves the valency error.

    The minimum and maximum lengths are calculated based on a desired target
    length:

    Parameters:
        target (float): The target length.
        tol (float): Length deviation tolerance. Defaults to `0.1`
        kmax (int): The number of iterations.
        verbose (bool): Print feedback messages, if True.

    Returns:
        None
    """
    if verbose:
        print
        print target
        
        
    reduce = 0.63
    max_dis = 0.03   
    min_dis = 0.03
    
    boundary = set(mesh.vertices_on_boundary())
    count = 0
    
  
    kmax_approach = float(kmax_approach)
    for k in xrange(kmax):
        

        
        
        if verbose:
            print
            print k
        count += 1
        # split
        
        
        if count == 1:
            
            
            visited = set()
            for u, v in mesh.edges():
                
                

                
                # is this correct?
                if u in visited or v in visited:
                    continue
                
#                 pt = mesh.edge_midpoint(u,v)
#                 para = rs.SurfaceClosestPoint(srf,pt)
#                 data = rs.SurfaceCurvature(srf,para)
#                 
#                 gauss = abs(data[7]+0.000000000000000000001)
#                 if gauss == 0.0:
#                     gauss = 0.00000000000001
#                 elif gauss > 1.0:
#                     gauss = 1
#                 trg_len = (1-(gauss/1)) * (trg_len_max - trg_len_min) + trg_len_min
#                 
#                 
#                 lmin = (1 - tol) * (4.0 / 5.0) * trg_len
#                 lmax = (1 + tol) * (4.0 / 3.0) * trg_len
#                 fac = float(target_start/trg_len)
#                 
#                 if k <= kmax_approach and 1==1:
#                     scale_val = fac*(1.0-k/kmax_approach)
#                     dlmin = lmin*scale_val
#                     dlmax = lmax*scale_val 
#                 else:
#                     dlmin = 0
#                     dlmax = 0                
                
#                 
#                 if k>200:
#                     rs.AddTextDot(round(gauss,3),pt)
                
                
                l = mesh.edge_length(u, v)
                
                pt = mesh.edge_midpoint(u,v)
                pt2 = rs.BrepClosestPoint (srf, pt)[0]
                dis = distance(pt,pt2)
                
                if dis > max_dis:
                    trg_len = l * reduce  
                else:
                    trg_len = l
                lmin = (1 - tol) * (4.0 / 5.0) * trg_len
                lmax = (1 + tol) * (4.0 / 3.0) * trg_len
                fac = float(target_start/trg_len)
                if k <= kmax_approach and 1==1:
                    scale_val = fac*(1.0-k/kmax_approach)
                    dlmin = lmin*scale_val
                    dlmax = lmax*scale_val 
                else:
                    dlmin = 0
                    dlmax = 0 

                    
#                 if l <= lmax:
#                     continue
                if l <= lmax+dlmax:
                
                    continue
                if verbose:
                    print 'split edge: {0} - {1}'.format(u, v)
                split_edge(mesh, u, v, allow_boundary=allow_boundary)
                visited.add(u)
                visited.add(v)
        # collapse
        elif count == 2:
            visited = set()
            for u, v in mesh.edges():
                
          
                
                # is this correct?
                if u in visited or v in visited:
                    continue
                
  
#                 pt = mesh.edge_midpoint(u,v)
#                 para = rs.SurfaceClosestPoint(srf,pt)
#                 data = rs.SurfaceCurvature(srf,para)
#                 
#                 gauss = abs(data[7]+0.000000000000000000001)
#                 if gauss == 0.0:
#                     gauss = 0.00000000000001
#                 elif gauss > 1.0:
#                     gauss = 1
#                 trg_len = (1-(gauss/1)) * (trg_len_max - trg_len_min) + trg_len_min
#                 
#                 
#                 lmin = (1 - tol) * (4.0 / 5.0) * trg_len
#                 lmax = (1 + tol) * (4.0 / 3.0) * trg_len
#                 fac = float(target_start/trg_len)
#                 
#                 if k <= kmax_approach and 1==1:
#                     scale_val = fac*(1.0-k/kmax_approach)
#                     dlmin = lmin*scale_val
#                     dlmax = lmax*scale_val 
#                 else:
#                     dlmin = 0
#                     dlmax = 0                
#                 
#                 
#                 if k>200:
#                     rs.AddTextDot(round(gauss,3),pt)
                
                l = mesh.edge_length(u, v)

                pt = mesh.edge_midpoint(u,v)
                pt2 = rs.BrepClosestPoint (srf, pt)[0]
                dis = distance(pt,pt2)
                
                if dis < min_dis:
                    trg_len = l 
                else:
                    trg_len = l
                lmin = (1 - tol) * (4.0 / 5.0) * trg_len
                lmax = (1 + tol) * (4.0 / 3.0) * trg_len
                fac = float(target_start/trg_len)
                if k <= kmax_approach and 1==1:
                    scale_val = fac*(1.0-k/kmax_approach)
                    dlmin = lmin*scale_val
                    dlmax = lmax*scale_val 
                else:
                    dlmin = 0
                    dlmax = 0               
                         
                
#                 if l >= lmin:
#                     continue
                if l >= lmin-dlmin:
                    continue
                if verbose:
                    print 'collapse edge: {0} - {1}'.format(u, v)
                collapse_edge(mesh, u, v)
                visited.add(u)
                visited.add(v)
                for nbr in mesh.halfedge[u]:
                    visited.add(nbr)
        # swap
        elif count == 3:
            visited = set()
            for u, v in mesh.edges():
                if u in visited or v in visited:
                    continue
                f1 = mesh.halfedge[u][v]
                f2 = mesh.halfedge[v][u]
                if f1 is None or f2 is None:
                    continue
                v1 = mesh.face[f1][v]
                v2 = mesh.face[f2][u]
                valency1 = mesh.vertex_degree(u)
                valency2 = mesh.vertex_degree(v)
                valency3 = mesh.vertex_degree(v1)
                valency4 = mesh.vertex_degree(v2)
                if u in boundary:
                    valency1 += 2
                if v in boundary:
                    valency2 += 2
                if v1 in boundary:
                    valency3 += 2
                if v2 in boundary:
                    valency4 += 2
                current_error = abs(valency1 - 6) + abs(valency2 - 6) + abs(valency3 - 6) + abs(valency4 - 6)
                flipped_error = abs(valency1 - 7) + abs(valency2 - 7) + abs(valency3 - 5) + abs(valency4 - 5)
                if current_error <= flipped_error:
                    continue
                if verbose:
                    print 'swap edge: {0} - {1}'.format(u, v)
                swap_edge(mesh, u, v)
                visited.add(u)
                visited.add(v)
        # count
        else:
            count = 0
            
        
#             if not has_split and not has_collapsed and not has_swapped and dlmin == 0:
#                 termin += 1
#                 if  termin > 10:
#                     print "break asdddddddddddddddddddddddddddddddddddddddddddddddddddddddd"
#                     break
#             else:
#                 termin = 0
            
        # smoothen
        mesh_smooth_on_local_plane(mesh,k=1,d=0.2,fixed=boundary)  
        if ufunc:
            ufunc(mesh,k)
            

    
          

def mesh_smooth_on_local_plane(mesh, k=1, d=0.5,fixed=None):
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
    boundary = set(fixed)
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
    
def normalize_values(values,old_max,old_min,new_max,new_min):
    old_range = (old_max - old_min)  
    new_range = (new_max - new_min)  
    return [(((old_value - old_min) * new_range) / old_range) + new_min for old_value in values]
    


def nurbs_to_mesh_ani(srf,trg_len_min,trg_len_max,vis):
    trg_len = trg_len_max
    
    
    u_div = 30
    v_div = 30
    u_domain = rs.SurfaceDomain(srf, 0)
    v_domain = rs.SurfaceDomain(srf, 1)
    u = (u_domain[1] - u_domain[0]) / (u_div - 1)
    v = (v_domain[1] - v_domain[0]) / (v_div - 1)
    

    gauss = []
    for i in xrange(u_div):
        for j in xrange(v_div):
            data = rs.SurfaceCurvature (srf, (u_domain[0] + u * i, v_domain[0] + v * j))
            gauss.append(abs(data[7]))
            pt = rs.EvaluateSurface(srf,u_domain[0] + u * i, v_domain[0] + v * j)
            #rs.AddTextDot(round(abs(data[7]),3),pt)
    gauss_max = max(gauss)
    gauss_min = min(gauss)
    
    print gauss_max
    print gauss_min
    

            
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
    
    target_start = max(edge_lengths)/22

    rs.EnableRedraw(False)
    
    srf_id = rs.coerceguid(srf, True)
    brep = rs.coercebrep(srf_id, False)   
    tolerance = rs.UnitAbsoluteTolerance()
    
    fixed = outbound_keys+[item for sublist in inbounds_keys for item in sublist]
    user_func = wrapper(brep,tolerance,fixed,vis)
    

    remesh_ani(srf,mesh,trg_len_min,trg_len_max,gauss_min,gauss_max,
       tol=0.1, divergence=0.008, kmax=400,
       target_start=target_start, kmax_approach=200,
       verbose=False, allow_boundary=False,
       ufunc=user_func)
 
    for k in xrange(1):
        mesh_smooth_on_local_plane(mesh,k=1,d=0.2,fixed=fixed)  
        user_func(mesh,k)
    
    return draw_light(mesh,temp = False)    
    
    


    