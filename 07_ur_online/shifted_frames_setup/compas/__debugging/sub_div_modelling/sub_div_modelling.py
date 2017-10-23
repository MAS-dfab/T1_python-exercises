
import time
import rhinoscriptsyntax as rs  
import math
from compas_rhino.datastructures.mesh import RhinoMesh
from compas_rhino.conduits.lines import LinesConduit
import compas_rhino.utilities as rhino

from compas.geometry.arithmetic import add_vectors
from compas.geometry.arithmetic import subtract_vectors
from compas.geometry.functions import distance
from compas.geometry.transformations import normalize
from compas.geometry.transformations import scale


import subdivision_uf
#from compas.datastructures.mesh.algorithms.subdivision import subdivision
from compas.datastructures.mesh.operations.split import split_edge
from compas.datastructures.mesh.algorithms.orientation import mesh_unify_cycle_directions

# check for subdivision http://xrt.wikidot.com/blog:31
# more mesh stuff to implement: 
# - quadrilateralize mesh -> tris to quads  

class RhinoMesh(RhinoMesh):



    # --------------------------------------------------------------------------
    # drawing
    # --------------------------------------------------------------------------
    def draw(self,
             name=None,
             layer=None,
             clear=True,
             redraw=True,
             show_faces=True,
             show_vertices=True,
             show_edges=True,
             vertex_color=None,
             edge_color=None,
             face_color=None,
             show_faces_mesh=False):
        """"""
        # set default options
        if not isinstance(vertex_color, dict):
            vertex_color = {}
        if not isinstance(edge_color, dict):
            edge_color = {}
        if not isinstance(face_color, dict):
            face_color = {}
        self.name  = name or self.name
        self.layer = layer or self.layer
        # delete all relevant objects by name
        objects  = rhino.get_objects(name='{0}.mesh'.format(self.name))
        objects += rhino.get_objects(name='{0}.vertex.*'.format(self.name))
        objects += rhino.get_objects(name='{0}.edge.*'.format(self.name))
        rhino.delete_objects(objects)
        # draw the requested components
        if show_faces:
            faces     = []
            color     = self.color['face']
            polylines = []
            for fkey in self.face:
                face = self.face_coordinates(fkey, ordered=True)
                face_vertices = self.face_vertices(fkey, ordered=True)
                v = len(face)
                if v < 3:
                    print 'Degenerate face: {0} => {1}'.format(fkey, face)
                    continue
                else:
                    #indices = str(face_vertices).replace(',','-').replace('\'','').replace(' ','').replace('[','').replace(']','')
                    polylines.append({
                    'points': face+[face[0]],
                    'name'  : '{0}.face.{1}'.format(self.name,fkey),
                    'layer' : layer
                    
                    
                    })
            rhino.xdraw_polylines(polylines,                               
                               layer=self.layer,
                               clear=clear,
                               redraw=(True if redraw and not (show_edges or show_vertices) else False))
        if show_faces_mesh:
            key_index = dict((key, index) for index, key in self.vertices_enum())
            xyz       = [self.vertex_coordinates(key) for key in self.vertices_iter()]
            faces     = []
            color     = self.color['face']
            for fkey in self.face:
                face = self.face_vertices(fkey, ordered=True)
                v = len(face)
                if v < 3:
                    print 'Degenerate face: {0} => {1}'.format(fkey, face)
                    continue
                if v == 3:
                    faces.append([key_index[k] for k in face + [face[-1]]])
                elif v == 4:
                    faces.append([key_index[k] for k in face])
                else:
                    c = len(xyz)
                    xyz.append(self.face_center(fkey))
                    for i in range(-1, len(face) - 1):
                        key = face[i]
                        nbr = face[i + 1]
                        vertices = [c, key_index[key], key_index[nbr], key_index[nbr]]
                        faces.append(vertices)
            rhino.xdraw_mesh(xyz,
                             faces,
                             color,
                             self.name,
                             layer=self.layer,
                             clear=clear,
                             redraw=(True if redraw and not (show_edges or show_vertices) else False))
        if show_edges:
            lines = []
            color = self.color['edge']
            for u, v in self.edges_iter():
                lines.append({
                    'start': self.vertex_coordinates(u),
                    'end'  : self.vertex_coordinates(v),
                    'name' : '{0}.edge.{1}-{2}'.format(self.name, u, v),
                    'color': edge_color.get((u, v), color),
                })
            rhino.xdraw_lines(lines,
                              layer=self.layer,
                              clear=(True if clear and not show_faces else False),
                              redraw=redraw)#(True if redraw and not show_vertices else False))
        if show_vertices:
            points = []
            color  = self.color['vertex']
            for key in self.vertices_iter():
                points.append({
                    'pos'  : self.vertex_coordinates(key),
                    'name' : '{0}.vertex.{1}'.format(self.name, key),
                    'color': vertex_color.get(key, color),
                })
            rhino.xdraw_points(points,
                               layer=self.layer,
                               clear=(True if clear and not (show_faces or show_edges) else False),
                               redraw=redraw)


  
  
