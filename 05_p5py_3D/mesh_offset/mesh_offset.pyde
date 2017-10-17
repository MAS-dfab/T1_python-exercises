add_library('peasycam')
add_library('hd')

def setup():
    size(800,600,P3D)
    cam = PeasyCam(this,500)
    noStroke()
    
    m = MeshFactory.fabricateBox(220,170,120)
    m.constructTopology()
    m = RuleCatmull().replace(m)
    m = RulePyramide().replace(m,20)
        
    RuleOffset().offset(m,10.0,True)
    
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