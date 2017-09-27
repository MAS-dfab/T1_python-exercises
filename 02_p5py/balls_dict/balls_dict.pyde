def setup():
    size(800,600)
    
    global balls
    
    balls = []
    for i in range(100):
        b = {}
        b['pos'] = PVector(random(60,width-60),random(60,height-60))
        b['vel'] = PVector.random2D();
        b['vel'].mult(random(3,7))
        b['rad'] = random(30,50)
        balls.append(b)
    
def draw():
    # calculation
    global balls
    for b in balls:
        b['pos'] = b['pos'].add(b['vel'])
        if b['pos'].x+b['rad']> width or b['pos'].x-b['rad']<0:
            b['vel'].x *= -1
        if b['pos'].y+b['rad']>height or b['pos'].y-b['rad']<0:
            b['vel'].y *= -1
    
    # display
    background(80)
    for b in balls:
        ellipse(b['pos'].x,b['pos'].y,2*b['rad'],2*b['rad'])