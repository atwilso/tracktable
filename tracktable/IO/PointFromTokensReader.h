/*
 * Copyright (c) 2014-2017 National Technology and Engineering
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

#ifndef __tracktable_point_from_tokens_reader_h
#define __tracktable_point_from_tokens_reader_h

#include <tracktable/Core/TracktableCommon.h>
#include <tracktable/Core/detail/trait_signatures/HasProperties.h>
#include <tracktable/Core/PropertyConverter.h>

#include <tracktable/IO/GenericReader.h>
#include <tracktable/IO/ParseExceptions.h>
#include <tracktable/IO/detail/HeaderStrings.h>
#include <tracktable/IO/detail/PointHeader.h>
#include <tracktable/IO/detail/SetProperties.h>

#include <iterator>
#include <iostream>
#include <istream>
#include <string>
#include <cassert>
#include <map>
#include <stdexcept>
#include <vector>

#include <boost/lexical_cast.hpp>
#include <boost/shared_ptr.hpp>
#include <boost/tokenizer.hpp>
#include <boost/algorithm/string/trim.hpp>

namespace tracktable {

/** Read points from lists of tokens.
 *
 * PointFromTokensReader expects as its input an iterator that will yield
 * iterator ranges.  That is, each value of the iterator is a (begin,
 * end) pair of iterators that will produce a set of tokens for one
 * point.
 *
 * Think of it with this common use case.  Somewhere upstream you are
 * reading lines from a text file.  Your reader takes lines from the
 * file and separates each line into a list of tokens using some
 * delimiter.  PointFromTokensReader takes each of those lists of tokens, one
 * list at a time, and turns it into a point of some user-requested
 * type.
 */

template<typename PointT, typename SourceIterT>
class PointFromTokensReader : public GenericReader<PointT>
{
public:
  typedef PointT                                point_type;
  typedef SourceIterT                           source_iterator_type;
  typedef boost::shared_ptr<point_type>         point_shared_ptr_type;

  PointFromTokensReader()
    : ObjectIdColumn(-1)
    , TimestampColumn(-1)
    , IgnoreHeader(false)
    , WarningsEnabled(true)
    {
    }

  PointFromTokensReader(const PointFromTokensReader& other)
    : SourceBegin(other.SourceBegin)
    , SourceEnd(other.SourceEnd)
    , CoordinateMap(other.CoordinateMap)
    , FieldMap(other.FieldMap)
    , ObjectIdColumn(other.ObjectIdColumn)
    , TimestampColumn(other.TimestampColumn)
    , IgnoreHeader(false)
    , WarningsEnabled(true)
    { }


  PointFromTokensReader(source_iterator_type const& start, source_iterator_type const& finish)
    : SourceBegin(start)
    , SourceEnd(finish)
    , ObjectIdColumn(-1)
    , TimestampColumn(-1)
    , IgnoreHeader(false)
    , WarningsEnabled(true)
    { }

  virtual ~PointFromTokensReader()
    {
    }

  PointFromTokensReader& operator=(PointFromTokensReader const& other)
    {
      this->SourceBegin     = other.SourceBegin;
      this->SourceEnd       = other.SourceEnd;
      this->CoordinateMap   = other.CoordinateMap;
      this->FieldMap        = other.FieldMap;
      this->ObjectIdColumn  = other.ObjectIdColumn;
      this->TimestampColumn = other.TimestampColumn;
      this->IgnoreHeader    = other.IgnoreHeader;
      this->WarningsEnabled = other.WarningsEnabled;
      this->PropertyReadWrite = other.PropertyReadWrite;
      return *this;
    }

  bool operator==(PointFromTokensReader const& other) const
    {
      return (
        this->SourceBegin        == other.SourceBegin
        && this->SourceEnd       == other.SourceEnd
        && this->CoordinateMap   == other.CoordinateMap
        && this->FieldMap        == other.FieldMap
        && this->ObjectIdColumn  == other.ObjectIdColumn
        && this->TimestampColumn == other.TimestampColumn
        && this->IgnoreHeader    == other.IgnoreHeader
        && this->WarningsEnabled == other.WarningsEnabled
	&& this->PropertyReadWrite == other.PropertyReadWrite
        );
    }

  bool operator!=(PointFromTokensReader const& other) const
  {
    return !(*this == other);
  }

  void set_object_id_column(int column)
    {
      this->ObjectIdColumn = column;
    }

  void set_timestamp_column(int column)
    {
      this->TimestampColumn = column;
    }

