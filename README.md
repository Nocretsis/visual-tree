# Visual Tree Python Package

## Introduction

this is a simple tool to visualize the tree structure of any recursable object in python.

## Installation

```bash
pip install visual-tree
```

## Usage

```python
from visual_tree import VisualTree
tree = VisualTree(
    root=6,
    root_validator=lambda x: x > 1 and not x%2,
    root_extend_func=lambda x: range(x))

# print the tree
tree.report()

# print the tree directly
print(tree.daily())

# get the tree as a list of strings
list_of_tree = tree.growing()
```
result
```Python result
6
├──── 0
├──── 1
├──── 2
│     ├──── 0
│     └──── 1
├──── 3
├──── 4
│     ├──── 0
│     ├──── 1
│     ├──── 2
│     │     ├──── 0
│     │     └──── 1
│     └──── 3
└──── 5
```

## Example

look at the [example.py](./example.py) file for more examples.

## License

Apache License 2.0 (see [LICENSE](./LICENSE) file)
