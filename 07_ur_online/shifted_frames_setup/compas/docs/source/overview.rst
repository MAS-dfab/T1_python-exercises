.. _overview:

********************************************************************************
Overview
********************************************************************************

The main library of compas defines the core functionality of the framework
and provides packages for easy integration with CAD software.
The core package (:mod:`compas`) provides viewers and plotters such that it can
be used entirely standalone. The CAD intergation packages simplify working with
three-dimensional geometric data. They provide functionality for processing
geometric models, for visualizing and interacting with :mod:`compas` datastructures,
and for ...


Core functionality
==================

* :mod:`compas`

  * :mod:`compas.com`
  * :mod:`compas.datastructures`
  * :mod:`compas.files`
  * :mod:`compas.geometry`
  * :mod:`compas.interop`
  * :mod:`compas.numerical`
  * :mod:`compas.solvers`
  * :mod:`compas.utilities`
  * :mod:`compas.visualization`


compas.com
----------

:mod:`compas.com` is a package for communicating with external software
such as Matlab.


compas.datastructures
---------------------

:mod:`compas.datastructures` defines three types of fundamental datastructures:
Network, Mesh, and VolMesh.

The Network is an implementation of a general edge graph.
The Mesh is an implementation of a halfedge datastructure for polygonal surface
meshes.
The volumetric mesh (or VolMesh) is the equivalent of a mesh for cellular objects.


compas.files
------------

:mod:`compas.files` provides support for file formats related to the definition
of geometry, (additive) manufacturing, and ...


CAD integration
===============

* :mod:`compas_blender`
* :mod:`compas_dynamo`
* :mod:`compas_grasshopper`
* :mod:`compas_maya`
* :mod:`compas_rhino`

