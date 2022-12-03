from __content.build_tree import visual_tree as build_tree

import pathlib


# example as folder explorer#

class folder:
    def __init__(self, path: pathlib.Path):
        self.path = path
    def __iter__(self): # extend source
        for i in self.path.iterdir():
            yield folder(i)
    def __str__(self): # content format
        return str(self.path.name)
    def __bool__(self): # validate source
        return self.path.is_dir()
    
    
folder_from = folder(pathlib.Path('.').absolute())
tree = build_tree(folder_from,max_depth=2)
tree()
""" result:
visual_tree
├──*sample.py
├──*__content
│  ├──*build_tree.py
│  ├──*component.py
│  └──*__pycache__
│     └──*...
└──*__init__.py
"""
######################


# example as data structure#
data = {
    'a': [1,2,3],
    'b': { 'c': 1, 'd': 2, 'e': 3 },
    'f': 'hello world',
    'g': (1,2,3),
    'h': 1,
    'i': None,
    'j': True}

from typing import Iterable
# interface between data structure and visual_tree
class interface: 
    def __init__(self, _data, _name = None):
        self.data = _data
        self.name = _name
        
    def __iter__(self): # extend source
        if isinstance(self.data, dict):
            for k,v in self.data.items():
                yield interface(v, k)
        elif isinstance(data,Iterable):
            for value in self.data:
                yield interface(value)
        else:
            print('not iterable')
            yield interface(self.data)
    
    def __str__(self) -> str: # content format
        if self.name is None:
            return str(self.data)
        if isinstance(self.data,Iterable) and not isinstance(self.data,str):
             return str(self.name)
        else:
            return f'{self.name} : {self.data}'


tree = build_tree(interface(data, 'data'),
                  # validate source if we not set __bool__ method in interface class
                  valid=lambda x: isinstance(x.data,Iterable) and not isinstance(x.data,str)
                  )
tree()
"""result:
data
├──*a
│  ├──*1
│  ├──*2
│  └──*3
├──*b
│  ├──*c : 1
│  ├──*d : 2
│  └──*e : 3
├──*f : hello world
├──*g
│  ├──*1
│  ├──*2
│  └──*3
├──*h : 1
├──*i : None
└──*j : True
"""