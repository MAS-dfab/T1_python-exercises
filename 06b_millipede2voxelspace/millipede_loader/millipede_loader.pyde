add_library('peasycam')
add_library('hd')

def setup():
    size(1200,675,P3D)
    noStroke()
    cam = PeasyCam(this,700)
    
    global vs, shp, shp2
    
    # the self made way
    with open('export 2.txt','r') as f:
        lns = f.readlines()
        nx = int(lns[0])
        ny = int(lns[1])
        nz = int(lns[2])
        # vs = VoxelSpace(nx,ny,nz)
        x1 = float(lns[3])
        y1 = float(lns[4])
        z1 = float(lns[5])
        dim = float(lns[6])
        num = nx*ny*nz
        bx = Box(x1,y1,z1,x1+nx*dim,y1+ny*dim,z1+nz*dim)
        vs = VoxelSpace()
        vs.construct(bx,dim)
        for i in range(num):
            vs.set(i,float(lns[i+7]))
    vs.setValueToBorders(5)
    shp = vs.getPShape(this,0)

    # the HD library way
    vs2 = VoxelSpace()
    t = vs2.loadValuesPlain(sketchPath()+'/data/export 2.txt')
    vs2.setValueToBorders(5)
    shp2 = vs2.getPShape(this,0)
    
def draw():
    background(77)
    directionalLight(255,127,  0, 1, 0, 0)
    directionalLight(  0,255,127, 0, 1, 0)
    directionalLight(127,  0,255, 0, 0, 1)
    directionalLight(255,  0,127,-1, 0, 0)
    directionalLight(127,255,  0, 0,-1, 0)
    directionalLight(  0,127,255, 0, 0,-1)
    
    translate(0,-200,0)
    shape(shp)
    translate(-500,0,0)
    shape(shp2)
    