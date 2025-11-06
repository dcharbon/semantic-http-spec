.. index:: RDF Context Link Header

.. Copyright © 2025 David Charboneau
..    This work is licensed under Creative Commons Attribution 4.0 International
..    https://creativecommons.org/licenses/by/4.0/


.. _RDF Context Link Header:

***********************
RDF Context Link Header
***********************

A conforming :ref:`Semantic HTTP Resource` **MUST** provide a ``link`` header
for any HTTP response that returns an entity body specifying an RDF context
resource. The ``link`` header **MUST** include a ``rel`` attribute with the
value of ``context`` or recognized equivalent. The JSON-LD standard context
link header is the only recognized equivalent in this revision of the standard.

Example
=======

For a JSON resource, specifying the RDF Context using a valid *RDF Context Link
Header* would look like:

.. sourcecode:: http

   link: <http://example.com/contexts/user.json;
         rel="http://www.w3.org/ns/json-ld#context";
         type="application/ld+json"
