from typing import Callable, Tuple

from ...graphqls import (
    QueryColorMapData,
    QueryColorMapPayload,
    QueryControlMapData,
    QueryControlMapPayloadItem,
    QueryPosMapPayloadItem,
    SubControlFrame,
    SubPositionFrame,
)
from ..models import Color, ColorMap, ControlMap, ControlMapElement, PosMap


def rgb_to_hex(rgb: Tuple[int, int, int]) -> str:
    r, g, b = rgb
    return f"#{r:02x}{g:02x}{b:02x}"


def gql_pos_frame_sub_to_query(frameSub: SubPositionFrame) -> QueryPosMapPayloadItem:
    frameQuery = QueryPosMapPayloadItem(start=frameSub.start, pos=[])

    frameQuery.pos = list(map(lambda pos: (pos[0], pos[1], pos[2]), frameSub.pos))

    return frameQuery


# def gql_pos_map_query_to_state(response: QueryPosMapData) -> PosMap:
#     pass


def gql_control_map_query_to_state(response: QueryControlMapData) -> ControlMap:
    payload = response.frameIds

    control_map: ControlMap = {}

    for id, frame in payload.items():
        control_map_element = ControlMapElement(
            start=frame.start, fade=frame.fade, status={}
        )

        # TODO: Convert control frame status
        # this requires dancer list
        # control_map_element.status

        control_map[id] = control_map_element

    return control_map


def gql_control_frame_sub_to_query(
    frameSub: SubControlFrame,
) -> QueryControlMapPayloadItem:
    frameQuery = QueryControlMapPayloadItem(
        start=frameSub.start, fade=frameSub.fade, status=[]
    )

    frameQuery.status = list(
        map(
            lambda partControls: list(
                map(lambda partControl: (partControl[0], partControl[1]), partControls)
            ),
            frameSub.status,
        )
    )

    return frameQuery


def gql_color_map_query_to_state(response: QueryColorMapData) -> ColorMap:
    payload: QueryColorMapPayload = response.colorMap

    color_map: ColorMap = {}

    for id, color in payload.items():
        color_map[id] = Color(
            id=id,
            name=color.color,
            color_code=rgb_to_hex(color.colorCode),
            rgb=color.colorCode,
        )

    return color_map
