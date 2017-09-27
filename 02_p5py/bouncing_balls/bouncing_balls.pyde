def setup():
    size(800,600)
    
    global pos, vel, rad
    global pos2, vel2, rad2
    pos = PVector(width/2,height/2)
    vel = PVector.random2D()
    vel.mult(random(2,4))
    rad = 50
    
    pos2 = PVector(width/2,height/2)
    vel2 = PVector.random2D()
    vel2.mult(random(2,4))
    rad2 = 60
    
def draw():
    global pos, vel, rad
    global pos2, vel2, rad2

    # calculation
    pos.add(vel)
    pos2.add(vel2)
    if pos.x+rad > width or pos.x-rad < 0:
        vel.x *= -1
    if pos.y+rad > height or pos.y-rad < 0:
        vel.y *= -1
        pos.add(vel)
    if pos2.x+rad2 > width or pos2.x-rad2 < 0:
        vel2.x *= -1
    if pos2.y+rad2 > height or pos2.y-rad2 < 0:
        vel2.y *= -1

    # drawing
    background(80)

    fill(255,0,0)
    ellipse(pos.x, pos.y, 2*rad,2*rad)
    
    fill(0,200,255)
    ellipse(pos2.x, pos2.y, 2*rad2,2*rad2)
    