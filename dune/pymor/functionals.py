#! /usr/bin/env python
# This file is part of the dune-pymor project:
#   https://github.com/pyMor/dune-pymor
# Copyright Holders: Felix Albrecht, Stephan Rave
# License: BSD 2-Clause License (http://opensource.org/licenses/BSD-2-Clause)

import pybindgen
from pybindgen import retval, param

import numpy as np

from pymor.la import NumpyVectorArray
from pymor.operators import LincombOperatorInterface
from pymor.operators.basic import OperatorBase

def inject_VectorBasedImplementation(module, exceptions, interfaces, CONFIG_H, Traits, template_parameters=None):
    assert(isinstance(module, pybindgen.module.Module))
    assert(isinstance(exceptions, dict))
    assert(isinstance(interfaces, dict))
    for element in interfaces:
        assert(isinstance(element, str))
        assert(len(element) > 0)
    assert(isinstance(CONFIG_H, dict))
    assert(isinstance(Traits, dict))
    for key in Traits.keys():
        assert(isinstance(Traits[key], str))
        assert(len(Traits[key].strip()) > 0)
    assert('SourceType' in Traits)
    SourceType = Traits['SourceType']
    assert('ScalarType' in Traits)
    ScalarType = Traits['ScalarType']
    if template_parameters is not None:
        if isinstance(template_parameters, str):
            assert(len(template_parameters.strip()) > 0)
            template_parameters = [ template_parameters ]
        elif isinstance(template_parameters, list):
            for element in template_parameters:
                assert(isinstance(element, str))
                assert(len(element.strip()) > 0)
    module = module.add_cpp_namespace('Dune').add_cpp_namespace('Pymor').add_cpp_namespace('Functionals')
    Class = module.add_class('VectorBased',
                             parent=[interfaces['Dune::Pymor::FunctionalInterfaceDynamic'],
                                     interfaces['Dune::Pymor::Parametric']],
                             template_parameters=template_parameters)
    Class.add_method('type_this', retval('std::string'), [], is_const=True, is_static=True,
                     throw=[exceptions['PymorException'], exceptions['DuneException']])
    Class.add_method('type_source', retval('std::string'), [], is_const=True, is_static=True,
                     throw=[exceptions['PymorException'], exceptions['DuneException']])
    Class.add_method('type_scalar', retval('std::string'), [], is_const=True, is_static=True,
                     throw=[exceptions['PymorException'], exceptions['DuneException']])
    Class.add_method('type_frozen', retval('std::string'), [], is_const=True, is_static=True,
                     throw=[exceptions['PymorException'], exceptions['DuneException']])
    Class.add_method('linear', retval('bool'), [], is_const=True)
    Class.add_method('dim_source', retval('unsigned int'), [], is_const=True)
    Class.add_method('apply',
                     retval(ScalarType),
                     [param('const ' + SourceType + ' &', 'source')],
                     is_const=True,
                     throw=[exceptions['PymorException']])
    Class.add_method('apply',
                     retval(ScalarType),
                     [param('const ' + SourceType + ' &', 'source'),
                      param('const Dune::Pymor::Parameter', 'mu')],
                     is_const=True,
                     throw=[exceptions['PymorException']])
    return Class


class WrappedFunctionalBase(OperatorBase):

    wrapped_type = None

    vec_type_source = None

    type_source = None
    type_range = NumpyVectorArray

    dim_range = 1

    _wrapper = None

    def __init__(self, op):
        assert isinstance(op, self.wrapped_type)
        self._impl = op
        self.dim_source = op.dim_source()
        self.linear = op.linear()
        if hasattr(op, 'parametric') and op.parametric():
            pt = self._wrapper.parameter_type(op.parameter_type())
            self.build_parameter_type(pt, local_global=True)

    def apply(self, U, ind=None, mu=None):
        assert isinstance(U, self.type_source)
        vectors = U._list if ind is None else [U._list[i] for i in ind]
        if self.parametric:
            mu = self._wrapper.dune_parameter(self.parse_parameter(mu))
            R = np.array([self._impl.apply(v._impl, mu) for v in vectors])[..., np.newaxis]
            return NumpyVectorArray(R, copy=False)
        else:
            assert self.check_parameter(mu)
            R = np.array([self._impl.apply(v._impl) for v in vectors])[..., np.newaxis]
            return NumpyVectorArray(R, copy=False)


def wrap_functional(cls, wrapper):

    class WrappedFunctional(WrappedFunctionalBase):
        wrapped_type = cls
        vec_type_source = wrapper[cls.type_source()]
        type_source = wrapper.vector_array(vec_type_source)
        _wrapper = wrapper

        def __init__(self, op):
            WrappedFunctionalBase.__init__(self, op)
            self.lock()

    WrappedFunctional.__name__ = cls.__name__
    return WrappedFunctional


