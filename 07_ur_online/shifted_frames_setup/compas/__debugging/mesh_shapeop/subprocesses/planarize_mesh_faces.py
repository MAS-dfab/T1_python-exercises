"""Module docstring"""

import sys

sys.path.insert(0, '/Users/vanmelet/bitbucket/compas_framework/src')


from compas.datastructures.mesh.mesh import Mesh
from compas.xlibs.shapeop import planarize_mesh_faces
from compas.xlibs.shapeop import circularize_mesh_faces


__author__    = 'Tom Van Mele'
__copyright__ = 'Copyright 2016, Block Research Group - ETH Zurich'
__license__   = 'MIT license'
__email__     = 'vanmelet@ethz.ch'


def main(mesh):
    planarize_mesh_faces(mesh)


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