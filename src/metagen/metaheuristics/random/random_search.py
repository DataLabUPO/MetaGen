"""
    Copyright (C) 2023 David Gutierrez Avilés and Manuel Jesús Jiménez Navarro

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from copy import deepcopy
from typing import Callable, List

from metagen.framework import Domain, Solution


class RandomSearch:

    """
    RandomSearch is a class for performing a random search optimization algorithm.

    It generates and evaluates random solutions in a search space to find an optimal solution.

    :param domain: The search domain that defines the solution space.
    :type domain: Domain
    :param fitness: The fitness function used to evaluate solutions.
    :type fitness: Callable[[Solution], float]
    :param search_space_size: The size of the search space. Default is 30.
    :type search_space_size: int, optional
    :param iterations: The number of optimization iterations. Default is 20.
    :type iterations: int, optional

    **Code example**

    .. code-block:: python

        from metagen.framework import Domain
        from metagen.metaheuristics import RandomSearch
        
        domain = Domain()

        domain.defineInteger(0, 1)

        fitness_function = ...

        search = RandomSearch(domain, fitness_function, search_space_size=50, iterations=100)
        optimal_solution = search.run()

    """

    def __init__(self, domain: Domain, fitness: Callable[[Solution], float], search_space_size: int = 30,
                 iterations: int = 20) -> None:

        self.domain = domain
        self.fitness = fitness
        self.search_space_size = search_space_size
        self.iterations = iterations

    def run(self) -> Solution:
        """
        Run the random search optimization algorithm.

        This method generates and evaluates random solutions in the search space to find an optimal solution.

        :return: The optimal solution found.
        :rtype: Solution
        """

        potential_solutions: List[Solution] = list()
        solution_type: type[Solution] = self.domain.get_connector().get_type(
            self.domain.get_core())
        
        for _ in range(0, self.search_space_size):
            potential_solutions.append(solution_type(
                self.domain, connector=self.domain.get_connector()))
        solution: Solution = deepcopy(min(potential_solutions))

        for _ in range(0, self.iterations):
            for ps in potential_solutions:
                ps.mutate()
                ps.evaluate(self.fitness)
                if ps < solution:
                    solution = deepcopy(ps)

        return solution
