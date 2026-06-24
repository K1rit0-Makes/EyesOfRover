import json

from langchain_core.tools import tool

DATA_FILE = "data/scene_memory.json"


def load_scenes():

    with open(
        DATA_FILE,
        "r"
    ) as file:

        return json.load(
            file
        )


@tool
def search_object(
    object_name: str
):
    """
    Find all scenes containing an object.
    """

    scenes = load_scenes()

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
def count_object_occurrences(
    object_name: str
):
    """
    Count how many scenes contain an object.
    """

    scenes = load_scenes()

    count = 0

    object_name = object_name.lower()

    for scene in scenes:

        scene_objects = [

            obj.lower()

            for obj in scene["objects"]
        ]

        if object_name in scene_objects:

            count += 1

    return {
        "object_name":
        object_name,

        "count":
        count
    }


@tool
def get_scene(
    scene_id: int
):
    """
    Retrieve a scene by scene ID.
    """

    scenes = load_scenes()

    for scene in scenes:

        if scene["scene_id"] == scene_id:

            return scene

    return None


@tool
def find_nearby_objects(
    object_name: str
):
    """
    Find objects commonly seen
    with another object.
    """

    scenes = load_scenes()

    object_name = object_name.lower()

    nearby_objects = set()

    for scene in scenes:

        scene_objects = [

            obj.lower()

            for obj in scene["objects"]
        ]

        if object_name in scene_objects:

            for obj in scene_objects:

                if obj != object_name:

                    nearby_objects.add(
                        obj
                    )

    return {

        "target_object":
        object_name,

        "nearby_objects":
        sorted(
            list(
                nearby_objects
            )
        )
    }


@tool
def get_latest_scene():
    """
    Return the latest scene.
    """

    scenes = load_scenes()

    if len(scenes) == 0:

        return None

    return scenes[-1]

@tool
def list_all_objects():
    """
    Return all unique objects ever seen.
    """

    scenes = load_scenes()

    objects = set()

    for scene in scenes:

        for obj in scene["objects"]:

            objects.add(
                obj.lower()
            )

    return sorted(
        list(objects)
    )
@tool
def first_observation(
    object_name: str
):
    """
    Return the first scene where
    an object was observed.
    """

    scenes = load_scenes()

    object_name = object_name.lower()

    for scene in scenes:

        scene_objects = [

            obj.lower()

            for obj in scene["objects"]
        ]

        if object_name in scene_objects:

            return scene

    return None

@tool
def last_observation(
    object_name: str
):
    """
    Return the latest scene where
    an object was observed.
    """

    scenes = load_scenes()

    object_name = object_name.lower()

    latest = None

    for scene in scenes:

        scene_objects = [

            obj.lower()

            for obj in scene["objects"]
        ]

        if object_name in scene_objects:

            latest = scene

    return latest

@tool
def object_timeline(
    object_name: str
):
    """
    Return all scenes containing
    an object in chronological order.
    """

    scenes = load_scenes()

    object_name = object_name.lower()

    timeline = []

    for scene in scenes:

        scene_objects = [

            obj.lower()

            for obj in scene["objects"]
        ]

        if object_name in scene_objects:

            timeline.append(
                {
                    "scene_id":
                    scene["scene_id"],

                    "timestamp":
                    scene["timestamp"]
                }
            )

    return timeline

@tool
def compare_scenes(
    scene_a: int,
    scene_b: int
):
    """
    Compare two scenes.
    """

    scenes = load_scenes()

    first = None
    second = None

    for scene in scenes:

        if scene["scene_id"] == scene_a:

            first = scene

        if scene["scene_id"] == scene_b:

            second = scene

    if first is None or second is None:

        return {
            "error":
            "Scene not found"
        }

    objects_a = set(

        obj.lower()

        for obj in first["objects"]
    )

    objects_b = set(

        obj.lower()

        for obj in second["objects"]
    )

    return {

        "scene_a":
        scene_a,

        "scene_b":
        scene_b,

        "added":
        sorted(
            list(
                objects_b - objects_a
            )
        ),

        "removed":
        sorted(
            list(
                objects_a - objects_b
            )
        )
    }

