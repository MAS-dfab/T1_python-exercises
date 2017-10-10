'''
interacting agents tutorial by Patrick Bedarf (RA) for MAS DFAB 2017, ETH Zurich
based on Daniel Shiffman's book "The Nature of Code", Chapter 6. Autonomous Agents
'''
add_library('peasycam')
add_library('controlP5')
add_library('dxf')
from peasy import PeasyCam
from Classes import Flock, Boid, Grid

def setup():
    global bound, cam, cp5, font, a, g, flock, boids, ali, sep, coh, tGrid, bReset
    #size(800, 800, OPENGL)
    fullScreen(P3D, 1)
    cam = PeasyCam(this, 200)
    cam.setMinimumDistance(10)
    cam.setMaximumDistance(1000)
    
    #GUI design - slider, toggles, buttons and other goodies    
    cp5 = ControlP5(this)
    a = 20 #gui scale multiplier
    font = createFont("Calibri Bold", 0.75*a)
    bReset = createButton("Reset", width-5*a, 2*a, 3*a, 3*a)
    tGrid = createToggle("Grid", width-9*a, 2*a, 3*a, 3*a)
    
    sSize = createSlider("DotSize", 22*a, 2*a, 12*a, a, 0.2, 10.0, 5.0)
    sForce = createSlider("MaxForce", 22*a, 4*a, 12*a, a, 0.0, 1.0, 0.05)
    sSpeed = createSlider("MaxSpeed", 22*a, 6*a, 12*a, a, 0.0, 5.0, 1.0)
    cp5.setAutoDraw(False)
    
    bound = 200
    g = Grid(200, 70)
    
    col = 255
    boids = []
    flock = Flock(boids)
    for i in range(200):
        b = Boid(random(-bound/2, bound/2), random(-bound/2, bound/2), 0, col)
        flock.addBoid(b)

def draw():
    background(50)
    smooth()  
    
    # associate toggles and sliders
    showGrid = tGrid.getBooleanValue()
    reset = bReset.getBooleanValue()
    dts = cp5.getController("DotSize").getValue()
    mxf = cp5.getController("MaxForce").getValue()
    mxs = cp5.getController("MaxSpeed").getValue()
    
    flock.run(bound, dts, mxf, mxs)
    
    if reset:
        col = random(255)
        flock.boids = []
        for i in range(20):
            b = Boid(random(-bound/2, bound/2), random(-bound/2, bound/2), 0, col)
            flock.addBoid(b)
        bReset.setValue(False)
    
    if showGrid:
        g.display()
    
    
    
    gui()

def gui():
    # control cam clipping plane
    perspective(PI/3.0, width/float(height),  1,  100000)
    # prevent cam rotation while cp5
    if mouseY < 11*a:
           cam.setActive(False)
    else:
        cam.setActive(True)
    # drawing update
    hint(DISABLE_DEPTH_TEST)
    cam.beginHUD()
    if mouseY < 11*a:
        noStroke()
        fill(255, 10)
        rect(0, 0, width, 11*a)
    cp5.draw()
    cam.endHUD()
    hint(ENABLE_DEPTH_TEST)

def createToggle(name, posX, posY, sX, sY):
    b = cp5.addToggle(name).setPosition(posX, posY).setSize(sX, sY)
    b.setFont(font)
    b.setColorValue(10).setColorActive(color(0, 255, 200)).setColorForeground(color(120)).setColorBackground(color(70))
    return b

def createButton(name, posX, posY, sX, sY):
    b = cp5.addToggle(name).setPosition(posX, posY).setSize(sX, sY)
    b.setFont(font)
    b.setColorForeground(color(255, 0, 0)).setColorBackground(color(70))
    return b

def createSlider(name, posX, posY, sX, sY, rS, rE, sV):
    s = cp5.addSlider(name).setPosition(posX, posY).setSize(sX, sY).setRange(rS, rE).setValue(sV)
    s.setFont(font)
    s.setColorValue(10).setColorActive(color(0, 255, 200)).setColorForeground(color(0, 255, 200)).setColorBackground(color(70))
    return s