def setup():
    size(1200,675)
    
    global c1,c2, pix_field
    c1 = Circle(width/2,height/2, 250)
    c2 = Circle(width/2+300,height/2-50,150)
    
    pix_field = PImage(width,height)
    
    for x in range(width):
        for y in range(height):
            dst1 = c1.get_distance(x,y)
            dst2 = c2.get_distance(x,y)
            
            # union
            #dst = min(dst1,dst2)
            
            # subtraction
            #dst = max(dst1,-dst2)
            
            # intersection
            dst = max(dst1,dst2)
            
            if abs(dst)<2:
                col = color(255)
            else:
                dst = map(dst,-250,430,0,255)
                col = color(255-dst,dst,0)
            pix_field.set(x,y,col)
    
def draw():
    background(77)
    
    #global c
    #ellipse(c.x,c.y,2*c.r,2*c.r)
    
    global pix_field
    image(pix_field,0,0)
    
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
    
def mousePressed():
    global c
    dst = c.get_distance(mouseX,mouseY)
    print(dst)
    
    
    
    
    
    
    
    
    
    
    
    
    