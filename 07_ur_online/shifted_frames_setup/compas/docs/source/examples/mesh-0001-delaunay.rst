.. _example_mesh-delaunay-from-points:

********************************************************************************
Delaunay triangulation
********************************************************************************

.. raw:: html

    <figure class="figure">

.. rst-class:: figure-img img-fluid

.. image:: /images/example-mesh-delaunay-from-points.*

.. raw:: html

    <figcaption class="figure-caption"></figcaption>
    </figure>

.. raw:: html

    <div class="card bg-light">
    <div class="card-body">
    <div class="card-title">Downloads</div>

* :download:`example-mesh-delaunay.3dm </_examples/example-mesh-delaunay.3dm>`
* :download:`mesh-delaunay-from-points.py </_examples/mesh-delaunay-from-points.py>`

.. raw:: html

    </div>
    </div>

.. container:: alert alert-warning

    .. important::
        
        This delaunay triangulation algorithm works in the xy-plane. However, the 
        input can be 3d points resulting in a 2.5d heightfield mesh.


.. literalinclude:: /_examples/mesh-delaunay-from-points.py

