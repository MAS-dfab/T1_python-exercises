add_library('peasycam')
add_library('hd')

def setup():
    size(800,600,P3D)
    cam = PeasyCam(this,500)
    noStroke()
    
    d = 100.0
    
    m = Mesh()
    
    n1 = Node( d, d, d)
    n2 = Node(-d,-d, d)
    n3 = Node(-d, d,-d)
    n4 = Node( d,-d,-d)
    
    f1 = Face([n3,n2,n1])
    m.addFace(f1)
    f2 = Face([n1,n4,n3])
    m.addFace(f2)
    f3 = Face([n2,n4,n1])
    m.addFace(f3)
    f4 = Face([n3,n4,n2])
    m.addFace(f4)
        
    global shp
    shp = m.getPShape(this)
    
def draw():
    background(77)
    directionalLight(255,127,  0, 1, 0, 0)
    directionalLight(  0,255,127, 0, 1, 0)
    directionalLight(127,  0,255, 0, 0, 1)
    directionalLight(255,  0,127,-1, 0, 0)
    directionalLight(127,255,  0, 0,-1, 0)
    directionalLight(  0,127,255, 0, 0,-1)
    
    shape(shp)