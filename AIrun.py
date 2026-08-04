from agent.graph import graph


query = input(
    "\nAsk Eyes Of Rover: "
)


result = graph.invoke(
    {
        "user_query": query,

        "actions": [],

        "tool_results": [],

        "final_answer": ""
    }
)


print(
    "\n========== FINAL ANSWER ==========\n"
)

print(
    result["final_answer"]
)