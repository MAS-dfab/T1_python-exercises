add_library('peasycam')
add_library('hd')
import random

def setup():
    size(800,600,P3D)
    cam = PeasyCam(this,500)
    #stroke(255)
    noStroke()
    
    global dx,dy,dz
    dx = 250.0
    dy = 200.0
    dz = 150.0
    bx = Box(-dx/2,-dy/2,-dz/2,dx/2,dy/2,dz/2)
    vs = VoxelSpace()
    vs.construct(bx,1.5)
    vs.setValueToAll(10000)
    vd = VoxelDistance(vs)
    
    pts = []
    for i in range(50):
        p = PVector.random3D()
        p.mult(90)
        pts.append(p)
        
    # just some mesh to have a network of edges
    m = MeshFactory.fabricateBox(220,170,120)
    m.constructTopology()
    m = RuleCatmull().replace(m)
    m = RulePyramide().replace(m,20)
        
    # place a cylinder along every edge
    for i in range(m.getNumEdges()):
        e = m.getEdge(i)
        c = Cylinder(e.n1.x,e.n1.y,e.n1.z,e.n2.x,e.n2.y,e.n2.z,5)
        c.captype = Cylinder.ROUND;
        vd.addVol(c,bx)
        
    # blur voxelspace to have smooth filleted nodes
    # attention: diameter of cylinders gets reduced!
    VoxelBlur.blur(vs,6)
    
    global shp
    shp = vs.getPShape(this,0.0)
    stroke(255)
    noFill()

    
def draw():
    background(77)
    directionalLight(255,127,  0, 1, 0, 0)
    directionalLight(  0,255,127, 0, 1, 0)
    directionalLight(127,  0,255, 0, 0, 1)
    directionalLight(255,  0,127,-1, 0, 0)
    directionalLight(127,255,  0, 0,-1, 0)
    directionalLight(  0,127,255, 0, 0,-1)
    
    box(dx,dy,dz)
        
    shape(shp)