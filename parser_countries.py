from graph.polygon import Polygon
from collections import namedtuple
import re
Point = namedtuple('Point', 'x y')
reg_for_color = re.compile(r'color=#[\w\d]{6}')


class Parser:
    def __init__(self, countries):
        countries = countries.replace('"', '')
        self.countries = countries.split('},{')

    def _parse_countries(self):
        countries = dict()
        i = 0
        c = ''
        for country in self.countries:
            color = re.findall(reg_for_color, country)
            if len(color) != 0:
                c = color[0]
                country = country.replace(c+',', '')
            if c != '':
                countries[i] = list()
                countries[i].append(c)
                countries[i].append(country.replace('{', '').replace('}', ''))
            else:
                countries[i] = country.replace('{', '').replace('}', '')
            c = ''
            i += 1
        return countries

    def _parse_regions(self):
        countries = self._parse_countries()
        all_regions = dict()
        i = 0
        for country in countries:
            if isinstance(countries[country], list):
                country_regions = countries[country][1].split('],[')
            else:
                country_regions = countries[country].split('],[')
            for region in country_regions:
                all_regions[i] = region.replace('[', '').replace(']', '')
                i += 1
            if isinstance(countries[country], list):
                self.countries[country] = list()
                self.countries[country].append(countries[country][0])
                self.countries[country].append(all_regions.copy())
            else:
                self.countries[country] = all_regions.copy()
            i = 0
            all_regions = dict()

    def get_tree(self):
        self._parse_regions()
        for country in self.countries:
            if isinstance(country, list):
                sup_country = country[1]
            else:
                sup_country = country
            for region in sup_country:
                new_region = list()
                regs = sup_country[region].split('),(')
                for reg in regs:
                    r = reg.split(',')
                    new_region.append(Point(int(r[0]
                                                .replace('(', '')
                                                .replace(')', '')),
                                            int(r[1]
                                                .replace('(', '')
                                                .replace(')', ''))))
                if len(new_region) < 3:
                    raise ValueError('You should give three points for region')
                sup_country[region] = Polygon(new_region)
                if isinstance(country, list):
                    country[1] = sup_country.copy()
                else:
                    country = sup_country.copy()
        return self.countries
