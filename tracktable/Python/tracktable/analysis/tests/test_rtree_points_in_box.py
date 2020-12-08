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

from __future__ import print_function, division, absolute_import

import sys
from six.moves import range
from tracktable.analysis.rtree import RTree
from tracktable.domain import feature_vectors as fv

def test_points_in_box(point_type):
    points = []

    for i in range(10):
        point = point_type()
        for d in range(len(point)):
            point[d] = i
        points.append(point)

    box_min = point_type()
    box_max = point_type()

    for d in range(len(box_min)):
        box_min[d] = 2.5
        box_max[d] = 6.5

    tree = RTree(points)

    points_in_box = tree.find_points_in_box(box_min, box_max)

    # We expect to get points 3, 4, 5 and 6.
    if set([3, 4, 5, 6]) != set(points_in_box):
        print("ERROR: Expected points in box to have indices [3, 4, 5, 6].  Instead we got {}.".format(sorted(points_in_box)))
        return 1
    else:
        return 0

def main():
    error_count = 0

    for dimension in range(1, 30):
        point_type = fv.POINT_TYPES[dimension]
        error_count += test_points_in_box(point_type)

    return error_count

if __name__ == '__main__':
    sys.exit(main())
