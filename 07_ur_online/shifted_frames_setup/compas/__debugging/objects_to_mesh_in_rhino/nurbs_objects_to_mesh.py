


from objects_to_mesh import nurbs_to_mesh
import rhinoscriptsyntax as rs  


if __name__ == '__main__':
    
    poly_srf = rs.GetObjects("Select Objects",8+16)
    
    if poly_srf:
        srfs_explo = rs.ExplodePolysurfaces(poly_srf) 
    
    if srfs_explo:
        srfs = srfs_explo
    else:
        srfs = poly_srf
       
        
    trg_len = rs.GetReal("Target Edges Length",0.75)
    rhino_meshes = []
    for i,srf in enumerate(srfs):
        print("Computing Surface {0} of {1}".format(i+1,len(srfs)+1))
        rs.EnableRedraw(False)
        rs.HideObject(srf)
        rhino_meshes.append(nurbs_to_mesh(srf,trg_len,vis=5))
        if srfs_explo:
            rs.DeleteObject(srf)

    rs.ShowObjects(srfs)
    rs.JoinMeshes(rhino_meshes, True)