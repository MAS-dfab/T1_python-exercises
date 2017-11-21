add_library('hd')
add_library('peasycam')

import hdgeom.primitives.DistFieldStack.BoolType as bt

def setup():
    size(800,600,P3D)
    noStroke()
    cam = PeasyCam(this,500)
    
    hd = 100
    bx = Box(-hd,-hd,-hd,hd,hd,hd)
    
    dfs = DistFieldStack()
    ns = Noise(bx)
    ns.scalefactor = 3
    dfs.appendElement(ns, bt.addition)
    dfs.appendElement(Sphere(0,0,0,hd-5), bt.intersection)
    dfs.appendElement(Cylinder(0,0,-hd,0,0,hd,30),bt.subtraction)

    vs = VoxelSpace(bx,100)
    vs.setValueToAll(10000)
    vd = VoxelDistance(vs)
        
    vd.addVol(dfs, bx)
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