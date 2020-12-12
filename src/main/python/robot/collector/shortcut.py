from robot.api import Collector, X
from typing import Any, Dict
from robot.collector import core

const = core.ConstCollector
as_text = core.AsTextCollector
text = core.TextCollector
attr = core.AttrCollector
css = core.CssCollector
pipe = core.PipeCollector
array = core.ArrayCollector
any = core.AnyCollector
default = core.DefaultCollector


def dict(*args: Collector[X, Dict[str, Any]], **kwargs: Collector[X, Any]) -> Collector[X, Dict[str, Any]]:
    return core.DictCollector(
        args,
        kwargs
    )
