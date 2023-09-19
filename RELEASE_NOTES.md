# Tracktable Release Notes

## VERSION 1.7.0, 1 September 2023

Welcome back!  We have a couple of new user-facing features, a lot of 
improvements to infrastructure and documentation (including tutorials),
and a generous handful of bugfixes.

We extend a big thank-you and a fond farewell to Michael Fadem, the
driving force behind most of the engineering improvements over the past
couple years.  Michael has moved on from Sandia and we miss him very much.


### New features in 1.7.0

- Maps in Folium can now be created with the `attr` and `crs` 
  parameters.  The `attr` argument is used to pass an attribution string
  for custom tile sets.  The `crs` argument names a coordinate transform
  to project geographical points into pixel coordinates and back.  The
  functions `tracktable.render.render_trajectories.render_trajectories()` 
  and `tracktable.render.render_heatmap.render_heatmap()` both support these
  new arguments.

- Trajectory maps in Folium can be animated.  See the arguments `animate`,
  `anim_display_update_interval`, `anim_trail_duration`, and `use_markers`
  in `tracktable.render.render_trajectories.render_trajectories()`.
  
- New function `tracktable.rw.load.load_trajectories()` that will load a
  `.traj`, `.csv`, or `.tsv` file and assemble points into trajectories.
  An optional flag will cause it to return points instead of trajectories.
  Examples that load trajectories or points have been updated to use this
  feature.

- Sea ports and airports can be rendered into maps for both the Cartopy
  and Folium back ends.

- Docs and data have been separated out into their own repositories
  implemented as submodules. Note that you will need to `git clone --recursive` 
  when cloning the source code.


### Bug fixes

- We identified and fixed a problem with the I/O library that could cause 
  a buffer overflow if the user opened a file containing UTF-8 data in 
  Python in text mode and then passed it to one of Tracktable's loaders.  

- Map scale bars were being rendered incorrectly in static images under
  map projections that did not use geodetic coordinates (longitude/
  latitude) as their native coordinate system.
  
- Tests for C++ point generators and great circle estimation were failing
  because points did not initialize their coordinates by default.  Fixing
  this results in a very minor slowdown.

- Setting a point property's value to None no longer crashes the interpreter.

- DeprecatedDeclaration.h was not being installed when the user called
  `make install`.  


### Known issues

- The documentation for `tracktable.rw.load.load_trajectories()` implies 
  that it takes a file-like object as its input.  It does not -- it takes
  a string containing a filename.


### Other changes

- The data generators in `tracktable.examples.data_generators` have now moved
  to `tracktable.data_generators`.   

- Movies can be rendered directly from `tracktable.render.render_movie.render_trajectory_movie`
  now.  This subsumes the code that used to be in the 
  `movie_from_trajectories` example. 

- Jupyter notebook tutorials are built locally and stored in a 
  separate repository (tracktable-docs) so that we no longer run
  into the CPU usage limits when uploading to ReadTheDocs.

- The latest release branch in our repository is now called `main`,
  not `master`.

- Sample data has been moved into a separate repository (tracktable-data)
  to help keep the Tracktable repository itself small(er).

### Infrastructure and Support

#### Python 3.6, 3.7 no longer supported

We no longer officially support Python 3.6 or 3.7.  Python 3.6 stopped
getting security updates in December 2021.  Python 3.7 stopped getting
security updates in June 2023.  

Having said that, we have not yet made any changes to the code that 
actually require Python 3.8 or newer.  

If you need to build and run Tracktable 1.7 in an environment where you
absolutely cannot update to a more recent Python version, contact us.  
We sympathize -- we have plenty of experience with such environments --
and we'll work with you to get you up and running.

#### Wheels available on PyPI, GitHub

