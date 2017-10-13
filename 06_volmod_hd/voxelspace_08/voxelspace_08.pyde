add_library('peasycam')
add_library('hd')

def setup():
    size(1200,675,P3D)
    cam = PeasyCam(this,500)
    noStroke()
    
    global dx,dy,dz
    dx = 500.0
    dy = 300.0
    dz = 300.0
    b = Box(-dx/2,-dy/2,-dz/2,dx/2,dy/2,dz/2)
    vs = VoxelSpace()
    vs.construct(b,3.0)
    vs.setValueToAll(10000)
    vd = VoxelDistance(vs)
        
    pts = []
    a = TWO_PI/50
    for i in range(250):
        r = 50 + i/250.0 * 50
        x = -dx/2+50 + i/250.0*400
        y = r * sin(i*a)
        z = r * cos(i*a)
        pts.append(PVector(x,y,z))
        
    for i in range(250-1):
        c = Cylinder(pts[i].x,pts[i].y,pts[i].z,pts[i+1].x,pts[i+1].y,pts[i+1].z,15)
        c.captype = Cylinder.ROUND
        vd.addVol(c,b)
    
    global shp
    shp = vs.getPShape(this,0.0)
    
def draw():
    background(77)
    directionalLight(255,127,  0, 1, 0, 0)
    directionalLight(  0,255,127, 0, 1, 0)
    directionalLight(127,  0,255, 0, 0, 1)
    directionalLight(255,  0,127,-1, 0, 0)
    directionalLight(127,255,  0, 0,-1, 0)
    directionalLight(  0,127,255, 0, 0,-1)
    
    shape(shp)
    
    global dx,dy,dz
    noFill()
    stroke(255)
    box(dx,dy,dz)