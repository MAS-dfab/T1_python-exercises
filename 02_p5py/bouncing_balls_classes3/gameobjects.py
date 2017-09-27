class Ball:
    def __init__(self,ps):
        self.pos = ps
        
        self.vel = PVector.random2D()
        self.vel.mult(random(3,5))
        self.rad = random(20,50)
        self.col = color(random(100,255),random(100,255),random(100,255))
        
    def update(self):
        self.pos.add(self.vel)
        if self.pos.x+self.rad > width or self.pos.x-self.rad < 0:
            self.vel.x *= -1
        if self.pos.y+self.rad > height or self.pos.y-self.rad < 0:
            self.vel.y *= -1
            
    def display(self):
        fill(self.col)
        ellipse(self.pos.x, self.pos.y, 2*self.rad, 2*self.rad)
        
class Dog:
    def __init__(self,ps):
        self.pos = ps
        self.vel = PVector.random2D()
        self.vel.mult(random(3,5)) 
        
    def update(self):
        self.pos.add(self.vel)
        
    def display(self):
        rectMode(CENTER)
        fill(227,224,201)
        pushMatrix()
        translate(self.pos.x,self.pos.y)
        rotate(atan2(self.vel.y,self.vel.x))
        rect(0,0,100,60)
        popMatrix()
        
        
        
        