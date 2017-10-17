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
    vs.construct(b,3.0)
    vs.setValueToAll(10000)
    vd = VoxelDistance(vs)
    
    vb = VBox(-240,-50,-130,240,50,130)
    vd.addVol(vb,b)
    
    factor = 2.0
    for x in range(vs.nX):
        gradient_pos = float(x)/vs.nX
        for y in range(vs.nY):
            for z in range(vs.nZ):
                # calculate schwarz surface
                vn = cos(x/factor)+cos(y/factor)+cos(z/factor)
                # get existing value
                ve = vs.get(x,y,z)
                # calculate new "composite" value
                v = (1-gradient_pos)*ve + gradient_pos*vn*10
                # set new value to voxel space
                vs.set(x,y,z,v)
    
    vd.intVol(vb,b)
    
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