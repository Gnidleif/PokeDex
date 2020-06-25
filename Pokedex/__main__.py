#!/usr/bin/python3
import os, csv, re
from pokedex import update

def readPokedex():
    pokemons = {}
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    with open(os.path.join(__location__, 'pokedex.csv'), 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = "{} {}".format(row['Number'], row['Name'])
            pokemons[key] = dict(row)
    return pokemons

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

if __name__ == "__main__":
    import sys
    main(sys.argv[1:])