  int object_id_column() const
    {
      return this->ObjectIdColumn;
    }

  int timestamp_column() const
    {
      return this->TimestampColumn;
    }

  void set_coordinate_column(int coordinate, int column)
    {
      this->CoordinateMap[coordinate] = column;
    }

  void set_real_field_column(std::string const& field, int column)
  {
    this->FieldMap[field] = io::detail::ColumnTypeAssignment::real(column);
  }

  void set_integer_field_column(std::string const& field, int column)
  {
    this->FieldMap[field] = io::detail::ColumnTypeAssignment::integer(column);
  }

  void set_time_field_column(std::string const& field, int column)
  {
    this->FieldMap[field] = io::detail::ColumnTypeAssignment::timestamp(column);
  }

  void set_string_field_column(std::string const& field, int column)
  {
    this->FieldMap[field] = io::detail::ColumnTypeAssignment::string(column);
  }

  int coordinate_column(int coordinate) const
    {
      tracktable::IntIntMap::const_iterator iter(this->CoordinateMap.find(coordinate));
      if (iter != this->CoordinateMap.end())
        {
        return (*iter).second;
        }
      else
        {
        return -1;
        }
    }

  int real_field_column(std::string const& field) const
    {
      if (this->has_real_field_column(field))
        {
        PropertyAssignmentMap::const_iterator iter(this->FieldMap.find(field));
        return (*iter).second.column;
        }
      else
        {
        return -1;
        }
    }

  int integer_field_column(std::string const& field) const
    {
      if (this->has_integer_field_column(field))
        {
        PropertyAssignmentMap::const_iterator iter(this->FieldMap.find(field));
        return (*iter).second.column;
        }
      else
        {
        return -1;
        }
    }

  int string_field_column(std::string const& field) const
    {
      if (this->has_string_field_column(field))
        {
        PropertyAssignmentMap::const_iterator iter(this->FieldMap.find(field));
        return (*iter).second.column;
        }
      else
        {
        return -1;
        }
    }

  int time_field_column(std::string const& field) const
  {
    if (this->has_time_field_column(field))
      {
      PropertyAssignmentMap::const_iterator iter(this->FieldMap.find(field));
      return (*iter).second.column;
      }
    else
      {
      return -1;
      }
  }

  bool has_coordinate_column(int coordinate) const
  {
    return (this->CoordinateMap.find(coordinate) != this->CoordinateMap.end());
  }

  bool has_real_field_column(std::string const& field) const
  {
    PropertyAssignmentMap::const_iterator iter = this->FieldMap.find(field);
    return (iter != this->FieldMap.end() &&
            (*iter).second.type == TYPE_REAL);
  }

  bool has_integer_field_column(std::string const& field) const
    {
      PropertyAssignmentMap::const_iterator iter = this->FieldMap.find(field);
      return (iter != this->FieldMap.end() &&
              (*iter).second.type == TYPE_INTEGER);
    }

  bool has_string_field_column(std::string const& field) const
  {
    PropertyAssignmentMap::const_iterator iter = this->FieldMap.find(field);
    return (iter != this->FieldMap.end() &&
            (*iter).second.type == TYPE_STRING);
  }

  bool has_time_field_column(std::string const& field) const
  {
    PropertyAssignmentMap::const_iterator iter = this->FieldMap.find(field);
    return (iter != this->FieldMap.end() &&
            (*iter).second.type == TYPE_TIMESTAMP);
  }

  void clear_coordinate_assignments()
    {
      this->CoordinateMap.clear();
    }

  void set_warnings_enabled(bool onoff)
    {
      this->WarningsEnabled = onoff;
    }

  bool warnings_enabled() const
    {
      return this->WarningsEnabled;
    }

  bool ignore_header() const
    {
      return this->IgnoreHeader;
    }

  void set_ignore_header(bool onoff)
    {
      this->IgnoreHeader = onoff;
    }

  void set_input_range(source_iterator_type my_begin, source_iterator_type my_end)
  {
    this->SourceBegin = my_begin;
    this->SourceEnd = my_end;
  }

  void set_timestamp_format(string_type const& format)
  {
    this->PropertyReadWrite.set_timestamp_input_format(format);
  }

  void set_null_value(string_type const& value)
    {
      this->PropertyReadWrite.set_null_value(value);
    }

  string_type null_value() const
    {
      return this->PropertyReadWrite.null_value();
    }
  
