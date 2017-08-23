__version__ = (0, 0, 1)

try:
    from .core import CollectorFactory
    from .core import Robot
except ImportError:
    pass
