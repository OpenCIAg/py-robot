__version__ = (0, 0, 3)

try:
    from .core import CollectorFactory
    from .core import Robot
except ImportError:
    pass
