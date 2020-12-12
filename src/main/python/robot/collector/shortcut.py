from robot.api import Collector, I
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


def dict(*args: Collector[I, Dict[str, Any]], **kwargs: Collector[I, Any]) -> Collector[I, Dict[str, Any]]:
    return core.DictCollector(
        args,
        kwargs
    )
