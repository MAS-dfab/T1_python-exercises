add_library('peasycam')
add_library('hd')

def setup():
    size(1200,675,P3D)
    cam = PeasyCam(this,500)
    noStroke()
    
    global dx,dy,dz
    dx = 500.0
    dy = 500.0
    dz = 500.0
    b = Box(-dx/2,-dy/2,-dz/2,dx/2,dy/2,dz/2)
    vs = VoxelSpace()
    vs.construct(b,3.0)
    vs.setValueToAll(10000)
    
    vd = VoxelDistance(vs)
    
    #s1 = Sphere(0,0,0,170)
    #vd.addVol(s1,b)
    
    #s2 = Sphere(150,20,0,80)
    #vd.intVol(s2,b)
    
    cyl = Cylinder(0,0,-300,0,0,300,70)
    vd.addVol(cyl,b)
    
    ext = Extrusion(4,80,400)
    p = Plane(0,0,0,1,0,0)
    ext.setPlane(p)
    #vd.addVol(ext,b)
    vd.addSmooth(ext,b,90)
    
    star = Extrusion()
    rds = [60,80]
    a = TWO_PI/10
    for i in range(10):
        r = rds[i%2]
        p = PVector(r * cos(i*a), r * sin(i*a), 0)
        star.addPoint(p)
    star.height = 400
    p = Plane(0,0,0,0,1,0)
    star.setPlane(p)
    #vd.addVol(star,b)
    vd.addSmooth(star,b,90)
    
    vs.makeShell(10,1)
    
    s = Sphere(600,0,0,420)
    vd.subVol(s,b)
    
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
    
    
    
    
    
    
    
    
    
    