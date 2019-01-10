#
# Copyright (c) 2014-2017 National Technology and Engineering
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

"""movie_from_csv.py - Example of how to render a movie of a bunch of trajectories from a CSV file
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.animation
from matplotlib import pyplot

import csv
import datetime
import numpy
import shlex
import sys

import example_point_reader
import example_trajectory_builder
import example_trajectory_rendering
import example_movie_rendering

from tracktable.feature              import annotations
from tracktable.filter.trajectory     import ClipToTimeWindow as ClipTrajectoryToTimeWindow, FilterByBoundingBox as FilterTrajectoriesByBoundingBox
from tracktable.render                import colormaps, mapmaker, paths
from tracktable.core                  import geomath
from tracktable.script_helpers        import argument_groups, argparse

# ----------------------------------------------------------------------

# Note: There is more work to do here to expose options for the
# linewidths, line colors, Z-order and background color for the map.
# That work will happen once we get this script up and running in the
# first place.

def parse_args():
    parser = argparse.ArgumentParser(description='Render a movie of traffic found in a delimited text file',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    argument_groups.use_argument_group("delimited_text_point_reader", parser)
    argument_groups.use_argument_group("trajectory_assembly", parser)
    argument_groups.use_argument_group("trajectory_rendering", parser)
    argument_groups.use_argument_group("mapmaker", parser)
    argument_groups.use_argument_group("movie_rendering", parser)


    parser.add_argument('--resolution', '-r',
                        nargs=2,
                        type=int,
                        help='Resolution of movie frames.  Defaults to 800 600.')

    parser.add_argument('--dpi',
                        type=int,
                        default=72,
                        help='DPI of movie frames.')

    parser.add_argument('--trail-duration',
                        help="How long should each object's trail last? (seconds)",
                        type=int,
                        default=300)

    parser.add_argument('--highlight',
                        nargs=1,
                        help="File containing trajectories to highlight")

    parser.add_argument('point_data_file',
                        nargs=1,
                        help='Delimited text file containing point data')

    parser.add_argument('movie_file',
                        nargs=1,
                        help='Filename for trajectory movie')


    args = parser.parse_args()
    if args.resolution is None:
        args.resolution = [ 800, 600 ]
    if args.delimiter == 'tab':
        args.delimiter = '\t'

    return args


# ----------------------------------------------------------------------

def setup_point_source(filename, args):
    """
    Instantiate and configure a delimited text point source using the
    filename and parameters supplied by the user.
    """

    config_reader = example_point_reader.configure_point_reader
    field_map = {}
    for column_name in [ 'object_id',
                         'timestamp',
                         'longitude',
                         'latitude',
                         'altitude',
                         'speed',
                         'heading' ]:

        field_name_in_args = '{}_column'.format(column_name)
        if hasattr(args, field_name_in_args):
            field_map[column_name] = getattr(args, field_name_in_args)

    infile = open(filename, 'rb')
    point_source = config_reader(infile,
                                 delimiter=args.delimiter,
                                 comment_character=args.comment_character,
                                 field_map=field_map)

    return point_source.points()


# ----------------------------------------------------------------------

def setup_trajectory_source(point_source, args):

    args = argument_groups.extract_arguments("trajectory_assembly", args)

    source = example_trajectory_builder.configure_trajectory_builder(**args)
    source.input = point_source

    return source.trajectories()


# ----------------------------------------------------------------------

def main():
    args = parse_args()

    dpi = args.dpi
    image_resolution = args.resolution
    if image_resolution is None:
        image_resolution = [ 800, 600 ]
    figure_dimensions = [ float(image_resolution[0]) / dpi, float(image_resolution[1]) / dpi ]

    print("STATUS: Initializing image")
    figure = pyplot.figure(figsize=figure_dimensions, facecolor='black', edgecolor='black')

    axes = figure.add_axes([0, 0, 1, 1], frameon=False, facecolor='black')
    axes.set_frame_on(False)

    mapmaker_kwargs = argument_groups.extract_arguments("mapmaker", args)
    (mymap, base_artists) = mapmaker.mapmaker(**mapmaker_kwargs)

    print("STATUS: Initializing point source for main data file")
    main_point_source = setup_point_source(args.point_data_file[0], args)

    print("STATUS: Initializing trajectory source for main data file")
    main_trajectory_source = setup_trajectory_source(main_point_source, args)

    print("STATUS: Collecting all trajectories from main source")
    all_trajectories = list(main_trajectory_source)

    highlight_trajectories = []
    if len(args.highlight) > 0:
        print("STATUS: Initializing point source for highlight data file")
        highlight_point_source = setup_point_source(args.highlight[0], args)
        print("STATUS: Initializing trajectory source for highlight data file")
        highlight_trajectory_source = setup_trajectory_source(highlight_point_source, args)
        print("STATUS: Collecting trajectories to highlight")
        highlight_trajectories = list(highlight_trajectory_source)


    movie_kwargs = argument_groups.extract_arguments("movie_rendering", args)

    movie_writer = example_movie_rendering.setup_encoder(**movie_kwargs)

    # This set of arguments will be passed to the savefig() call that
    # grabs the latest movie frame.  This is the place to put things
    # like background color, tight layout and friends.
    savefig_kwargs = { 'facecolor': figure.get_facecolor(),
                       'figsize': figure_dimensions,
                       'frameon': False }

    trajectory_kwargs = argument_groups.extract_arguments("trajectory_rendering", args)

    example_movie_rendering.render_trajectory_movie(
        movie_writer,
        basemap=mymap,
        trajectories=all_trajectories,
        dpi=args.dpi,
        figure=figure,
        filename=args.movie_file[0],
        num_frames=movie_kwargs['fps'] * movie_kwargs['duration'],
        start_time=movie_kwargs['start_time'],
        end_time=movie_kwargs['end_time'],
        trail_duration = datetime.timedelta(seconds=args.trail_duration),
        savefig_kwargs=savefig_kwargs,
        axes=axes,
        trajectory_rendering_args=trajectory_kwargs,
        highlight_trajectories=highlight_trajectories
    )

    pyplot.close()

    return 0

# ----------------------------------------------------------------------

if __name__ == '__main__':
    sys.exit(main())
