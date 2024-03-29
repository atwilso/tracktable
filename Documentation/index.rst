.. Tracktable documentation master file, created by
   sphinx-quickstart on Sat Aug 30 12:10:57 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Tracktable!
======================

Tracktable's purpose is to load, assemble, analyze and render the
paths traced out by moving objects.  We combine the best tools and
techniques we can find from both Python and C++ with the intent of
making all of our capabilities easily accessible from both languages.
We want to make it easy to...

* Render trajectories as histograms (heatmaps), track
  plots and movies.
* Run heavy-duty analysis in C++ and manipulate the results quickly in
  Python.
* Couple algorithms from top to bottom:

  - databases to store raw data,

  - filtering and cleaning techniques to assemble points into
  trajectories,

  - computational geometry to characterize them,

  - clustering and spatial data structures to find groups, and

  - visualization to help communicate your findings.

* Have fun!

We'll warn you up front that this is Tracktable's first public release.
Version 0.9.9 is a beta test.  Late beta, to be sure, but beta 
nonetheless.  We've done our best to make everything run smoothly but
it's safe to expect a few rough edges.  Please tell us about them so
that we can improve Tracktable!


Documentation
=============

.. toctree::
   :maxdepth: 2

   installation.rst
   user_guide.rst
   examples.rst
   reference.rst
   conventions.rst
   contacts.rst
   credits.rst
   todo.rst

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

