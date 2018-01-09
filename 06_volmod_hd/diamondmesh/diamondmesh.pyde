add_library('peasycam')
add_library('hd')

def setup():
    size(800,600,P3D)
    noStroke()
    global shp,s2
    cam = PeasyCam(this,500)
    m = OBJImportExport.loadFromOBJ(sketchPath('')+'/data/diamond.obj')
    #s2 = m.getPShape(this)

    # create a box the size of the mesh
    b = Box()
    for p in m.getPoints():
        b.addPoint(p.x,p.y,p.z)
    print(b)

    # make it a bit bigger
    b.offset(20)
    vs = VoxelSpace(b,100)
    vs.setValueToAll(1000)
    vd = VoxelDistance(vs)
    
    # calculate distance to mesh faces for every voxel
    vd.scanMeshDistanceAll(m)

    # save slices through VoxelSpace as images
    cm = VoxelToImages.getHueMapper(vs)
    VoxelToImages.saveVoxelsAsImageStack(vs,sketchPath('')+'/imstack/',cm)

    shp = vs.getPShape(this, 3.0)

def draw():
    background(77)
    directionalLight(255,128,0,1,0,0)
    directionalLight(0,255,128,0,1,0)
    directionalLight(128,0,255,0,0,1)
    directionalLight(255,0,128,-1,0,0)
    directionalLight(128,255,0,0,-1,0)
    directionalLight(0,128,255,0,0,-1)

    shape(shp)
    #shape(s2)
