from langgraph.graph import StateGraph
from langgraph.graph import END

from agent.state import RoverState

from agent.nodes import (
    planner_node,
    search_object_node,
    count_object_node,
    get_scene_node,
    nearby_objects_node,
    latest_scene_node,
    answer_node
)


builder = StateGraph(
    RoverState
)


builder.add_node(
    "planner",
    planner_node
)

builder.add_node(
    "search_object",
    search_object_node
)

builder.add_node(
    "count_object",
    count_object_node
)

builder.add_node(
    "get_scene",
    get_scene_node
)

builder.add_node(
    "nearby_objects",
    nearby_objects_node
)

builder.add_node(
    "latest_scene",
    latest_scene_node
)

builder.add_node(
    "answer",
    answer_node
)


def route_action(
    state
):

    return state["action"]


builder.add_conditional_edges(
    "planner",
    route_action,
    {
        "SEARCH_OBJECT":
        "search_object",

        "COUNT_OBJECT_OCCURRENCES":
        "count_object",

        "GET_SCENE":
        "get_scene",

        "FIND_NEARBY_OBJECTS":
        "nearby_objects",

        "GET_LATEST_SCENE":
        "latest_scene"
    }
)


builder.add_edge(
    "search_object",
    "answer"
)

builder.add_edge(
    "count_object",
    "answer"
)

builder.add_edge(
    "get_scene",
    "answer"
)

builder.add_edge(
    "nearby_objects",
    "answer"
)

builder.add_edge(
    "latest_scene",
    "answer"
)

builder.add_edge(
    "answer",
    END
)


builder.set_entry_point(
    "planner"
)


graph = builder.compile()