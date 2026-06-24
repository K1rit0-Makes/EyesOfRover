from agent.graph import graph


query = input(
    "\nAsk Eyes Of Rover: "
)


result = graph.invoke(
    {
        "user_query":
        query,

        "action":
        "",

        "object_name":
        None,

        "scene_id":
        None,

        "tool_result":
        None,

        "final_answer":
        ""
    }
)


print(
    "\n========== FINAL ANSWER ==========\n"
)

print(
    result["final_answer"]
)