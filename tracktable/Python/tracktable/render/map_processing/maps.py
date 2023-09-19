#
# Copyright (c) 2014-2023 National Technology and Engineering
# Solutions of Sandia, LLC. Under the terms of Contract DE-NA0003525
# with National Technology and Engineering Solutions of Sandia, LLC,
# the U.S. Government retains certain rights in this software.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


#
# tracktable/render/maps.py - Friendly interface around Basemap
#
# The functions in this file make it easy to draw maps of various
# interesting places around the world.

# TODO:
#
# map_for_country?
#

from __future__ import absolute_import, division, print_function

import logging

import cartopy.crs
from matplotlib import pyplot as plt
from tracktable.core import geomath

airports = None
ports = None
cities = None

CONVENIENCE_MAPS = {
    'conus': {
        'min_corner': (-130, 22),
        'max_corner': (-65, 50)
    },

    'europe': {
#        'projection': cartopy.crs.EuroPP,
        'min_corner': (-11, 34),
        'max_corner': (35, 72)
    },

    'north_america': {
        'min_corner': (-160, 11),
        'max_corner': (-63, 83)
    },

    'south_america': {
        'min_corner': (-85, -60),
        'max_corner': (-30, 35)
    },

    'australia': {
        'min_corner': (110, -45),
        'max_corner': (155, -10)
    },

    # Cartopy complains and renders a map with the wrong dimensions
    # if min_corner and max_corner are equal mod 360, so we're excluding
    # a tiny sliver of the world.
    'world': {
        'min_corner': (-179.999, -90),
        'max_corner': (179.999, 90)
    }
}

# ----------------------------------------------------------------------


def _ensure_airports_loaded():
    global airports
    if airports is None:
        from tracktable.info import airports

def _ensure_cities_loaded():
    global cities
    if cities is None:
        from tracktable.info import cities

def _ensure_ports_loaded():
    global ports
    if ports is None:
        from tracktable.info import ports

# ----------------------------------------------------------------------


def available_maps():
    """ Supply available maps
    Returns:
        All available maps
    """
    global CONVENIENCE_MAPS
    return CONVENIENCE_MAPS.keys()

# ----------------------------------------------------------------------


def _flatten(l, ltypes=(list, tuple)):
    ltype = type(l)
    my_list = list(l)
    i = 0
    while i < len(my_list):
        while isinstance(my_list[i], ltypes):
            if not my_list[i]:
                my_list.pop(i)
                i -= 1
                break
            else:
                my_list[i:i + 1] = my_list[i]
        i += 1
    return ltype(my_list)


# ----------------------------------------------------------------------


def airport_map(airport_id,
                region_size=(200, 200),
                projection=cartopy.crs.Miller):
    """Draw a map for a region surrounding an airport.

    Create a map for the region surrounding the requested airport.

    The region will be a rectangle in lon/lat space with the specified
    width and height in KM. We'll do our best to convert those into a
    lat/lon bounding box.

    We default to the Miller Cylindrical projection. It does a pretty
    good job of showing the world in familiar shapes although
    distortion sets in above/below about 50 degrees. Fortunately,
    things are still quite recognizable. If you would prefer a
    different projection then change the value of projection from
    cartopy.crs.Miller to something else.

    Args:
        airport_id (str): ID of the airport to generate a map around. example 'ORD' or 'KORD' for O'Hare.

    Keyword Args:
        region_size (point2d): (Default: (200, 200))
        projection (Matplotlib axes): (Default: cartopy.crs.Miller)

    Returns:
        This function returns axes for Matplotlib.
    """

    _ensure_airports_loaded()

    airport_info = airports.airport_information(airport_id)
    if airport_info is None:
        raise KeyError(("ERROR: Can't find information "
                        "for airport '{}'").format(airport_id))

    width = region_size[0]
    height = region_size[1]

    airport_location = airport_info.position

    latitude_span = height / geomath.latitude_degree_size(airport_location[1])

    bottom_latitude = airport_location[1] - latitude_span / 2
    top_latitude = airport_location[1] + latitude_span / 2

    # Allow for the possibility that we've gone past the poles
    if top_latitude > 90:
        top_latitude = 90 - top_latitude
    if bottom_latitude < -90:
        bottom_latitude = -180 - bottom_latitude

    longitude_width_at_top = max(
        geomath.longitude_degree_size(top_latitude), 1
        )
    longitude_width_at_bottom = max(
        geomath.longitude_degree_size(bottom_latitude), 1
        )

    # This could go wrong at very high latitudes but seems OK for now
    longitude_span = width / min(longitude_width_at_top,
                                 longitude_width_at_bottom)

    min_corner = (
        airport_location[0] - longitude_span/2,
        bottom_latitude
        )

    max_corner = (
        airport_location[0] + longitude_span/2,
        top_latitude
        )

    return instantiate_map(min_corner,
                           max_corner,
                           projection=projection)

