#
# Copyright (c) 2014-2020 National Technology and Engineering
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

"""Convenience wrappers for geographic map creation and decoration
"""

from __future__ import print_function

from matplotlib import pyplot

import cartopy
import cartopy.crs
import logging
from tracktable.render import maps
from tracktable.render import geographic_decoration as decoration


def mapmaker(domain='terrestrial', *args, **kwargs):
    """Generate a map for a given domain

    Keyword Args:
        domain (str): Domain to create the map in (Default: 'terrestrial')
        args (tuple): Arguments to be passed to specific map creation (Default: tuple)
        kwargs (dict): Any other arguments to customize the generated map (Default: dict)

    Returns:
        A terrestrial or cartesian domain map

    """

    if kwargs.get('map_bbox', None) is not None:
        kwargs['map_bbox'] = _make_bounding_box(kwargs['map_bbox'], domain)

    if domain == 'terrestrial':
        return terrestrial_map(*args, **kwargs)
    elif domain == 'cartesian' or domain == 'cartesian2d':
        return cartesian_map(*args, **kwargs)
    else:
        raise ValueError(('Mapmaker only works on the terrestrial and '
                          ' cartesian2d domains, not "{}".').format(domain))

# ----------------------------------------------------------------------

def cartesian_map(map_bbox=None,
                  gridline_spacing=None,
                  axes=None,
                  **kwargs):
    """Create a Cartesian map

    Since Cartesian space is flat and undistinguished, a "map" is just
    a display region. You can also change the background color and
    draw axes/grid lines on the figure.

    Keyword Args:
        map_bbox ([minLon, maxLon, minLat, maxLat]): bounding box for
            custom map extent. By default automatically set to
            make all trajectories visible. (Default: None)
        gridline_spacing (int): Spaceing to put between grid lines (Default: None)
        axes (GeoAxes): Domain to create the map in (Default: None)
        kwargs (dict): Any other arguments to customize the generated map (Default: dict)

    Returns:
        A cartesian domain map

    """

    if axes is None:
        axes = pyplot.axes(projection=cartopy.crs.PlateCarree())

    logging.getLogger(__name__).debug(
        "cartesian_map: map_bbox is {}".format(map_bbox))

    axes.set_aspect(kwargs.get('aspect', 'equal'))
    if map_bbox is not None:
        axes.set_xlim(left=map_bbox.min_corner[0],
                      right=map_bbox.max_corner[0])
        axes.set_ylim(bottom=map_bbox.min_corner[1],
                      top=map_bbox.max_corner[1])

    return (axes, list())

# ----------------------------------------------------------------------