  // These two methods are for the Python wrappers.  In C++-land they
  // explicitly break encapsulation -- don't use them! -- but in
  // Python-land they make for a much more Pythonic interface.
  tracktable::IntIntMap& __coordinate_assignments()
    {
      return this->CoordinateMap;
    }

  void __set_coordinate_assignments(tracktable::IntIntMap const& cmap)
    {
      this->CoordinateMap = cmap;
    }

protected:
  typedef io::detail::PropertyAssignmentMap PropertyAssignmentMap;
  typedef std::vector<settings::string_type> string_vector_type;

  IntIntMap             CoordinateMap;
  PropertyAssignmentMap FieldMap;

  source_iterator_type  SourceBegin;
  source_iterator_type  SourceEnd;

  int                   ObjectIdColumn;
  int                   TimestampColumn;

  bool                  IgnoreHeader;
  bool                  WarningsEnabled;

  PropertyConverter     PropertyReadWrite;

  point_shared_ptr_type next_item()
    {
      point_shared_ptr_type NextPoint;

      std::size_t required_num_tokens =
        this->CoordinateMap.size()
        + this->FieldMap.size()
        + static_cast<std::size_t>(traits::has_object_id<point_type>::value)
        + static_cast<std::size_t>(traits::has_timestamp<point_type>::value)
        ;

      for (IntIntMap::iterator iter = this->CoordinateMap.begin();
           iter != this->CoordinateMap.end();
           ++iter)
        {
        if (iter->second == -1)
          {
          -- required_num_tokens;
          }
        }

      if (this->TimestampColumn == -1)
        {
        -- required_num_tokens;
        }

      if (this->ObjectIdColumn == -1)
        {
        -- required_num_tokens;
        }

      while (this->SourceBegin != this->SourceEnd)
        {
        try
          {
          string_vector_type _tokens;
          this->get_tokens_from_input(_tokens);

#if defined(COPIOUS_DEBUG_OUTPUT)
          std::cout << "DEBUG: Token list has " << _tokens.size() << " entries: ";
          for (string_vector_type::iterator iter = _tokens.begin();
               iter != _tokens.end();
               ++iter)
            {
            std::cout << "'" << *iter << "' ";
            }
          std::cout << "\n";
#endif
          if (_tokens.size() == 0)
            {
            // Skip empty lines.  Should this even be possible?
            ++(this->SourceBegin);
            continue;
            }

          if (_tokens[0] == io::detail::PointFileMagicString && this->IgnoreHeader)
            {
            std::cout << "WARNING: Found point header but IgnoreHeader is enabled.\n";
            }

          if (_tokens[0] == io::detail::PointFileMagicString
              && !this->IgnoreHeader)
            {
            this->configure_reader_from_header(_tokens);
            ++(this->SourceBegin);
            continue;
            }
          else
            {
            // It's a token list that isn't a header.  Let's try to
            // parse it as a point.
            if (_tokens.size() >= required_num_tokens)
              {
              NextPoint = point_shared_ptr_type(new point_type);
              this->populate_coordinates_from_tokens(_tokens, NextPoint);
              this->populate_properties_from_tokens(_tokens, NextPoint);
              ++(this->SourceBegin);
              return NextPoint;
              }
            else
              {
              if (this->WarningsEnabled)
                {
                std::cout << "WARNING: Not enough tokens to assemble point.  Expected " << required_num_tokens << ", found " << _tokens.size() << ".  Point will be skipped.\n";
                }
              ++(this->SourceBegin);
              }
            }
          }
        catch (ParseError const& e)
          {
          if (this->WarningsEnabled)
            {
            std::cout << "ERROR: " << e.what() << "\n";
            NextPoint = point_shared_ptr_type();
            }
          ++(this->SourceBegin);
          }
        catch (boost::bad_lexical_cast& e)
          {
          if (this->WarningsEnabled)
            {
            std::cout << "WARNING: Cast error while parsing point: " << e.what() << "\n";
            }
          ++(this->SourceBegin);
          }
        catch (std::exception& e)
          {
          if (this->WarningsEnabled)
            std::cout << "WARNING: Exception while parsing point: "
                      << e.what() << "\n";
          ++(this->SourceBegin);
          }
        }
      return NextPoint;
    }

  // ----------------------------------------------------------------------

