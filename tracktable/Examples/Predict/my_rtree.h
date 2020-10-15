/*
 * Copyright (c) 2013-2020 National Technology and Engineering
 * Solutions of Sandia, LLC. Under the terms of Contract DE-NA0003525
 * with National Technology and Engineering Solutions of Sandia, LLC,
 * the U.S. Government retains certain rights in this software.
 */

//
// rtree
//
// Our rtree implementation
//
// Created by Danny Rintoul.
//

#ifndef __rtree
#define __rtree
#include "Common.h"
#include <utility>

#include <boost/array.hpp>
#include <boost/geometry/geometries/point.hpp>
#include <boost/geometry/geometries/register/point.hpp>
#include <boost/geometry/geometries/adapted/boost_array.hpp>

#include <tracktable/Analysis/GuardedBoostGeometryRTreeHeader.h>

// Here is the "by hand" thing that needs to be set for each run
// It describes the structure of your point.  There is probably a better
// way to do this.

BOOST_GEOMETRY_REGISTER_BOOST_ARRAY_CS(cs::cartesian)

typedef my_data* rtree_data_value;
typedef std::vector<rtree_data_value>::iterator data_itr;
typedef boost::geometry::index::quadratic<16> construction_parameters;
typedef boost::geometry::model::box<Feature> feature_vector_box;

template <typename Container>
class my_indexable
{
//  typedef typename Container::iterator iterator;
  typedef typename Container::value_type* ptr;
  typedef typename Container::const_reference cref;
  Container const& container;

public:
  typedef cref result_type;
  explicit my_indexable(Container const& c) : container(c) {}
//  result_type operator()(iterator itr) const { return *itr; }
  result_type operator()(ptr p) const { return *p; }
};
typedef my_indexable< std::vector<rtree_data_value> > indexable_getter;

namespace boost { namespace geometry { namespace index {

template <>
struct indexable<rtree_data_value>
{
    typedef rtree_data_value value_type;
    typedef Feature const& result_type;
    result_type operator()(value_type const& v) const { return v->Point; }
};

}}}
typedef boost::geometry::index::rtree<rtree_data_value, construction_parameters > my_rtree;

#endif
