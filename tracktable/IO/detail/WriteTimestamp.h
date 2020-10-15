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

// Typesafe code for writing out the timestamp from an object.  Uses
// tag dispatch on tracktable::traits::HasTimestamp.

#ifndef __tracktable_io_WriteTimestamp_h
#define __tracktable_io_WriteTimestamp_h

#include <boost/date_time/time_facet.hpp>
#include <tracktable/Core/TimestampConverter.h>

namespace tracktable { namespace io { namespace detail {

template<bool has_timestamp>
struct write_timestamp
{
  template<typename point_t, typename out_iter_t>
  static inline void apply(
    point_t const& /*thing*/,
    TimestampConverter& /*formatter*/,
    out_iter_t& /*where_to_write*/
    )
    {
      // This is the default version - there is no object ID
      // write
      return;
    }
};

template<>
struct write_timestamp<true>
{
  template<typename point_t, typename out_iter_t>
  static inline void apply(point_t const& thing, TimestampConverter& formatter, out_iter_t& where_to_write)
    {
      (*where_to_write++) = formatter.timestamp_to_string(thing.timestamp());
    }
};


} } } // close namespace tracktable::io::detail

#endif