  void configure_reader_from_header(string_vector_type const& tokens)
    {
      io::detail::PointHeader header;
      header.read_from_tokens(tokens.begin(), tokens.end());

      if (
        header.Dimension != std::size_t(traits::dimension<point_type>::value)
        && this->WarningsEnabled
        )
        {
        std::cout << "WARNING: PointFromTokensIterator: Header indicates points with dimension "
                  << header.Dimension << " but reader's point type has dimension "
                  << traits::dimension<point_type>::value << ".\n";
        }

      if (header.HasObjectId)
        {
        this->ObjectIdColumn = 0;
        }
      if (header.HasTimestamp)
        {
        this->TimestampColumn = 1;
        }

      this->configure_coordinate_assignments(header.HasObjectId,
                                             header.HasTimestamp,
                                             header.Dimension);

      std::size_t first_property_column_in_point_data =
        static_cast<std::size_t>(header.HasObjectId)
        + static_cast<std::size_t>(header.HasTimestamp)
        + header.Dimension;
/*
      std::size_t first_property_assignment_column =
        1 // header token
        + 1 // domain
        + 1 // dimension
        + static_cast<std::size_t>(header.HasObjectId)
        + static_cast<std::size_t>(header.HasTimestamp)
        + 1 // number of properties
        ;
*/
      this->configure_field_assignments(header,
                                        first_property_column_in_point_data);
    }

  // ----------------------------------------------------------------------

  void configure_coordinate_assignments(bool object_id_present,
                                        bool timestamp_present,
                                        std::size_t expected_dimension)
    {
      this->CoordinateMap.clear();

      std::size_t first_coordinate_column = 0;
      first_coordinate_column += static_cast<std::size_t>(object_id_present);
      first_coordinate_column += static_cast<std::size_t>(timestamp_present);
      for (std::size_t d = 0; d < expected_dimension; ++d)
        {
        this->CoordinateMap[static_cast<int>(d)] = static_cast<int>(first_coordinate_column + d);
        }
    }

  // ----------------------------------------------------------------------

  void configure_field_assignments(io::detail::PointHeader const& header,
                                   std::size_t first_property_column)
    {
      this->FieldMap.clear();

      for (std::size_t i = 0; i < header.PropertyNames.size(); ++i)
        {
        string_type property_name(header.PropertyNames[i]);
        PropertyUnderlyingType property_type(header.PropertyTypes[i]);

        this->FieldMap[property_name] = io::detail::ColumnTypeAssignment(first_property_column + i, property_type);
        }
    }

  // ----------------------------------------------------------------------

  void get_tokens_from_input(string_vector_type& tokens)
    {
      typedef typename source_iterator_type::value_type token_iterator_range;
      token_iterator_range token_range(*this->SourceBegin);
      tokens.assign(token_range.first, token_range.second);
      for (string_vector_type::iterator iter = tokens.begin();
           iter != tokens.end();
           ++iter)
        {
        boost::algorithm::trim(*iter);
        }
    }

  // ----------------------------------------------------------------------

  void populate_coordinates_from_tokens(string_vector_type const& tokens,
                                        point_shared_ptr_type point)
    {
      for (IntIntMap::const_iterator iter = this->CoordinateMap.begin();
           iter != this->CoordinateMap.end();
           ++iter)
        {
        int coord = (*iter).first;
        int column = (*iter).second;

        if (tokens.at(column).size() == 0)
          {
          throw EmptyCoordinateError(coord);
          }
        try
          {
          if (iter->second == -1) continue; // skip missing coordinates
          settings::point_coordinate_type value(boost::lexical_cast<settings::point_coordinate_type>(tokens.at(column)));
          (*point)[coord] = value;
          }
        catch (boost::bad_lexical_cast e)
          {
          std::ostringstream fieldbuf;
          fieldbuf << "coordinate " << coord;
          throw LexicalCastError(fieldbuf.str(), tokens.at(column), "double");
          }
        }
    }

  // ----------------------------------------------------------------------

  void populate_properties_from_tokens(string_vector_type const& tokens,
                                       point_shared_ptr_type point)
    {
      io::detail::set_properties<
        point_type,
        traits::has_properties<point_type>::value
        >::apply(*point, tokens, this->FieldMap, this->PropertyReadWrite);

      if (this->ObjectIdColumn != -1)
        {
        io::detail::set_object_id<
          point_type,
          traits::has_object_id<point_type>::value
          >::apply(*point, tokens, this->ObjectIdColumn);
        }

      if (this->TimestampColumn != -1)
        {
        io::detail::set_timestamp<
          point_type,
          traits::has_timestamp<point_type>::value
          >::apply(*point, tokens, this->TimestampColumn, this->PropertyReadWrite.timestamp_converter());
        }
    }
};

} // close namespace tracktable

#endif
