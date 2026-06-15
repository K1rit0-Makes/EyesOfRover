import json
import os
import cv2

from datetime import datetime

FILE_NAME = "scene_memory.json"
SCENE_FOLDER = "scenes"

os.makedirs(
    SCENE_FOLDER,
    exist_ok=True
)


def load_scenes():

    if not os.path.exists(FILE_NAME):

        return []

    with open(
        FILE_NAME,
        "r"
    ) as file:

        return json.load(file)


def save_scene(
    objects,
    frame
):

    scenes = load_scenes()

    current_scene = sorted(
        list(objects)
    )

    # Ignore empty scenes

    if len(current_scene) == 0:

        return False

    # Compare with previous scene

    if scenes:

        previous_scene = sorted(
            scenes[-1]["objects"]
        )

        if previous_scene == current_scene:

            return False

    scene_id = len(scenes) + 1

    image_name = (
        f"scene_{scene_id}.png"
    )

    image_path = os.path.join(
        SCENE_FOLDER,
        image_name
    )

    cv2.imwrite(
        image_path,
        frame
    )

    new_scene = {

        "scene_id":
        scene_id,

        "timestamp":
        datetime.now().isoformat(),

        "objects":
        current_scene,

        "image":
        image_path
    }

    scenes.append(
        new_scene
    )

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