# ----------------------------------------------------------------------


def port_map(port_name,
            port_country=None,
            region_size=(200, 200),
            projection=cartopy.crs.Miller):
    """Draw a map for a region surrounding a port.

    Create a map for the region surrounding the requested port.

    The region will be a rectangle in lon/lat space with the specified
    width and height in KM. We'll do our best to convert those into a
    lat/lon bounding box.

    We default to the Miller Cylindrical projection. It does a pretty
    good job of showing the world in familiar shapes although
    distortion sets in above/below about 50 degrees. Fortunately,
    things are still quite recognizable. If you would prefer a
    different projection then change the value of projection from
    cartopy.crs.Miller to something else.

    Args:
        port_name (str): Name of the port to generate a map around.

    Keyword Args:
        port_country (str): Country that the port is located in. Required if a port_name matches multiple ports. (Default: None)
        region_size (point2d): (Default: (200, 200))
        projection (Matplotlib axes): Cartopy projection to generate a map onto. (Default: cartopy.crs.Miller)

    Returns:
        This function returns axes for Matplotlib.
    """

    _ensure_ports_loaded()

    port_info = ports.port_information(port_name, country=port_country)
    if port_info == []:
        raise KeyError(("Can't find information for port '{}'").format(port_name))
    if type(port_info) is list:
        raise AttributeError("More then one port with the name {} found, provide the port's country to narrow results or use the ports WPI number.".format(port_name))

    width = region_size[0]
    height = region_size[1]

    port_location = port_info.position

    latitude_span = height / geomath.latitude_degree_size(port_location[1])

    bottom_latitude = port_location[1] - latitude_span / 2
    top_latitude = port_location[1] + latitude_span / 2

    # Allow for the possibility that we've gone past the poles
    if top_latitude > 90:
        top_latitude = 90 - top_latitude
    if bottom_latitude < -90:
        bottom_latitude = -180 - bottom_latitude

    longitude_width_at_top = max(
        geomath.longitude_degree_size(top_latitude), 1
        )
    longitude_width_at_bottom = max(
        geomath.longitude_degree_size(bottom_latitude), 1
        )

    # This could go wrong at very high latitudes but seems OK for now
    longitude_span = width / min(longitude_width_at_top,
                                 longitude_width_at_bottom)

    min_corner = (
        port_location[0] - longitude_span/2,
        bottom_latitude
        )

    max_corner = (
        port_location[0] + longitude_span/2,
        top_latitude
        )

    return instantiate_map(min_corner,
                           max_corner,
                           projection=projection)

# ----------------------------------------------------------------------


