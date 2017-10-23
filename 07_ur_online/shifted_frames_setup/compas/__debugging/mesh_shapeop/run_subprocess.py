import os
import sys

HERE = os.path.dirname(__file__)

sys.path.insert(0, '/Users/vanmelet/bitbucket/compas_framework/src')

import compas
import compas_rhino.utilities as rhino

from compas_rhino.utilities.scripts import ScriptServer

server = ScriptServer(HERE + '/subprocesses', HERE + '/subprocesses/temp', '/opt/local/bin/pythonw')

# from compas.datastructures.mesh.mesh import Mesh
# from compas_rhino.xxx import add_mesh_gui_helpers
# Mesh = add_mesh_gui_helpers(Mesh)
# mesh = Mesh.from_obj()

from compas_rhino.datastructures.mesh import RhinoMesh

mesh = RhinoMesh.from_obj(compas.find_resource('faces.obj'))
mesh.attributes['name'] = 'FACES'

mesh.vertex['25']['z'] = 0.0
mesh.vertex['29']['z'] = 0.0

res = server.mesh_force_density(mesh=mesh.to_data())
mesh.data = res['mesh']

# res = server.planarize_mesh_faces(mesh=mesh.to_data())
# mesh.data = res['mesh']

res = server.circularize_mesh_faces(mesh=mesh.to_data())
mesh.data = res['mesh']

mesh.draw()