def inject_LinearAffinelyDecomposedVectorBasedImplementation(module,
                                                             exceptions,
                                                             interfaces,
                                                             CONFIG_H,
                                                             Traits,
                                                             template_parameters=None):
    assert(isinstance(module, pybindgen.module.Module))
    assert(isinstance(exceptions, dict))
    assert(isinstance(interfaces, dict))
    for element in interfaces:
        assert(isinstance(element, str))
        assert(len(element) > 0)
    assert(isinstance(CONFIG_H, dict))
    assert(isinstance(Traits, dict))
    for key in Traits.keys():
        assert(isinstance(Traits[key], str))
        assert(len(Traits[key].strip()) > 0)
    assert('SourceType' in Traits)
    SourceType = Traits['SourceType']
    assert('ComponentType' in Traits)
    ComponentType = Traits['ComponentType']
    assert('ScalarType' in Traits)
    ScalarType = Traits['ScalarType']
    assert('FrozenType' in Traits)
    FrozenType = Traits['ComponentType']
    if template_parameters is not None:
        if isinstance(template_parameters, str):
            assert(len(template_parameters.strip()) > 0)
            template_parameters = [ template_parameters ]
        elif isinstance(template_parameters, list):
            for element in template_parameters:
                assert(isinstance(element, str))
                assert(len(element.strip()) > 0)
    module = module.add_cpp_namespace('Dune').add_cpp_namespace('Pymor').add_cpp_namespace('Functionals')
    Class = module.add_class('LinearAffinelyDecomposedVectorBased',
                             parent=[interfaces['Dune::Pymor::AffinelyDecomposedFunctionalInterfaceDynamic'],
                                     interfaces['Dune::Pymor::Parametric']],
                             template_parameters=template_parameters)
    Class.add_method('type_this', retval('std::string'), [], is_const=True, is_static=True,
                     throw=[exceptions['PymorException'], exceptions['DuneException']])
    Class.add_method('type_source', retval('std::string'), [], is_const=True, is_static=True,
                     throw=[exceptions['PymorException'], exceptions['DuneException']])
    Class.add_method('type_scalar', retval('std::string'), [], is_const=True, is_static=True,
                     throw=[exceptions['PymorException'], exceptions['DuneException']])
    Class.add_method('type_frozen', retval('std::string'), [], is_const=True, is_static=True,
                     throw=[exceptions['PymorException'], exceptions['DuneException']])
    Class.add_method('num_components', retval('unsigned int'), [], is_const=True, throw=[exceptions['PymorException']])
    Class.add_method('component_and_return_ptr',
                     retval(ComponentType + ' *', caller_owns_return=True),
                     [param('const int', 'qq')],
                     is_const=True,
                     throw=[exceptions['PymorException']],
                     custom_name='component')
    Class.add_method('coefficient_and_return_ptr',
                     retval('Dune::Pymor::ParameterFunctional *', caller_owns_return=True),
                     [param('const int', 'qq')],
                     is_const=True,
                     throw=[exceptions['PymorException']],
                     custom_name='coefficient')
    Class.add_method('has_affine_part', retval('bool'), [], is_const=True, throw=[exceptions['PymorException']])
    Class.add_method('affine_part_and_return_ptr',
                     retval(ComponentType + ' *', caller_owns_return=True),
                     [],
                     is_const=True,
                     throw=[exceptions['PymorException']],
                     custom_name='affine_part')
    Class.add_method('linear', retval('bool'), [], is_const=True, throw=[exceptions['PymorException']])
    Class.add_method('dim_source', retval('unsigned int'), [], is_const=True, throw=[exceptions['PymorException']])
    Class.add_method('apply',
                     retval(ScalarType),
                     [param('const ' + SourceType + ' &', 'source')],
                     is_const=True,
                     throw=[exceptions['PymorException']])
    Class.add_method('apply',
                     retval(ScalarType),
                     [param('const ' + SourceType + ' &', 'source'),
                      param('const Dune::Pymor::Parameter', 'mu')],
                     is_const=True,
                     throw=[exceptions['PymorException']])
    Class.add_method('freeze_parameter_and_return_ptr',
                     retval(FrozenType + ' *', caller_owns_return=True),
                     [param('const Dune::Pymor::Parameter', 'mu')],
                     is_const=True,
                     throw=[exceptions['PymorException']],
                     custom_name='freeze_parameter')
    return Class


def wrap_affinely_decomposed_functional(cls, wrapper):

    class WrappedFunctional(LincombOperatorInterface, WrappedFunctionalBase):
        wrapped_type = cls
        vec_type_source = wrapper[cls.type_source()]
        type_source = wrapper.vector_array(vec_type_source)
        _wrapper = wrapper

        def __init__(self, op):
            WrappedFunctionalBase.__init__(self, op)
            operators = [self._wrapper[op.component(i)] for i in xrange(op.num_components())]
            coefficients = [op.coefficient(i) for i in xrange(op.num_components())]
            if op.has_affine_part():
                operators.append(self._wrapper[op.affine_part()])
                coefficients.append(1.)
                self.affine_part = True
            else:
                self.affine_part = False
            self.operators = tuple(operators)
            self.coefficients = tuple(coefficients)
            self.lock()

        def evaluate_coefficients(self, mu):
            mu = self._wrapper.dune_parameter(self.parse_parameter(mu))
            if self.affine_part:
                return [c.evaluate(mu) for c in self.coefficients[:-1]] + [1.]
            else:
                return [c.evaluate(mu) for c in self.coefficients]

    WrappedFunctional.__name__ = cls.__name__
    return WrappedFunctional