def get_edge_keys_and_param(message='Select edge.',layer=None):
    if layer:
        objs = rs.ObjectsByLayer(layer)
        selectable = []
        for obj in objs:
            if "edge" in rs.ObjectName(obj):
                selectable.append(obj)
    else: selectable = None
    guid = rs.GetObjectEx(message,4,False,False,selectable)
    uv = None
    t = None
    if guid:
        guid = guid[0]
        name = rs.ObjectName(guid).split('.')
        if 'edge' in name:
            pt = rs.GetPointOnCurve(guid,"Select point on edge")
            if not pt: return None,None
            param = rs.CurveClosestPoint(guid,pt)
            lb,ub = rs.CurveDomain(guid)
            t = (param-lb)/(ub-lb)
            print (lb,ub)
            key = name[-1]
            uv = tuple(key.split('-'))
    return uv,t


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


def get_faces_from_polylines(polys,points):
    for key in polys:
        poly_points = polys[key]['points']
        indices = []
        for point in poly_points:
            indices.append(str(rs.PointArrayClosestPoint(points,point)))
        polys[key]['indices'] = indices
    return polys
     
def get_points_from_polylines(polys):
    points = []
    for key in polys:
        points += polys[key]['points']       
    return rs.CullDuplicatePoints(points)

def get_endpoints(lines):
    
    for line in lines:
        points = rs.CurveStartPoint(line),rs.CurveEndPoint(line)
        


def add_sharp_edges(polys,points,sharp_edges):
    fixed_nodes = []
    if sharp_edges:
        for edge in sharp_edges:
            pt1,pt2 = rs.CurveStartPoint(edge),rs.CurveEndPoint(edge)
            index1 = str(rs.PointArrayClosestPoint(points,pt1))
            index2 = str(rs.PointArrayClosestPoint(points,pt2))
            flag1 = False
            flag2 = False
            for key in polys:
                indices = polys[key]['indices']
                for i,index in enumerate(indices):

                    if index == index1:
                        if flag1:
                            #rs.AddTextDot(index,points[int(index)])
                            points.append(points[int(index)])
                            indices[i] = str(len(points)-1)
                        flag1 = True
                    if index == index2:
                        if flag2:
                            #rs.AddTextDot(index,points[int(index)])
                            points.append(points[int(index)])
                            indices[i] = str(len(points)-1)
                        flag2 = True
                polys[key]['indices'] = indices
    return polys,points


def split_face(mesh, fkey, u, v):
    """Split a face by inserting an edge between two specified vertices.

    Parameters:
        fkey (str) : The face key.
        u (str) : The key of the first split vertex.
        v (str) : The key of the second split vertex.

    """
    if u not in mesh.face[fkey] or v not in mesh.face[fkey]:
        raise ValueError('The split vertices do not belong to the split face.')
    if mesh.face[fkey][u] == v:
        raise ValueError('The split vertices are neighbours.')
    d = mesh.face[fkey][u]
    f = [u]
    while True:
        f.append(d)
        if d == v:
            break
        d = mesh.face[fkey][d]
    d = mesh.face[fkey][v]
    g = [v]
    while True:
        g.append(d)
        if d == u:
            break
        d = mesh.face[fkey][d]
    f = mesh.add_face(f)
    g = mesh.add_face(g)
    del mesh.face[fkey]
    return f, g


