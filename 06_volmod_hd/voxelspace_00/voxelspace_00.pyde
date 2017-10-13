add_library('peasycam')
add_library('hd')

def setup():
    size(1200,675,P3D)
    cam = PeasyCam(this,500)
    noStroke()
    
    global vs, s1, s2, b
    dx = 600.0
    dy = 400.0
    dz = 300.0
    b = Box(-dx/2,-dy/2,-dz/2,dx/2,dy/2,dz/2)
    vs = VoxelSpace()
    vs.construct(b,5.0)
    vs.setValueToAll(1000)
    
    #vd = VoxelDistance(vs)
    
    s1 = Sphere(0,0,0,140)
    #vd.addVol(s1,b)
    
    #shp = vs.getPShape(this,0.0)
    
def draw():
    background(77)
    directionalLight(255,127,  0, 1, 0, 0)
    directionalLight(  0,255,127, 0, 1, 0)
    directionalLight(127,  0,255, 0, 0, 1)
    directionalLight(255,  0,127,-1, 0, 0)
    directionalLight(127,255,  0, 0,-1, 0)
    directionalLight(  0,127,255, 0, 0,-1)
    
    vs.setValueToAll(1000)
    vd = VoxelDistance(vs)
    vd.addVol(s1,b)
    s2 = Sphere(sin(frameCount/50.0)*200,0,60,90)
    vd.addVol(s2,b)
    shp = vs.getPShape(this,0.0)
    
    shape(shp)
    
    
    
    
    
    
    
    
    
    