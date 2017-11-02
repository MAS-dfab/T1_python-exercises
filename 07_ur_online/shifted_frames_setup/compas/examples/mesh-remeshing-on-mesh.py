"""Remeshing a 3D mesh."""

from __future__ import print_function

import rhinoscriptsyntax as rs

import compas_rhino

from compas.utilities import geometric_key

from compas.geometry import centroid_points

from compas.datastructures.mesh import Mesh
from compas.datastructures.mesh.algorithms import smooth_mesh_centroid
from compas.datastructures.mesh.algorithms import optimise_trimesh_topology

from compas.cad.rhino.geometry.mesh import RhinoMesh
from compas.cad.rhino.geometry.curve import RhinoCurve

from compas.cad.rhino.conduits.mesh import MeshConduit


__author__    = ['Tom Van Mele', 'Matthias Rippmann']
__copyright__ = 'Copyright 2017, BRG - ETH Zurich',
__license__   = 'MIT'
__email__     = 'van.mele@arch.ethz.ch'


# define the mesh boundary smoother

def smooth_mesh_boundary(mesh, boundary, fixed=None):
    for i in range(10):
        key_xyz = {key: mesh.vertex_coordinates(key) for key in boundary}
        for key in boundary:
            if key in fixed:
                continue
            points = []
            for nbr in mesh.vertex_neighbours(key):
                if key not in boundary:
                    continue
                points.append(key_xyz[key])
            x, y, z = centroid_points(points)
            mesh.vertex[key]['x'] = x
            mesh.vertex[key]['y'] = y
            mesh.vertex[key]['z'] = z


# define the post-processing function
# that will be called at every iteration

def callback(mesh, k, args):
    # prevent the dreaded Rhino spinning wheel
    compas_rhino.wait()

    # unpack the user-defined argument list
    conduit, fixed, target, border = args

    # find the boundary vertices
    boundary = set(mesh.vertices_on_boundary())

    # smooth
    smooth_mesh_centroid(mesh, fixed=boundary, kmax=1)
    smooth_mesh_boundary(mesh, boundary, fixed=fixed)

    # pull the mesh vertices back to the target and border
    for key, attr in mesh.vertices(data=True):
        if key in fixed:
            continue
        if key in boundary:
            x, y, z = border.closest_point(mesh.vertex_coordinates(key))
            attr['x'] = x
            attr['y'] = y
            attr['z'] = z
        else:
            x, y, z = target.closest_point(mesh.vertex_coordinates(key))
            attr['x'] = x
            attr['y'] = y
            attr['z'] = z

    # update the conduit at the specified rate
    conduit.redraw(k)


# get the target mesh
# and its border

guid_target = compas_rhino.select_mesh()
guid_border = compas_rhino.select_polyline()

# get fixed points

points = compas_rhino.get_point_coordinates(compas_rhino.select_points())

# triangulate the input mesh

rs.MeshQuadsToTriangles(guid_target)

# make a remeshing mesh

mesh = compas_rhino.mesh_from_guid(Mesh, guid_target)

# update its attributes

mesh.attributes['name'] = 'Remeshed'
mesh.update_default_vertex_attributes({'is_fixed': False})

# make the target and border objects

target = RhinoMesh(guid_target)
border = RhinoCurve(guid_border)

# make a map of vertex coorindates
# with 1 float precision

gkey_key = {geometric_key(mesh.vertex_coordinates(key), '1f'): key for key in mesh.vertices()}

# identify fixed points

for xyz in points:
    gkey = geometric_key(xyz, '1f')
    if gkey in gkey_key:
        key = gkey_key[gkey]
        mesh.vertex[key]['is_fixed'] = True

# find the fixed vertices

fixed = set(mesh.vertices_where({'is_fixed': True}))

# create a conduit for visualisation

conduit = MeshConduit(mesh, color=(255, 255, 255), refreshrate=5)

# set the target length

target_length = 0.25

# visualise the process with a conduit
with conduit.enabled():
    optimise_trimesh_topology(mesh,
                              target_length,
                              tol=0.1,
                              divergence=0.01,
                              kmax=500,
                              allow_boundary_split=True,
                              allow_boundary_collapse=True,
                              smooth=False,
                              fixed=fixed,
                              callback=callback,
                              callback_args=(conduit, fixed, target, border))

compas_rhino.draw_mesh(mesh, layer='remeshed', clear_layer=True)
