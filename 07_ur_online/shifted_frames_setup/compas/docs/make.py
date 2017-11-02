from importlib import import_module

modules = [
    'compas',
    'compas.com',
    'compas.datastructures',
    'compas.files',
    'compas.geometry',
    'compas.hpc',
    'compas.interop',
    'compas.numerical',
    'compas.visualization',
    'compas.utilities',

    'compas_blender',
    'compas_grasshopper',

    'compas_rhino',
    # 'compas_rhino.conduits',
    # 'compas_rhino.forms',
    # 'compas_rhino.geometry',
    # 'compas_rhino.helpers',
    # 'compas_rhino.numerical',
    # 'compas_rhino.ui',
    # 'compas_rhino.utilities',
]


for name in modules:
    obj = import_module(name)

    print obj

    with open('source/reference/{0}.rst'.format(name), 'wb+') as fp:
        fp.write(obj.__doc__)
