def setup():
    size(1200,675)
    noFill()
    stroke(255,255,0)
    
    global c1,c2,r1, render_image, dist_vals
    c1 = Circle(width/2,height/2, 250)
    c2 = Circle(width/2+300,height/2-50,150)
    r1 = Rectangle(width/2-200,height/2+100,400.0,320.0)
    
    render_image = PImage(width,height)
    # create list of 0's
    dist_vals = [0 for i in range(width*height)]
    
    # calculate distances
    for x in range(width):
        for y in range(height):
            dst1 = c1.get_distance(x,y)
            dst2 = c2.get_distance(x,y)
            dst3 = r1.get_distance(x,y)
            
            # union
            #dst = min(dst1,dst2)
            
            # subtraction
            dst = max(dst1,-dst2)
            
            dst = min(dst,dst3)
            
            # intersection
            #dst = max(dst1,dst2)
            
            
            dist_vals[y*width+x] = dst
   
    # rendering
    mx = max(dist_vals)
    mn = min(dist_vals)
    for x in range(width):
        for y in range(height):
            dst = dist_vals[y*width+x]
            if abs(dst)<2:
                col = color(255)
            else:
                dst = map(dst,mn,mx,0,255)
                col = color(255-dst,dst,0)
            render_image.set(x,y,col)
    
def draw():
    background(77)
    
    #global c
    #ellipse(c.x,c.y,2*c.r,2*c.r)
    
    global render_image
    image(render_image,0,0)
    
    dst = dist_vals[mouseY*width+mouseX]
    ellipse(mouseX,mouseY,2*dst,2*dst) 
    
class Circle():
    def __init__(self, _x, _y, _r):
        self.x = _x
        self.y = _y
        self.r = _r
        
    def get_distance(self, _x, _y):
        dx = self.x - _x
        dy = self.y - _y
        d = sqrt(dx*dx + dy*dy) - self.r
        return d
    
class Rectangle():
    def __init__(self, _x, _y, _a, _b):
        self.x = _x
        self.y = _y
        self.a = _a
        self.b = _b
        
    def get_distance(self, _x, _y):
        dx = self.x - _x
        dy = self.y - _y
        d = max(abs(dx)-self.a/2.0, abs(dy)-self.b/2.0)
        return d
    
def mousePressed():
    global dist_vals
    dst = dist_vals[mouseY*width+mouseX]
    print(dst)
    
    
    
    
    
    
    
    
    
    
    
    
    