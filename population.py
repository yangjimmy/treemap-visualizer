"""Assignment 2: Modelling Population Data

=== CSC148 Fall 2016 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto

=== Module Description ===
This module contains a new class, PopulationTree, which is used to model
population data drawn from the World Bank API.
Even though this data has a fixed hierarchichal structure (only three levels:
world, region, and country), because we are able to model it using an
AbstractTree subclass, we can then run it through our treemap visualisation
tool to get a nice interactive graphical representation of this data.

NOTE: You'll need an Internet connection to access the World Bank API
to get started working on this assignment.

"""
import json
import urllib.request as request

from tree_data import AbstractTree


# Constants for the World Bank API urls.
WORLD_BANK_BASE = 'http://api.worldbank.org/countries'
WORLD_BANK_POPULATIONS = (
    WORLD_BANK_BASE +
    '/all/indicators/SP.POP.TOTL?format=json&date=2014:2014&per_page=270'
)
WORLD_BANK_REGIONS = (
    WORLD_BANK_BASE + '?format=json&date=2014:2014&per_page=310'
)


class PopulationTree(AbstractTree):
    """A tree representation of country population data.

    This tree always has three levels:
      - The root represents the entire world.
      - Each node in the second level is a region (defined by the World Bank).
      - Each node in the third level is a country.

    The data_size attribute corresponds to the 2014 population of the country,
    as reported by the World Bank.

    See https://datahelpdesk.worldbank.org/ for details about this API.
    """
    def __init__(self, world, root=None, subtrees=None, data_size=0):
        """Initialize a new PopulationTree.

        If <world> is True, then this tree is the root of the population tree,
        and it should load data from the World Bank API.
        In this case, none of the other parameters are used.

        If <world> is False, pass the other arguments directly to the superclass
        constructor. Do NOT load new data from the World Bank API.

        @type self: PopulationTree
            The population tree object to be initialized
        @type world: bool
            If the population tree to be initialized is the root (the world)
        @type root: object
            The name of the region or country
        @type subtrees: list[PopulationTree] | None
            The regions or countries
        @type data_size: int
            The population of the region or country
        """
        if world:
            region_trees = _load_data()
            AbstractTree.__init__(self, 'World', region_trees)
        else:
            if subtrees is None:
                subtrees = []
            AbstractTree.__init__(self, root, subtrees, data_size)

    def get_separator(self):
        """
        @type self: PopulationTree
            The population tree object which to return the information of
        @rtype: str
            The region, name and population of the country
        """
        s = ''
        if self.is_empty():
            s = ''
        elif self._parent_tree is None and self._subtrees == []:
            s = self._root
        elif self._parent_tree is not None and self._subtrees == []:
            s = 'World' + '/' + self._parent_tree.get_root() + '/' + self._root
        elif self._parent_tree is not None and self._subtrees != []:
            s = self._parent_tree.get_root + self._root()
        else:
            s = ''
        return s


def _load_data():
    """Create a list of trees corresponding to different world regions.

    Each tree consists of a root node -- the region -- attached to one or
    more leaves -- the countries in that region.

    @rtype: list[PopulationTree]
        List of trees that correspond to the world's regions
    """
    # Get data from World Bank API.
    country_populations = _get_population_data()
    regions = _get_region_data()

    # Be sure to read the docstring of the PopulationTree constructor to see
    # how to call it.
    # You'll want to complete the two helpers called above first (otherwise
    # this function won't run).
    # You can complete this function *without* using recursion.
    # Remember that each region tree has only two levels:
    #   - a root storing the name of the region
    #   - zero or more leaves, each representing a country in the region

    regions_list = []
    for r in regions:
        countries_list = []
        for c in regions[r]:
            if c in country_populations:
                countries_list += [PopulationTree(False, c, None,
                                                  country_populations[c])]
        regions_list += [PopulationTree(False, r, countries_list)]
    # for i in regions_list:
    #     print(i._root + ',' + str(i.data_size))
    #     for j in i._subtrees:
    #         print('     ' + str(j._root) + ' ' + str(j.data_size))
    return regions_list


def _get_population_data():
    """Return country population data from the World Bank.

    The return value is a dictionary, where the keys are country names,
    and the values are the corresponding populations of those countries.

    Ignore all countries that do not have any population data,
    or population data that cannot be read as an int.

    @rtype: dict[str, int]
        The countries with their respective populations
    """
    # The first element returned is ignored because it's just metadata.
    # The second element's first 47 elements are ignored because they aren't
    # countries.
    _, population_data = _get_json_data(WORLD_BANK_POPULATIONS)
    population_data = population_data[47:]

    countries = {}

    for i in range(0, len(population_data)):
        # find countries
        # find populations
        country = population_data[i]['country']['value']
        population = population_data[i]['value']
        try:
            population = int(population)
            countries[country] = population
        except TypeError:
            # when it's None
            pass

    return countries


def _get_region_data():
    """Return country region data from the World Bank.

    The return value is a dictionary, where the keys are region names,
    and the values a list of country names contained in that region.

    Ignore all regions that do not contain any countries.

    @rtype: dict[str, list[str]]
        The world's region with its contained countries
    """
    # We ignore the first component of the returned JSON, which is metadata.
    _, country_data = _get_json_data(WORLD_BANK_REGIONS)

    regions = {}

    for i in range(0, len(country_data)):
        region = country_data[i]['region']['value']
        country = country_data[i]['name']
        if country is not None:
            if region not in regions:
                # create the dictionary key
                regions[region] = []
            # add the country to the list of countries of that region
            regions[region].append(country)

    return regions


def _get_json_data(url):
    """Return a dictionary representing the JSON response from the given url.

    You should not modify this function.

    @type url: str
    @rtype: Dict
    """
    response = request.urlopen(url)
    return json.loads(response.read().decode())

# Helpers for AbstractTree ===================================================


def extract_nested(nested_lst):
    """
    Extract a list from a nested list. Does not mutate the original list
    @type nested_lst: list[object|list]
        List to be flattened out
    @rtype: list[object]
        Flattened list (non-nested)
    """
    if not isinstance(nested_lst, list):
        return nested_lst
    else:
        lst = []
        for i in range(0, len(nested_lst)):
            if isinstance(nested_lst[i], list):
                lst += extract_nested(nested_lst[i])
            else:
                lst += [nested_lst[i]]
        return lst

# ============================================================================

if __name__ == '__main__':
    import python_ta
    # Remember to change this to check_all when cleaning up your code.
    python_ta.check_errors(config='pylintrc.txt')
    python_ta.check_all(config='pylintrc.txt')
