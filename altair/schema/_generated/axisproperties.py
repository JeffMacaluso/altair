# This file auto-generated by altair.schema.parser.write_files().
# do not modify directly.

import traitlets as T
from ..baseobject import BaseObject
from .axisorient import AxisOrient


class AxisProperties(BaseObject):
    subdivide = T.CFloat(default_value=None, allow_none=True, help="""If provided, sets the number of minor ticks between major ticks (the value 9 results in decimal subdivision).""")
    tickSizeMinor = T.CFloat(default_value=None, allow_none=True, min=0, help="""The size, in pixels, of minor ticks.""")
    tickSizeEnd = T.CFloat(default_value=None, allow_none=True, min=0, help="""The size, in pixels, of end ticks.""")
    axisWidth = T.CFloat(default_value=None, allow_none=True, help="""Width of the axis line.""")
    orient = T.Instance(AxisOrient, default_value=None, allow_none=True, help="""The orientation of the axis.""")
    labelBaseline = T.Unicode(default_value=None, allow_none=True, help="""Text baseline for the label.""")
    titleOffset = T.CFloat(default_value=None, allow_none=True, help="""A title offset value for the axis.""")
    properties = T.Any(default_value=None, allow_none=True, help="""Optional mark property definitions for custom axis styling.""")
    tickSize = T.CFloat(default_value=None, allow_none=True, min=0, help="""The size, in pixels, of major, minor and end ticks.""")
    labels = T.Bool(default_value=None, allow_none=True, help="""Enable or disable labels.""")
    ticks = T.CFloat(default_value=None, allow_none=True, min=0, help="""A desired number of ticks, for axes visualizing quantitative scales.""")
    values = T.List(T.CFloat(default_value=None, allow_none=True), default_value=None, allow_none=True)
    title = T.Unicode(default_value=None, allow_none=True, help="""A title for the axis.""")
    layer = T.Unicode(default_value=None, allow_none=True, help="""A string indicating if the axis (and any gridlines) should be placed above or below the data marks.""")
    titleMaxLength = T.CFloat(default_value=None, allow_none=True, min=0, help="""Max length for axis title if the title is automatically generated from the field's description.""")
    labelAlign = T.Unicode(default_value=None, allow_none=True, help="""Text alignment for the Label.""")
    format = T.Unicode(default_value=None, allow_none=True, help="""The formatting pattern for axis labels.""")
    characterWidth = T.CFloat(default_value=None, allow_none=True, help="""Character width for automatically determining title max length.""")
    tickPadding = T.CFloat(default_value=None, allow_none=True, help="""The padding, in pixels, between ticks and text labels.""")
    labelAngle = T.CFloat(default_value=None, allow_none=True, help="""The rotation angle of the axis labels.""")
    labelMaxLength = T.CFloat(default_value=None, allow_none=True, min=1, help="""Truncate labels that are too long.""")
    offset = T.CFloat(default_value=None, allow_none=True, help="""The offset, in pixels, by which to displace the axis from the edge of the enclosing group or data rectangle.""")
    tickSizeMajor = T.CFloat(default_value=None, allow_none=True, min=0, help="""The size, in pixels, of major ticks.""")
    grid = T.Bool(default_value=None, allow_none=True, help="""A flag indicate if gridlines should be created in addition to ticks.""")
    shortTimeLabels = T.Bool(default_value=None, allow_none=True, help="""Whether month and day names should be abbreviated.""")
