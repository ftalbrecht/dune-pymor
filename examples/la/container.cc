// This file is part of the dune-pymor project:
//   https://github.com/pyMor/dune-pymor
// Copyright Holders: Felix Albrecht, Stephan Rave
// License: BSD 2-Clause License (http://opensource.org/licenses/BSD-2-Clause)

#include "container.hh"

EigenDenseVector* createVector(const int ss)
{
  return EigenDenseVector::create(ss);
}
