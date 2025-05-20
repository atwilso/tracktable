#
# Copyright (c) 2014-2023 National Technology and Engineering
# Solutions of Sandia, LLC. Under the terms of Contract DE-NA0003525
# with National Technology and Engineering Solutions of Sandia, LLC,
# the U.S. Government retains certain rights in this software.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""trajectory_map_from_csv.py - Render trajectories on a map

Note:
    Cartopy v0.18.0 is required to successfully render maps and pass
    our internal tests.

This is both an example of how to use the library and a convenient
script that you can use to get started quickly.  You must provide as
input a delimited text file with at least 4 columns: object_id,
timestamp, longitude, latitude.  (All columns beyond those first four
will be ignored.)  The points in this file will be assembled into
trajectories and then rendered onto a map of part of the world.  The
points in the input file MUST be sorted either (1) by object ID and
then by ascending timestamp or (2) strictly by ascending timestamp.

You can control the following aspects of the rendering:

- What domain the points are in.  You must specify this with '--domain
  cartesian2d' or '--domain terrestrial'.

- Which part of the world is displayed in the map (terrestrial domain).
  This defaults to the whole world but can be changed with the --map
  argument.  Your options are 'region:world', 'region:conus' (continental
  US), 'region:north_america' and 'region:europe'.  You may also specify
  'airport:KJFK' for a region surrounding an airport.

- What part of the Cartesian plane is displayed in the image (
  cartesian2d domain).

TODO: Make sure that custom bounding boxes work for Cartesian
trajectories as well.

- Whether or not trajectories are colored differently at beginning and
  end.  By default, trajectories will be greenish when they begin and
  white-yellow when they end.

- Which colormap is used to render the scalars.  This defaults to the
  'autumn' color scale built into matplotlib.  You may specify the
  name of another if you prefer.  Note that you can only use the
  predefined colormaps here.  If you need a custom colormap, use this
  script as a starting point for your own code.

- The resolution of the output image with '--resolution 800 600' or
  whatever you choose.

- The output format.  This is automatically deduced from the output
  filename.

- The DPI of the output image.  Defaults to 72 (typical screen
  resolution).  Note that this will affect things like line thickness
  for borders: matplotlib sizes those things in points rather than
  pixels.

- Terrestrial domain only: Whether to draw continent boundaries,
  country borders, latitude/longitude graticules and (within North
  America) state borders.  By default all four are turned on.  Use
  '--omit-continents', '--omit-countries', '--omit-states' and
  '--omit-lonlat' to turn them off.  These will by default be drawn
  over the top of the histogram.

- The delimiter used to separate columns in the text file.  You can
  specify any single character to the '--delimiter' option or the
  magic strings 'tab' or '\t'.  (If it's easy for you to type in a
  literal tab then go ahead.  Just be sure to quote it.)

- Terrestrial domain only: Whether or not to draw cities, either with
  --draw-largest-cities or --draw-cities-above-size.
