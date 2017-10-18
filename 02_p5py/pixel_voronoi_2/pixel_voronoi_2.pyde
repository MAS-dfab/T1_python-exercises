def setup():
    size(400,400)
    #colorMode(HSB)
    
    global pts
    pts = []
    for i in range(20):
        p = PVector(random(width),random(height),random(255))
        pts.append(p)
    
    global pic
    #pic = createImage(width,height,RGB)
    #pic.loadPixels()
    pixel_space = [(-1,-1) for i in range(width*height)]
    for x in range(width):
        for y in range(height):
            min_dist = 9999
            cp = None
            ix = -1
            for i,p in enumerate(pts):
                d = dist(x,y,p.x,p.y)
                if d < min_dist:
                    min_dist = d
                    cp = p
                    ix = i
            #pic.set(x,y,color(min_dist,255,255))
            pixel_space[y*width+x] = (ix,min_dist)
            #pic.set(x,y,color(cp.z,255,255))
            
    vals = [-1 for i in range(width*height)]
    for x in range(width):
        for y in range(height):
            same = True
            v = pixel_space[y*width+x][0]
            for dx in range(-1,1):
                for dy in range(-1,1):
                    if x+dx>0 and x+dx<width and y+dy>0 and y+dy<height:
                        if pixel_space[(y+dy)*width+(x+dx)][0] != v:
                            same = False
                            break
            vals[y*width+x] = int(same)
         
    pic = createImage(width,height,RGB)
    for x in range(width):
        for y in range(height):
            pic.set(x,y,color(vals[y*width+x]*255))
    pic.loadPixels()                
    
def draw():
    background(255)
    image(pic,0,0)
    
    for p in pts:
        ellipse(p.x,p.y,5,5)