def terrestrial_map(map_name,
                    draw_coastlines=True,
                    draw_countries=True,
                    draw_states=True,
                    draw_lonlat=True,
                    fill_land=True,
                    fill_water=True,
                    land_fill_color='#101010',
                    water_fill_color='#000000',
                    land_zorder=4,
                    water_zorder=4,
                    lonlat_spacing=10,
                    lonlat_color='#A0A0A0',
                    lonlat_linewidth=0.2,
                    lonlat_zorder=6,
                    coastline_color='#808080',
                    coastline_linewidth=1,
                    coastline_zorder=5,
                    country_color='#606060',
                    country_fill_color='#303030',
                    country_linewidth=0.5,
                    country_zorder=3,
                    state_color='#404040',
                    state_fill_color='none',
                    state_linewidth=0.3,
                    state_zorder=2,
                    draw_largest_cities=None,
                    draw_cities_larger_than=None,
                    city_label_size=12,
                    city_dot_size=2,
                    city_dot_color='white',
                    city_label_color='white',
                    city_zorder=6,
                    border_resolution='110m',
                    map_bbox=None,
                    map_projection=None,
                    map_scale_length=None,
                    region_size=None,
                    axes=None,
                    **kwargs):

    """Create and decorate a terrestrial map

    Call the Cartopy toolkit to create a map of some predefined area,
    up to and including the entire world. The map will be decorated
    with some subset of coastlines, country borders, state/province
    borders and cities according to the keyword arguments you supply
    to mapmaker() or terrestrial_map().

    Args:
      map_name:            Region name ('region:XXX' or 'airport:XXX' or 'city:XXX' or 'custom'). Available regions are in tracktable.render.maps.available_maps().

    Keyword Args:
      draw_coastlines (bool):                       Whether or not to draw coastlines on the map (Default: True)
      draw_countries (bool):                        Whether or not to draw country borders on the map (Default: True)
      draw_states (bool):                           Whether or not to draw US/Canada state borders (Default: True)
      draw_lonlat (bool):                           Whether or not to draw longitude/latitude lines (Default: True)
      fill_land (bool):                             Whether or not to fill in the land areas (Default: True)
      fill_water (bool):                            Whether or not to fill in the land areas (Default: True)
      land_fill_color (str):                        Color name or hex string for land area (Default: '#101010')
      water_fill_color (str):                       Color name or hex string for sea area (Default: '#000000')
      land_zorder (int):                            Image layer for land (Default: 4)
      water_zorder (int):                           Image layer for sea (Default: 4)
      lonlat_spacing (int):                         Distance in degrees between lon/lat lines (Default: 10)
      lonlat_color (str):                           Color name or hex string for longitude/latitude lines (Default: '#A0A0A0')
      lonlat_linewidth (float):                     Width (in point) for lon/lat lines (Default: 0.2)
      lonlat_zorder (int):                          Image layer for coastlines (Default: 6)
      coastline_color (str):                        Color name or hex string for coastlines (Default: '#808080')
      coastline_linewidth (float):                  Width (in points) of coastlines (Default: 1)
      coastline_zorder (int):                       Image layer for coastlines (Default: 5)
      country_color (str):                          Color name or hex string for coastlines (Default: '#606060')
      country_fill_color (str):                     Color name or hex string for coastlines (Default:'#303030' )
      country_linewidth (float):                    Width (in points) of coastlines (Default: 0.5)
      country_zorder (int):                         Image layer for coastlines (Default: 3)
      state_color (str):                            Color name or hex string for coastlines (Default: '#404040')
      state_fill_color (str):                       Color name or hex string for coastlines (Default: 'none')
      state_linewidth (float):                      Width (in points) of coastlines (Default: 0.3)
      state_zorder (int):                           Image layer for coastlines (Default: 2)
      draw_largest_cities (int):                    Draw the N largest cities on the map (Default: None)
      draw_cities_larger_than (int):                Draw cities with populations greater than N (Default: None)
      city_label_size (int):                        Size (in points) for city name labels (Default: 12)
      city_dot_size (int):                          Size (in points) for city markers (Default: 2)
      city_dot_color (str):                         Color name or hex string for city markers (Default: 'white')
      city_label_color (str):                       Color name or hex string for city names (Default: 'white')
      city_zorder (int):                            Color name or hex string for city names (Default: 6)
      border_resolution (str):                      Detail of borders (Default: '110m')
      map_bbox ([minLon, maxLon, minLat, maxLat]):  Bounding box for custom map extent (Default: None)
      map_projection (Basemap):                     Cartopy CRS projection object (optional) (Default: None)
      map_scale_length (float):                     Length of map scale indicator (in km) (Default: None)
      region_size (float):                          Size of region depicted around an airport (km width x km height) (Default: None)
      axes (GeoAxes):                               Matplotlib axes to render into (Default: None)
      kwargs (dict):                                Any other arguments to customize the generated map (Default: dict)

    Raises:
      KeyError: unknown map name

    Returns:
      (basemap, artist_list): Basemap instance and a list of Matplotlib artists that were rendered
    """

    if map_name == "custom":
        map_axes = maps.instantiate_map(
            min_corner=map_bbox.min_corner,
            max_corner=map_bbox.max_corner,
            projection=map_projection
            )
        artists = []

    else:
        map_axes = maps.predefined_map(
            map_name,
            region_size=region_size,
            projection=map_projection
            )
        artists = []

    if draw_coastlines:
        artists.extend(
            decoration.draw_coastlines(
                map_axes,
                edgecolor=coastline_color,
                zorder=coastline_zorder
            ))

    if fill_land:
        artists.extend(
            decoration.fill_land(
                map_axes,
                facecolor=land_fill_color,
                zorder=land_zorder
                ))

    if fill_water:
        water_actors = decoration.fill_oceans(
            map_axes,
            facecolor=water_fill_color,
            zorder=water_zorder
            )
        lake_actors = decoration.fill_lakes(
            map_axes,
            facecolor=water_fill_color,
            zorder=water_zorder
            )
        artists.extend(water_actors)
        artists.extend(lake_actors)

    if draw_countries:
        artists.extend(
            decoration.draw_countries(
                map_axes,
                edgecolor=country_color,
                facecolor=country_fill_color,
                linewidth=country_linewidth,
                zorder=country_zorder
                ))

    if draw_states:
        artists.extend(
            decoration.draw_states(
                map_axes,
                edgecolor=state_color,
                facecolor=state_fill_color,
                linewidth=state_linewidth,
                zorder=state_zorder
                ))

    if draw_lonlat:
        artists.extend(
            decoration.draw_lonlat(
                map_axes,
                color=lonlat_color,
                linewidth=lonlat_linewidth,
                zorder=lonlat_zorder
                ))

    if draw_largest_cities is not None:
        artists.extend(
            decoration.draw_largest_cities(
                map_axes,
                draw_largest_cities,
                dot_color=city_dot_color,
                dot_size=city_dot_size,
                label_color=city_label_color,
                label_size=city_label_size
            ))

    if draw_cities_larger_than is not None:
        artists.extend(
            decoration.draw_cities_larger_than(
                map_axes,
                draw_cities_larger_than,
                dot_color=city_dot_color,
                dot_size=city_dot_size,
                label_color=city_label_color,
                label_size=city_label_size
            ))

    if map_scale_length is not None:
        artists.extend(
            decoration.draw_scale(
                map_axes,
                map_scale_length,
                label_color=city_label_color,
                label_size=city_label_size
            ))

    return (map_axes, artists)


def _make_bounding_box(bbox_args, domain):
    """Make a sensible bounding box out of whatever the user gave us."""

    # Case 1: Is it a list of coordinates from the command line?
    if type(bbox_args) is list and len(bbox_args) == 4:
        if domain == 'terrestrial':
            from tracktable.domain.terrestrial import BoundingBox as TerrestrialBoundingBox
            min_corner = (bbox_args[0], bbox_args[1])
            max_corner = (bbox_args[2], bbox_args[3])
            return TerrestrialBoundingBox(min_corner, max_corner)
        elif domain == 'cartesian2d':
            from tracktable.domain.cartesian2d import BoundingBox as Cartesian2DBoundingBox
            min_corner = (bbox_args[0], bbox_args[1])
            max_corner = (bbox_args[2], bbox_args[3])
            return Cartesian2DBoundingBox(min_corner, max_corner)
        else:
            raise ValueError('Custom bounding box for domain {} is not defined.'.format(domain))
    # Case 2: is it a bbox already?
    else:
        # just hope for the best
        return bbox_args

