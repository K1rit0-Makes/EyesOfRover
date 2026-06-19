from typing import TypedDict


class RoverState(TypedDict):

    user_query: str

    tool_result: list

    final_answer: str