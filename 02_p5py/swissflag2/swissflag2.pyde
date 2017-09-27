def setup():
    size(800,800)
    noStroke()
    fill(255)
    rectMode(CENTER)
    #background(255,0,0)
    
def draw():
    background(255,0,0)
    
    translate(mouseX,mouseY)
    angle = frameCount/50.0
    rotate(angle)
    
    a = 150
    b = a/5 * 17
    rect(0,0,a,b)
    rect(0,0,b,a)