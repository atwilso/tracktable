
.. _userguide-python-input:

=====
Input
=====

.. _point-input-python:

-----------
Point Input
-----------

There are three ways to get point data into Tracktable:

1. Instantiate and populate :py:class:`BasePoint` and :py:class:`TrajectoryPoint` objects by hand.
2. Load points from a delimited text file.
3. Create points algorithmically.

.. _manually-instantiate-points-python:

Manually instantiate Points
---------------------------

For instructions on manually instantiating both :py:class:`BasePoint` and :py:class:`TrajectoryPoint`
objects refer to the :ref:`Point Classes section <userguide-python-point-classes>` of
the Python user guide.

.. _loading-points-file-python:

Loading Points from Delimited Text
----------------------------------

Tracktable has a flexible point reader for delimited text files. Each
point domain provides two versions of it, one for loading base points
(coordinates only) and one for loading trajectory points.

.. code-block:: python
   :linenos:

    from tracktable.domain.terrestrial import TrajectoryPointReader

	with open('point_data.csv', 'rb') as infile:
	 	reader = TrajectoryPointReader()
	reader.input = infile
	reader.delimiter = ','

	# Columns 0 and 1 are the object ID and timestamp
	reader.object_id_column = 0
	reader.timestamp_column = 1

	# Columns 2 and 3 are the longitude and
	# latitude (coordinates 0 and 1)
	reader.coordinates[0] = 2
	reader.coordinates[1] = 3

	# Column 4 is the altitude
	reader.set_real_field_column("altitude", 4)

	for point in reader:
		# Do whatever you want with the points here

.. _python-point-sources:

Algorithmically Creating Points
-------------------------------

.. important:: To create points algorithmically we will need to supply
   (at a minimum) coordinates, a timestamp and an ID.

There are a handful of algorithmic point source generators within Tracktable.
The most useful used of which is :py:class:`TrajectoryPointSource` which will
generate points interpolated between a given start and finish point as shown
by the example below. These points can then be assembled into trajectories which
will shown below but explained in further detail in the
:ref:`Trajectory Assembly <python-trajectory-assembly>` section.

.. code-block:: python
   :linenos:

	from tracktable.domain.terrestrial import TrajectoryPoint
	from tracktable.feature.interpolated_points import TrajectoryPointSource
	from tracktable.analysis.assemble_trajectories import AssembleTrajectoryFromPoints

	albuquerque = TrajectoryPoint( -106.5, 35.25 )
	albuquerque.timestamp = Timestamp.from_string('2010-01-01 12:00:00')
	albuquerque.object_id = 'flight1'

	san_diego1 = TrajectoryPoint( -117.16, 32.67 )
	san_diego1.timestamp = Timestamp.from_string('2010-01-01 15:00:00')
	san_diego1.object_id = 'flight1'

	san_diego2 = TrajectoryPoint( -117.16, 32.67 )
	san_diego2.timestamp = Timestamp.from_string('2010-01-01 16:00:00')
	san_diego2.object_id = 'flight1'

	seattle = TrajectoryPoint( -122.31, 47.60 )
	seattle.timestamp = Timestamp.from_string('2010-01-01 19:00:00')
	seattle.object_id = 'flight1'

	denver = TrajectoryPoint( -104.98, 39.79 )
	denver.timestamp = Timestamp.from_string('2010-01-01 19:01:00')
	denver.object_id = 'flight1'

	new_york = TrajectoryPoint( -74.02, 40.71 )
	new_york.timestamp = Timestamp.from_string('2010-01-02 00:00:00')
	new_york.object_id = 'flight1'

	# Now we want sequences of points for each flight.
	abq_to_sd = TrajectoryPointSource()
	abq_to_sd.start_point = albuquerque
	abq_to_sd.end_point = san_diego1
	abq_to_sd.num_points = 180

	sd_to_sea = TrajectoryPointSource()
	sd_to_sea.start_point = san_diego2
	sd_to_sea.end_point = seattle
	sd_to_sea.num_points = 360 # flying very slowly

	denver_to_nyc = TrajectoryPointSource()
	denver_to_nyc.start_point = denver
	denver_to_nyc.end_point = new_york
	denver_to_nyc.num_points = 600 # wow, very densely sampled

	all_points = list(itertools.chain( abq_to_sd.points(),
                                    	sd_to_sea.points(),
                                        denver_to_nyc.points() ))

	trajectory_assembler = AssembleTrajectoryFromPoints()
	trajectory_assembler.input = all_points
	trajectory_assembler.separation_time = timedelta(minutes=30)
	trajectory_assembler.separation_distance = 100
	trajectory_assembler_minimum_length = 10

.. _trajectory-input-python:

----------------
Trajectory Input
----------------

There are two ways to get trajectory data into Tracktable:

1. Instantiate and populate :py:class:`Trajectory` objects by hand.
2. Load trajectories from a delimited text file.

.. _manually-instantiate-trajectories-python:

Manually instantiate Trajectories
---------------------------------

For instructions on manually instantiating :py:class:`Trajectory`
objects refer to the :ref:`Trajectories section <userguide-python-trajectories>`
of the Python user guide.

.. _loading-trajectories-file-python:

Loading Trajectories from Delimited File
----------------------------------------

Tracktable has a flexible trajectory reader for delimited text files. Each
point domain provides a trajectory reader, the functionality between each
is the same just for a different domain type.

.. code-block:: python
   :linenos:

    from tracktable.domain.terrestrial import TrajectoryReader

	with open('trajectories.csv', 'rb') as infile:
	 	reader = TrajectoryReader()
	reader.input = inFile

	# Columns 0 and 1 are the object ID and timestamp
	reader.object_id_column = 0
	reader.timestamp_column = 1

	# Columns 2 and 3 are the longitude and
	# latitude (coordinates 0 and 1)
	reader.coordinates[0] = 2
	reader.coordinates[1] = 3

	# Column 4 is the altitude
	reader.set_real_field_column("altitude", 4)

	# Note that by iterating over the reader, you get a collection of points together as
	# trajectories. Just like the point reader, you can edit the delimiting character and
	# comment character as well as the column properties.
	for traj in reader:
		# Do whatever you want with the points here


----------------------------

.. _userguide-python-output:

======
Output
======

.. _point-output-python:

------------
Point Output
------------

In order to output both :py:class:`BasePoint` and :py:class:`TrajectoryPoint`
from Tracktable the appropriate point writer needs to be used. These writers are
``BasePointWriter`` and ``TrajectoryPointWriter`` respectively. Each point domain
has it's own version of the writers. These output can be to a delimited file or a
standard output buffer. Below is an example of outputing :py:class:`TrajectoryPoint`
to a file, outputing a :py:class:`BasePoint` or using a buffer would have a similar
stucture.

.. code-block:: python
   :linenos:

	from tracktable.domain.terrestrial import TrajectoryPointWriter

	with open('point_output.csv', 'wb') as outfile:
		writer = TrajectoryPointWriter(outfile)
	 	writer.write(points)

.. _trajectory-output-python:

-----------------
Trajectory Output
-----------------

Similar to the point output, in order to output a :py:class:`Trajectory` from Tracktable the
``TrajectoryWriter`` needs to be used. The functionality of the writer is the same as the
:py:class:`BasePoint` and :py:class:`TrajectoryPoint` writers.

.. code-block:: python
   :linenos:

	from tracktable.domain.terrestrial import TrajectoryPointWriter

	with open('point_output.csv', 'wb') as outfile:
	 	writer = TrajectoryPointWriter(outfile)
	 	writer.write(points)