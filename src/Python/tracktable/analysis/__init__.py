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

"""Tracktable Trajectory Library - Analysis module

Here you will find algorithms for clustering, range queries, nearest
neighbor search and (eventually) dimensionality reduction.

"""

# TODO (mjfadem): Remove this file in release 1.8

import warnings
import sys

# Imports for the new module locations
import tracktable.algorithms
import tracktable.algorithms.dbscan
import tracktable.algorithms.distance_geometry

import tracktable.applications
import tracktable.applications.assemble_trajectories

import tracktable.domain
import tracktable.domain.rtree

# This just stops the source line from printing with the warning
def format_warning(message, category, filename, lineno, file=None, line=None):
    return '%s:%s: %s:%s\n' % (filename, lineno, category.__name__, message)

warnings.formatwarning = format_warning

# Allow the DeprecationWarning through since it's disabled by default
warnings.simplefilter("always", category=DeprecationWarning)

# This will display a DeprecationWarning when the source modules are imported
warnings.warn(" \ntracktable.analysis have been deprecated, its submodules have been relocated to more appropriate locations which are listed below. tracktable.analysis will be fully removed in release 1.8.\n\n"
        "\ttracktable.analysis.assemble_trajectories -> tracktable.applications.assemble_trajectories\n"
        "\ttracktable.analysis.dbscan                -> tracktable.algorithms.dbscan\n"
        "\ttracktable.analysis.distance_geometry     -> tracktable.algorithms.distance_geometry\n"
        "\ttracktable.analysis.rtree                 -> tracktable.domain.rtree\n", category=DeprecationWarning)

# Aliases to smooth the transition of relocation of the tracktable.analysis submodules
sys.modules['tracktable.analysis.assemble_trajectories'] = tracktable.applications.assemble_trajectories
sys.modules['tracktable.analysis.dbscan'] = tracktable.algorithms.dbscan
sys.modules['tracktable.analysis.distance_geometry'] = tracktable.algorithms.distance_geometry
sys.modules['tracktable.analysis.rtree '] = tracktable.domain.rtree
