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
# notice, this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
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

"""test_utilities - Functions to verify test output

Our Python tests typically create text files or images.  This module
contains functions that will let us easily verify that they match our
ground truth files, including computing differences where appropriate.
"""

from __future__ import print_function, division

import numpy as np
from tracktable.core import tracktable_logging as tt_logging

try:
    import PIL
    from PIL import Image
    PIL_AVAILABLE=True
except ImportError:
    tt_logging('warning', 'Python image library not available.  Image tests will automatically fail.')
    PIL_AVAILABLE=False

import datetime
import io
import os.path
import pickle
import random
import sys
if sys.version_info[0] == 2:
    import StringIO

random.seed(1234)

# useful constants for the rest of the world - the choice of NO_ERROR
# == 0 is so that we can return it to the shell and have it treated as
# a result code
NO_ERROR = 0
ERROR = 1

def log_test_output(*args, **kwargs):
    print(*args, **kwargs)

# ----------------------------------------------------------------------

def image_mse(imageA, imageB):
    # the 'Mean Squared Error' between the two images is the
    # sum of the squared difference between the two images;
    # NOTE: the two images must have the same dimension
    imageA = np.array(imageA)
    imageB = np.array(imageB)

    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])
    
    # return the MSE, the lower the error, the more "similar"
    # the two images are
    return err

# ----------------------------------------------------------------------

def compare_images(expected, actual, tolerance=1):
    """Compare two images pixel-by-pixel.

    Args:
      image1 (str): Filename for image 1

      image2 (str): Filename for image 2

      tolerance (float): Number from 0 to 255 describing how much per-pixel difference is acceptable

    Returns:
      None if images compare equal, string explaining problem if images are different

    Note:
      At present we delegate this to Matplotlib's image comparison
      routine since it does all kinds of nice conversions and
      measurements.  We will bring this in-house if we ever need to.
    """

    global PIL_AVAILABLE
    if not PIL_AVAILABLE:
        return False
    else:
        expected_image = Image.open(expected)
        actual_image = Image.open(actual)

        computed_mse = image_mse(expected_image, actual_image)
        if computed_mse >= tolerance:
            tt_logging.log('error', 'Image comparison failed: tolerance = {}, computed mean squared error = {}'.format(tolerance, computed_mse))
        return computed_mse < tolerance

# ----------------------------------------------------------------------

def compare_image_to_ground_truth(filename,
                                  ground_truth_dir,
                                  test_dir,
                                  tolerance=1):
    test_image_filename = os.path.join(test_dir, filename)
    expected_image_filename = os.path.join(ground_truth_dir, filename)

    result = compare_images(expected_image_filename,
                            test_image_filename,
                            tolerance=tolerance)

    if not result:
        return ERROR
    else:
        return NO_ERROR

# ----------------------------------------------------------------------

def version_appropriate_string_buffer(contents=None):
    if sys.version_info[0] == 2:
        buffer_type = StringIO.StringIO
    else:
        buffer_type = io.BytesIO

    if contents is None:
        return buffer_type()
    else:
        return buffer_type(contents)

# ----------------------------------------------------------------------

def pickle_and_unpickle(thing):
    picklebuf = pickle.dumps(thing)
    reconstituted = pickle.loads(picklebuf)

    if thing == reconstituted:
        return NO_ERROR
    else:
        print("ERROR: pickle_and_unpickle: Pickling did not reproduce input {}".format(type(thing)))
        return ERROR

# ----------------------------------------------------------------------

def set_random_properties(thing):
    thing.properties["my_float"] = random.uniform(-50, 50)
    thing.properties["my_time"] = datetime.datetime.now() + datetime.timedelta(minutes=random.randint(0, 1439))
    thing.properties["my_int"] = random.randint(-1000, 1000)
    thing.properties["my_string"] = "Random String {}".format(random.randint(0, 1000))

# ----------------------------------------------------------------------

def set_random_coordinates(thing, min_coord=-85, max_coord=85):
    for i in range(len(thing)):
        thing[i] = random.uniform(min_coord, max_coord)

# ----------------------------------------------------------------------

def create_random_point(point_class, add_properties=False):
    my_point = point_class()
    set_random_coordinates(my_point)
    if add_properties:
        set_random_properties(my_point)
    return my_point

# ----------------------------------------------------------------------

def create_random_trajectory(trajectory_class, point_class, min_length=10, max_length=100):
    object_id = "random_object_id_{}".format(random.randint(1, 1000))
    starting_timestamp = datetime.datetime.now()

    my_trajectory = trajectory_class()
    trajectory_length = random.randint(min_length, max_length)
    for i in range(trajectory_length):
        my_point = create_random_point(point_class, add_properties=True)
        my_point.object_id = object_id
        my_point.timestamp = starting_timestamp + datetime.timedelta(minutes=i)
        my_trajectory.append(my_point)

    set_random_properties(my_trajectory)

    return my_trajectory

# ----------------------------------------------------------------------

def create_random_trajectory_point(point_class):
    my_point = create_random_point(point_class, add_properties=True)
    my_point.timestamp = datetime.datetime.now() + datetime.timedelta(minutes=random.randint(1, 1439))
    my_point.object_id = "random_object_id_{}".format(random.randint(1, 1000))

    return my_point

