from enum import Enum

class DISPLAY_PREFIX(Enum):
    """prefix for display"""
    node_middle = '├──*'
    node_last = '└──*'
    root_last = '   '
    root_middle = '│  '
    
