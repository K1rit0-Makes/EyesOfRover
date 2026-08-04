import json

from agent.conversation_memory import (
    get_recent_conversations,
    save_conversation,
)
from agent.llm import get_llm
from agent.tools import (
    compare_scenes,
    count_object_occurrences,
    find_nearby_objects,
    first_observation,
    get_latest_scene,
    get_scene,
    last_observation,
    list_all_objects,
    object_timeline,
    search_object,
)

llm = get_llm()


TOOLS = {
    "SEARCH_OBJECT": search_object,
    "COUNT_OBJECT_OCCURRENCES": count_object_occurrences,
    "GET_SCENE": get_scene,
    "FIND_NEARBY_OBJECTS": find_nearby_objects,
    "GET_LATEST_SCENE": get_latest_scene,
    "LIST_ALL_OBJECTS": list_all_objects,
    "FIRST_OBSERVATION": first_observation,
    "LAST_OBSERVATION": last_observation,
    "OBJECT_TIMELINE": object_timeline,
    "COMPARE_SCENES": compare_scenes,
}


def planner_node(state):
    print("\n========== PLANNER ==========\n")

    response = llm.invoke(
        f"""
You are the planning module of Eyes Of Rover.

Your ONLY job is to decide which tools should be executed.

You may call ONE OR MORE tools.

Available Tools

SEARCH_OBJECT
COUNT_OBJECT_OCCURRENCES
GET_SCENE
FIND_NEARBY_OBJECTS
GET_LATEST_SCENE
LIST_ALL_OBJECTS
FIRST_OBSERVATION
LAST_OBSERVATION
OBJECT_TIMELINE
COMPARE_SCENES

User Query

{state["user_query"]}

Return ONLY valid JSON.

Example 1

{{
    "actions":[
        {{
            "tool":"SEARCH_OBJECT",
            "object_name":"keyboard"
        }}
    ]
}}

Example 2

{{
    "actions":[
        {{
            "tool":"SEARCH_OBJECT",
            "object_name":"keyboard"
        }},
        {{
            "tool":"COUNT_OBJECT_OCCURRENCES",
            "object_name":"keyboard"
        }}
    ]
}}

Example 3

{{
    "actions":[
        {{
            "tool":"GET_SCENE",
            "scene_id":5
        }},
        {{
            "tool":"COMPARE_SCENES",
            "scene_a":5,
            "scene_b":8
        }}
    ]
}}
"""
    )

    data = json.loads(response.content)

    state["actions"] = data["actions"]

    print("Planned Actions\n")

    for action in state["actions"]:
        print(action)

    return state


def execute_tools_node(state):
    print("\n========== EXECUTOR ==========\n")

    results = []

    for action in state["actions"]:
        tool_name = action["tool"]

        print("Executing:", tool_name)

        if tool_name not in TOOLS:
            results.append(
                {"tool": tool_name, "result": {"error": "Unknown Tool"}}
            )
            continue

        tool = TOOLS[tool_name]

        arguments = {}

        if "object_name" in action:
            arguments["object_name"] = action["object_name"]

        if "scene_id" in action:
            arguments["scene_id"] = action["scene_id"]

        if "scene_a" in action:
            arguments["scene_a"] = action["scene_a"]

        if "scene_b" in action:
            arguments["scene_b"] = action["scene_b"]

        result = tool.invoke(arguments)

        results.append({"tool": tool_name, "result": result})

    state["tool_results"] = results

    print("\nExecuted Tools\n")

    for result in results:
        print(result["tool"])

    return state


def answer_node(state):
    print("\n========== ANSWER ==========\n")

    response = llm.invoke(
        f"""
You are Eyes Of Rover.

User Query

{state["user_query"]}

Tool Results

{state["tool_results"]}

Recent Conversation Memory

{get_recent_conversations()}

Answer ONLY using the tool results.

Never invent information.

If multiple tool results are available,
combine them into a single natural answer.
"""
    )
    state["final_answer"] = response.content.strip()

    save_conversation(state["user_query"], state["final_answer"])

    print(state["final_answer"])

    print("\n========== END ANSWER ==========\n")

    return state