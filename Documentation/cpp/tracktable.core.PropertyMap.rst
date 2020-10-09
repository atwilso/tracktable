==================
PropertyMap Module
==================


---------------
Module Contents
---------------

.. doxygentypedef:: tracktable::PropertyMap
.. doxygenfunction:: tracktable::has_property
.. doxygenfunction:: tracktable::property
.. doxygenfunction:: tracktable::string_property
.. doxygenfunction:: tracktable::real_property
.. doxygenfunction:: tracktable::timestamp_property
.. todo:: Breathe doesn't easily support overloaded functions utilizing ``doxygenfunction::``, need to figure out
          how to handle the manually declared overloaded functions. This is why ``set_property`` throws the following
          warnings.
.. doxygenfunction:: tracktable::set_property (PropertyMap& properties, string_type const& name, double value)
.. doxygenfunction:: tracktable::set_property (PropertyMap& properties, string_type const& name, string_type const& value)
.. doxygenfunction:: tracktable::set_property (PropertyMap& properties, string_type const& name, Timestamp const& value)
.. doxygenfunction:: tracktable::set_property (PropertyMap& properties, string_type const& name, int64_t value)
.. doxygenfunction:: tracktable::set_property (PropertyMap& properties, string_type const& name, PropertyValueT const& value)
.. doxygenfunction:: tracktable::property_with_default
.. doxygenfunction:: tracktable::real_property_with_default
.. doxygenfunction:: tracktable::string_property_with_default
.. doxygenfunction:: tracktable::timestamp_property_with_default
.. doxygenfunction:: tracktable::property_map_to_string