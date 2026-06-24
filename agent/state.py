from typing import TypedDict
from typing import Optional
from typing import Any


class RoverState(TypedDict):

    user_query: str

    action: str

    object_name: Optional[str]

    scene_id: Optional[int]

    tool_result: Any

    final_answer: str