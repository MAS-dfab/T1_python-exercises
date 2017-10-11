add_library('peasycam')
from mesh_obj import Face, Mesh, Node

def setup():
    size(800,800,P3D)
    cam=PeasyCam(this, 400)
    
    global myMesh
    
    n1 = Node(-100,-100,0)
    n2 = Node( 100,-100,0)
    n3 = Node( 100, 100,0)
    n4 = Node(-100, 100,0)
    f = Face([n1,n2,n3,n4])
    myMesh = Mesh()
    myMesh.add_face(f)
    
def draw():
    background(255)
    global myMesh
    myMesh.display()
    
def keyPressed():
    global myMesh
    if key=='e':
        myMesh.export_obj(sketchPath()+'/meshexport.obj')
        
    if key=='i':
        myMesh = import_obj(sketchPath()+'/meshexport.obj')
        
    if key=='s':
        myMesh = myMesh.city_subdivide()
        
def import_obj(path):
    input_file = open(path,'r')
    lines = input_file.readlines()
    input_file.close()
    mesh = Mesh()
    for l in lines:
        parts = l.split(' ')
        if parts[0]=='v':
            x,y,z = [float(c) for c in parts[1:]]
            mesh.nodes.append(Node(x,y,z))
        elif parts[0]=='f':
            mesh.add_face(Face([mesh.nodes[int(i)-1] for i in parts[1:]]))
        else:
            continue
    print len(mesh.nodes),len(mesh.faces)
        
    return mesh