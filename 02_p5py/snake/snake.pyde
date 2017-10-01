# from here: https://www.youtube.com/watch?v=xGmXxpIj6vs
# original in javascript / html5
# by Chris DeLeon

def setup():
    size(400,400)
    noStroke()
    fill(0,255,0)
    frameRate(10)
    
    global px,py,gs,tc,ax,ay,vx,vy,trail,tail
    px=py=10 # start position of snake
    tc = 20 # tile count
    gs = 20 # tile size
    ax=ay=15 # position of first apple
    vx=vy=0 # velocity x / y
    trail=[] # list of dicts of past positions
    tail=5 # initial minimal tail length
    
def draw():
    global px,py,gs,tc,ax,ay,vx,vy,trail,tail
    # move snake
    px+=vx
    py+=vy
    # snake on torus
    if px<0:
        px=tc-1
    if px>tc-1:
        px=0
    if py<0:
        py=tc-1
    if py>tc-1:
        py=0
        
    background(0)
    # draw snake
    fill(0,255,0)
    for e in trail:
        rect(e['x']*gs,e['y']*gs,gs-2,gs-2)
        # check self intersection
        if e['x']==px and e['y']==py:
            tail = 5
    # add current position to trail
    trail.append({'x':px,'y':py})
    while len(trail)>tail:
        trail.pop(0)
        
    # check if apple found
    if ax==px and ay==py:
        tail+=1
        # generate next random apple pos
        ax = floor(random(tc))
        ay = floor(random(tc))
    fill(255,0,0)
    rect(ax*gs,ay*gs,gs-2,gs-2)
    
def keyPressed():
    # move snake with arrow keys
    global vx,vy
    if key==CODED:
        if keyCode==UP:
            vx= 0
            vy=-1
        elif keyCode==LEFT:
            vx=-1
            vy= 0
        elif keyCode==DOWN:
            vx= 0
            vy= 1
        elif keyCode==RIGHT:
            vx= 1
            vy= 0
        else:
            pass
    
    
    