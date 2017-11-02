import rhinoscriptsyntax as rs  
from compas_rhino.datastructures.mesh import RhinoMesh
  
  
srf = rs.GetObject("Select Surface",8)   
 
u_div = 20
v_div = 12
kmax = 1000
vis = 2

mesh = RhinoMesh.from_surface(srf,u_div,v_div)

for k in range(kmax):
    
    nodes_dict = {key: [] for key in mesh.vertices()}
    for fkey in mesh.faces_iter():
        
        # planarize mesh face
        keys,points = mesh.face_vertices_and_coordinates(fkey,ordered=True)
        points_planar = mesh.face_planarize(fkey)
        
        # store "disconnected" vertices               
        for i,key in enumerate(keys):
            nodes_dict[key].append(points_planar[i])

    # insert additional constraints here:
    # e.g.: length constraints, angle constraints, etc.
      
    # connect "disconnected" vertices        
    for key in mesh.vertices():
        cent = centroid(nodes_dict[key])
        mesh.vertex[key]['x'] = cent[0]
        mesh.vertex[key]['y'] = cent[1]
        mesh.vertex[key]['z'] = cent[2]   
                
    if k%vis == 0:
        mesh.draw(name="planar_mesh",layer="planar")  
            
mesh.draw(name="planar_mesh",layer="planar")       


