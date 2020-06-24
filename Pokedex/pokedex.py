#!/usr/bin/python3
from urllib.request import Request, urlopen
from html_table_parser import HTMLTableParser
import re, csv, os

class Pokemon:
    def __init__(self, num, name, types):
        self._num = num
        self._name = name
        self._types = types

    def __repr__(self):
        return "#{}: {} - {}".format(self._num, self._name, self._types)

def fetchPokemonTable(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    web = urlopen(req).read()
    webstr = web.decode('utf-8')
    p = HTMLTableParser()
    p.feed(webstr)
    return p.tables[0][1:]

def createPokemons(rows):
    pokemons = []
    for row in rows:
        num = row[0].rjust(3, '0')
        name = row[1]
        types = row[2].split()
        rgx = re.compile(r"^(\w+)\s{2}(.+)$")
        m = rgx.match(row[1])
        if m:
            name = "{} ({})".format(m.group(1), m.group(2))
        pokemons.append(Pokemon(num, name, types))
    return pokemons

def writeToCsv(pokemons):
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    with open(os.path.join(__location__, 'pokemon.csv'), 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['number', 'name', 'type1', 'type2']
        writer = csv.DictWriter(f, fieldnames = fieldnames)
        writer.writeheader()
        for row in pokemons:
            writer.writerow({'number': row._num, 'name': row._name, 'type1': row._types[0], 'type2': row._types[1] if len(row._types) > 1 else ''})

def updatePokemons():
    url = 'https://pokemondb.net/pokedex/all'
    web = fetchPokemonTable(url)
    pokemons = createPokemons(web)
    writeToCsv(pokemons)