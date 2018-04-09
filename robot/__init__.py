__version__ = (0, 0, 4)

try:
    from .core import CollectorFactory
    from .core import Robot
except ImportError:
    pass
