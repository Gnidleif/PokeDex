#!/usr/bin/python3
from urllib.request import Request, urlopen
from html_table_parser import HTMLTableParser
import re, csv, os

class Pokemon:
    def __init__(self, num, name, types):
        self.Number = num
        self.Name = name
        self.Types = types

def fetchTable(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    web = urlopen(req).read().decode('UTF-8')
    p = HTMLTableParser()
    p.feed(web)
    return p.tables[0][1:]

def createPokemons(table):
    rgx = re.compile(r"^([\w\s\.']+)\s{2}(.+)$")
    pokemons = []
    for row in table:
        num = row[0].rjust(3, '0')
        name = row[1]
        types = row[2].split()
        match = rgx.match(row[1])
        if match:
            if match.group(1) in match.group(2):
                name = match.group(2)
            else:
                name = "{} {}".format(match.group(2), match.group(1))

        pokemons.append(Pokemon(num, name, types))
    return pokemons

def createTypes(table):
    types = {}
    keys = list(zip(*table))[0]
    values = list(zip(*table))[1:]
    keyVals = dict(zip(keys, values))
    for k in keyVals:
        keyVals[k] = dict(zip(keys, keyVals[k]))
        switch = {
            '': 1.0,
            '0': 0.0,
            '½': 0.5,
            '2': 2.0,
        }
        for l in keyVals[k]:
            keyVals[k][l] = switch[keyVals[k][l]]
        types[k] = keyVals[k]
    return types

def getTypeRelationships(pokemon, types):
    result = {}
    for t in pokemon.Types:
        row = types[t]
        for k in row:
            if k not in result:
                result[k] = row[k]
            else:
                result[k] *= row[k]
    return result

def writePokedex(pokemons, types, relationships):
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    with open(os.path.join(__location__, 'pokedex.csv'), 'w', newline='', encoding='utf-8') as f:
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
                'Number': pokemons[i].Number,
                'Name': pokemons[i].Name,
                'Type1': pokemons[i].Types[0],
                'Type2': pokemons[i].Types[1] if len(pokemons[i].Types) > 1 else '',
            }
            toWrite.update(relationships[i])
            writer.writerow(toWrite)

def readPokedex():
    pokemons = {}
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    with open(os.path.join(__location__, 'pokedex.csv'), 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = "{} {}".format(row['Number'], row['Name'])
            pokemons[key] = dict(row)
    return pokemons

def update():
    url = 'https://pokemondb.net/pokedex/all'
    table = fetchTable(url)
    pokemons = createPokemons(table)

    url = 'https://pokemondb.net/type'
    table = fetchTable(url)
    print(list(zip(*table))[0])
    types = createTypes(table)

    relationships = []
    for pokemon in pokemons:
        relationships.append(getTypeRelationships(pokemon, types))
    writePokedex(pokemons, types.keys(), relationships)

def compileStats(pokemon):
    return {
        'Number': pokemon['Number'],
        'Name': pokemon['Name'],
        'Type': "/".join(filter(None, [pokemon['Type1'], pokemon['Type2']])),
        'Immune': ','.join(filter(lambda x: pokemon[x] == '0.0', [x for x in pokemon])),
        'Quarter': ','.join(filter(lambda x: pokemon[x] == '0.25', [x for x in pokemon])),
        'Half': ','.join(filter(lambda x: pokemon[x] == '0.5', [x for x in pokemon])),
        'Double': ','.join(filter(lambda x: pokemon[x] == '2.0', [x for x in pokemon])),
        'Quadruple': ','.join(filter(lambda x: pokemon[x] == '4.0', [x for x in pokemon])),
    }

def main(args):
    if len(args) == 0:
        update()
        return
    search = " ".join(args)
    pokemons = readPokedex()
    rgx = re.compile(r".*{}.*".format(search), re.IGNORECASE)
    for key in pokemons:
        if rgx.match(key):
            print(compileStats(pokemons[key]))