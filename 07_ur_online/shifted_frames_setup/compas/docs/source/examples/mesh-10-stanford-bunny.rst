.. _example_mesh-stanford-bunny:

********************************************************************************
The Stanford Bunny
********************************************************************************

.. raw:: html

    <figure class="figure">

.. rst-class:: figure-img img-fluid

.. image:: /images/example-mesh-stanford-bunny.jpg

.. raw:: html

    <figcaption class="figure-caption"></figcaption>
    </figure>

.. raw:: html

    <div class="card bg-light">
    <div class="card-body">
    <div class="card-title">Downloads</div>

* :download:`mesh-stanford-bunny.py </_examples/mesh-stanford-bunny.py>`

.. raw:: html

    </div>
    </div>

.. literalinclude:: /_examples/mesh-stanford-bunny.py

.. code-block:: none
    
    ply
    format ascii 1.0
    comment zipper output
    element vertex 35947
    property float x
    property float y
    property float z
    property float confidence
    property float intensity
    element face 69451
    property list uchar int vertex_indices
    end_header
