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


import sys
import os.path
import traceback

import matplotlib
matplotlib.use('Agg')

from matplotlib import pyplot
from tracktable.render.mapmaker import mapmaker
from tracktable.core import test_utilities

def test_europe_map(ground_truth_dir,
                    test_output_dir,
                    image_filename='EuropeMap.png'):

    pyplot.figure(figsize=(8, 6))
    (mymap, artists) = mapmaker(
        domain='terrestrial',
        map_name='region:europe',
        lonlat_linewidth=0.25,
        lonlat_color='#4040A0',
        state_color='#806060',
        country_color='#408040',
        draw_coastlines=True,
        draw_countries=True,
        draw_states=True,
        draw_lonlat=True,
        fill_land=True,
        fill_water=True,
        coastline_linewidth=2,
        coastline_color='#B0B0B0',
        land_fill_color='#404040',
        water_fill_color='#000030'
   )

    pyplot.savefig(os.path.join(test_output_dir, image_filename),
                   dpi=150)
    pyplot.close()

    return test_utilities.compare_image_to_ground_truth(image_filename,
                                                        ground_truth_dir,
                                                        test_output_dir)

# ----------------------------------------------------------------------

def test_mapmaker(ground_truth_path, test_output_path):
    return test_europe_map(ground_truth_path, test_output_path)

# ----------------------------------------------------------------------

def main():
    if len(sys.argv) != 3:
        print("usage: {} ground_truth_dir test_output_dir".format(sys.argv[0]))

    return test_mapmaker(sys.argv[1], sys.argv[2])

# ----------------------------------------------------------------------

if __name__ == '__main__':
    sys.exit(main())
