from agent.tools import search_object


def search_node(
    state
):

    result = search_object.invoke(
        {
            "object_name":
            "keyboard"
        }
    )

    state["tool_result"] = result

    return state