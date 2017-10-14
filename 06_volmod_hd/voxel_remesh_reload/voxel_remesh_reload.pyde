add_library('peasycam')
add_library('hd')

def setup():
    size(1200,675,P3D)
    cam = PeasyCam(this,500)
    noStroke()
    
    m = OBJImportExport.loadFromOBJ(sketchPath()+'/spiral_8.obj')
    
    # just some sample subdivisions
    m.constructTopology()
    m = RuleCatmull().replace(m)
    m = RulePyramide().replace(m,1.5)
    
    global shp
    shp = m.getPShape(this)

def draw():
    background(77)
    directionalLight(255,127,  0, 1, 0, 0)
    directionalLight(  0,255,127, 0, 1, 0)
    directionalLight(127,  0,255, 0, 0, 1)
    directionalLight(255,  0,127,-1, 0, 0)
    directionalLight(127,255,  0, 0,-1, 0)
    directionalLight(  0,127,255, 0, 0,-1)

    shape(shp)
