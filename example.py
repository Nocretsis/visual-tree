from pathlib import Path
from visual_tree.VisualTree import VisualTree

tree = VisualTree(
    root=Path('.').absolute(),
    root_validator=Path.is_dir,
    root_extend_func=Path.iterdir,
    naming_child=lambda x: x.name)

tree.report()
""" result:
visual_tree
├──── .gitignore
├──── build
│     ├──── bdist.win-amd64
│     └──── lib
│           └──── visual_tree
│                 ├──── VisualTree.py
│                 └──── __init__.py
├──── example.py
├──── LICENSE
├──── visual_tree
│     ├──── VisualTree.py
│     ├──── __init__.py
│     └──── __pycache__
│           ├──── VisualTree.cpython-310.pyc
│           └──── __init__.cpython-310.pyc
└──── README.md
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
            return repr(self.data)
        if isinstance(self.data,Iterable) and not isinstance(self.data,str):
             return repr(self.name)
        else:
            return f'{repr(self.name)} : {repr(self.data)}'
        
    def __bool__(self): # validate source
        return isinstance(self.data,Iterable) and not isinstance(self.data,str)


tree = VisualTree(interface(data, 'data'),
                  # extend source if we set __iter__ method in interface class
                  # root_extend_func=...
                  
                  # content format if we set __str__ method in interface class
                  # naming=...
            
                  root_validator=interface.__bool__,
                  )
tree.report()
"""result:
'data'
├──── 'a'
│     ├──── 1
│     ├──── 2
│     └──── 3
├──── 'b'
│     ├──── 'c' : 1
│     ├──── 'd' : 2
│     └──── 'e' : 3
├──── 'f' : 'hello world'
├──── 'g'
│     ├──── 1
│     ├──── 2
│     └──── 3
├──── 'h' : 1
├──── 'i' : None
└──── 'j' : True
"""