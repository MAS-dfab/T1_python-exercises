def setup():
    size(1200,675)
    
    global c, pix_field
    c = Circle(width/2,height/2, 250)
    pix_field = PImage(width,height)
    
    for x in range(width):
        for y in range(height):
            dst = c.get_distance(x,y)
            dst = map(dst,-c.r,430,0,255)
            col = color(dst,255-dst,0)
            pix_field.set(col,x,y)
    
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
    
    
    
    
    
    
    
    
    
    
    
    
    