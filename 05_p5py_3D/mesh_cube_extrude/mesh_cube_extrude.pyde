add_library('peasycam')
from mesh_obj import Face, Mesh, Node

def setup():
    size(800,800,P3D)
    cam=PeasyCam(this, 400)
    
    global faces, myMesh
    
    faces=[]
    
    d=100
    d=d/2
    
    v0=Node(-d,-d,-d)
    v1=Node( d,-d,-d)
    v2=Node( d, d,-d)
    v3=Node(-d, d,-d)
    v4=Node(-d,-d, d)
    v5=Node( d,-d, d)
    v6=Node( d, d, d)
    v7=Node(-d, d, d)
        
    faces.append(Face([v0,v3,v2,v1])) 
    faces.append(Face([v0,v1,v5,v4]))
    faces.append(Face([v1,v2,v6,v5]))
    faces.append(Face([v2,v3,v7,v6]))
    faces.append(Face([v0,v4,v7,v3])) 
    faces.append(Face([v4,v5,v6,v7]))
    
    myMesh = Mesh()
    for f in faces:
        myMesh.add_face(f)
        
    #myMesh = myMesh.subdiv_w(0.5)
    myMesh = myMesh.subdiv_g(2,3)
    myMesh = myMesh.subdiv_t(0.5,20)
    myMesh = myMesh.subdiv_t(0.3,5)
        
    #myMesh = myMesh.subdiv_p(100)
    #myMesh = myMesh.subdiv_p(50)
    
def draw():
    background(120)
    global myMesh
    directionalLight(155,0,120,1,0,0)
    directionalLight(255,0,120,-1,0,0)
    
    directionalLight(0,155,120,0,1,0)
    directionalLight(0,255,120,0,-1,0)
    
    directionalLight(0,0,155,0,0,1)
    directionalLight(0,0,255,0,0,-1)
    myMesh.display()
    
def keyPressed():
    global myMesh
    if key=='e':
        myMesh.export_obj(sketchPath()+'/meshexport.obj')
        
    if key=='i':
        myMesh = import_obj(sketchPath()+'/meshexport.obj')
        
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