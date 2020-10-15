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

#include <tracktable/Core/PointLonLat.h>
#include <tracktable/Core/PointCartesian.h>
#include <tracktable/Core/TrajectoryPoint.h>

#include <tracktable/IO/PointWriter.h>

#include <iostream>
#include <cstdlib>
#include <sstream>
#include <vector>

template<typename point_type>
int test_point_writer()
{
  typedef tracktable::TrajectoryPoint<point_type> trajectory_point_type;
  typedef std::vector<trajectory_point_type> point_vector_type;

  point_vector_type points;

  for (std::size_t point_id = 0; point_id < 10; ++point_id)
    {
    trajectory_point_type next_point;
    for (std::size_t i = 0; i < tracktable::traits::dimension<trajectory_point_type>::value; ++i)
      {
      next_point[i] = 10*i + point_id;
      }

    next_point.set_timestamp(tracktable::time_from_string("2015-01-05 18:00:00"));
    next_point.set_object_id("test_object");

    // Set example string, numeric and timestamp properties
    std::ostringstream outbuf;
    next_point.set_property("basic_string", "Hi Mom!");

    outbuf << "String, with, embedded, commas, ID " << point_id;
    next_point.set_property("string_with_commas", outbuf.str());

    next_point.set_property("my_number", (int64_t)(12345 + point_id));

    outbuf.str(std::string());
    outbuf << "2014-07-" << std::setw(2) << std::setfill('0') << ((point_id + 1) % 30) << " " << std::setw(2) << std::setfill('0') << ((point_id + 1) % 24) << ":12:00";
    next_point.set_property("my_timestamp", tracktable::time_from_string(outbuf.str()));
    points.push_back(next_point);
    }

  std::ostringstream outbuf;
  tracktable::PointWriter writer(outbuf);
  writer.set_field_delimiter("\t");
  writer.write(points.begin(), points.end());

  std::cout << "Output of point writer with tabs for delimiters:\n";
  std::cout << outbuf.str() << "(end)\n";

  writer.set_field_delimiter(",");
  outbuf.str(std::string());
  writer.write(points.begin(), points.end());

  std::cout << "Output of point writer with commas for delimiters:\n";
  std::cout << outbuf.str() << "(end)\n";
  return 0;
}

int main(int /*argc*/, char* /*argv*/[])
{
  int num_errors = 0;

  num_errors += test_point_writer<tracktable::PointLonLat>();
  num_errors += test_point_writer<tracktable::PointCartesian<2> >();

  return num_errors;
}
