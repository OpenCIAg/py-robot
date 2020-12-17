import logging
from dataclasses import dataclass, field
from logging import Logger

from robot.api import Collector, XmlNode, Context

__logger__ = logging.getLogger(__name__)


@dataclass()
class CssCollector(Collector[XmlNode, XmlNode]):
    css_selector: str
    logger: Logger = field(default=__logger__, compare=False)

    async def __call__(self, context: Context, item: XmlNode) -> XmlNode:
        return item.find_by_css(self.css_selector)
