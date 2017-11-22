add_library('hd')
add_library('peasycam')

import hdgeom.primitives.Lattice.LatticeType as lt

def setup():
    size(800,600,P3D)
    noStroke()
    cam = PeasyCam(this,150)
    
    hd = 50
    bx = Box(-hd,-hd,-hd,hd,hd,hd)
    
    vs = VoxelSpace()
    vs.construct(bx,1)
    vs.setValueToAll(10000)
    vd = VoxelDistance(vs)
    vd.addVol(Cylinder(0,0,-45,0,0,45,45),bx)
    vd.subVol(Sphere(0,50,50,60),bx)
    
    vs2 = VoxelSpace()
    vs2.construct(bx,1)
    vs2.setValueToAll(10000)
    vd2 = VoxelDistance(vs2)
    lat = Lattice(bx)
    #lat.lType = lt.Gyroid
    #lat.lType = lt.Lidinoid
    lat.lType = lt.FischerKoch
    lat.scalefactor = 2.5
    vd2.addVol(lat,bx)
    
    for i in range(len(vs.values)):
        vs.values[i] += vs2.values[i]
      
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