class Ball:
    def __init__(self,ps,vl):
        self.pos = ps
        self.vel = vl
        self.rad = random(40,80)
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