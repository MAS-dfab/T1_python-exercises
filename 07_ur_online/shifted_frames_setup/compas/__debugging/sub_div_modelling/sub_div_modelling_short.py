import rhinoscriptsyntax as rs  

from compas_rhino.datastructures.mesh import RhinoMesh
import compas_rhino.utilities as RhinoBRG

from compas.datastructures.mesh.algorithms.subdivision import subdivision


#start mesh sub division modelling
polylines = rs.GetObjects("Select Polylines",4)

mesh_obj = RhinoMesh.from_polylines(polylines)
mesh_unify_cycle_directions(mesh_obj)


while True:
    #draw control mesh
    mesh_obj.draw(name="control",layer="SD_control")
    #generate and draw subdivision mesh
    sub_mesh_obj = subdivision.catmullclark_subdivision(steps)
    sub_mesh_obj.draw(name="sub_div",layer="SD_mesh")
    
    selection = rs.GetString("Commands: ",selection,["offset","split","unweld","move_vertex","extrude_face","steps"])

    if selection == "offset":
        fkeys = RhinoBRG.get_face(mesh_obj)
        dis = rs.GetReal("Offset value",dis)
        offset_face(mesh_obj,fkey,dis)
         
    elif selection == "split":
        uv,t = RhinoBRG.get_edge_keys_and_param(mesh_obj)
        add_loop(mesh_obj,uv,t)
             
    # more modifications...
            

sub_mesh_obj = subdivision.catmullclark_subdivision(steps)
sub_mesh_obj.draw(name="sub_div",layer="SD_mesh")
             
             
             
             
             
             
             



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