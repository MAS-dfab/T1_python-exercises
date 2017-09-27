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
    
    jack = Dog(PVector(50,50))
    jack.ballofinterest = listofballs[0]
    
def draw():
    global listofballs, jack
    # calculation
    for myball in listofballs:
        myball.update()
    
    jack.update()
    
    if jack.ballofinterest != None:
        d = PVector.sub(jack.ballofinterest.pos, jack.pos).mag()
        if d < jack.ballofinterest.rad+50:
            listofballs.remove(jack.ballofinterest)
            jack.ballofinterest = None
    else:
        maxdist = -99999999.0
        ix = -1 
        for i,ball in enumerate(listofballs):
            d = PVector.sub(ball.pos, jack.pos).mag()
            if d > maxdist:
                maxdist = d
                ix = i
        if ix>=0:
            jack.ballofinterest = listofballs[ix]
        else:
            print("JACK WON")
            noLoop()
    
    #for i in range(10):
    #    b = listofballs[i]
    #    print(str(i)+" : "+str(b.pos.x))

    # drawing
    background(80)
    for myball in listofballs:
        myball.display()
    
    jack.display()