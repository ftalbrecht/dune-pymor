#! /usr/bin/env python
# This file is part of the dune-pymor project:
#   https://github.com/pymor/dune-pymor
# Copyright Holders: Stephan Rave, Felix Schindler
# License: BSD 2-Clause License (http://opensource.org/licenses/BSD-2-Clause)

import pybindgen


def inject_exceptions(module, CONFIG_H):
    assert(isinstance(module, pybindgen.module.Module))
    exceptions = dict()
    namespace = module.add_cpp_namespace('Dune')
    exceptions['Exception'] = namespace.add_exception('Exception', message_rvalue='%(EXC)s.what().c_str()')
    # exceptions['PymorException'] = namespace.add_exception('PymorException',
    #                                                        parent=exceptions['DuneException'],
    #                                                        message_rvalue='%(EXC)s.pymorWhat()')
    # namespace = namespace.add_cpp_namespace('Pymor').add_cpp_namespace('Exception')
    # for exception_id in ['types_are_not_compatible', 'Exception', 'Exception', 'Exception',
    #                      'you_have_to_implement_this', 'Exception', 'this_is_not_parametric',
    #                      'this_does_not_make_any_sense', 'requirements_not_met', 'wrong_input', 'not_invertible',
    #                      'linear_solver_failed', 'io_error']:
    #     exceptions[exception_id] = namespace.add_exception(exception_id,
    #                                                        parent=exceptions['PymorException'])
    return module, exceptions
