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


# This is tracktable/Python/tracktable/render/tests/CMakeLists.txt
#
# Here we list the Python tests that we need to run to make sure that
# our rendering code is working.  These are basically "smoke tests" --
# we don't yet have the ability to verify the content of an image.


include(PythonTest)

add_python_test(P_Mapmaker_Airport
  tracktable.render.tests.test_mapmaker_airport "${Tracktable_SOURCE_DIR}/TestData/GroundTruth" "${Tracktable_BINARY_DIR}/TestOutput/"
)

add_python_test(P_Mapmaker_CONUS
  tracktable.render.tests.test_mapmaker_conus "${Tracktable_SOURCE_DIR}/TestData/GroundTruth" "${Tracktable_BINARY_DIR}/TestOutput/"
)

add_python_test(P_Mapmaker_NorthAmerica
  tracktable.render.tests.test_mapmaker_north_america "${Tracktable_SOURCE_DIR}/TestData/GroundTruth" "${Tracktable_BINARY_DIR}/TestOutput/"
)

add_python_test(P_Mapmaker_Europe
  tracktable.render.tests.test_mapmaker_europe "${Tracktable_SOURCE_DIR}/TestData/GroundTruth" "${Tracktable_BINARY_DIR}/TestOutput/"
)
