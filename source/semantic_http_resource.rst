.. index:: Semantic HTTP Resource

.. Copyright © 2025 David Charboneau
..    This work is licensed under Creative Commons Attribution 4.0 International
..    https://creativecommons.org/licenses/by/4.0/


.. _Semantic HTTP Resource:

**********************
Semantic HTTP Resource
**********************

A conforming *Semantic HTTP Resource* is a URL-addressable resource that
satisfies the following requirements:

  * **MUST** provide a :ref:`Schema Link Header` for any HTTP response that
    returns an entity body.

  * **MUST** provide a :ref:`RDF Context Link Header` for any HTTP response that
    returns an entity body.

  * **MUST** support the HTTP OPTIONS method and provide a Semantic HTTP
    OPTIONS entity as the response body for an OPTIONS request. HTTP OPTIONS
    responses **MUST** also include the :ref:`Schema Link Header` and
    :ref:`RDF Context Link Header`.
