/*
* Copyright (c) 2014-2020 National Technology and Engineering
* Solutions of Sandia, LLC. Under the terms of Contract DE-NA0003525
* with National Technology and Engineering Solutions of Sandia, LLC,
* the U.S. Government retains certain rights in this software.
*
* Redistribution and use in source and binary forms, with or without
* modification, are permitted provided that the following conditions
* are met:
*
* 1. Redistributions of source code must retain the above copyright
* notice, this list of conditions and the following disclaimer.
*
* 2. Redistributions in binary form must reproduce the above copyright
* notice, this list of conditions and the following disclaimer in the
* documentation and/or other materials provided with the distribution.
*
* THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
* "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
* LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
* A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
* HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
* SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
* LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
* DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
* THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
* (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
* OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
*/

/*
* RadiusOfGyration - Signature for the "radius of gyration of a
* trajectory" algorithm.  Must be specialized by subclasses.
*/

#ifndef __tracktable_core_detail_algorithm_signatures_RadiusOfGyration_h
#define __tracktable_core_detail_algorithm_signatures_RadiusOfGyration_h

#include <boost/mpl/assert.hpp>

namespace tracktable { namespace algorithms {

template<typename T>
struct radius_of_gyration
{
  BOOST_MPL_ASSERT_MSG(
    sizeof(T) == 0,
    RADIUS_OF_GYRATION_NOT_IMPLEMENTED_FOR_THIS_TRAJECTORY_TYPE,
    (types<T>)
  );
};

} } // exit namespace tracktable::algorithms

namespace tracktable {

template<typename TrajectoryT>
double radius_of_gyration(TrajectoryT const& path)
{
  return algorithms::radius_of_gyration<TrajectoryT>::apply(path);
}

} // exit namespace tracktable


#endif
