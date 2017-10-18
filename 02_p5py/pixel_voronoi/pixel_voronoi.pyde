def setup():
    size(400,400)
    colorMode(HSB)
    
    global pts
    pts = []
    for i in range(20):
        p = PVector(random(width),random(height),random(255))
        pts.append(p)
    
    global pic
    pic = createImage(width,height,RGB)
    pic.loadPixels()
    for x in range(width):
        for y in range(height):
            min_dist = 9999
            cp = None
            for p in pts:
                d = dist(x,y,p.x,p.y)
                if d < min_dist:
                    min_dist = d
                    cp = p
            #pic.set(x,y,color(min_dist,255,255))
            pic.set(x,y,color(cp.z,255,255))
            
    pic.loadPixels()                
    
def draw():
    background(255)
    image(pic,0,0)
    
    for p in pts:
        ellipse(p.x,p.y,5,5)