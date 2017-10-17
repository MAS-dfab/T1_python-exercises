add_library('controlP5')
add_library('peasycam')
add_library('hd')

def setup():
    global dx,dy,dz,vs,vs1,vs2,cp5,blender,cam

    size(1200,675,P3D)
    cam = PeasyCam(this,500)
    noStroke()
    
    vxdim = 8.0
    dx = 500.0
    dy = 400.0
    dz = 300.0
    b = Box(-dx/2,-dy/2,-dz/2,dx/2,dy/2,dz/2)
    vs1 = VoxelSpace()
    vs1.construct(b,vxdim)
    vs1.setValueToAll(10000)
    vd1 = VoxelDistance(vs1)

    vs2 = VoxelSpace()
    vs2.construct(b,vxdim)
    vs2.setValueToAll(10000)
    vd2 = VoxelDistance(vs2)
    
    vb = VBox(-230,-180,-130,230,180,130,25)
    vd1.addVol(vb,b)
    
    t = Torus(0,0,0,140,50)
    vd2.addVol(t,b)
    
    vs = VoxelSpace()
    vs.construct(b,vxdim)
    vs.setValueToAll(10000)
    
    cp5 = ControlP5(this)
    blender = createSlider('BlendPos',40,40,200,20,0.0,0.99,0.5)
    cp5.setAutoDraw(False)
        
def draw():
    background(77)
    directionalLight(255,127,  0, 1, 0, 0)
    directionalLight(  0,255,127, 0, 1, 0)
    directionalLight(127,  0,255, 0, 0, 1)
    directionalLight(255,  0,127,-1, 0, 0)
    directionalLight(127,255,  0, 0,-1, 0)
    directionalLight(  0,127,255, 0, 0,-1)
    
    f = blender.getValue()
    vs.values = [f*a+(1-f)*b for a,b in zip(vs1.values,vs2.values)]
    shp = vs.getPShape(this,0.0)
    shape(shp)
    
    pushStyle()
    noFill()
    stroke(255)
    box(dx,dy,dz)
    popStyle()
    
    gui()
    
def gui():
    # control cam clipping plane
    #perspective(PI/3.0, width/float(height),  1,  100000)
    # prevent cam rotation while cp5
    if mouseY < 100:
        cam.setActive(False)
    else:
        cam.setActive(True)
    # drawing update
    hint(DISABLE_DEPTH_TEST)
    cam.beginHUD()
    cp5.draw()
    cam.endHUD()
    hint(ENABLE_DEPTH_TEST)
    
def createSlider(name, posX, posY, sX, sY, rS, rE, sV):
    s = cp5.addSlider(name).setPosition(posX, posY).setSize(sX, sY).setRange(rS, rE).setValue(sV)
    #s.setFont(font)
    #s.setColorValue(10).setColorActive(color(0, 255, 200)).setColorForeground(color(0, 255, 200)).setColorBackground(color(70))
    return s