We are now building wheels for Python versions up through 3.11.  On Linux,
we build and upload wheels to [PyPI](https://www.pypi.org) for Python 
versions 3.6 through 3.11.  On Windows and MacOS (Intel), we build wheels
for Python 3.8 through 3.11.  On MacOS (Apple Silicon/arm64), we build
wheels for Python 3.10 and 3.11.  

#### Internal changes to build infrastructure

We've moved all of our Linux build infrastructure to Docker containers
for easier management.  This also helps us build wheels with the `manylinux`
standard that are usable on most common distributions.  Along the way,
we've integrated test coverage and code linting into our CI pipeline.

We're planning to do something similar for our Windows builds now that
Docker on Windows hosts can run containers with the Windows kernel.

MacOS build and test procedures are still run via shell scripts due to
the lack of container support in the MacOS kernel.  


## VERSION 1.6.0, 16 September 2021

NOTE:

This release includes a hotfix for a download error in Cartopy.  As soon
as the Cartopy team is able to fix this in a new release we will update
our version requirements and remove the hotfix.  For more information
about the underlying problem, see https://github.com/nvkelso/natural-earth-vector/issues/581.


This release includes major API changes:

- Render module (`tracktable.render`) has been refactored to abstract away
  details of the back end

- Analysis module (`tracktable.analysis`) has been split into Applications
  (`tracktable.applications`) and Algorithms (`tracktable.algorithms`).
  Bindings from the Analysis module are still in place with deprecation
  warnings and will be removed in release 1.8.

The Applications module contains functions for prediction, anomaly
detection, clustering, and "boxiness" (how close a trajectory is to a
perfect square).  We will be refining and updating these modules
in the next few releases.

We've added better debugging support for our import process.  The common
error about being unable to import `_core_types` has been augmented by
tests to find out exactly where in the import chain things are going wrong.


This release also includes revamped Python tutorials and demos which should be easier to follow
and try out for yourself! Find them in the code at `...tracktable/Python/tracktable/examples`
and on ReadTheDocs at https://tracktable.readthedocs.io/en/latest/examples/examples.html.

### GENERAL UPDATES SINCE 1.5.0

- The refactor of `tracktable.render` should allow for better ease of use going forward as well
as providing abstraction the parts of the module that shouldn't be used directly.

- `tracktable.analysis` has been deprecated in favor of
  `tracktable.algorithms`, `tracktable.applications` and `tracktable.domain`.
  All functions under `tracktable.analysis` are still usable.  The bindings in
  `tracktable.analysis` will be removed in release 1.8 and will print deprecation
  warnings in 1.6 and 1.7.

- Fully removed `tracktable.io` and `tracktable.source`.

- `core_types` error messages have been updated and we've included additional debugging capabilities.

### NEW CAPABILITIES SINCE 1.5.0

- We've added in the ability to render heatmaps directly from the
  `tracktable.render` module! This process is identical to that of
  `render_trajectories`.

- Two new modules have been added.
  - `tracktable.applications` contains pre-built analysis applications such
    as anomaly detection, trajectory prediction, clustering, trajectory
    assembly from points, and trajectory partitioning.  We invite you to use
    these in your own applications and look at the source code if you want
    to modify or improve them.

  - `tracktable.algorithms` contains the algorithmic building blocks used
    in the Applications module, chiefly boxiness, DBSCAN and distance
    geometry.

- A scale can now be added to static maps.

- Trajectories can be simplified directly when calling `render_trajectories`.

- It's now possible to add points one at a time to an R-tree.
  - We've also reduced the R-tree's memory usage.

### BUGS FIXED SINCE 1.5.0

- The reader for .traj files was skipping trajectories with fewer points
  than the previous one.

- Minor C++ type issues.

- Time zones on Python datetime objects were being ignored when assigning
  to a trajectory timestamp.


### SPECIFIC ISSUES:

- #68 - Better debug support for import errors
- #293 - Python cartesian plots need to be revisted to address GeoAxes issues
- #307 - Finalize deprecation of tracktable.io and tracktable.source
- #336 - draw_scale
- #368 - Reduce Python R-tree memory usage
- #369 - Allow for user-specified point indices for RTree points
- #374 - Very Small Type Problem in C++ Code
- #375 - Simplify Trajectories During Render_Trajectories
- #377 - Cleanup render_trajectories.py
- #379 - Interactive heat map rendering
- #381 - Move python and data files for new example notebooks from bread crumbs to tracktable
- #382 - Move tutorial_1 from bread crumbs to tracktable
- #383 - Move tutorial_2 from bread crumbs to tracktable
- #384 - Move tutorial_3 from bread crumbs to tracktable
- #385 - Move tutorial_04 from bread_crumbs to tracktable
- #386 - Move tutorial_5A from bread_crumbs to tracktable
- #387 - Move tutorial_5B from bread_crumbs to tracktable
- #388 - Move tutorial_5C from bread_crumbs to tracktable
- #389 - Move tutorial_6 from bread_crumbs to tracktable
- #390 - Move prediction demo from bread_crumbs to tracktable
- #391 - Move anomaly detection demo from bread_crumbs to tracktable
- #392 - Move boxiness demo from bread_crumbs to tracktable
- #393 - Move rendezvous from bread_crumbs to tracktable
- #394 - Move shape clustering from bread_crumbs to tracktable
- #395 - Cleanup Python WIP Examples
- #398 - Investigate Cap Stew Notebook Examples For Useful Code
- #399 - Refactor Structure Of Render Module
- #405 - Update Docs And Website With New Information About Core_Types Error
- #410 - Timestamp should be converted to UTC when assigned to a point
- #412 - Refactor tracktable.analysis
- #421 - Cartopy feature downloads are broken












## VERSION 1.5.0, 3 April 2021

This release includes major updates to the documentation.  The Python and C++ user guides have been overhauled.  Example Jupyter notebooks are now included in the documentation.

We are also building wheels for Python 3.9 as of this release.  Tracktable 1.6, due in summer 2021, will be the last version to support Python 3.5.  (Python 3.5 has reached the end of its support window.  See https://www.python.org/downloads/release/python-3510/ for details.)

### DEPENDENCY UPDATES

Tracktable now requires a compiler that supports C++14.  This means GCC 5, Clang 3.4, Microsoft Visual C++ 19 (2015), and Intel C++ 17.

We now require CMake 19 in order to support Python 3.9.

Advance warning: we will be moving our required Boost version to 1.75 as of Tracktable 1.7, due in Q3 2021.

### BUGS FIXED SINCE 1.4.1

TrajectoryReader was printing excessive debug output.

ECEF (Earth Centered / Earth Fixed) coordinate conversion would fail if `tracktable.domain.cartesian3d` had not already been imported.

Specific issues:

- #322 - Update conf.py file to handle auto pathing
- #314 - render_trajectories for Folium needs to be updated to match changes in bbox parameter ordering
- #309 - Incorrect parameter order specified in documentation for render_trajectories
- #308 - degrees function missing math import
- #306 - Relocate files in tracktable.source to more appropriate locations
- #304 - Document tracktable::simplify
- #303 - Params for Clustering Example Notebook
- #301 - Jupyter example notebooks failing to render maps
- #262 - Move object ID out of Classify into its own example
- #218 - Clean up C++ Classify example
- #217 - Clean up C++ Filter Example
- #215 - Clean up C++ Reduce example
- #214 - Clean up C++ Cluster example
- #132 - Clean up C++ Predict example
- #116 - Clean up C++ Serialization example
- #1 - Basemap deprecation warnings

Specific merge requests not addressed above:

- !210: Docs Warning Fix & Missing Changes
- !208: Pull in Boost compatibility fixes that arose with 1.74
- !204: Make example_* scripts in tracktable.examples conform to Python style
- !203: CI YAML updates
- !202: Update all code copyrights to 2021
- !200: Resolve "Revamp User Guide"
- !199: Verify all documentation updates build on ReadTheDocs prior to release
- !197: Missing API documentation
- !194: Remove unused file CentroidTerrestrial.h

### UPCOMING FEATURES

In 1.6 and 1.7 we expect to add:

- Python bindings for C++ data generators
- Python bindings for KML output
- Readers and writers for trajectories in GeoJSON
- API cleanup for render_trajectories
- More documentation updates and example notebooks






## VERSION 1.4.1, 1 December 2020

This is a bugfix release with a few features that will be rolled out officially in Tracktable 1.5.0, due early in 2021.

### BUGS FIXED SINCE 1.4.0

A regression arose in an interaction between Cartopy, Jupyter, and Shapely that caused static map rendering to error out in Jupyter notebooks.

Specific issues:

- #252: Allow users to skip undelimited headers in point input files
- #254: Fix segfault when file not terminated by newline
- #255: Log line numbers when reporting errors from point reader
- #282: `tracktable::subtract_in_place` did not return its results properly.
- #308: Missing `math` import in `tracktable.core.geomath`
- #309: Incorrect parameter order in documentation for `render_trajectories()`
- #314: `render_trajectories()` for Folium updated to take bounding box components in the right order

### FEATURES IN PROGRESS

These features will show up if you look at the source code but are not ready for production use yet.

- Data generators in C++
- Command-line factories in C++ (helpers for command-line options)
- KML output for trajectories
- C++ example source code cleaned up
- Lots of documentation additions and improvements

### INCOMPATIBLE API CHANGES

- C++ header files previously found under `tracktable/IO/` are now under `tracktable/RW/`.  This parallels a change in the Python module structure.
- The Python module formerly known as `tracktable.io` is now `tracktable.rw`.  The old bindings are still in place and will issue a deprecation warning.
- The Python trajectory assembler is now in the `tracktable.analysis.assemble_trajectories` module instead of `tracktable.source.trajectory`.  The old bindings are still in place and will issue a deprecation warning.

(Note: Yes, it is poor practice to introduce a breaking API change in a point release.  We apologize for the mess.)

### KNOWN ISSUES IN 1.4.1

Forcing the PlateCarree projection when rendering maps using Cartopy may cause data drawn on top of a map to be slightly offset from its true location.  This is most likely to occur if you choose a projection other than PlateCarree.








## VERSION 1.4.0, 14 October 2020

This is a feature release.

### NEW FEATURES SINCE 1.3.1

The main feature is an implementation of ECEF (Earth Centered / Earth Fixed) coordinates.  ECEF coordinates (see [Wikipedia](https://en.wikipedia.org/wiki/ECEF)) are a 3D Cartesian space where the Earth lies centered within the cube whose corners are [-1, -1, -1] and [1, 1, 1].  This coordinate frame rotates with the Earth: x=0 will always be aligned with the prime meridian.

You can get an ECEF version of a terrestrial point by calling :python:`tracktable.core.geomath.ECEF(my_point, altitude_field="altitude")`, :python:`tracktable.core.geomath.ECEF_from_feet(my_point, altitude_in_feet)`, and :python:`tracktable.core.geomath.ECEF_from_meters(my_point, altitude_in_meters)`.  These functions are also available in C++ as members of :cpp:`tracktable::domain::terrestrial::TerrestrialTrajectoryPoint`.

We have also added a `clone()` method to trajectories in Python.  This will return a new copy of a trajectory instead of a pointer to the original.  This method is unneeded in C++: :cpp:`new_trajectory = original_trajectory` will suffice.

We have updated the insert() method for trajectories in Python to allow multiple points to be inserted with one function call.  Similarly, slicing a trajectory (like any other list) will now return a new trajectory that inherits its parent's metadata.

Interactive trajectory rendering is available in :python:`tracktable.render.render_trajectories.render_trajectories()`.  This will use [Folium](https://python-visualization.github.io/folium/) if you are inside a Jupyter notebook and [Cartopy](https://scitools.org.uk/cartopy/docs/latest/) otherwise.  We intend to clean up the API for trajectory rendering for 1.5.0.

Alert readers will notice some infrastructure for test data generators.  These are still work in progress and are slated for release in 1.5.0.

The latest release in our Github repository (https://github.com/sandialabs/tracktable) is now on branch 'main'.  The branch named 'master' is deprecated and will be emptied out in release 1.5.0 except for a text file pointing visitors to the branch 'main'.

### BUGS FIXED SINCE 1.3.1

Many undocumented functions and methods are now documented.  This is a major effort under way.  We encourage users to send us bug reports on documentation that is missing or still in error.

Specific issues:

* #86: Avoid a divide-by-zero issue when rendering trajectories that don't move

* #212: Propagate coordinate system through Cartopy rendering so data stays aligned with map

* #245: Distance geometry values were not being scaled properly

* #250: Spherical clustering option is missing on DBSCAN bindings


### KNOWN ISSUES IN 1.4.0

Functions in binary extension classes are not yet included in the documentation.

Point readers will trip an assertion and probably crash when reading a file that does not end with a newline.




## VERSION 1.3.1, 21 July 2020

This is a patch release.

### NEW FEATURES SINCE 1.3.0

* This release includes the beta launch of interactive trajectory rendering in Jupyter notebooks using [Folium](https://python-visualization.github.io/folium/).  There is an example of how to do this in the Render_Trajectories example notebook.  The notebooks can either be downloaded from Tracktable's web site (
<https://tracktable.sandia.gov/downloads/documentation.html>) or copied from an installation using :python:`tracktable.examples.copy_example_notebooks('/where/to/put/them')`.  Expect tweaks to the API for interactive trajectories between now and the official launch in 1.4.0.

* The trajectory writers (:python:`tracktable.domain.<domain>.TrajectoryWriter`) will now accept single trajectories as well as lists of trajectories as arguments to `write()`.

* New function: :python:`tracktable.info.cities.get_city()` will retrieve City objects based on spelling, location, or country.

* New function: :python:`tracktable.analysis.dbscan.cluster_labels_to_dict` will create a dictionary containing cluster IDs and feature vectors that can easily be converted to a [Pandas] DataFrame.  We would like to hear feedback on how this function could better suit your use case.

* Added capability: Trajectories in C++ now have reverse iterators and explicit functions for const iterators.  Added `rbegin()`, `rend()`, `crbegin()` and `crend()`.

### BUGS FIXED SINCE 1.3.0

(Note: the issue numbers are internal to our development process.  We don't yet have a way to expose our issue queue to the outside world.)

* Issue #181: Cartopy maps have wrong aspect ratio when min_longitude and max_longitude are the same.

* Issue #182: :python:`tracktable.examples.copy_example_notebooks()` will now create the destination directory for you if it does not already exist.

* Issue #184: In an attempt to make PointReader quieter, we accidentally made it even noisier.

* Issue #76: The Simple Clustering example refers to a data set that is not included in Tracktable.  We've moved the notebook back into Work In Progress status until we can fix this.

* Issue #202: If you install Tracktable's Python package on a very, very new Windows system, you might be missing the Visual C++ runtime.  This is now mentioned in our documentation and FAQ.  We don't currently have a way to distribute that ourselves.

### HOTFIXES SINCE 1.3.0

We launched 1.3.0 without the Jupyter notebooks in the wheel.  Oops.

### KNOWN ISSUES

We believe there are no major bugs loose at the moment.





## VERSION 1.3.0, 19 May 2020

This is a feature release.

### NEW FEATURES SINCE 1.2

* Distance geometry code has been added to C++ and Python.  Distance geometry is a family of algorithms that operate on curves represented as a (partial)
matrix of distances between points sampled from the curve.  In C++, check out the functions :cpp:`tracktable::distance_geometry_by_distance()` and
:cpp:`tracktable:distance_geometry_by_time()`.  In Python, check out the module
:python:`tracktable.analysis.distance_geometry`.

* We now include several Jupyter notebooks as examples of how to use Tracktable.  These are in addition to the scripts in :python:`tracktable.examples`.  You can download the scripts from the Tracktable web site (<https://tracktable.sandia.gov>) or copy them from the installed library with the following commands:
```python
import tracktable.examples
tracktable.examples.copy_example_notebooks('/path/to/my/notebooks')
```

* Log messages have been cleaned up.  Log output from C++ now uses Boost's logging facilities.  Log output from C++ now uses Python's `logging` module.  The function `tracktable.core.log.set_log_level()` will set the minimum severity for both.  Particularly noisy modules such as the point reader and trajectory assembler are now much quieter.

* We now use the [Libtool library versioning scheme](https://www.gnu.org/software/libtool/manual/html_node/Updating-version-info.html) for the Tracktable shared libraries.

* We now support Python 3.8.

* We include support for building RPMs containing Tracktable's shared libraries.  These RPMs do not yet include the Python interface.

* Along with RPM support, we generate a [pkg-config](https://people.freedesktop.org/~dbn/pkg-config-guide.html) configuration file.

* Python example scripts for rendering heatmaps, trajectory maps, and making movies are back.

* Terrestrial points have an `ECEF()` method that will return the earth-centered earth-facing (ECEF) coordinates for the point.

* We now require a compiler capable of C++11.

* It is now possible to generate just the C++ documentation instead of C++ and Python.  The CMake variable `BUILD_DOCUMENTATION_CXX_ONLY` controls this.

### NOTABLE FIXES

* Boost versions 1.71 and newer were failing to compile due to a CMake issue.
* TrajectoryWriter was failing and sometimes crashing because the destination file would sometimes be closed before its final flush.
* The function `tracktable.core.geomath.convex_hull_aspect_ratio()` would return NaN for degenerate trajectories (those whose convex hull was a single point or line segment).  While this is mathematically correct, we've changed it to return 0 for convenience.  The value 0 should not appear except in degenerate situations.
* `tracktable.core.geomath.speed_between()` was always returning 0.
* We now use CMake's FindThreads module to find and link against thread libraries.  Some Boost components now require this.




VERSION 1.2.4, 23 January 2019
------------------------------

This is a bugfix release.  There are no new features.

### UPDATES SINCE 1.2.3

No features have been updated or added.

### NOTABLE FIXES

* Remnants of some old logging code were causing `tracktable.render.paths.draw_traffic()` to raise exceptions.
* There was an uncommon case in `tracktable.render.paths.draw_traffic()` that would cause an error if no label generator was set (which is the default).

### HOTFIXES SINCE 1.2.3

No hotfixes have been deployed since 1.2.3.

### KNOWN ISSUES

If you configure a point reader with a coordinate that does not exist for the point type (e.g. `reader.coordinates[2] = 4` for a domain like `terrestrial` that only has coordinates 0 and 1), Tracktable will fail an assertion and exit when the reader loads its data.

VERSION 1.2.3, 18 January 2019
------------------------------

This is a bugfix release.  There are no new features.

We are no longer building Python wheels for Python 2.7.  Python 2.7 is [no longer supported at all](https://www.python.org/doc/sunset-python-2/) by the Python Software Foundation as of January 1, 2020.  We expect to remove CMake support for Python 2 in Release 1.3, due out in mid-to-late February.


### UPDATES SINCE 1.2.2

* Configuration files now insist upon Boost 1.61 or newer and CMake 3.12 or newer.  There were a few old instances that would only require 1.57 and 2.8, respectively.

### NOTABLE FIXES

* Trajectory assembler now correctly prints its separation duration.
* The Cartopy map example no longer relies on outdated/removed example code.
* There was a bug that caused `tracktable.core.geomath.compute_bounding_box` to fail on trajectories that had been loaded from pickle files instead of assembled from points.  Fixed.

### HOTFIXES SINCE 1.2.2

* No hotfixes have been deployed since 1.2.2.

### KNOWN ISSUES

* Building for Python 3.8 is error-prone because of changes to CMake's infrastructure for finding Boost, Python, and Boost's Python library.
* There may be trouble building against Boost versions 1.71 and newer because of changes to the way Boost and CMake interact.
* If you build from source on Linux you will probably need to add `-lpthread` to CMAKE_EXE_LINKER_FLAGS.

VERSION 1.2.2, 2 January 2019
-----------------------------

This is a quality-of-life release.

### UPDATES SINCE 1.2.1

* The C++ function `tracktable::point_at_fraction` and the Python function `tracktable.core.geomath.point_at_fraction` have both been renamed to `point_at_length_fraction` to remove confusion about what they do.  The previous name was ambiguous: was the interpolation fraction being computed with respect to trajectory duration or with respect to travel distance?  In Python, `point_at_fraction` will print a deprecation warning.  In C++, `point_at_fraction` is simply gone.  The deprecated Python binding will be removed in release 1.3.
* Tracktable should be much quieter.  All debug/info/warning/error messages are now directed to a logger instead of writing directly to standard output or standard error.  Right now the C++ and Python messages go to different destinations.  Log messages in C++ go to `boost::log`.  Log messages in Python go to the standard `logging` module.  We will unify these in a future release.

### HOTFIXES SINCE 1.2.1

No hotfixes have been deployed since the last release.


VERSION 1.2.1, Mid-November 2019
--------------------------------

This is a bug-fix/documentation release.

### DOCUMENTATION UPDATES

* The Installation page in the documentation has had its list of dependencies brought up to date.  It also now contains a recommendation that you install from binary packages on Pip wherever possible.
* There are now Jupyter notebooks in `tracktable/Python/tracktable/examples/notebook_examples`.  We are working through the Python examples one at a time to bring them up to date and provide Jupyter versions.

### NOTABLE FIXES

* Custom map bounding boxes were not working in `tracktable.render.mapmaker.mapmaker()`.
* Bounding boxes (`tracktable.domain.<domain>.BoundingBox`) were not printing correctly.
* Bounding box corners could not be correctly accessed from Python.  They now show up as properties min_corner and max_corner.
* Bounding boxes can now be constructed from two point-like objects.  A point-like object is anything that can be treated like an array of coordinates.

### HOTFIXES SINCE 1.2.0

* The module `tracktable.source.random_point_source` has been replaced by `tracktable.source.point`, formerly known as `tracktable.source.scatter`.
* The module `tracktable.source` is now included in the installer.
* Link syntax in Markdown README fixed.
* PyPI classifier strings for Linux and OS X fixed.
* Auditwheel now correctly requests `manylinux1` platform tag on Linux.
* README.md now included in wheel.
* Windows build now correctly links against libpython.


VERSION 1.2.0, October 2019
---------------------------

This is a major update.

### NEW FEATURES

* We are now using [Cartopy](https://scitools.org.uk/cartopy/docs/latest/) instead of Basemap to render geographic maps.  Basemap no longer works with recent versions of Matplotlib and is at end-of-life along with Python 2.7.

* We can now build wheels (Python binary install packages) for Python versions 3.5, 3.6, 3.7, and possibly even 2.7.  We will be uploading these to PyPI so that you can `pip install tracktable` instead of building from source.  We will also make these available for download on our web site.

* Jupyter notebook examples!  They are in the `notebooks` subdirectory under the Python examples, or you can get them as a separate zip file on [our web site](https://tracktable.sandia.gov).

* We finally have a web site!  Visit us at <https://tracktable.sandia.gov>.

* Documentation is now hosted at <https://tracktable.readthedocs.io>.

* Python examples are getting overhauled one by one.  A file named `example_foo.py` will have a fully self-contained example of how to use some specific capability in the library.  The other examples (`heatmap_from_points`, `trajectory_map_from_points` and `movie_from_points`) are ready to run on your own data.

* New module tracktable.io.point with a convenient interface for instantiating point readers (trajectory points and base points).  Soon this will get bindings for point writers as well.

* Points and trajectories can now be serialized using `boost::serialization` or Python's `pickle` module.

### NOTABLE FIXES

* Examples were relying on the nonexistent module `tracktable.source.random_point_source`.  It has been replaced with `tracktable.source.scatter`.

* `tracktable.io` and `tracktable.analysis` modules were not getting installed by `make install`.

* Data files for `tracktable.info` were not getting installed by `make install`.

* Timestamp format was not configurable on Python trajectory point reader.

* Point metadata properties are now on trajectory point reader (where they belong) instead of base point reader.

### OUTSTANDING ISSUES

* We expect a few rough edges on the Cartopy support, especially decoration features in `tracktable.render.mapmaker` that don't quite work like they should.

* C++ examples still need cleanup.


VERSION 1.1.1, August 2019
--------------------------

This version includes two bugfixes since 1.1.0:

* The Python module ```tracktable.analysis``` was not being installed
  during ```make install```.

* The ```current_length``` property was not exposed on TrajectoryPoint
  instances.

VERSION 1.1.0, May 2019
-----------------------

This version is the last in which we will actively support Python 2.7.
Python 2 is scheduled to
[end support](https://www.python.org/dev/peps/pep-0373/)
on January 1, 2020.
Many packages (TensorFlow, Pandas, iPython, Matplotlib, NumPy,
SciPy... see [the Python 3 Statement](https://python3statement.org/)
for the full list) have already dropped support for Python 2.

We also expect that this will be the last version of Tracktable that
uses Basemap for its back-end rendering layer.  Basemap's maintainer
has stated that there will be one final release at the end of 2019
followed by honorable retirement.  We thank the entire Basemap team,
past and present, for their many years of service.


### NEW FEATURES

* Tracktable now has mailing lists!  Send a blank email to
  <listname>-join  at software dot sandia dot gov to request membership.  The
  available lists are:

  * tracktable-announce - Very low volume.  New releases of Tracktable
    will be announced here.

  * tracktable-develop - Discussions of new features and changes to
    the library will be conducted here.

  * tracktable-commit - Commit messages will be forwarded to this list.

* We are moving the repository to GitHub.  Starting with this release,
  the canonical URL will be
  [https://github.com/sandialabs/tracktable](https://github.com/sandialabs/tracktable)
  with documentation at ReadTheDocs.

* As of Version 1.1, we require Boost 1.61 or newer and CMake 3.0 or newer.

* Functions ``tracktable.core.current_memory_use()`` and
  ``tracktable.core.peak_memory_use()`` are now available.

* Functions on trajectories:

  * ``time_at_fraction()`` will give you a point along a trajectory at any
    fraction between beginning and end.

* Functions on points:

  * ``extrapolate()`` is like ``interpolate()`` in that it takes two
    points and a floating-point number and interpolates between the
    start and end points according to that float.  Unlike
    ``interpolate()``, it doesn't do any bounds checking: it is perfectly
    legitimate to ask for ``extrapolate(hither, yon, -1.0)``.

  * ``distance()`` now computes distance between any combination of
    points and trajectories.

* Clustering with DBSCAN:

  * The DBSCAN interface has been cleaned up.  You will no longer
    instantiate ``tracktable::DBSCAN``.  Instead, call
    ``tracktable::cluster_with_dbscan()``.

  * You can decorate the points you feed to DBSCAN.  For example, if
    you want to store your own index, you can pass in a
    ``std::pair<PointType, int>``.

* Trajectory I/O using JSON:

  * We now support reading and writing trajectories to JSON in Python.
    Check out the functions ``json_from_trajectory`` and
    ``trajectory_from_json`` in the ``tracktable.io.read_write_json``
    module.  Look for JSON support in C++ in an upcoming version.

* The example scripts in the Python directory now have their own page
  in the documentation.


### NOTABLE FIXES

* We can now use Boost versions up to 1.69.  As of Boost 1.67, the
  name of the Python shared library changed in a way that broke our
  build process.  Fixed.  Note, however, that we cannot yet deal with
  CMake-ified versions of Boost.

* We detect Anaconda's Python interpreter on OS X and modify the link
  flags so that loading Tracktable in Python code does not instantly
  generate a segmentation fault.

* Many spurious compilation warnings in Boost have been disabled.

* Distances in the terrestrial domain are now returned properly in
  kilometers.

* We use ``sphinx.autodoc_mock_imports`` in our documentation so that you do not
  need to build the entire toolkit just to create the documentation.
  This still needs a little work to remove the need for CMake.


### OUTSTANDING ISSUES

* The C++ examples need to be cleaned up and documented.  This would
  be a good "getting started" exercise for people who are new to the
  code base.

* There are several useful scripts in
  ``tracktable/Python/tracktable/examples/work_in_progress`` that need
  minor fixes to run with the latest API.


### COMING SOON

* We are experimenting with various replacements for Basemap.  As of
  May 2019 the leading contenders are
  [Cartopy](https://scitools.org.uk/cartopy/docs/latest/) for offline
  rendering and either
  [Folium/Leaflet](https://python-visualization.github.io/folium/) or
  [Plotly](https://plot.ly/) for interactive rendering.  We welcome
  suggestions and discussion!  Please join the tracktable-develop
  mailing list if you're interested.

* We are almost ready to move our documentation to ReadTheDocs.  Look
  for an announcement on the ``tracktable-announce`` mailing list.

* C++11 features will be permitted in new contributions to the library.


--------------------------------------------------------------------


VERSION 1.0.5, March 2018
-------------------------

This is a bug-fix release.

NEW FEATURES
------------

* No new features.


NOTABLE FIXES
-------------

* Writing to files or to file-like objects in Python caused a
  segfault.  See the commit on Feb 21 2018 whose hash begins with
  8db2248d for details.

* C++ headers for convex hulls were not being installed with 'make
  install'.


OUTSTANDING ISSUES
------------------

* Link errors / segfaults under certain OSX configurations, especially
  the Anaconda Python environment.



----------------------------------------------------------------------


VERSION 1.0.4, November 2017
----------------------------

NEW FEATURES
------------

* Trajectories can be written to and read from JSON and Python
  dictionaries.  At the moment this is only present in Python.  Check
  out tracktable.io.read_write_dictionary and
  tracktable.io.read_write_json.

NOTABLE FIXES
-------------

* References to ``std::cout`` are still in Boost's geometry library.  This
  causes compile problems if I don't work around it.

* ``tracktable.core.Timestamp.from_string()`` should now honor ``%z``
  in Python 3.  Support for the ``%z`` directive is missing in Python
  2.

----------------------------------------------------------------------


VERSION 1.0.3, October 2017
---------------------------

Cleanup release.  We've removed the old Python point writers.  These
were made obsolete by the introduction of point domains.

We've also fixed some tests that were failing because of numeric
imprecision.

Copyright notices on all files updated after NTESS replaced Sandia
Corporation (Lockheed Martin) as the operator of Sandia National Labs.

----------------------------------------------------------------------


VERSION 1.0.2
-------------

There is no Version 1.0.2.


----------------------------------------------------------------------


VERSION 1.0.1, April 2016
-------------------------

NEW FEATURES
------------

* Convex hull measures for 2D spaces (Cartesian and geographic)
* Support Python 3
* Property values can now be null

NOTABLE FIXES
-------------

* Minimize calls to ``std::imbue``.  This was 90% or more of the time
  it took to read trajectories.

----------------------------------------------------------------------


VERSION 1.0, January 2016
-------------------------

NEW FEATURES
------------

* DBSCAN clustering exposed to Python
* RTree spatial index exposed to Python
* Point writers in C++ exposed to Python
* Trajectory writer added to C++
* Named property values can now be integers

NOTABLE FIXES
-------------

* Python wrappers for feature vectors no longer need quite as much memory at compile time
* Guard against NaN results for math on the sphere
* Timestamps are now interpolated with microsecond resolution

----------------------------------------------------------------------


VERSION 0.9, September 2015
---------------------------

First public alpha release.

### NEW FEATURES


* Boost r-tree exposed to C++ and Python for all point types along with common query functions.
* Convenience method ``tracktable.core.geomath.recompute_speed`` added since we have to do this so often
* Configurable timestamp input format
* Point writer generalized to work with all domains, output to stream instead of requiring filename
* Add "feature vector" point types (undecorated vectors of doubles) for clustering


### NOTABLE FIXES

* Length of terrestrial trajectories now returned in kilometers instead of radians


----------------------------------------------------------------------


VERSION 0.3, March 2015
-----------------------

Internal release only.


### NEW FEATURES

* Tracktable now builds with Visual Studio!
* Automatic bounding box computation (used for culling during rendering)
* Tests of image generating code now compare against ground truth image


### NOTABLE FIXES

* Avoid compiler-specific definitions of ``size_t`` in favor of ``std::size_t``


----------------------------------------------------------------------


VERSION 0.2, December 2014
--------------------------

Internal release only.

### NEW FEATURES


* Allow points in 2D and 3D Cartesian space as well as geographic space
* ``tracktable.render.mapmaker`` - convenience calls for many common map use cases
* Delimited text point writer added to Python
* Delimited text point reader added to C++, exposed to Python
* Named properties added to ``tracktable::Trajectory``
* Code in ``tracktable.examples`` can now be used as a module
* ``tracktable::Trajectory`` can now be used with ``boost::geometry`` functions
* Header files install into ``${INSTALL}/include/tracktable``
* Add DBSCAN clustering code to C++

### NOTABLE FIXES


* ``PYTHONPATH`` was not being set for regression tests.
* CMake install path was not being propagated to all modules.


----------------------------------------------------------------------


VERSION 0.1, September 2014
---------------------------

Internal release only: not released to public.

### NEW FEATURES


* Movie-making script can now run in parallel
* Example scripts all use common command-line arguments, including reading arguments from files
* Added timezone support for clock rendering
* Doxygen documentation present but incomplete
* Overall documentation now builds using Sphinx
* Decree: distances shall be specified in kilometers

### NOTABLE FIXES


* Histogram buckets have reasonable sizes on both small and large maps
* City labels were not rendering near cities
* Radius of the Earth was wrong
* Copyright notice adjusted to use proper Sandia language
* License file for external data cleaned up


----------------------------------------------------------------------

VERSION 0, July 2014
----------------------

Initial milestone: not released to public.

### NEW FEATURES

* Points and trajectories in geographic domain implemented in C++ and exposed to Python.
* Math on points and trajectories implemented in C++ and exposed to Python.
* Python script added for movie making on geographic maps.
* Python script added for still images on geographic maps.
* Python scripts for all rendering methods added to examples directory.
