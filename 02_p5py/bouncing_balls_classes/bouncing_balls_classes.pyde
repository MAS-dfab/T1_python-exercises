from gameobjects import Ball

def setup():
    size(800,600)
    
    global myball
    pos = PVector(width/2,height/2)
    vel = PVector.random2D()
    vel.mult(random(2,4))
    myball = Ball(pos,vel)
    
def draw():
    global myball
    # calculation
    myball.update()

    # drawing
    background(80)
    myball.display()
    