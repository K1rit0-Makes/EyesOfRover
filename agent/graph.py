from langgraph.graph import StateGraph

from agent.state import RoverState
from agent.nodes import search_node


builder = StateGraph(
    RoverState
)

builder.add_node(
    "search",
    search_node
)

builder.set_entry_point(
    "search"
)

builder.set_finish_point(
    "search"
)

graph = builder.compile()