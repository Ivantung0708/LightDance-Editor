from dataclasses import dataclass
from typing import Dict, List, Tuple, Union

from dataclass_wizard import JSONWizard
from gql import gql

from ..core.models import ID, RGB, ColorID, ColorName

"""
Fiber
"""

QueryFiberDataPayload = Tuple[ColorID, int]

"""
LED
"""

QueryLEDDataPayload = Tuple[ColorID, int]


"""
Dancer
"""


QueryDancerStatusPayloadItem = Union[QueryFiberDataPayload, QueryLEDDataPayload]
QueryDancerStatusPayload = List[QueryDancerStatusPayloadItem]


"""
Coordinates
"""

QueryCoordinatesPayload = Tuple[float, float, float]


"""
PositionRecord
"""


QueryPosRecordData = List[ID]


GET_POS_RECORD = gql(
    """
    query posRecord {
        positionFrameIDs
    }
    """
)


"""
PositionMap
"""


@dataclass
class QueryPosMapPayloadItem(JSONWizard):
    start: int
    pos: List[QueryCoordinatesPayload]


QueryPosMapPayload = Dict[ID, QueryPosMapPayloadItem]


@dataclass
class QueryPosMapData(JSONWizard):
    frameIds: QueryPosMapPayload


GET_POS_MAP = gql(
    """
    query posMap {
        PosMap {
            frameIds
        }
    }
    """
)


"""
ControlRecord
"""


QueryControlRecordData = List[ID]

GET_CONTROL_RECORD = gql(
    """
    query controlRecord {
        controlFrameIDs
    }
    """
)


"""
ControlMap
"""


@dataclass
class QueryControlMapPayloadItem(JSONWizard):
    start: int
    fade: bool
    status: List[QueryDancerStatusPayload]


QueryControlMapPayload = Dict[ID, QueryControlMapPayloadItem]


@dataclass
class QueryControlMapData(JSONWizard):
    frameIds: QueryControlMapPayload


GET_CONTROL_MAP = gql(
    """
    query controlmap {
        ControlMap {
            frameIds
        }
    }
    """
)


"""
EffectList
"""


"""
ColorMap
"""


@dataclass
class QueryColorMapPayloadItem(JSONWizard):
    color: ColorName
    colorCode: RGB


QueryColorMapPayload = Dict[ColorID, QueryColorMapPayloadItem]


@dataclass
class QueryColorMapData(JSONWizard):
    colorMap: QueryColorMapPayload


GET_COLOR_MAP = gql(
    """
    query ColorMap {
        colorMap {
            colorMap
        }
    }
    """
)
