from langgraph.graph import (
    StateGraph,
    END
)

from agent.state import (
    RoverState
)

from agent.nodes import (
    planner_node,
    execute_tools_node,
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
    "execute_tools",
    execute_tools_node
)

builder.add_node(
    "answer",
    answer_node
)


builder.set_entry_point(
    "planner"
)


builder.add_edge(
    "planner",
    "execute_tools"
)

builder.add_edge(
    "execute_tools",
    "answer"
)

builder.add_edge(
    "answer",
    END
)


graph = builder.compile()