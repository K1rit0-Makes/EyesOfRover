import json
import os
import cv2

from datetime import datetime

from scene_compare import compare_images

FILE_NAME = "scene_memory.json"
SCENE_FOLDER = "scenes"

IMAGE_SIMILARITY_THRESHOLD = 85

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

    if len(current_scene) == 0:

        print(
            "Empty Scene - Skipping"
        )

        return False

    # ----------------------
    # SEARCH ENTIRE MEMORY
    # ----------------------

    best_similarity = 0
    best_scene_id = None

    for scene in scenes:

        similarity = compare_images(
            scene["image"],
            frame
        )

        if similarity > best_similarity:

            best_similarity = similarity

            best_scene_id = scene["scene_id"]

    # ----------------------
    # FOUND KNOWN SCENE
    # ----------------------

    if best_similarity >= IMAGE_SIMILARITY_THRESHOLD:

        print(
            f"\nKnown Scene Found"
        )

        print(
            f"Scene ID: {best_scene_id}"
        )

        print(
            f"Similarity: {best_similarity}%"
        )

        print(
            "Skipping Save\n"
        )

        return False

    # ----------------------
    # NEW SCENE
    # ----------------------

    print(
        "\nNew Scene Detected"
    )

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

    print(
        f"Scene {scene_id} Saved\n"
    )

    return True