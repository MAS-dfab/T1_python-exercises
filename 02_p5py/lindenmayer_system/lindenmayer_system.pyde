def setup():
    size(800,800)
    
    global rule, axiom, l, theta
    rule = 'F'
    axiom = 'F[+F][-F]'
    l = 100
    theta = radians(30)
    
def draw():
    translate(width/2,0)
    render_L_system()
    
def render_L_system():
    global rule, l, theta
    
    for c in rule:
        if c=='F':
            line(0,0,0,l)
            translate(0,l)
        elif c=='[':
            pushMatrix()
            l *= 0.8
        elif c==']':
            popMatrix()
            l *= 1.25
        elif c=='+':
            rotate(theta)
        elif c=='-':
            rotate(-theta)

def replace():
    global rule, axiom
    rule = rule.replace('F',axiom)
    print(rule)
    
def keyPressed():
    replace()
    
    
    
    
    
    
    