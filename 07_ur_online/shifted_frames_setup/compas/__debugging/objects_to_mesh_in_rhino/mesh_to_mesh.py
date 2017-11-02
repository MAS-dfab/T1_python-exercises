



from objects_to_mesh import mesh_to_mesh
import rhinoscriptsyntax as rs  


if __name__ == '__main__':
    
    rhino_mesh = rs.GetObject("Select Object",32)
    
    rhino_mesh_dup = rs.CopyObject(rhino_mesh)
    rs.HideObject(rhino_mesh_dup)
    
    trg_len = rs.GetReal("Target Edges Length",0.3)
    
    
    rs.MeshQuadsToTriangles(rhino_mesh)
    
    rhino_mesh = mesh_to_mesh(rhino_mesh,trg_len,vis=5)
    
    rs.SelectObject(rhino_mesh)
    for i in range(3):
        rs.Command("-Smooth Factor=1  CoordinateSystem=World  X=Yes  Y=Yes  Z=Yes  FixBoundaries=Yes ",False)
    
    
    rs.ShowObject(rhino_mesh_dup)
    
    
    #mesh_to_mesh(mesh,trg_len,vis=10)