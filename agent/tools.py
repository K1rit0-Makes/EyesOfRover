import json

from langchain_core.tools import tool

DATA_FILE = "data/scene_memory.json"


@tool
def search_object(
    object_name: str
):
    """
    Search scene memory for scenes
    containing a specific object.
    """

    with open(
        DATA_FILE,
        "r"
    ) as file:

        scenes = json.load(
            file
        )

    results = []

    object_name = object_name.lower()

    for scene in scenes:

        scene_objects = [

            obj.lower()

            for obj in scene["objects"]
        ]

        if object_name in scene_objects:

            results.append(
                scene
            )

    return results


@tool
def get_scene(
    scene_id: int
):
    """
    Retrieve a scene using its scene ID.
    """

    with open(
        DATA_FILE,
        "r"
    ) as file:

        scenes = json.load(
            file
        )

    for scene in scenes:

        if scene["scene_id"] == scene_id:

            return scene

    return None