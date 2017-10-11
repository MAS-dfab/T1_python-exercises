add_library('peasycam')
from mesh_obj import Face, Mesh, Node

def setup():
    size(800,800,P3D)
    cam=PeasyCam(this, 400)
    noStroke()
    
    global faces, myMesh
    
    faces=[]
    
    d=90
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
        
    myMesh = hilbert_3d(myMesh,2)
        
    #myMesh = myMesh.subdiv_w(0.5)
    # myMesh = myMesh.subdiv_g(2,3)
    # myMesh = myMesh.subdiv_t(0.5,20)
    # myMesh = myMesh.subdiv_t(0.3,5)
        
    # for i in range(1,3):
    #     myMesh = myMesh.subdiv_p(50/float(i))
    #myMesh = myMesh.subdiv_p(50)
    
def draw():
    background(77)
    directionalLight(255,128,0,1,0,0)
    directionalLight(0,255,128,0,1,0)
    directionalLight(128,0,255,0,0,1)
    directionalLight(255,0,128,-1,0,0)
    directionalLight(128,255,0,0,-1,0)
    directionalLight(0,128,255,0,0,-1)
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

def hilbert_3d(m, i):
    if m.faces[0].generation>i:
        return m
    else:
        tm = Mesh()
        for f in m.faces:
            gridfaces = f.sd_grid(3,3)
            tf = gridfaces[4]
            extrudes = tf.sd_tapered(0.25,-90 / pow(3,tf.generation),True)
            gridfaces.pop(4)
            for ef in extrudes:
                ef.generation -= 1
            gridfaces.extend(extrudes)
            tm.faces.extend(gridfaces)
        
        return hilbert_3d(tm,i)
