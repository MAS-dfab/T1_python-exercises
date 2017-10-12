add_library('peasycam')
add_library('hd')

def setup():
    size(1200,675,P3D)
    cam = PeasyCam(this,500)
    noStroke()
    
    global dx,dy,dz,vs
    dx = 500.0
    dy = 400.0
    dz = 300.0
    b = Box(-dx/2,-dy/2,-dz/2,dx/2,dy/2,dz/2)
    vs = VoxelSpace()
    vs.construct(b,3.0)
    vs.setValueToAll(10000)
    vd = VoxelDistance(vs)
    
    p = Pipe()
    p.addControlPoint(-200,-100,0)
    p.addControlPoint( 200,-100,80)
    p.addControlPoint(-200, 100,-80)
    p.addControlPoint( 200, 100,0)
    p.startRad = 10
    p.endRad = 20
    vd.addVol(p,b)
    
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
    box(5)
    
def keyPressed():
    if key=='e':
        vs.saveMCube(0,sketchPath()+"/"+get_time_stamp()+".obj")
        
def get_time_stamp():
    s = str(year())+str(month())+str(day())+str(hour())+str(minute())+str(second())
    return s
        
        
        
        
        
        
        
        
    
    
    
    
    
    
    
    
    
    