#!/usr/bin/python3
from urllib.request import Request, urlopen
from html_table_parser import HTMLTableParser
from pokedex import Pokemon, updatePokemons
import re, csv, os

def fetchTypeTable(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    web = urlopen(req).read().decode('UTF-8')
    p = HTMLTableParser()
    p.feed(web)
    return p.tables[0][1:]

def createTypes(table):
    poketypes = {}
    keys = list(zip(*table))[0]
    values = list(zip(*table))[1:]
    test = dict(zip(keys, values))
    for k in test:
        test[k] = dict(zip(keys, test[k]))
        switch = {
            '': 1.0,
            '0': 0.0,
            '½': 0.5,
            '2': 2.0,
        }
        for l in test[k]:
            test[k][l] = switch[test[k][l]]
        poketypes[k] = test[k]
    return poketypes

def readFromCsv():
    pokemons = []
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    with open(os.path.join(__location__, 'pokemon.csv'), 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            types = [row['type1']]
            if row['type2'] != '':
                types.append(row['type2'])
            pokemons.append(Pokemon(row['number'], row['name'], types))
    return pokemons

def getTypeRelationships(pokemon, poketypes):
    result = {}
    for t in pokemon._types:
        row = poketypes[t]
        for k in row:
            if k not in result:
                result[k] = row[k]
            else:
                result[k] *= row[k]
    return result

def writeToCsv(pokemons, types, relationships):
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    with open(os.path.join(__location__, 'poketypes.csv'), 'w', newline='', encoding='utf-8') as f:
        fieldnames = [
            'Number', 
            'Name', 
            'Type1', 
            'Type2', 
        ]
        fieldnames.extend(types)
        writer = csv.DictWriter(f, fieldnames = fieldnames)
        writer.writeheader()
        for i in range(len(pokemons)):
            toWrite = {
                'Number': pokemons[i]._num,
                'Name': pokemons[i]._name,
                'Type1': pokemons[i]._types[0],
                'Type2': pokemons[i]._types[1] if len(pokemons[i]._types) > 1 else '',
            }
            toWrite.update(relationships[i])
            writer.writerow(toWrite)

def update():
    updatePokemons()
    url = 'https://pokemondb.net/type'
    t = fetchTypeTable(url)
    poketypes = createTypes(t)
    pokemons = readFromCsv()
    relationships = []
    for i in range(len(pokemons)):
        relationships.append(getTypeRelationships(pokemons[i], poketypes))

    writeToCsv(pokemons, poketypes.keys(), relationships)