from pathlib import Path
from visual_tree.VisualTree import VisualTree

tree = VisualTree(
    root=Path('.'),
    root_validator=Path.is_dir,
    root_extend_func=Path.iterdir,
    naming_child=lambda x: x.name)

tree.report()
""" result:
.
├──── build
│     └──── bdist.win-amd64
├──── dist
│     ├──── visual-tree-0.0.2.tar.gz
│     └──── visual_tree-0.0.2-py3-none-any.whl
├──── example.py
├──── LICENSE
├──── README.md
├──── setup.py
├──── VisualTree.py
├──── visual_tree
├──── visual_tree.egg-info
│     ├──── dependency_links.txt
│     ├──── PKG-INFO
│     ├──── SOURCES.txt
│     └──── top_level.txt
├──── __init__.py
└──── __pycache__
      └──── VisualTree.cpython-310.pyc
"""
######################


# example as data structure#
from typing import Iterable

data = {
    'a': [1,2,3],
    'b': { 'c': 1, 'd': 2, 'e': 3 },
    'f': 'hello world',
    'g': (1,2,3),
    'h': 1,
    'i': None,
    'j': True}

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


tree = VisualTree(interface(data, 'data'),
                  # validate source if we not set __bool__ method in interface class
                  root_validator=lambda x: isinstance(x.data,Iterable) and not isinstance(x.data,str)
                  )
tree.report()
"""result:
data
├──── a
│     ├──── 1
│     ├──── 2
│     └──── 3
├──── b
│     ├──── c : 1
│     ├──── d : 2
│     └──── e : 3
├──── f : hello world
├──── g
│     ├──── 1
│     ├──── 2
│     └──── 3
├──── h : 1
├──── i : None
└──── j : True
"""