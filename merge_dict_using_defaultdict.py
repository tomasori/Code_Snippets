'''Merge two or more dictionaries.
   For similar keys, values are combined into a list.
   Non similar keys, individual value is put into list.'''

from collections import defaultdict

d1 = {'a': 'x', 'b': 'y', 'c': 'z'}
d2 = {'a': 'j', 'c': 'z', 'z': 'aa'}
d3 = {'a': 3, 'b': 1, 'C': 'aa', 'Z': 4, 7 : "yyy"}

dd = defaultdict(list)
for d in (d1, d2, d3): # you can list as many input dicts as you want here
    for key, value in d.items():
        # dd[key].append(value)
        dd[key].append(value)

new_d = dict(dd)    # convert from a collection.defaultdict class to a dict()

for key in new_d:
    print('{} : {}'.format(key, new_d[key]))

# import pprint
# pp = pprint.PrettyPrinter(indent=3)
# pp.pprint(new_d)