def add_loop(mesh,uv,t=0.5,steps=1000000):
    
    u,v = uv[0],uv[1]
    #get first face key
    fkey_uv = mesh.halfedge[u][v]
    if not fkey_uv:#if boundary edge
        u,v = uv[1],uv[0]
        fkey_uv = mesh.halfedge[u][v]
        t = 1-t
    else:#if middle edge find boundary if exists
        u_start = u
        v_start = v
        count = 0
        while count < steps:
            for i in range(len(mesh.face[fkey_uv])-2):#go to opposite edge of quad face (reverse order as below; for triagnles)
                u = mesh.face[fkey_uv][u]
            v = mesh.face[fkey_uv][u]
            u,v = v,u
            fkey_uv = mesh.halfedge[u][v]
            if fkey_uv == None:#stop if boundary is reached
                u,v = v,u
                fkey_uv = mesh.halfedge[u][v]
                t = 1-t
                break
            if (u,v) == (u_start,v_start):#stop if loop is closed
                break
            count +=1
    #start inserting edges from u,v computed in the first step
    vkey_1 = split_edge(mesh, u,v, t, allow_boundary=True)
    first_v = vkey_1
    u_2 = vkey_1
    count = 0
    while count < steps:
        for i in range(2):#go to opposite edge of quad face
            u_2 = mesh.face[fkey_uv][u_2]
        v_2 = mesh.face[fkey_uv][u_2]
        if first_v in mesh.face[fkey_uv].keys() and count > 0:#break if closed
            split_face(mesh,fkey_uv, vkey_1, first_v)
            break
        vkey_2 = split_edge(mesh, u_2,v_2, 1-t, allow_boundary=True)
        split_face(mesh,fkey_uv, vkey_1, vkey_2)
        fkey_uv = mesh.halfedge[v_2][vkey_2]
        if not fkey_uv:#break if boundary
            break
        u_2 = vkey_2
        vkey_1 = vkey_2
        count +=1
    
def offset_face(mesh,fkey,t):
    
    cent = mesh.face_centroid(fkey)
    vcords = mesh.face_coordinates(fkey,ordered=True)
    vkeys = mesh.face_vertices(fkey,ordered=True)
    
    pts=[]
    vecs = []

    keys = [None] * len(vcords)
    for i,vcor in enumerate(vcords):
        vec1 = rs.VectorUnitize(rs.VectorCreate(vcords[i-2],vcords[i-1]))
        vec2 = rs.VectorUnitize(rs.VectorCreate(vcords[i],vcords[i-1]))
        vec = rs.VectorAdd(vec1,vec2)
        vec = rs.VectorUnitize(vec)
        ang = rs.VectorAngle(vec,vec1)
        ang = math.radians(ang)
        l = t/ math.sin(ang)
        vec = rs.VectorScale(vec,l)
        pt = rs.PointAdd(vcords[i-1],vec)
        keys[i-1] = mesh.add_vertex(x=pt[0],y=pt[1],z=pt[2])
    for i,vkey in enumerate(vkeys):
        mesh.add_face([vkeys[i],keys[i],keys[i-1],vkeys[i-1]])
    mesh.add_face(keys)
    del mesh.face[fkey]
        
    
    
    
def face_vertices(self, fkey, ordered=False):
    if not ordered:
        return self.face[fkey].keys()
    start = self.face[fkey].keys()[0]
    v = self.face[fkey][start]
    vertices = [start]
    count = 1000
    while count:
        if v == start:
            break
        vertices.append(v)
        v = self.face[fkey][v]
        count -= 1
    return vertices
    
def get_faces(mesh,layer=None):
    out = None
    if layer:
        objs = rs.ObjectsByLayer(layer)
        selectable = []
        for obj in objs:
            if "face" in rs.ObjectName(obj):
                selectable.append(obj)
    else: selectable = None
    
    faces = rs.GetObjects ("Select faces", 4, group=True, preselect=False, select=False, objects=selectable)
    fkeys = []
    if faces:
        for face in faces:
            if face:
                name = rs.ObjectName(face)
                fkey = name.split(".")[-1]
                if fkey: 
                    fkeys.append(fkey)
    return fkeys

def get_vertices(mesh,layer=None):
    out = None
    if layer:
        objs = rs.ObjectsByLayer(layer)
        selectable = []
        for obj in objs:
            if "vertex" in rs.ObjectName(obj):
                selectable.append(obj)
    else: selectable = None
    print selectable
    indices = []
    vertices = rs.GetObjects("Select vertices",1,False,False,False,selectable)
    if vertices:
        for vertex in vertices:
            name = rs.ObjectName(vertex)
            indices.append(name.split(".")[-1])
    return indices


