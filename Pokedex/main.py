#!/usr/bin/python3
import os, csv, re

def readFromCsv():
    pokemons = {}
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    with open(os.path.join(__location__, 'poketypes.csv'), 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = "{} {}".format(row['Number'], row['Name'])
            pokemons[key] = dict(row)
    return pokemons

def compileStats(pokemon):
    return {
        'No': pokemon['Number'],
        'Name': pokemon['Name'],
        'Type': "/".join(filter(None, [pokemon['Type1'], pokemon['Type2']])),
        'Quarter': ', '.join(filter(lambda x: pokemon[x] == '0.25' and x != 'Number', [x for x in pokemon])),
        'Half': ', '.join(filter(lambda x: pokemon[x] == '0.5' and x != 'Number', [x for x in pokemon])),
        'Double': ', '.join(filter(lambda x: pokemon[x] == '2' and x != 'Number', [x for x in pokemon])),
        'Quadruple': ', '.join(filter(lambda x: pokemon[x] == '4' and x != 'Number', [x for x in pokemon])),
    }

def main(args):
    if len(args) == 0:
        return
    search = args[0]
    rgx = re.compile(r".*{}.*".format(search), re.IGNORECASE)
    pokemons = readFromCsv()
    for key in pokemons:
        if rgx.match(key):
            print(compileStats(pokemons[key]))

if __name__ == "__main__":
    import sys
    main(sys.argv[1:])