def city_map(city_name,
            city_country=None,
            city_location=None,
            region_size=(200, 200),
            projection=cartopy.crs.Miller):
    """Draw a map for a region surrounding a city.

    Create a map for the region surrounding the requested city.

    The region will be a rectangle in lon/lat space with the specified
    width and height in KM. We'll do our best to convert those into a
    lat/lon bounding box.

    We default to the Miller Cylindrical projection. It does a pretty
    good job of showing the world in familiar shapes although
    distortion sets in above/below about 50 degrees. Fortunately,
    things are still quite recognizable. If you would prefer a
    different projection then change the value of projection from
    cartopy.crs.Miller to something else.

    Args:
        city_name (str): Name of the city to generate a map around.

    Keyword Args:
        city_country (str): two character country code.  (Default: None).
        city_location (tuple, TrajectoryPoint, BasePoint): location to search near (Default: None).
        region_size (point2d): (Default: (200, 200))
        projection (Matplotlib axes): Cartopy projection to generate a map onto. (Default: cartopy.crs.Miller)

    Returns:
        This function returns axes for Matplotlib.
    """

    _ensure_cities_loaded()

    city_info = cities.get_city(city_name, country=city_country, location=city_location)
    if city_info is None:
        raise KeyError(("ERROR: Can't find information for city '{}'").format(city_info))

    width = region_size[0]
    height = region_size[1]

    # TODO (mjfadem): This might be (lat, lon) not (lon, lat).
    city_location = city_info.location

    latitude_span = height / geomath.latitude_degree_size(city_location[1])

    bottom_latitude = city_location[1] - latitude_span / 2
    top_latitude = city_location[1] + latitude_span / 2

    # Allow for the possibility that we've gone past the poles
    if top_latitude > 90:
        top_latitude = 90 - top_latitude
    if bottom_latitude < -90:
        bottom_latitude = -180 - bottom_latitude

    longitude_width_at_top = max(
        geomath.longitude_degree_size(top_latitude), 1
        )
    longitude_width_at_bottom = max(
        geomath.longitude_degree_size(bottom_latitude), 1
        )

    # This could go wrong at very high latitudes but seems OK for now
    longitude_span = width / min(longitude_width_at_top,
                                 longitude_width_at_bottom)

    min_corner = (
        city_location[0] - longitude_span/2,
        bottom_latitude
        )

    max_corner = (
        city_location[0] + longitude_span/2,
        top_latitude
        )

    return instantiate_map(min_corner,
                           max_corner,
                           projection=projection)

# ---------------------------------------------------------------------


def region_map(region_name,
               projection=None):
    """Create map for predefined region

    Create a geographic map for one of several common regions in the
    world. For a list of supported regions please see
    tracktable.maps.available_maps().

    Args:
       region_name (str): Name of desired region

    Keyword Arguments:
       projection (Matplotlib axes): a projection from cartopy.crs (Default: None)

    Returns:
       Cartopy axes for given region
    """

    if region_name not in available_maps():
        raise ValueError(("There is no predefined map "
                          "for region '{}'.").format(region_name))

    global CONVENIENCE_MAPS
    params = CONVENIENCE_MAPS[region_name]

    if projection is None:
        projection = cartopy.crs.Miller

    logger = logging.getLogger(__name__)
    logger.debug("region_map: projection is {}".format(projection))

    map_axes = instantiate_map(
        min_corner=params['min_corner'],
        max_corner=params['max_corner'],
        projection=projection
        )

    logger.debug("region_map: map_axes are {}".format(map_axes))
    return map_axes

# ----------------------------------------------------------------------


def _instantiate_map_common(projection=None):
    """ Instantiates axes with the given projection, default = Miller
    """
    if projection is None:
        projection = cartopy.crs.Miller
    elif isinstance(projection, str):
        projection = getattr(cartopy.crs, projection)

    axes = plt.axes(projection=projection())
    return axes
# ----------------------------------------------------------------------


def instantiate_map_global(projection=None):
    """Draw a map with custom projection gloabl extent.

    Keyword Args:
      projection (Matplotlib axes): a projection from cartopy.crs (Default: None)

    Returns:
      Matplotlib Axes instance

    """
    axes = _instantiate_map_common(projection=projection)
    axes.set_global()

    logger = logging.getLogger(__name__)
    logger.debug(("instantiate_map: Map successfully instantiated. "
                  "Axes: {}").format(axes))
    axes.tracktable_projection = projection
    return axes

# ----------------------------------------------------------------------


