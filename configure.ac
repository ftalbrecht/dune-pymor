# This file is part of the dune-pymor project:
#   https://github.com/pymor/dune-pymor
# Copyright Holders: Stephan Rave, Felix Schindler
# License: BSD 2-Clause License (http://opensource.org/licenses/BSD-2-Clause)

# -*- Autoconf -*-
# Process this file with autoconf to produce a configure script.
AC_PREREQ(2.50)
DUNE_AC_INIT # gets module version from dune.module file
AM_INIT_AUTOMAKE
AC_CONFIG_SRCDIR([])
AC_CONFIG_HEADERS([config.h])

AM_INIT_AUTOMAKE([subdir-objects])

# we need no more than the standard DE-stuff
# this module depends on dune-common
# this implies checking for [dune-common]
DUNE_CHECK_ALL

# implicitly set the Dune-flags everywhere
AC_SUBST(AM_CPPFLAGS, $DUNE_CPPFLAGS)
AC_SUBST(AM_LDFLAGS, $DUNE_LDFLAGS)
LIBS="$DUNE_LIBS"

AC_DEFINE([HAVE_DUNE_PYMOR], [1], [We are always here.])

AC_CONFIG_FILES([
  Makefile
  dune/Makefile
  dune/pymor/Makefile
  lib/Makefile
  m4/Makefile
  dune-pymor.pc
])
AC_OUTPUT
# finally print the summary information
DUNE_SUMMARY_ALL
