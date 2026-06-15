import json
import os

from datetime import datetime

FILE_NAME = "scene_memory.json"


def load_scenes():

    if not os.path.exists(FILE_NAME):

        return []

    with open(
        FILE_NAME,
        "r"
    ) as file:

        return json.load(file)


def save_scene(objects):

    scenes = load_scenes()

    current_scene = sorted(
        list(objects)
    )

    # ----------------------
    # COMPARE WITH PREVIOUS
    # ----------------------

    if scenes:

        previous_scene = sorted(
            scenes[-1]["objects"]
        )

        if previous_scene == current_scene:

            return False

    # ----------------------
    # CREATE NEW SCENE
    # ----------------------

    new_scene = {

        "scene_id":
        len(scenes) + 1,

        "timestamp":
        datetime.now().isoformat(),

        "objects":
        current_scene
    }

    scenes.append(
        new_scene
    )

    # ----------------------
    # SAVE JSON
    # ----------------------

    with open(
        FILE_NAME,
        "w"
    ) as file:

        json.dump(
            scenes,
            file,
            indent=4
        )

    return True