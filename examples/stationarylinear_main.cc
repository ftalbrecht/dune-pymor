// This file is part of the dune-pymor project:
//   https://github.com/pymor/dune-pymor
// Copyright holders: Stephan Rave, Felix Schindler
// License: BSD 2-Clause License (http://opensource.org/licenses/BSD-2-Clause)

#include "config.h"

#include <boost/exception/exception.hpp>

#include <dune/stuff/common/color.hh>

#include <dune/pymor/common/exceptions.hh>

#include "stationarylinear.hh"
#include <dune/stuff/common/reenable_warnings.hh>

using namespace Dune;
using namespace Dune::Pymor;

int main(int /*argc*/, char** /*argv*/)
{
  try {
    std::cout << "creating analytical problem... ";
    const Example::AnalyticalProblem* problem = new Example::AnalyticalProblem();
    std::cout << "done" << std::endl;

    std::cout << "discretizing... ";
    Example::SimpleDiscretization discretization(problem);
    std::cout << "done" << std::endl;

    const auto lhsOperator = discretization.get_operator();
    std::cout << "parameter_type of the left hand side is:\n  " << lhsOperator.parameter_type() << std::endl;

    const auto rhsFunctional = discretization.get_rhs();
    std::cout << "parameter_type of the right hand side is:\n  " << rhsFunctional.parameter_type() << std::endl;

    Dune::Pymor::Parameter mu = {{"diffusion", "dirichlet",  "force",      "neumann"},
                                {{1, 1, 1, 1}, {1, 1, 1, 1}, {1, 1, 1, 1}, {1, 1, 1, 1}}};
    std::cout << "solving for mu = " << mu << "... ";
    auto solution = discretization.create_vector();
    discretization.solve(solution, mu);
    std::cout << "done" << std::endl;

    const std::string filename = "solution.txt";
    std::cout << "writing solution to '" << filename << "'... ";
    discretization.visualize(solution, filename, "solution");
    std::cout << "done" << std::endl;

    // if we came that far, we can as well be happy about it
    return EXIT_SUCCESS;
  } catch (Dune::Exception& e) {
    std::cerr << "Dune reported error: " << e << std::endl;
  } catch (boost::exception& e) {
    std::cerr << "boost reported error! " << std::endl;
  } catch (std::exception& e) {
    std::cerr << "stl reported error: " << e.what() << std::endl;
  } catch (...) {
    std::cerr << "Unknown exception thrown!" << std::endl;
  }
  return EXIT_FAILURE;
}
