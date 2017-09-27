def setup():
    size(800,800)
    noStroke()
    fill(255)
    rectMode(CENTER)
    #background(255,0,0)
    global angle, dir
    angle = 0
    dir = 1
    
def draw():
    background(255,0,0)
    
    translate(width/2,height/2)
    global angle, dir
    angle = angle+dir*0.02
    if angle > HALF_PI or angle < 0:
        dir *= -1
    rotate(angle)
    
    a = 150
    b = a/5 * 17
    rect(0,0,a,b)
    rect(0,0,b,a)