def instantiate_map(min_corner,
                    max_corner,
                    projection=None):
    """Draw a map with custom projection and bounding box.

    If min_corner and max_corner are set then we will set the map
    extents to match. If they are None then we will stick with
    whatever the defaults for the map projection are. You will always
    want to specify the extents unless the projection doesn't have any
    (e.g. whole-globe projections) or is defined with special extents
    (the OSGB projection, sensible for the UK and not much else).

    Args:
      min_corner (point2d): (lon, lat) coordinates of southwest corner
      max_corner (point2d): (lon, lat) coordinates of northeast corner

    Keyword Args:
      projection (Matplotlib axes): a projection from cartopy.crs (Default: None)

    Returns:
      Matplotlib Axes instance

    """

    axes = _instantiate_map_common(projection=projection)

    if min_corner is not None and max_corner is not None:
        axes.set_extent(
            [min_corner[0],
             max_corner[0],
             min_corner[1],
             max_corner[1]]
        )

    logger = logging.getLogger(__name__)
    logger.debug(("instantiate_map: Map successfully instantiated. "
                  "Axes: {}").format(axes))
    axes.tracktable_projection = projection
    return axes


# ----------------------------------------------------------------------

def predefined_map(mapname,
                   country=None,
                   location=None,
                   region_size=(200, 200),
                   projection=None):
    """Create a map of one of several familiar regions in the world.

    You can ask for one of four types of map.

        Region: one of 'region:conus' (continental US), 'region:europe',
                      'region:world', 'region:north_america',
                      'region:south_america', 'region:australia'

        Airport: 'airport:DFW' where 'DFW' is the 3- or 4-letter ICAO
                 abbreviation for the airport you want

        Port: 'port:Alexandria' where 'Alexandria' is the port name

        City: 'city:WashingtonDC' where 'WashingtonDC' is the city name
          without spaces or punctuation marks.

    For the airport, port and city maps you may specify an additional
    'region_size' argument that gives the desired width and height of
    the map region in KM. For example, a 200km-by-100km window
    centered on St. Louis airport could be created this way:

    .. code-block:: python

        my_map_axes = predefined_map('airport:STL', region_size=(200, 100))

    For the port and city maps you may need to specify the country (ports and cities)
    or location (cities) to search near if the port or city shares a name with
    another port or city in our internal database.

    .. code-block:: python

        my_map_axes = predefined_map('port:Newport', country="United Kingdom")

    Args:
        mapname (str): String naming which predefined map you want

    Keyword Arg:
        country (str): Two character country code for city maps, full country name for port maps. Required if a port or city name matches multiple items.  (Default: None).
        location (tuple, TrajectoryPoint, BasePoint): Location to search near, exclusively used for city maps (Default: None).
        region_size (point2d): 2-element tuple with (width, height) as km (Default: (200, 200))
        projection (Matplotlib axes): a projection from cartopy.crs (Default: None)

    Returns:
      Matplotlib axes (via Cartopy) into which you can render your data
    """

    if region_size is None:
        region_size = (200, 200)

    mapname_upper = mapname.upper()
    if mapname_upper.startswith('AIRPORT:'):
        airport_id = mapname.split(':')[1].upper()
        return airport_map(airport_id, region_size=region_size, projection=projection)

    if mapname_upper.startswith('PORT:'):
        port_name = mapname.split(':')[1].upper()
        return port_map(port_name, port_country=country, region_size=region_size, projection=projection)

    elif mapname_upper.startswith('CITY:'):
        city_name = mapname.split(':')[1]
        return city_map(city_name, city_country=country, city_location=location, region_size=region_size, projection=projection)

    elif mapname_upper.startswith('REGION:'):
        region_name = mapname.split(':')[1]
        return region_map(region_name, projection=projection)

    else:
        raise KeyError(("Unknown name for predefined map: {}"
                        " Valid argments are 'region:<region>', 'city:<city>'"
                        " 'airport:<airport>' or 'port:<port>'.").format(mapname))

# ----------------------------------------------------------------------
