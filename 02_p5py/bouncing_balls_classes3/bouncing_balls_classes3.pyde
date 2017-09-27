from gameobjects import Ball, Dog

def setup():
    size(800,600)
    
    global listofballs, jack
    listofballs = []
    print(len(listofballs))
    for i in range(10):
        pos = PVector(width/2,height/2)
        myball = Ball(pos)
        listofballs.append(myball)
    print(len(listofballs))
    
    jack = Dog(PVector(width/2,height/2))
    
def draw():
    global listofballs, jack
    # calculation
    for myball in listofballs:
        myball.update()
    
    jack.update()
        
    #for i in range(10):
    #    b = listofballs[i]
    #    print(str(i)+" : "+str(b.pos.x))

    # drawing
    background(80)
    for myball in listofballs:
        myball.display()
    
    jack.display()