def create_conduit(mesh):
    tic = time.time()
    lines = [(mesh.vertex_coordinates(u), mesh.vertex_coordinates(v)) for u, v in mesh.edges_iter()]
            
    try:
        conduit = LinesConduit(lines)
        conduit.Enabled = True
        conduit.redraw()
    except Exception as e:
        conduit.Enabled = False
        del conduit
        raise e

    tac = time.time()
    print '{0} s for conduit'.format(round(tac-tic,4))
    return conduit

def unweld(mesh,fkey,keys):
    
    face_vkeys = mesh.face_vertices(fkey,ordered=True)
    vkeys = []
    for key in keys:
        x,y,z = mesh.vertex_coordinates(key)
        vkey = mesh.add_vertex(x=x, y=y, z=z)
        vkeys.append(vkey)
        
    for i,key in enumerate(face_vkeys):
        try:
            index = keys.index(key)
            face_vkeys[i]= vkeys[index]
        except:
            pass
    mesh.add_face(face_vkeys)
    del mesh.face[fkey]
    
    mesh_unify_cycle_directions(mesh)

#create mesh from polylines
polylines = rs.GetObjects("Select Polylines",4)
polys = get_polyline_points(polylines)
points = get_points_from_polylines(polys)
polys = get_faces_from_polylines(polys,points)
mesh_faces = [polys[key]['indices'] for key in polys]
mesh_vertices = points

mesh_obj = RhinoMesh.from_vertices_and_faces(mesh_vertices,mesh_faces)
mesh_unify_cycle_directions(mesh_obj)

#get fixed nodes
fixed=[]
fixed_objs = rs.ObjectsByLayer("SD_fixed")
fixed_coords = [rs.PointCoordinates(obj) for obj in fixed_objs]
if fixed_objs:
    for i,vertex in enumerate(mesh_vertices):
        index = rs.PointArrayClosestPoint(fixed_coords,vertex)
        if rs.Distance(fixed_coords[index],vertex)<0.1:
            fixed.append(str(i))


rs.DeleteObjects(polylines)


steps = 2

