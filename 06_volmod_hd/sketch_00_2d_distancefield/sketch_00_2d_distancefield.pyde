def setup():
    size(1200,675)
    
    global c
    c = Circle(width/2,height/2, 250)
    
def draw():
    background(77)
    
    global c
    ellipse(c.x,c.y,2*c.r,2*c.r)
    
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
    
    
    
    
    
    
    
    
    
    
    
    
    