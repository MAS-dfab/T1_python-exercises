"""Module docstring"""

import sys

sys.path.insert(0, '/Users/vanmelet/bitbucket/compas_framework/src')


from compas.datastructures.mesh.mesh import Mesh
from compas.datastructures.mesh.numerical.methods import mesh_fd


__author__    = 'Tom Van Mele'
__copyright__ = 'Copyright 2016, Block Research Group - ETH Zurich'
__license__   = 'MIT license'
__email__     = 'vanmelet@ethz.ch'


def main(mesh):
    mesh.set_dva({'is_anchor': False, 'pz': 0.0})
    mesh.set_dea({'q': 1.0})

    for key in mesh:
        mesh.vertex[key]['is_anchor'] = mesh.vertex_degree(key) == 2

    for u, v in mesh.edges():
        if mesh.is_edge_naked(u, v):
            mesh.edge[u][v]['q'] = 5.0

    mesh_fd(mesh)


# ==============================================================================
# SCRIPT
# ==============================================================================

if __name__ == '__main__':

    import sys
    import json
    import cStringIO
    import cProfile
    import pstats
    import traceback
    from json import encoder

    ipath = sys.argv[1]
    opath = sys.argv[2]

    with open(ipath, 'rb') as f:
        idict = json.load(f)

    try:
        profile = cProfile.Profile()
        profile.enable()
        # ----------------------------------------------------------------------
        # profiler enabled
        # ----------------------------------------------------------------------
        mesh = Mesh.from_data(idict['mesh'])
        main(mesh)
        data = {'mesh': mesh.to_data()}
        # ----------------------------------------------------------------------
        # profiler disabled
        # ----------------------------------------------------------------------
        profile.disable()
        stream = cStringIO.StringIO()
        stats  = pstats.Stats(profile, stream=stream)
        stats.strip_dirs()
        stats.sort_stats(1)
        stats.print_stats(20)
        odict = {}
        odict['data']       = data
        odict['error']      = None
        odict['profile']    = stream.getvalue()
        odict['iterations'] = None
    except:
        odict = {}
        odict['data']       = None
        odict['error']      = traceback.format_exc()
        odict['profile']    = None
        odict['iterations'] = None

    e_frepr = encoder.FLOAT_REPR
    encoder.FLOAT_REPR = lambda o: format(o, '.16g')
    with open(opath, 'wb+') as f:
        json.dump(odict, f)
    encoder.FLOAT_REPR = e_frepr