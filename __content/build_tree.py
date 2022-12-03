from enum import Enum
from .component import DISPLAY_PREFIX
from typing import Union

def check_DISPLAY_PREFIX(_cls: Union[Enum,DISPLAY_PREFIX]):
    """check if prefix is a valid DISPLAY_PREFIX

    Args:
        prefix (DISPLAY_PREFIX): prefix to be checked

    Returns:
        bool: True if prefix is a valid DISPLAY_PREFIX
    """
    if _cls is DISPLAY_PREFIX:
        return
    
    if not isinstance(_cls, Enum):
        raise TypeError(f'prefix must be an Enum, not {_cls.__class__.__name__}')
    
    # check member of DISPLAY_PREFIX
    try:
        _cls.node_middle.value
        _cls.node_last.value
        _cls.root_middle.value
        _cls.root_last.value
    except AttributeError as e:
        raise ValueError(f'prefix must be a DISPLAY_PREFIX, not {_cls.__class__.__name__}') from e

class visual_tree:
    """visual tree builder
        Usage: 
            >>> import _this_
            >>> tree = _this_.build_tree(src)
            
        ### get tree as multiline string
            >>> tree.tree
            
        ### get tree as list of lines or generator
            >>> list(tree)
            or
            >>> for line in tree:
            >>>     print(line)
            
        ### print tree directly
            >>> tree()
            
        ### get number of children
            >>> len(tree)
            
        ### get source string
            >>> str(tree)
            
        compulsory args:
            * src: source of tree
            
        optional args:
            * mkchild: extenting function of source (default: src.__iter__)
            * valid: validate function of source (default: src.__bool__)
            * formator: prefix format of tree (default: DISPLAY_PREFIX)
            
        display prefix formator is an Enum with 4 members:
            - node_middle: prefix of node in middle of tree (default: '├──*')
            - node_last: prefix of node in last of tree     (default: '└──*')
            - root_middle: prefix of root in middle of tree (default: '   ')
            - root_last: prefix of root in last of tree     (default: '│  ')
            
        optional kwargs: (only use when you know what you are doing)
            * max_depth: max depth of tree, if not provided, will expand to the end
            * show_max_remain: if reached max_depth, show '...' (default: True)
            
        hidden args: (you should not use these arguments)
            * display_prefix_str: previous prefix of tree (should be left empty) (default: '')
            * checked_DISPLAY_PREFIX: if False, will check if display_prefix is a valid DISPLAY_PREFIX (should be left empty) (default: False)
            * is_last: None-> will set nothing, True-> will set to last, False-> will set to middle (should be left empty) (default: None)
            
        """
    def __init__(self, source,
                 mkchild=None, valid=None, formator=DISPLAY_PREFIX,
                 **kwargs):
        self.__source = source
        
        # extend source method 
        self.__extend_source = mkchild
        if self.__extend_source is None:
            if not hasattr(self.__source, '__iter__'):
                raise TypeError(f'source must be iterable if extent method is not provided')
        elif not callable(self.__extend_source):
            raise TypeError(f'extent must be a callable')
        
        # validate source is iterable
        self.__validate_source = valid
        if self.__validate_source is None:
            if not hasattr(self.__source, '__bool__'):
                raise TypeError(f'source must be boolable if validate method is not provided')
        elif not callable(self.__validate_source):
            raise TypeError(f'validate must be a callable')
        
        # display prefix enum
        self.__display_prefix = formator
        if kwargs.get('checked_DISPLAY_PREFIX', False):
            check_DISPLAY_PREFIX(self.__display_prefix)
            
        # max depth
        self.__max_depth = kwargs.get('max_depth')
        
        # show max remain
        self.__show_max_remain = kwargs.get('show_max_remain', True)
            
        # display prefix in string
        self.__display_prefix_str = kwargs.get('display_prefix_str', '')
        
        # is last child
        self.__is_last = kwargs.get('is_last')
        

        
    def __str__(self):
        return str(self.__source)
    
    def __iter__(self):
        # return tree as generator
        if self.__is_last is None:
            yield f'{self.__display_prefix_str}{self.__source}'
        else:
            prefix = self.__display_prefix.node_last.value if self.__is_last else self.__display_prefix.node_middle.value
            yield f'{self.__display_prefix_str}{prefix}{self.__source}'
            
        next_depth = None if self.__max_depth is None else self.__max_depth - 1
        if not bool(self):
            return
        
        numc = len(self)
        generator_ = enumerate(self.__source) if self.__extend_source is None else enumerate(self.__extend_source(self.__source))
        
        if self.__is_last is None:
            prefix = ''
        else:
            prefix = self.__display_prefix.root_last.value if self.__is_last else self.__display_prefix.root_middle.value
            
        if self.__max_depth is not None and self.__max_depth <= 0:
            if self.__show_max_remain:
                yield f'{self.__display_prefix_str}{prefix}{DISPLAY_PREFIX.node_last.value}...'
            return
    
        for idx,child in generator_:
            yield from visual_tree(
                source=child,
                mkchild=self.__extend_source,
                valid=self.__validate_source,
                format=self.__display_prefix,
                max_depth=next_depth,
                show_max_remain=self.__show_max_remain,
                
                display_prefix_str=self.__display_prefix_str + prefix,
                checked_DISPLAY_PREFIX=True,
                is_last=(idx == numc-1),

            )
            
    def __repr__(self):
        return f'visual_tree({self.__source})'
    
    def __call__(self):
        # print tree
        for line in iter(self):
            print(line)
            
    def __len__(self):
        try :
            return len(self.__source)
        except TypeError:
            if self.__extend_source is None:
                return len(list(self.__source))
            return len(list(self.__extend_source(self.__source)))
        except Exception as e:
            raise e
        
    def __bool__(self):
        if self.__validate_source is None:
            return self.__source.__bool__()
        return self.__validate_source(self.__source)
        
    @property
    def tree(self):
        return '\n'.join(self.__iter__())
            