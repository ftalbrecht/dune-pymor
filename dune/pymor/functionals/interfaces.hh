// This file is part of the dune-pymor project:
//   https://github.com/pymor/dune-pymor
// Copyright holders: Stephan Rave, Felix Schindler
// License: BSD 2-Clause License (http://opensource.org/licenses/BSD-2-Clause)

#ifndef DUNE_PYMOR_FUNCTIONALS_INTERFACES_HH
#define DUNE_PYMOR_FUNCTIONALS_INTERFACES_HH

#include <dune/stuff/common/type_utils.hh>
#include <dune/stuff/la/container/interfaces.hh>

#include <dune/pymor/common/exceptions.hh>
#include <dune/pymor/common/crtp.hh>
#include <dune/pymor/parameters/base.hh>
#include <dune/pymor/parameters/functional.hh>


namespace Dune {
namespace Pymor {
namespace Tags {


class FunctionalInterface {};
class AffinelyDecomposedFunctionalInterface : public FunctionalInterface {};


} // namespace Tags


template< class Traits >
class FunctionalInterface
  : public CRTPInterface< FunctionalInterface< Traits >, Traits >
  , public Parametric
  , public Tags::FunctionalInterface
{
protected:
  typedef CRTPInterface< FunctionalInterface< Traits >, Traits > CRTP;
public:
  typedef typename Traits::derived_type derived_type;
  typedef typename Traits::SourceType   SourceType;
  typedef typename Traits::ScalarType   ScalarType;
  typedef typename Traits::FrozenType   FrozenType;

  static_assert(std::is_base_of< Stuff::LA::VectorInterface< typename SourceType::Traits >, SourceType >::value,
                "SourceType has to be derived from Stuff::LA::VectorInterface!");

  static std::string type_this() {    return Stuff::Common::Typename< derived_type >::value(); }
  static std::string type_source() {  return Stuff::Common::Typename< SourceType >::value(); }
  static std::string type_scalar() {  return Stuff::Common::Typename< ScalarType >::value(); }
  static std::string type_frozen() {  return Stuff::Common::Typename< FrozenType >::value(); }

  FunctionalInterface(const ParameterType mu = ParameterType())
    : Parametric(mu)
  {}

  FunctionalInterface(const Parametric& other)
    : Parametric(other)
  {}

  bool linear() const
  {
    CHECK_INTERFACE_IMPLEMENTATION(CRTP::as_imp(*this).linear());
    return CRTP::as_imp(*this).linear();
  }

  DUNE_STUFF_SSIZE_T dim_source() const
  {
    CHECK_INTERFACE_IMPLEMENTATION(CRTP::as_imp(*this).dim_source());
    return CRTP::as_imp(*this).dim_source();
  }

  ScalarType apply(const SourceType& source, const Parameter mu = Parameter()) const
  {
    CHECK_INTERFACE_IMPLEMENTATION(CRTP::as_imp(*this).apply(source, mu));
    return CRTP::as_imp(*this).apply(source, mu);
  }

  FrozenType freeze_parameter(const Parameter mu = Parameter()) const
  {
    CHECK_INTERFACE_IMPLEMENTATION(CRTP::as_imp(*this).freeze_parameter(mu));
    return CRTP::as_imp(*this).freeze_parameter(mu);
  }
}; // class FunctionalInterface


template< class Traits >
class AffinelyDecomposedFunctionalInterface
  : public CRTPInterface< AffinelyDecomposedFunctionalInterface< Traits >, Traits >
  , public FunctionalInterface< Traits >
  , public Tags::AffinelyDecomposedFunctionalInterface
{
  typedef CRTPInterface< AffinelyDecomposedFunctionalInterface< Traits >, Traits > CRTP;
  typedef Pymor::FunctionalInterface< Traits > BaseType;
public:
  typedef typename Traits::derived_type   derived_type;
  typedef typename Traits::ComponentType  ComponentType;
  static_assert(std::is_base_of< Pymor::FunctionalInterface< typename ComponentType::Traits >, ComponentType >::value,
                "ComponentType has to be derived from FunctionalInterface");

  AffinelyDecomposedFunctionalInterface(const ParameterType mu = ParameterType())
    : BaseType(mu)
  {}

  AffinelyDecomposedFunctionalInterface(const Parametric& other)
    : BaseType(other)
  {}

  DUNE_STUFF_SSIZE_T num_components() const
  {
    CHECK_INTERFACE_IMPLEMENTATION(CRTP::as_imp(*this).num_components());
    return CRTP::as_imp(*this).num_components();
  }

  ComponentType component(const int qq) const
  {
    CHECK_INTERFACE_IMPLEMENTATION(CRTP::as_imp(*this).component(qq));
    return CRTP::as_imp(*this).component(qq);
  }

  ParameterFunctional coefficient(const int qq) const
  {
    CHECK_INTERFACE_IMPLEMENTATION(CRTP::as_imp(*this).coefficient(qq));
    return CRTP::as_imp(*this).coefficient(qq);
  }

  bool has_affine_part() const
  {
    CHECK_INTERFACE_IMPLEMENTATION(CRTP::as_imp(*this).has_affine_part());
    return CRTP::as_imp(*this).has_affine_part();
  }

  ComponentType affine_part() const
  {
    CHECK_INTERFACE_IMPLEMENTATION(CRTP::as_imp(*this).affine_part());
    return CRTP::as_imp(*this).affine_part();
  }
}; // class AffinelyDecomposedFunctionalInterface


} // namespace Pymor
} // namespace Dune

#endif // DUNE_PYMOR_FUNCTIONALS_INTERFACES_HH
