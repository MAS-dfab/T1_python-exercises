add_library('peasycam')
add_library('hd')
import random

def setup():
    size(800,600,P3D)
    cam = PeasyCam(this,500)
    stroke(255)
    
    pts = []
    for i in range(10):
        p = PVector.random3D()
        p.mult(100)
        pts.append(p)
        
    global edges
    edges = []
    meshes = []
    # however often you try
    # with 10 points, there will be a max of 45 edges
    # cocktail: n * (n-1) / 2
    for i in range(300):
        a = random.choice(pts)
        b = random.choice(pts)
        # only add unique edges not in the list already
        # if a and b are the same node, this is not valid edge
        # edge (a,b) and (b,a) are considered the same
        # undirected graph!
        if a!=b and (b,a) not in edges and (a,b) not in edges:
            edges.append((a,b))
                    
    print len(edges)
    stroke(255)

    
def draw():
    background(77)
    
    for e in edges:
        line(e[0].x,e[0].y,e[0].z,e[1].x,e[1].y,e[1].z)