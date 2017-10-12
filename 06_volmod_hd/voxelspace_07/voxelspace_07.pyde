add_library('peasycam')
add_library('hd')

def setup():
    size(1200,675,P3D)
    cam = PeasyCam(this,500)
    noStroke()
    
    global dx,dy,dz
    dx = 500.0
    dy = 400.0
    dz = 300.0
    b = Box(-dx/2,-dy/2,-dz/2,dx/2,dy/2,dz/2)
    vs = VoxelSpace()
    vs.construct(b,4.0)
    vs.setValueToAll(10000)
    #vd = VoxelDistance(vs)
    print vs.nX,vs.nY,vs.nZ
    
    for x in range(vs.nX):
        for y in range(vs.nY):
            for z in range(vs.nZ):
                # gyroid minimal surface
                # https://en.wikipedia.org/wiki/Gyroid
                v = sin(x/5.0)*cos(y/5.0) + sin(y/5.0)*cos(z/5.0) + sin(z/5.0)*cos(x/5.0)
                # make shell
                v = abs(v)-0.25
                vs.set(x,y,z,v)
    
    # set all the border planes to 1, to close        
    vs.setValueXPlane(0,1)
    vs.setValueXPlane(vs.nX-1,1)
    vs.setValueYPlane(0,1)
    vs.setValueYPlane(vs.nY-1,1)
    vs.setValueZPlane(0,1)
    vs.setValueZPlane(vs.nZ-1,1)
    
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