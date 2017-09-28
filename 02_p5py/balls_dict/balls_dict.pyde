def setup():
    size(800,600)
    noStroke()
    
    global balls
    
    # create empty list
    balls = []
    for i in range(100):
        # create empty dict
        b = {}
        # fill key / value pairs into dict
        b['pos'] = PVector(random(60,width-60),random(60,height-60))
        b['vel'] = PVector.random2D();
        b['vel'].mult(random(3,7))
        b['rad'] = random(10,30)
        b['col'] = color(random(150,255),random(150,255),random(150,255))
        # append dict to list
        balls.append(b)
    
def draw():
    # calculation
    global balls
    for b in balls:
        # add vel to pos to move
        b['pos'] = b['pos'].add(b['vel'])
        
        # check for boundary collision and bounce
        if b['pos'].x+b['rad']> width or b['pos'].x-b['rad']<0:
            b['vel'].x *= -1
        if b['pos'].y+b['rad']>height or b['pos'].y-b['rad']<0:
            b['vel'].y *= -1
    
    # display
    
    # for a fading traces effect, draw a semi-transparent rect
    # instead of a fully opaque background
    fill(80,20)
    rect(0,0,width,height)
    #background(80)
    for b in balls:
        fill(b['col'])
        ellipse(b['pos'].x,b['pos'].y,2*b['rad'],2*b['rad'])
       
# save one image when any key is pressed
def keyPressed():
    save('scrnsht.png')