# Copyright (c) 2014-2020 National Technology and Engineering
# Solutions of Sandia, LLC . Under the terms of Contract DE-NA0003525
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

###
### DetectAnaconda.cmake: Check whether a python interpreter is part of
### the Anaconda Python environment
###

# Continuum link their Python interpreters statically with the Python
# library.  This causes crashes on OS X when we load in a Python
# extension that is also linked with the Python library.  If we can
# detect this interpreter we can substitute a different set of link
# flags.
#
# We do this by trying to import the 'conda' module.  This program is
# Anaconda's package manager.  It is very unlikely that an Anaconda
# installation will not have it.

function(check_for_anaconda python_interpreter return_variable_name)

get_filename_component(
  _interpreter_directory
  ${python_interpreter}
  DIRECTORY
  )

if (EXISTS "${DIRECTORY}/conda")
  set(${return_variable_name} TRUE PARENT_SCOPE)
else ()
  # We might be in Anaconda but in a virtual environment.  If this is
  # the case, the CONDA_EXE environment variable will be set.
  if (DEFINED ENV{CONDA_EXE})
    set(${return_variable_name} TRUE PARENT_SCOPE)
  else (DEFINED ENV{CONDA_EXE})
    set(${return_variable_name} FALSE PARENT_SCOPE)
  endif (DEFINED ENV{CONDA_EXE})

endif ()


endfunction(check_for_anaconda)