"""

from __future__ import print_function

import itertools
import logging
import sys

import numpy

from tracktable.core import geomath
from tracktable.feature import annotations
from tracktable.render.map_processing import paths
from tracktable.render import render_map
from tracktable.rw.load import load_trajectories
from tracktable.script_helpers import argument_groups, argparse, n_at_a_time

import matplotlib
matplotlib.use('Agg')

# Traditionally, importing modules in Python after the first non-
# import statement is considered poor style.  We have to do it anyway
# in this case because we need to set Matplotlib's back end before
# we do anything with the toolkit.  The #noqa comment is to tell
# flake8, the Python style checker, that we really did mean to do this.
from matplotlib import pyplot # noqa

# ----------------------------------------------------------------------


def compute_figure_dimensions(resolution, dpi):
    """Compute figure dimensions in inches given resolution and dots per inch

    Given an image of resolution X by Y pixels and D dots per inch,
    the figure's dimensions in inches are (X/D, Y/D).

    Arguments:
        resolution {list or tuple of 2 ints}: Image resolution in pixels
        dpi {int}: Dots per inch for image

    Returns:
        Tuple of two floats containing image size in inches
    """

    return (float(resolution[0])/dpi, float(resolution[1])/dpi)

# --------------------------------------------------------------------


def extract_field_assignments(arg_dict):
    """Extract column->field assignments from arguments

    Field assignments are specified on the command line as arguments
    like '--real-field speed 12', meaning "take the contents
    of column 12 and add it to each point as a numeric field called
    speed".  This function iterates over the arguments and extracts
    all of those.

    Arguments:
        arg_dict {:obj:`dict`}: Command-line arguments to parse,
        specified as a :obj:`dict`.  To get a dictionary from the
        :obj:`Namespace` object returned by :code:`argparse.parse_args()`,
        call :code:`vars()` on the args object.

    Returns:
        Dictionary with three entries:
            'real': Dictionary mapping column names (strings) to
                    integer column IDs for real-valued fields
            'string': Dictionary mapping column names (strings) to
                    integer column IDs for string-valued fields
            'time': Dictionary mapping column names (strings) to
                    integer column IDs for timestamp-valued fields
    """

    return {
        'real': _extract_typed_field_assignments(arg_dict, 'real'),
        'string': _extract_typed_field_assignments(arg_dict, 'string'),
        'time': _extract_typed_field_assignments(arg_dict, 'time')
    }

# ----------------------------------------------------------------------


def initialize_canvas(resolution,
                      dpi=72,
                      facecolor='black'):
    """Set up Matplotlib canvas for rendering

    This function sets up a Matplotlib figure with specified resolution,
    DPI, and background/edge color.

    Since font sizes are specified in points, the combination of DPI and
    resolution determines how large a font will appear when text is
    rendered into the image.  One inch is 72 points, so a 12-point font
    will produce text where each line is (dpi / 6) pixels tall.

    Arguments:
        resolution {2 ints}: how large the images should be in pixels

    Keyword arguments:
        dpi {integer}: how many pixels per inch (pertains to text rendering).
            Defaults to 72.
        facecolor {string}: Default color for image background.  Can be
            specified as the name of a color ('black'), a float value for
            grays (0.75 == #B0B0B0), an RGBA tuple ((1, 0, 0, 1) is red),
            or an #RRGGBB string.  Defaults to 'black'.

    Returns:
        (figure, axes), where 'figure' is a Matplotlib figure and 'axes'
        are the default axes to render into.
    """

    figure_dimensions = compute_figure_dimensions(resolution, dpi)
    figure = pyplot.figure(figsize=figure_dimensions,
                           facecolor=facecolor)
    axes = figure.add_axes([0, 0, 1, 1], frameon=False, facecolor=facecolor)
    axes.set_frame_on(False)

    return (figure, axes)

# ----------------------------------------------------------------------

# Note: There is more work to do here to expose options for the
# linewidths, line colors, Z-order and background color for the map.
# That work will happen once we get this script up and running in the
# first place.


def parse_args():
    parser = argparse.ArgumentParser()
    argument_groups.use_argument_group('delimited_text_point_reader', parser)
    argument_groups.use_argument_group('mapmaker', parser)
    argument_groups.use_argument_group('trajectory_assembly', parser)
    argument_groups.use_argument_group('trajectory_rendering', parser)

    parser.add_argument('--trajectory-colormap',
                        default='gist_heat',
                        help='Name of Matplotlib colormap for trajectories')

    parser.add_argument('--trajectory-linewidth',
                        type=int,
                        default=1,
                        help='Width of trajectories on map in points')

    parser.add_argument('--resolution', '-r',
                        nargs=2,
                        type=int,
                        help=('Resolution of output image.  Defaults to '
                              '800 600.'))

    parser.add_argument('--dpi',
                        type=int,
                        default=72,
                        help='DPI of output image.')

    parser.add_argument('point_data_file',
                        nargs=1,
                        help='Delimited text file containing point data')

    parser.add_argument('image_file',
                        nargs=1,
                        help='Filename for trajectory image')

    args = parser.parse_args()

    if args.resolution is None:
        args.resolution = [800, 600]
    if args.delimiter == 'tab':
        args.delimiter = '\t'
    if args.object_id_column is None:
        args.object_id_column = 0
    if args.timestamp_column is None:
        args.timestamp_column = 1
    if args.coordinate0 is None:
      args.coordinate0 = 2
    if args.coordinate1 is None:
      args.coordinate1 = 3

    return args

# --------------------------------------------------------------------


def render_annotated_trajectories(trajectories,
                                  axes,
                                  color_map='plasma',
                                  decorate_head=False,
                                  head_size=2,
                                  head_color='white',
                                  linewidth_style='taper',
                                  linewidth=0.5,
                                  final_linewidth=0.01,
                                  scalar='progress',
                                  scalar_min=0,
                                  scalar_max=1,
                                  zorder=10):

    """Render decorated trajectories (with scalars) onto a map.

    Given a map instance and an iterable containing trajectories,
    draw the trajectories onto the map with the specified appearance
    parameters.  You can control the trajectory color, linewidth,
    z-order and whether or not a dot is drawn at the head of each
    path.

    The "annotated" part of render_annotated_trajectories refers to
    per-point scalar metadata on each trajectory.  For example, if your
    trajectories have a property "speed" at each point, you could render
    a movie where trajectories being displayed are color-coded by speed.
    If you supply the name of a property for the `scalar_property`
    argument, that property will be used along with `colormap` to determine
    color.  If you don't specify a property, trajectories will be colored
    so that traverse the entire colormap from start to finish.

    Arguments:
        axes {matplotlib Axes}: Axes to render into
        trajectories {iterable of Tracktable trajectories}: trajectories
            to render

    Keyword Arguments:
        color_map {name of colormap or :obj:`matplotlib.colors.Colormap`}:
            Trajectory scalars will be mapped to this color map.  (default:
            'plasma')
        decorate_head {boolean}: If true, a dot will be drawn at the current
            position of each object on the screen.  (default: False)
        head_size {float}: How large the dot should be for decorated
            trajectories, measured in points.  (default: 2)
        head_color {string or tuple}: What color the head dot should be for
            decorated trajectories.  Can be any Matplotlib color specification
            such as a color name, an '#RRGGBB' string, or a tuple of RGB or
            RGBA values.  The value 'scalar' means to use the scalar value
            at the head of the trajectory so that the dot is the same color
            as its trail.
        linewidth_style {string}: Either 'constant', in which case the lines
            for each trajectory will have constant width (see the `linewidth`
            parameter); or 'taper', in which case the line width will vary
            smoothly from `linewidth` at the object's current position to
            `final_linewidth` at the oldest end of the trail. (default:
            'taper')
        linewidth {float}: Width of trajectory trail subject to
            `linewidth_style`. (default: 0.5)
        final_linewidth {float}: Width of oldest end of trajectory trail.
            Only used when `linewidth_style` is 'taper'.
        scalar {string}: Real-valued property to be used to determine
            trajectory color.  You must make sure that this property is present
            at all points in the trajectory data.  The default 'progress'
            scalar is added automatically. (default: 'progress')
        scalar_min {float}: Bottom of range of scalar values that you care
            about. If your scalars are outside the range (0,1), you should set
            this.  Values below this will be treated as the minimum value.
            (default: 0)
        scalar_max {float}: Top of range of scalar values that you care about.
            If your scalars are outside the range (0,1), you should set this.
            Values above this will be treated as the maximum value.
            (default: 1)
        zorder {integer}: Z-order for drawn items.  Items with a higher
            Z-order will appear on top of items with a lower Z-order.  This is
            Matplotlib-specific. (default: 10)

    Returns:
        List of Matplotlib artists added to the figure.

    Raises:
        KeyError: The desired scalar is not present
        ValueError: linewidth_style is neither 'constant' nor 'taper'

    Note:
        A gallery of Matplotlib colormaps can be found at
          https://matplotlib.org/3.1.1/gallery/color/colormap_reference.html
    """

    if linewidth_style not in ['constant', 'taper']:
        raise ValueError(('Trajectory linewidth must be either "constant" or '
                          '"taper".  You supplied "{}".').format(
                          linewidth_style))
    if linewidth_style == 'taper':
        linewidths_for_trajectory = _make_tapered_linewidth_generator(
                                        linewidth, final_linewidth)
    else:
        linewidths_for_trajectory = _make_constant_linewidth_generator(
                                        linewidth)

    if not decorate_head:
        head_size = 0
        head_color = 'white'

    logger = logging.getLogger(__name__)

    def scalars_for_trajectory(trajectory):
        result = [0] * len(trajectory)
        try:
            for (i, point) in enumerate(trajectory):
                value = point.properties[scalar]
                if value is not None:
                    result[i] = value
        except KeyError:
            logger.error(('One or more points in trajectory do not have '
                          'the scalar field "{}".').format(scalar))

        return result

    return paths.draw_traffic( # Axes is used for map and `axes` keyword arg is set to None? Why?
              axes,
              trajectories,
              color_map=color_map,
              trajectory_scalar_generator=scalars_for_trajectory,
              trajectory_linewidth_generator=linewidths_for_trajectory,
              zorder=zorder,
              color_scale=matplotlib.colors.Normalize(vmin=scalar_min,
                                                      vmax=scalar_max),
              dot_size=head_size,
              dot_color=head_color)


# --------------------------------------------------------------------


def _make_tapered_linewidth_generator(initial_linewidth,
                                      final_linewidth):

    """Create a function that will make a tapered line width for a trajectory

    In order to render tapered trajectories whose lines get thinner as
    they get older, we need to generate a scalar array with as many
    components as the trajectory has segments.  The first entry in
    this array (corresponding to the OLDEST point) should have the
    value 'final_linewidth'.  The last entry (corresponding to the
    NEWEST point) should have the value 'initial_linewidth'.

    Args:
       initial_linewidth:  Width (in points) at the head of the trajectory
       final_linewidth:    Width (in points) at the tail of the trajectory

    Returns:
       A function that takes in a trajectory as an argument and
       returns an array of linewidths
    """

    def linewidth_generator(trajectory):
        return numpy.linspace(final_linewidth,
                              initial_linewidth,
                              len(trajectory))

    return linewidth_generator

# ----------------------------------------------------------------------


def _make_constant_linewidth_generator(linewidth):

    """Create a function that will make a constant line width for a trajectory

    Args:
       linewidth:  Width (in points) along the trajectory

    Returns:
       A function that takes in a trajectory as an argument and
       returns an array of linewidths
    """

    def linewidth_generator(trajectory):
        scalars = numpy.zeros(len(trajectory))
        scalars += float(linewidth)
        return scalars

    return linewidth_generator

# ----------------------------------------------------------------------


def _extract_typed_field_assignments(arguments,
                                     field_type):
    """Extract named field definitions from a dict of arguments

    When running this script, the user specifies named fields that
    the reader should process with arguments like
    '--real-field-column altitude 12'.  This will cause the reader
    to take column 12 in the data file, convert its contents to a
    floating-point number, and store the result in a property
    named "altitude" on each point.

    This function is a convenience: it extracts those declarations
    for a given field type (string, real, timestamp) from a dictionary
    or namespace of arguments, then returns the result as a dictionary
    that can be passed to trajectory_points_from_file().

    Arguments:
        arguments {dict}: Dictionary of parsed command-line arguments
        field_type {string}: What type of property to extract.  Must be
            'string', 'real' or 'time'.

    Returns:
        Dictionary containing { field_name: column_number } for the
        specified field type.  Dictionary will be empty if there are
        no assignments of that type.

    Raises:
        ValueError: invalid field type

    Note:
        Don't call this function directly unless you need the field
        assignments for one specific data type.  Instead, call
        `extract_field_assignments`.
    """

    if field_type not in ['string', 'real', 'time']:
        raise ValueError(('Field type ({}) must be one of "string", '
                          '"real", or "time".  Case matters').format(
                                field_type))

    arg_name = '{}_field_column'.format(field_type)
    field_assignments = dict()
    definition_list = arguments.get(arg_name, None)
    if definition_list is not None:
        if len(definition_list) > 0:
            for (field_name, column) in n_at_a_time(definition_list, 2):
                field_assignments[field_name] = int(column)

    return field_assignments


# ----------------------------------------------------------------------


def main():
    logger = logging.getLogger(__name__)
    args = parse_args()

    mapmaker_kwargs = argument_groups.extract_arguments("mapmaker", args)
    # Some of the argument names for trajectory rendering are out of
    # sync with their command-line parameter names.  We extract those
    # arguments manually at the render_annotated_trajectories
    # call instead of using extract_arguments("trajectory_rendering")
    # here.

    # Load all the trajectories into memory.
    point_filename = args.point_data_file[0]
    field_assignments = extract_field_assignments(vars(args))

    logger.info('Loading points and building trajectories.')
    trajectories = load_trajectories(point_filename,
        comment_character=args.comment_character,
        domain=args.domain,
        field_delimiter=args.delimiter,
        object_id_column=args.object_id_column,
        timestamp_column=args.timestamp_column,
        longitude_column=args.coordinate0,
        latitude_column=args.coordinate1,
        real_fields = field_assignments['real'],
        string_fields = field_assignments['string'],
        time_fields = field_assignments['time'],
        separation_distance = args.separation_distance, # km
        separation_time = args.separation_time, # minutes
        minimum_length = args.minimum_length, # points
        return_list=True
        )

    # Add the 'progress' annotation to all of our trajectories so
    # we have some way to color them
    trajectories = [annotations.progress(t) for t in trajectories]

    # We can compute the bounding box for Cartesian data automatically.
    # We don't need to do so for terrestrial data because the map will
    # default to the whole world.
    if (args.domain == 'cartesian2d' and
            (args.map_bbox is None or
             len(args.map_bbox) == 0)):

        args.map_bbox = geomath.compute_bounding_box(
            itertools.chain(*trajectories)
            )

    # Set up the map.
    #
    # There are a lot of keyword arguments for the map -- see
    # tracktable.script_helpers.argument_groups.mapmaker --
    # so rather than pull them out individually like we did for
    # the point reader we extract the whole dict using
    # tracktable.script_helpers.argument_groups.extract_arguments().

    logger.info('Initializing map canvas for rendering.')
    (figure, axes) = initialize_canvas(args.resolution,
                                       args.dpi)
    (mymap, map_artists) = render_map.render_map(**mapmaker_kwargs)

    if args.trajectory_linewidth == 'taper':
        linewidth_style = 'taper'
        linewidth = args.trajectory_initial_linewidth
        final_linewidth = args.trajectory_final_linewidth
    else:
        linewidth_style = 'constant'
        linewidth = args.trajectory_linewidth
        final_linewidth = linewidth

    # Eventually we will be able to use argument_groups.extract_arguments() for
    # this, but right now it's broken.  Not all of the parameters in the
    # trajectory rendering argument group are supported and some of the names
    # have changed.
    trajectory_rendering_kwargs = {
        'decorate_head': args.decorate_trajectory_head,
        'head_color': args.trajectory_head_color,
        'head_size': args.trajectory_head_dot_size,
        'color_map': args.trajectory_colormap,
        'scalar': args.trajectory_color,
        'scalar_min': args.scalar_min,
        'scalar_max': args.scalar_max,
        'linewidth_style': linewidth_style,
        'linewidth': linewidth,
        'final_linewidth': final_linewidth
    }

    render_annotated_trajectories(
      trajectories,
      mymap,
      **trajectory_rendering_kwargs
      )

    pyplot.savefig(args.image_file[0],
                   facecolor=figure.get_facecolor(),
                   dpi=args.dpi)

    pyplot.close()

    return 0

# ----------------------------------------------------------------------


if __name__ == '__main__':
    sys.exit(main())