if 1 == 1:
    break_flag = False
    selection = ""
    dis = 0.1
    

    
    
    while True:
        mesh_obj.draw(name="control",
                     layer="SD_mesh",
                     clear=True,
                     redraw=True,
                     show_faces=True,  # rename to display_faces?
                     show_vertices=True,  # rename to display_vertices?
                     show_edges=True,  # rename to display_edges?
                     vertex_color=None,
                     edge_color=None,
                     face_color=None)
        tic = time.time()
         
        sub_mesh_obj =  mesh_obj.copy()
        subdivision_uf.catmullclark_subdivision(sub_mesh_obj,k=steps,fixed=fixed)
        lines = [(sub_mesh_obj.vertex_coordinates(u), sub_mesh_obj.vertex_coordinates(v)) for u, v in sub_mesh_obj.edges_iter()]
 
        try:
            conduit.Enabled = False
            del conduit
        except: pass
 
        try:
            conduit = LinesConduit(lines,thickness=1, color=[255,255,255])
            conduit.Enabled = True
            conduit.redraw()
        except Exception as e:
            conduit.Enabled = False
            del conduit
            raise e       
        
 
        selection = rs.GetString("Commands: ",selection,["offset","split","unweld","move_vertex","extrude_face","steps"])
        if not selection: break_flag = True
        if selection == "offset":
            fkeys = get_faces(mesh_obj,"SD_mesh")
            dis = rs.GetReal("Offset value",dis)
            if fkeys and dis:
                for fkey in fkeys:
                    offset_face(mesh_obj,fkey,dis)
             
        if selection == "split":
            uv,t = get_edge_keys_and_param(layer="SD_mesh")
            if uv: 
                add_loop(mesh_obj,uv,t)
                 
                 
        if selection == "unweld":
            fkeys = get_faces(mesh_obj,"SD_mesh")
            keys = get_vertices(mesh_obj,"SD_mesh")
            for fkey in fkeys: 
                if fkey and keys:
                    face_vertices = mesh_obj.face_vertices(fkey)
                    legal_keys = []
                    for key in keys:
                        if key in face_vertices: 
                            legal_keys.append(key)
                    if legal_keys: unweld(mesh_obj,fkey,legal_keys)
        
        if selection == "move_vertex":
            keys = get_vertices(mesh_obj,"SD_mesh")
            
            if keys:
                pt1 = rs.GetPoint("from point")
                pt2 = rs.GetPoint("to point")
                
                
                vec = subtract_vectors(pt2,pt1)
                for key in keys:
                    point = mesh_obj.vertex_coordinates(key)
                    x,y,z = add_vectors(point,vec)
                    mesh_obj.vertex[key]['x'] = x
                    mesh_obj.vertex[key]['y'] = y
                    mesh_obj.vertex[key]['z'] = z 
        
        if selection == "extrude_face":
            fkey = get_faces(mesh_obj,"SD_mesh")[0]  
            
            norm = mesh_obj.face_normal(fkey,unitized=True)
            cent = mesh_obj.face_centroid(fkey)      
            pts = mesh_obj.face_coordinates(fkey, ordered=False)
            pts = rs.BoundingBox(pts)
            dis = distance(pts[0],pts[6])*2
            
            
            pt1 = add_vectors(cent,scale(norm,dis))
            pt2 = add_vectors(cent,scale(norm,-dis))
            
            line = rs.AddLine(pt1,pt2)
            pt_line = rs.GetPointOnCurve(line,"Pick Point on line")
            rs.DeleteObjects(line)
            vec = subtract_vectors(pt_line,cent)
                
            keys = mesh_obj.face_vertices(fkey, ordered=True)
        
            new_keys = []
            for key in keys:
                point = mesh_obj.vertex_coordinates(key)
                x,y,z = add_vectors(point,vec)
                new_keys.append(mesh_obj.add_vertex(x=x, y=y, z=z))
            
            mesh_obj.delete_face(fkey)
            
            mesh_obj.add_face(new_keys) 
            
            for i,key in enumerate(keys):
                mesh_obj.add_face([keys[i-1],keys[i],new_keys[i],new_keys[i-1]]) 
            
            
                    
                     
        if selection == "steps": 
            steps = rs.GetInteger("Subdivision steps",steps,1,5)     
#        mesh_obj.draw(name="control",
#                     layer="SD_mesh",
#                     clear=False,
#                     redraw=True,
#                     show_faces=False,  # rename to display_faces?
#                     show_vertices=False,  # rename to display_vertices?
#                     show_edges=False,  # rename to display_edges?
#                     vertex_color=None,
#                     edge_color=None,
#                     face_color=None,
#                     show_faces_mesh=True)
#        print mesh_obj
#        break

        if break_flag:
            
            try:
                conduit.Enabled = False
                del conduit
            except: pass
            break
            

objs = rs.ObjectsByLayer("SD_mesh")
if objs: rs.DeleteObjects(objs)

mesh_obj.draw(name="control",
             layer="Default",
             clear=False,
             redraw=True,
             show_faces=True,  # rename to display_faces?
             show_vertices=True,  # rename to display_vertices?
             show_edges=False,  # rename to display_edges?
             vertex_color=None,
             edge_color=None,
             face_color=None,
             show_faces_mesh=True)
             
             
sub_mesh_obj.draw(name="subdi",
             layer="SD_sub_mesh",
             clear=False,
             redraw=True,
             show_faces=False,  # rename to display_faces?
             show_vertices=False,  # rename to display_vertices?
             show_edges=False,  # rename to display_edges?
             vertex_color=None,
             edge_color=None,
             face_color=None,
             show_faces_mesh=True)
             
             
             
             
             
             
             



#key_index = dict((key, index) for index, key in mesh_obj.vertices_enum())
#xyz = [mesh_obj.vertex_coordinates(key) for key in mesh_obj.vertices_iter()]
#faces = []
#for fkey in mesh_obj.faces_iter():
#    face = mesh_obj.face_vertices(fkey,True)
#    face.append(face[-1])
#    faces.append([key_index[k] for k in face])
#if 1 == 1:
#    guid = rs.AddMesh(xyz, faces) 
#    polys = []
#else:
#    for fkey in faces:
#        pts = []
#        for key in fkey:
#            pts.append(xyz[key])
#        pts.append(xyz[fkey[0]])
#        rs.AddPolyline(pts)