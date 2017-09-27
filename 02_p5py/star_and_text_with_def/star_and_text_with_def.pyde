def setup():
    size(800,800)
    noStroke()
    fill(255)
    rectMode(CENTER)
    textSize(32)
    background(255,0,0)
    
def draw():
    #background(255,0,0)
    a = 150
    b = a/5 * 17
    #rect(width/2,height/2,a,b)
    #rect(width/2,height/2,b,a)
    
    fill(0,0,255)
    text('my text',width/2,height/2)
    
    fill(255)
    star(200,400,7,120,140)
    star(600,600,9,80,100)
    
    # beginShape()
    # a = TWO_PI/10
    # for i in range(10):
    #     m = i%2
    #     ca = i*a
    #     #r = 100 + m*150
    #     r = 250 - m*150
    #     vertex(width/2+r*cos(ca),height/2+r*sin(ca))
    # endShape(CLOSE)
    
def star(cx,cy,num,ra,rb):
    beginShape()
    a = TWO_PI/(num*2)
    for i in range(num*2):
        m = i%2
        ca = i*a
        r = ra + m*(rb-ra)
        vertex(cx+r*cos(ca),cy+r*sin(ca))
    endShape(CLOSE)