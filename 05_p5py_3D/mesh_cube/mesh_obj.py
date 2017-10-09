class Mesh():
    
    def __init__(self):
        self.faces=[]
        self.nodes=[]
    
    def add_face(self, f):
        self.faces.append(f)
        
    def subdiv_p(self, h):
        newFaces=[]
        for f in self.faces:
            newFaces.extend(f.sd_pyramid(h))
        
        m=Mesh()
        for f in newFaces:
            m.add_face(f)
        return m
    
    def subdiv_w(self, d):
        newFaces=[]
        for f in self.faces:
            newFaces.extend(f.sd_window(d,False))
            
        m=Mesh()
        for f in newFaces:
            m.add_face(f)
        
        return m
        
    def display(self):
        
        for f in self.faces:
            if (len(f.nodes)<4):
                fill(255)
            else:
                fill(255)
            beginShape()
            for n in f.nodes:
                vertex(n.x,n.y,n.z)
            endShape(CLOSE)
            
    def collect_nodes(self):
        for n in self.nodes:
            n.index = -1
        self.nodes = []
        
        ix = 1
        for f in self.faces:
            for n in f.nodes:
                if n.index == -1:
                    n.index = ix
                    self.nodes.append(n)
                    ix += 1
        print('number of nodes: '+str(len(self.nodes)))
        
    def export_obj(self,path):
        self.collect_nodes()
        
        out = createWriter(path)
        out.println('# mesh exported from p5py by mathias')
        
        for n in self.nodes:
            out.println('v '+str(n.x)+' '+str(n.y)+' '+str(n.z))
            
        for f in self.faces:
            index_list = [str(n.index) for n in f.nodes]
            
            # long version
            #index_list = []
            #for n in f.nodes:
            #    index_list.append(n.index)
            
            out.println('f '+' '.join(index_list))
        
        out.flush()
        out.close()

class Node(PVector):
    def __init__ (self, _x, _y, _z):
        self.x = _x
        self.y = _y
        self.z = _z
        self.index = -1
        
class Face():
    
    def __init__(self,nodes=[]):
        self.nodes=nodes
        
    def sd_pyramid(self, ampl_v):
        
        c=self.f_center()
        n=self.f_normal()
        n=n.mult(ampl_v)
        c=PVector.add(c,n)
        c=Node(c.x,c.y,c.z)
        
        newFaces = []
        
        for i in range( len(self.nodes)):
            nds=[]
            nds.append(self.nodes[i])
            nextIndex = (i+1)%len(self.nodes)
            nds.append(self.nodes[nextIndex])
            nds.append(c)
            f = Face(nds)
            newFaces.append(f)
        
        return newFaces
      
    def sd_window( self, d, cap=False):
        
        c = self.f_center()
        
        newNodes = []
        for n in self.nodes:
            rc=PVector.sub(c,n)
            rc.mult(d)
            n=PVector.add(n,rc)
            n=Node(n.x,n.y,n.z)
            newNodes.append(n)
        newFaces=[]
        for i in range(len(self.nodes)):
            nds=[]
            nextIndex=(i+1)%len(self.nodes)
            nds.append(self.nodes[i])
            nds.append(self.nodes[nextIndex])
            nds.append(newNodes[nextIndex])
            nds.append(newNodes[i])
            f=Face(nds)
            newFaces.append(f)
            
        if cap:
            newFaces.append(Face(newNodes))
            
        return newFaces

    def f_normal (self):
        v1 = PVector.sub(self.nodes[1],self.nodes[0])
        v2 = PVector.sub(self.nodes[2],self.nodes[0])
        n = PVector.cross(v1,v2)
        n.normalize()
        return n   
        
    def f_center(self):
        cx=0
        for n in self.nodes:
            cx+=n.x
        cx=cx/len(self.nodes)
        
        cy = sum([n.y for n in self.nodes])/len(self.nodes)
        
        cz = sum([n.z for n in self.nodes])/len(self.nodes)
        
        return Node(cx,cy,cz)
