import random
from typing import List, Any, TypeVar, Callable, Type, cast
from flask.views import MethodView
# from .dice.stringDie import stringDie
# Toggle Testing
testing = True
# testing = False
T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


class TableElement:
    name: str
    source: str
    page: int
    colStyles: List[str]
    colLabels: List[str]
    rows: List[List[str]]

    def __init__(self, name, source, page, colStyles, colLabels, rows, *args):
        self.name = name
        self.source = source
        self.page = page
        self.rollable = self.testStringforDie(colLabels[0])
        self.colLabels = colLabels
        if self.rollable:
            print("Table %s is rollable" % self.name)
            self.rows = []
            for row in rows:
                first = row[0].split("\u2013")
                if all([f.isnumeric() for f in first]) and len(first) == 2:
                    print(row, first, int(first[0]), int(first[1])+1)
                    for x in range(int(first[0]), int(first[1])+1):
                        t = [r for r in row]
                        t[0] = str(x)
                        self.rows.append(t)
                else:
                    print("Table %s isn't rollable" % self.name)
                    self.rows.append(row)
        else:
            self.rows = rows

        self.colStyles = colStyles

    def __getitem__(self, index):
        return self.rows[index]

    def __len__(self, index):
        return len(self.rows)

    def from_dict(obj: Any) -> 'TableElement':
        assert isinstance(obj, dict)
        name = from_str(obj.get("name"))
        source = from_str(obj.get("source"))
        page = from_int(obj.get("page"))
        colLabels = from_list(from_str, obj.get("colLabels"))
        rows = from_list(lambda x: from_list(from_str, x), obj.get("rows"))
        firstCol = [all([x.isnumeric() for x in r[0].split('\u2013')]) for r in rows]
        if all(firstCol):
            print("Number Table")
        if obj.get("colStyles"):
            colStyles = from_list(from_str, obj.get("colStyles"))
        else:
            maxrows = max([len(r) for r in rows])
            tempStyles = [[] for _ in range(maxrows)]
            for r in rows:
                for i,x in enumerate(r):
                    tempStyles[i].append(len(x))
            tempCol = [max(r) for r in tempStyles]
            colStyles = ["col-%d" %round(12*d/sum(tempCol)) for d in tempCol]
        return TableElement(name, source, page, colStyles, colLabels, rows)

    # def __dict__(self) -> dict:
    #     result: dict = {}
    #     result["name"] = from_str(self.name)
    #     result["source"] = from_str(self.source)
    #     result["page"] = from_int(self.page)
    #     result["colStyles"] = from_list(from_str, self.colStyles)
    #     result["colLabels"] = from_list(from_str, self.colLabels)
    #     result["rows"] = from_list(lambda x: from_list(from_str, x), self.rows)
    #     return result

    def testStringforDie(self, s):
        s = s.replace(' ','')
        print()
        print(s)
        sym = '+-*/'
        inequ = '<>='
        rerolls = [
            'dl',  # drop lowest
            'kl',  # keep lowest
            'kh',  # keep highest
            'dh',  # drop highest
            'r',   # reroll
            'ro',  # reroll
            'e',    # explode
            ' ',
            ';',
        ]
        obr = '{(['
        cbr = '})]'
        o = []
        for a in [cbr, obr, rerolls, sym, inequ, 'd']:
            t = list(a)
            o.extend(list(t))
        print(o)
        # o = ['}', ')', '{', '(', 'dl', 'kl', 'kh', 'dh', 'r', 'ro', 'e ', ';', '+', '-', '*', '/', '<', '>', '=', 'd']
        i = 0
        passes = 8 + len(s)
        while i < len(s) and passes > 0:
            passes -= 1
            if s[i].isnumeric():
                print(s[i], end='')
                i += 1
                continue
            elif i < len(s)-1:
                for k in range(2,0,-1):
                    if s[i:i+k] in o:
                        print(s[i:i+k], end='')
                        i += k
                        break

            elif i == len(s)-1:
                print('|', end='')
                if s[i] in o:
                    print(s[i], end='')
                    i += 1
                    continue
                else:
                    break
            else:
                break
        print('', len(s), i, )
        return i == len(s)



def tablefromdict(s: Any) -> List[TableElement]:
    return from_list(TableElement.from_dict, s)


def tabletodict(x: List[TableElement]) -> Any:
    return from_list(lambda x: to_class(TableElement, x), x)


def jsonWrite(name, data):
    filename = 'Saved Files/{}.json'.format(name)
    with open(filename, 'w') as json_file:
        json.dump(data, json_file)

def jsonRead(name):
    filename = 'Saved Files/{}.json'.format(name)
    with open(filename, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    return data


class TableRoller(MethodView):
    def get(self, id="", roll=""):
        # req_data = request.get_json()

        print("Get ID", id)
        if id == "":
            pass# return jsonify(global_history.history)
        elif roll == "":
            retrun
        else:
            return ()
        #     return jsonify(global_history.history.get(id))

    def options(self):
        print("Option:", request.get_json())
        return jsonify(0)

    def post(self):
        # console.log()
        req_data = request.get_json()
        # if isinstance(req_data['string'], list):
        #     id = [global_history.rollDie(s) for s in req_data['string']]
        # elif isinstance(req_data['string'], str):
        #     id = global_history.rollDie(req_data['string'])
        # s = stringDie(id)
        #     s.total()
        #     id = len(global_history.history)+1
        #     d = {'die':s.toDict(), 'id':id}
        #     global_history.history[id] = d
        #     return jsonify(d)
        print("Request Data", req_data)

        # jsonWrite("history", global_history.history)
        # print(id)
        # return jsonify(id)

if testing:
    test = {
        "name": "Ooze Rest Ambush",
        "source": "MPOSource",
        "page": 1,
        "colStyles": ["col-2 text-center", "col-10"],
        "colLabels": ["1d10", "Encounter"],
        "rows": [
            ["1", "1 Black Pudding"],
            ["2\u20133", "1d6 Gray Ooze"],
            ["4", "1d3 Psychic Grey Ooze"],
            ["5", "1 Slithering Tracker"],
            ["6\u20137", "1d3 Ochre Jelly"],
            ["8\u201310", "1d6 Ooblex Spawn"]
        ]
    }

    k = TableElement.from_dict(test)
    print(k.__dict__)

    test = [
            '{2d20; 10}kh1',
            '{2d20}+5',
            '{6d20}kh2',
            '{6d20}dh2',
            '{6d20}kl2',
            '{6d20}dl2',
            '2d20-1d4',
            '2d20kh1',
            '5',
            '6*2d20',
            '2d10/2',
            '6d4kh(1d4)',
            '{100d100; 5d2000}kh1',
            '4d6e3',
            '5d6r<=5',
            '5d6ro>=3',
            '1d20+4>=10',
            '2d20kh1+5>=10'
        ]
    a = 'abcdefg'
    print(a, a[1:2], a[1:3])
    [print(k.testStringforDie(s)) for s in test]
    # [print(s) for s in range(2,0,-1)]
