def setup():
    size(800,800)
    noStroke()
    fill(255)
    rectMode(CENTER)
    
def draw():
    background(255,0,0)
    a = 125 + sin(frameCount/20.0)*50
    b = a/5 * 17
    rect(mouseX,mouseY,a,b)
    rect(mouseX,mouseY,b,a)
    
    if frameCount % 10 == 0:
        saveFrame('cross-####.png')