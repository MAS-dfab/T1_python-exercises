class Grid:
    def __init__(self, s, c):
        self.s = s
        self.c = c
        
    def display(self):
        noFill()
        strokeWeight(0.5)
        stroke(self.c)
        for x in range(-self.s/2+5, self.s/2, 10):
            line(x, -self.s/2, -self.s/2, x, self.s/2, -self.s/2)
            line(-self.s/2, x, -self.s/2, self.s/2, x, -self.s/2)
        stroke(self.c)
        box(self.s, self.s, self.s)

class Flock:
    def __init__(self, boids):
        self.boids = boids
    
    def run(self, bound, dts, mxf, mxs):
        for b in self.boids:
            b.run(bound, dts, mxf, mxs)
    
    def addBoid(self, boid):
        self.boids.append(boid)
        return self.boids

class Boid:
    def __init__(self, x, y, z, col):
        self.x = x
        self.y = y
        self.z = z
        self.col = col
        
        self.loc = PVector(self.x, self.y, self.z)
        self.acc = PVector(0, 0, 0)
        self.vel = PVector(random(-1, 1), random(-1, 1), random(-1, 1))
               
    def run(self, bound, dts, mxf, mxs):
        self.maxspeed = mxs
        self.update()
        self.borders(bound)
        self.display(dts)
    
    def update(self):
        self.vel.add(self.acc)
        self.vel.limit(self.maxspeed)
        self.loc.add(self.vel)
        self.acc.mult(0)
      
    def display(self, dts):
        stroke(self.col)
        strokeWeight(dts)
        point(self.loc.x, self.loc.y, self.loc.z)
    
    def borders(self, bound):
        if (self.loc.x < -bound/2): self.loc.x = bound/2
        if (self.loc.y < -bound/2): self.loc.y = bound/2
        if (self.loc.z < -bound/2): self.loc.z = bound/2
        
        if (self.loc.x > bound/2): self.loc.x = -bound/2
        if (self.loc.y > bound/2): self.loc.y = -bound/2
        if (self.loc.z > bound/2): self.loc.z = -bound/2