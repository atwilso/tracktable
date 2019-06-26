#ifndef __tracktable_extract_pair_member_h
#define __tracktable_extract_pair_member_h

#include <utility>
#include <algorithm>

namespace tracktable {

template<class pair_type>
struct ExtractFirst : public std::unary_function<
  pair_type,
  typename pair_type::first_type
  >
{
  typename pair_type::first_type operator()(pair_type const& input) const
  {
    return input.first;
  }
};

template<class pair_type>
struct ExtractSecond : public std::unary_function<
  pair_type,
  typename pair_type::second_type
  >
{
  typename pair_type::second_type operator()(pair_type const& input) const
  {
    return input.second;
  }
};

} // namespace tracktable

#endif
