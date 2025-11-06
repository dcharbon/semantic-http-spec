.. index:: Semantic Architecture

.. Copyright © 2025 David Charboneau
..    This work is licensed under Creative Commons Attribution 4.0 International
..    https://creativecommons.org/licenses/by/4.0/


.. _Semantic Architecture:

*********************
Semantic Architecture
*********************

This specification can be viewed as a concrete realization of a more general
architecture. A *Semantic Architecture* for an API would retain the salient
parts of this specification to convey the schema description, semantic context,
and allowed methods over entities that are exchanged through an API over some
transport protocol. For example, it should be straightforward to define an API
provided over web sockets that provides a semantic architecture by defining
mechanisms for providing the equivalent to HTTP headers for the schema and
context, as well as an equivalent to the HTTP OPTIONS method to provide the
allowed actions for a given resource or object.

