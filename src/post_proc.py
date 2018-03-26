import pickle
import re
import sys

DEPT = sys.argv[-1] or 'amath'

code_re = re.compile('([A-Z][A-Z ]{2,5} [0-9]{3})')
find_class = lambda x: code_re.findall(x)
f  = lambda func: (
        lambda x: (
            func(x) and (
                tuple( i.strip()[:-3].strip()+i.strip()[-3:] for i in find_class(func(x).group(1)) ) \
                or None
            )
        )
     )

prereq = f(lambda x: re.search('Prerequisite: (.*?)\.?( Offered: |\Z)', x['description']))
joint  = f(lambda x: re.search('Offered: (.*?)\.?\Z', x['description']))

_get_items = lambda x: {'jointly': joint(x), 'prereq': prereq(x)}.items()
get_items= lambda x: tuple(filter(lambda e: e[1], _get_items(x)))

link_classes = lambda x: code_re.sub(lambda i: "[[{0}|{1}]]".format(i.group(), i.group()[:-4] +i.group()[-3:]), x)

data  = pickle.load(open('out/p/{}.p'.format(DEPT), 'rb'))
desc  = [{'description': link_classes(d['description'])} for d in data]
data  = [ dict( tuple(a.items()) + tuple(b.items()) ) for a, b in zip(data, desc) ]

meta_items = map(get_items, data)
data_items = [tuple(e.items()) for e in data]
data = [ dict(d+m) for d, m in zip(data_items, meta_items) ]

pickle.dump(data, open('out/p/{}.p'.format(DEPT), 'wb'))
