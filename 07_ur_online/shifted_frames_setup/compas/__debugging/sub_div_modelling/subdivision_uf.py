"""This module ...


..  Copyright 2014 BLOCK Research Group

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        `http://www.apache.org/licenses/LICENSE-2.0`_

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

from compas.datastructures.mesh.operations.split import split_edge


__author__     = ['Tom Van Mele', ]
__copyright__  = 'Copyright 2014, BLOCK Research Group - ETH Zurich'
__license__    = 'Apache License, Version 2.0'
__version__    = '0.1'
__email__      = 'vanmelet@ethz.ch'
__status__     = 'Development'
__date__       = '2015-12-03 13:43:05'


__all__ = [
    'subdivide',
]


def tri_subdivision(mesh):
    """"""
    for fkey in mesh.faces():
        mesh.insert_vertex(fkey)




def quad_subdivision(mesh):
    """"""
    # keep a copy of the faces before splitting the edges
    fkey_vertices = dict((fkey, mesh.face_vertices(fkey, ordered=True)) for fkey in mesh.face)
    # split every edge
    for u, v in mesh.edges():
        split_edge(mesh, u, v, allow_boundary=True)
    # insert a vertex at the centroid of every face
    # create a new face for every vertex of the old faces
    # [a (from split), key, d (from split), centroid]
    for fkey in mesh.faces():
        x, y, z = mesh.face_centroid(fkey)
        # ----------------------------------------------------------------------
        # temp
        # ----------------------------------------------------------------------
        attr = {}
        for key in mesh.face_vertices(fkey):
            for name in mesh.vertex[key]:
                attr[name] = None
        # ----------------------------------------------------------------------
        c = mesh.add_vertex(attr_dict=attr, x=x, y=y, z=z)
        for key in fkey_vertices[fkey]:
            rface = dict((j, i) for i, j in mesh.face[fkey].items())
            a = rface[key]
            d = mesh.face[fkey][key]
            mesh.add_face([a, key, d, c])
        del mesh.face[fkey]


def catmullclark_subdivision(mesh, k=1, fixed=None):
    """"""
    def average(points):
        p = len(points)
        return [coord / p for coord in map(sum, zip(*points))]
    if not fixed:
        fixed = []
    fixed = set(fixed)
    for _ in range(k):
        # keep track of original connectivity and vertex locations
        bkeys           = set(mesh.vertices_on_boundary())
        bkey_edgepoints = {}
        keys            = mesh.vertices()
        key_fkeys       = dict((key, mesh.vertex_faces(key)) for key in keys)
        fkey_vertices   = dict((fkey, mesh.face_vertices(fkey, ordered=True)) for fkey in mesh.faces())
        fkey_centroid   = dict((fkey, mesh.face_centroid(fkey)) for fkey in mesh.face)
        # apply quad subdivision scheme
        # keep track of the created edge points that are not on the boundary
        # keep track track of the new edge points on the boundary
        # and their relation to the previous boundary points
        edgepoints = []
        for u, v in mesh.edges():
            #check if edge is on boundary 
            if mesh.is_edge_naked(u, v):            
                w = split_edge(mesh, u, v, allow_boundary=True)
                if u in bkeys and v in bkeys:
    
                    if u not in bkey_edgepoints:
                        bkey_edgepoints[u] = []
                    if v not in bkey_edgepoints:
                        bkey_edgepoints[v] = []
                    bkey_edgepoints[u].append(w)
                    bkey_edgepoints[v].append(w)
                    continue
            else:
                w = split_edge(mesh, u, v, allow_boundary=True)
            edgepoints.append(w)
        for fkey in mesh.faces():
            x, y, z = fkey_centroid[fkey]
            # ------------------------------------------------------------------
            # temp
            # ------------------------------------------------------------------
            attr = {}
            count = 0
            for key in mesh.face_vertices(fkey):
                for name in mesh.vertex[key]:
                    if name not in attr:
                        attr[name] = 0
                    try:
                        attr[name] += mesh.vertex[key][name]
                    except:
                        attr[name] = None
                count += 1
            for name in attr:
                if attr[name] is not None:
                    attr[name] = attr[name] / count
            # ------------------------------------------------------------------
            c = mesh.add_vertex(attr_dict=attr, x=x, y=y, z=z)
            # ------------------------------------------------------------------
            for key in fkey_vertices[fkey]:
                rface = dict((j, i) for i, j in mesh.face[fkey].items())
                a = rface[key]
                d = mesh.face[fkey][key]
                mesh.add_face([a, key, d, c])
            del mesh.face[fkey]
        # these are the coordinates before updating
        key_xyz = dict((key, mesh.vertex_coordinates(key)) for key in mesh.vertex)
        # move each edge point to the average of the neighbouring centroids and
        # the original end points
        for w in edgepoints:
            nbrs = [key_xyz[nbr] for nbr in mesh.halfedge[w]]
            # move w to the average of its neighbours
            x, y, z = average(nbrs)
            mesh.vertex[w]['x'] = x
            mesh.vertex[w]['y'] = y
            mesh.vertex[w]['z'] = z
        # move each vertex to the weighted average of itself, the neighbouring
        # centroids and the neighbouring mipoints
        for key in keys:
            # ------------------------------------------------------------------
            if key in fixed:
                continue
            # if mesh.vertex[key]['is_fixed']:
            #     continue
            # ------------------------------------------------------------------
            if key in bkeys:
                nbrs = bkey_edgepoints[key]
                nbrs = set(nbrs)
                nbrs = [key_xyz[nbr] for nbr in nbrs]
                e = 0.5
                v = 0.5
                E = [coord * e for coord in average(nbrs)]
                V = [coord * v for coord in key_xyz[key]]
                x, y, z = [E[_] + V[_] for _ in range(3)]
            else:
                fnbrs = [fkey_centroid[fkey] for fkey in key_fkeys[key] if fkey is not None]
                nbrs = [key_xyz[nbr] for nbr in mesh.halfedge[key]]
                n = len(nbrs)
                n = float(len(nbrs))
                f = 1. / n
                e = 2. / n
                v = (n - 3.) / n
                F = [coord * f for coord in average(fnbrs)]
                E = [coord * e for coord in average(nbrs)]
                V = [coord * v for coord in key_xyz[key]]
                x, y, z = [F[_] + E[_] + V[_] for _ in range(3)]
            mesh.vertex[key]['x'] = x
            mesh.vertex[key]['y'] = y
            mesh.vertex[key]['z'] = z


# schemes:
# i: insert
# s: subdivide
# q: quad
# c: catmull-clark
def subdivide(mesh, scheme='i', **options):
    """Subdivide the input mesh."""
    options = options or {}
    if scheme == 'i' or scheme == 'insert':
        tri_subdivision(mesh)
        return
    if scheme == 's' or scheme == 'subdivision':
        tri_subdivision2(mesh)
        return
    if scheme == 'q' or scheme == 'quad':
        quad_subdivision(mesh)
        return
    if scheme == 'c' or scheme == 'catmull-clark':
        catmullclark_subdivision(mesh, **options)
        return
    raise NotImplementedError


def subdivided(mesh):
    """Return a subdivided mesh."""
    pass
