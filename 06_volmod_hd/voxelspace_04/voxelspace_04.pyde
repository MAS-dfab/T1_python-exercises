add_library('controlP5')
add_library('peasycam')
add_library('hd')

def setup():
    size(1200,675,P3D)
    
    global cam, cp5, shp, vs, iso_sldr, dx,dy,dz
    cam = PeasyCam(this,500)
    noStroke()
    
    # GUI stuff
    cp5 = ControlP5(this)
    iso_sldr = createSlider('IsoValue',40,40,200,20,0.0,0.99,0.5)
    cp5.setAutoDraw(False)
    
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
                # random perlin noise
                # returns a number between 0 and 1
                # often used for terrain generation in computer games
                v = noise(x/15.0,y/15.0,z/15.0)
                vs.set(x,y,z,v)

    # apply a gaussian blur to the entire voxelspace
    # second number is radius      
    VoxelBlur.blur(vs,6)
    
    # set all the border planes to 1, to close        
    vs.setValueXPlane(0,1)
    vs.setValueXPlane(vs.nX-1,1)
    vs.setValueYPlane(0,1)
    vs.setValueYPlane(vs.nY-1,1)
    vs.setValueZPlane(0,1)
    vs.setValueZPlane(vs.nZ-1,1)
    
    shp = vs.getPShape(this,0.5)
    
def draw():
    background(77)
    directionalLight(255,127,  0, 1, 0, 0)
    directionalLight(  0,255,127, 0, 1, 0)
    directionalLight(127,  0,255, 0, 0, 1)
    directionalLight(255,  0,127,-1, 0, 0)
    directionalLight(127,255,  0, 0,-1, 0)
    directionalLight(  0,127,255, 0, 0,-1)
    
    iv = iso_sldr.getValue()
    shp = vs.getPShape(this,iv)
    
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
