.. _example_mesh-skeleton-modeling:

********************************************************************************
Skeleton mesh modeling
********************************************************************************

.. raw:: html

    <figure class="figure">

.. rst-class:: figure-img img-fluid

.. image:: /images/example-mesh-skeleton-modeling.gif

.. raw:: html

    <figcaption class="figure-caption"></figcaption>
    </figure>

.. raw:: html

    <div class="card bg-light">
    <div class="card-body">
    <div class="card-title">Downloads</div>

* :download:`example-mesh-skeleton-modeling.3dm </_examples/example-mesh-skeleton-modeling.3dm>`
* :download:`mesh-skeleton-modeling.py </_examples/mesh-subd-modeling.py>`

.. raw:: html

    </div>
    </div>

.. container:: alert alert-info
 
    .. note::

        The simple implementation shown does not include angle checks between edges 
        meeting in one node. Hence, depending on the diameter of the cross section of 
        the "tubes", the location of the "inner cross sections" and the angles, the 
        code might produce incompatible convex hull geometries and therefore 
        degenerate subdivision meshes.  
 
.. literalinclude:: /_examples/mesh-subd-modeling.py
