if __name__ == '__main__':
    print('this is a module')
    print('do not run this file directly')
    exit(1)
from .__content.build_tree import visual_tree as build_tree
from .__content.component import DISPLAY_PREFIX

__all__ = ['build_tree', 'DISPLAY_PREFIX']

__version__ = '0.0.1'