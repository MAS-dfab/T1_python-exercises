add_library('hd')
add_library('peasycam')

def setup():
    size(800,600,P3D)
    noStroke()
    cam = PeasyCam(this,500)
    
    hd = 100
    bx = Box(-hd,-hd,-hd,hd,hd,hd)
    
    vs = VoxelSpace(bx,100)
    vs.setValueToAll(10000)
    vd = VoxelDistance(vs)
    
    lat = Lattice(bx)
    lat.scalefactor = 12
    lat.lType = lat.LatticeType.Gyroid
    # LatticeType {Schwarz, Gyroid, Lidinoid, Neovius, 
    #       FischerKoch, FRD, Diamond, DoubleDiamond, DoubleGyroid}
    lat.offset = 0.7
    
    vd.addVol(lat,bx)
    vs.setValueToBorders(20)
    
    global shp
    shp = vs.getPShape(this,0)
    
def draw():
    background(77)
    directionalLight(255,127,  0, 1, 0, 0)
    directionalLight(  0,255,127, 0, 1, 0)
    directionalLight(127,  0,255, 0, 0, 1)
    directionalLight(255,  0,127,-1, 0, 0)
    directionalLight(127,255,  0, 0,-1, 0)
    directionalLight(  0,127,255, 0, 0,-1)

    shape(shp)