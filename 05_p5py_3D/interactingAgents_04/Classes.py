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

#inplement system class
class System:
    def __init__(self, pop, bound):
        self.flocks = []
        self.count = range(len(pop))
            
        for p in pop:
            col = color(random(100, 255), random(100, 255), random(100, 255))
            boids = []
            flock = Flock(boids)
            for i in range(p):
                b = Boid(random(-bound/2, bound/2), random(-bound/2, bound/2), 0, col)
                flock.addBoid(b)
            
            self.flocks.append(flock)
        
    def run(self, ali, sep, coh, bound, dts, mxf, mxs):
        for flock in self.flocks:
            flock.run(ali, sep, coh, bound, dts, mxf, mxs)
    
    def displayBoids(self, dts):
        for i in self.count:
            for j in range(len(self.flocks[i].boids)):
                self.flocks[i].boids[j].display(dts)
    
    def displayTrails(self):
        for i in self.count:
            for j in range(len(self.flocks[i].boids)):
                self.flocks[i].boids[j].displayTrail()
    
    def resetTrails(self):
        for i in self.count:
            for j in range(len(self.flocks[i].boids)):
                self.flocks[i].boids[j].locList = []

class Flock:
    def __init__(self, boids):
        self.boids = boids
    
    def run(self, ali, sep, coh, bound, dts, mxf, mxs): 
        for b in self.boids:
            b.run(self.boids, ali, sep, coh, bound, dts, mxf, mxs) 
    
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
        global r
        r = 1.0
        self.locList = [] 
               
    def run(self, boids, ali, sep, coh, bound, dts, mxf, mxs): 
        self.maxforce = mxf 
        self.maxspeed = mxs
        self.flock(boids, ali, sep, coh)
        self.update()
        self.borders(bound)
        self.record(bound, 200.0) #add record method for drawing trails
        self.display(dts)
        
    
    def update(self):
        self.vel.add(self.acc)
        self.vel.limit(self.maxspeed)
        self.loc.add(self.vel)
        self.acc.mult(0)
    
    def flock(self, boids, Alignment, Separation, Cohesion):
        sep = self.separate(boids)
        ali = self.align(boids)
        coh = self.cohesion(boids)

        sep.mult(0.01 * Separation)
        ali.mult(0.01 * Alignment)
        coh.mult(0.01 * Cohesion)
        
        self.applyForce(sep)
        self.applyForce(ali)
        self.applyForce(coh)
    
    def applyForce(self, f):
        self.acc.add(f)
    
    def separate(self, boids):
        desiredseparation = r*2 #radius to look around, global r
        count = 0
        sum = PVector(0, 0, 0)
        for other in boids:
            d = PVector.dist(self.loc, other.loc)
            if ((d > 0) and (d < desiredseparation)): #if other is too close
                diff = PVector.sub(self.loc, other.loc) #a vector pointing away from other
                diff.normalize()
                diff.div(d)
                sum.add(diff) #add all vectors and increment count
                count += 1
        if (count > 0): #found at least one close other
            sum.div(count) #average: sum(all)/len(all)
            sum.normalize()
            sum.mult(self.maxspeed)
            sum.sub(self.vel) #Reynolds steering formula
            sum.limit(self.maxforce)
        return sum
    
    def align(self, boids):
        neighbordist = 50 #arbitrary look around
        sum = PVector(0, 0, 0)
        count = 0
        for other in boids:
            d = PVector.dist(self.loc, other.loc)
            if ((d > 0) and (d < neighbordist)):
                sum.add(other.vel) #add up all velocities
                count += 1
        if (count > 0):
            sum.div(count) #calc average by divide sum by total
            sum.normalize()
            sum.mult(self.maxspeed)
            steer = PVector.sub(sum, self.vel) #Reynolds steering formula
            steer.limit(self.maxforce)
            return steer
        else:
            return PVector(0, 0, 0) #if no close boids, steering forace is zero
    
    def cohesion(self, boids):
        neighbordist = 50
        sum = PVector(0, 0, 0)
        count = 0
        for other in boids:
            d = PVector.dist(self.loc, other.loc)
            if((d > 0) and (d < neighbordist)):
                sum.add(other.loc) #adding up all others locations
                count += 1
        if (count > 0):
            sum.div(count) # average location
            return self.seek(sum) #seek the average location as target
        else:
            return PVector(0, 0, 0)
        
    def seek(self, target):
        desired = PVector.sub(target, self.loc) 
        desired.normalize()
        desired.mult(self.maxspeed)
        steer = PVector.sub(desired, self.vel) #Reynolds steering formula
        steer.limit(self.maxforce)
        return steer
      
    def display(self, dts):
        stroke(self.col)
        strokeWeight(dts)
        point(self.loc.x, self.loc.y, self.loc.z)
    
    def record(self, bound, mxl):
        if self.loc.x > bound/2-1 or self.loc.y > bound/2-1 or self.loc.z > bound/2-1:
            self.locList = []
        elif self.loc.x < -bound/2+1 or self.loc.y < -bound/2+1 or self.loc.z < -bound/2+1:
            self.locList = []
        else:
            self.locList.append(self.loc.copy())
            if len(self.locList) > mxl:
                self.locList.pop(1)
    
    def displayTrail(self):
        beginShape()
        strokeWeight(0.5)
        stroke(self.col)
        noFill()
        for i in range(1, len(self.locList)):
            v = self.locList[i]
            vertex(v.x, v.y, v.z)
        endShape()
    
    def borders(self, bound):
        if (self.loc.x < -bound/2): self.loc.x = bound/2
        if (self.loc.y < -bound/2): self.loc.y = bound/2
        if (self.loc.z < -bound/2): self.loc.z = bound/2
        
        if (self.loc.x > bound/2): self.loc.x = -bound/2
        if (self.loc.y > bound/2): self.loc.y = -bound/2
        if (self.loc.z > bound/2): self.loc.z = -bound/2