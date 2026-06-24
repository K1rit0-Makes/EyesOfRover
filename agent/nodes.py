from agent.llm import get_llm

from agent.tools import (
    search_object,
    count_object_occurrences,
    get_scene,
    find_nearby_objects,
    get_latest_scene
)

from agent.conversation_memory import (
    save_conversation,
    get_recent_conversations
)


llm = get_llm()


def planner_node(
    state
):

    print(
        "\n========== PLANNER ==========\n"
    )

    response = llm.invoke(
        f"""
You are a planner.

Available Actions:

SEARCH_OBJECT
COUNT_OBJECT_OCCURRENCES
GET_SCENE
FIND_NEARBY_OBJECTS
GET_LATEST_SCENE

User Query:

{state["user_query"]}

Return ONLY valid JSON.

Examples:

{{
    "action":"SEARCH_OBJECT",
    "object_name":"keyboard",
    "scene_id":null
}}

{{
    "action":"COUNT_OBJECT_OCCURRENCES",
    "object_name":"cup",
    "scene_id":null
}}

{{
    "action":"GET_SCENE",
    "object_name":null,
    "scene_id":8
}}

{{
    "action":"FIND_NEARBY_OBJECTS",
    "object_name":"keyboard",
    "scene_id":null
}}

{{
    "action":"GET_LATEST_SCENE",
    "object_name":null,
    "scene_id":null
}}
"""
    )

    import json

    data = json.loads(
        response.content
    )

    state["action"] = data["action"]

    state["object_name"] = data.get(
        "object_name"
    )

    state["scene_id"] = data.get(
        "scene_id"
    )

    print(
        "Action:",
        state["action"]
    )

    print(
        "Object:",
        state["object_name"]
    )

    print(
        "Scene:",
        state["scene_id"]
    )

    return state


def search_object_node(
    state
):

    print(
        "\n========== SEARCH OBJECT ==========\n"
    )

    state["tool_result"] = (
        search_object.invoke(
            {
                "object_name":
                state["object_name"]
            }
        )
    )

    return state


def count_object_node(
    state
):

    print(
        "\n========== COUNT OBJECT ==========\n"
    )

    state["tool_result"] = (
        count_object_occurrences.invoke(
            {
                "object_name":
                state["object_name"]
            }
        )
    )

    return state


def get_scene_node(
    state
):

    print(
        "\n========== GET SCENE ==========\n"
    )

    state["tool_result"] = (
        get_scene.invoke(
            {
                "scene_id":
                state["scene_id"]
            }
        )
    )

    return state


def nearby_objects_node(
    state
):

    print(
        "\n========== NEARBY OBJECTS ==========\n"
    )

    state["tool_result"] = (
        find_nearby_objects.invoke(
            {
                "object_name":
                state["object_name"]
            }
        )
    )

    return state


def latest_scene_node(
    state
):

    print(
        "\n========== LATEST SCENE ==========\n"
    )

    state["tool_result"] = (
        get_latest_scene.invoke({})
    )

    return state


def answer_node(
    state
):

    print(
        "\n========== ANSWER ==========\n"
    )

    response = llm.invoke(
        f"""
You are Eyes Of Rover.

User Query:

{state["user_query"]}

Action:

{state["action"]}

Tool Result:

{state["tool_result"]}

Recent Conversation Memory:

{get_recent_conversations()}

Answer the user's question.

Only use the provided tool result.

Do not invent information.
"""
    )

    state["final_answer"] = (
        response.content.strip()
    )

    save_conversation(
        state["user_query"],
        state["final_answer"]
    )

    print(
        state["final_answer"]
    )

    print(
        "\n========== END ANSWER ==========\n"
    )

    return state