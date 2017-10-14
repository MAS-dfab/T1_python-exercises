add_library('peasycam')
add_library('hd')

def setup():
    size(800,600,P3D)
    noStroke()
    cam = PeasyCam(this,500)
    
    global shp,shp2
    m = MeshFactory.fabricateBox(400,300,200)

    f = m.getFace(0)
    #f.fix = True
    for p in f.getPoints():
        p.fix = True
    m.constructTopology()
    
    r = RuleCatmull()
    for i in range(5):
        m = r.replace(m)
            
    m2 = MeshFactory.fabricateIcosahedron(0,300,0,100)
    rp = RulePyramide()
    m2 = rp.replace(m2,30)

    shp = m.getPShape(this)
    shp2 = m2.getPShape(this)
    
def draw():
    background(77)
    directionalLight(255,127,  0, 1, 0, 0)
    directionalLight(  0,255,127, 0, 1, 0)
    directionalLight(127,  0,255, 0, 0, 1)
    directionalLight(255,  0,127,-1, 0, 0)
    directionalLight(127,255,  0, 0,-1, 0)
    directionalLight(  0,127,255, 0, 0,-1)
    
    shape(shp)
    shape(shp2)