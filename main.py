from ultralytics import YOLO
import cv2
import time

from memory import save_event
from scene_memory import save_scene

# ==========================
# SETTINGS
# ==========================

MIN_CONFIDENCE = 0.35

APPEAR_THRESHOLD = 20
DISAPPEAR_THRESHOLD = 20

SCENE_SAVE_INTERVAL = 5

# ==========================
# YOLO
# ==========================

model = YOLO("yolomodels/yolov8m.pt")

cap = cv2.VideoCapture(0)

# ==========================
# MEMORY STRUCTURES
# ==========================

detection_counter = {}

missing_counter = {}

confirmed_objects = set()

last_scene_save = time.time()

# ==========================
# MAIN LOOP
# ==========================

while True:

    success, frame = cap.read()

    if not success:
        break

    results = model(frame, verbose=False)

    visible_this_frame = set()

    # ----------------------
    # PROCESS DETECTIONS
    # ----------------------

    for box in results[0].boxes:

        confidence = float(box.conf[0])

        if confidence < MIN_CONFIDENCE:
            continue

        class_id = int(box.cls[0])

        object_name = model.names[class_id]

        visible_this_frame.add(object_name)

    # ----------------------
    # UPDATE COUNTERS
    # ----------------------

    for obj in visible_this_frame:

        detection_counter[obj] = (
            detection_counter.get(obj, 0) + 1
        )

        missing_counter[obj] = 0

        if (
            detection_counter[obj] >= APPEAR_THRESHOLD
            and obj not in confirmed_objects
        ):

            confirmed_objects.add(obj)

            print(f"{obj} appeared")

            save_event(
                obj,
                "appeared"
            )

    # ----------------------
    # HANDLE DISAPPEARANCE
    # ----------------------

    for obj in list(confirmed_objects):

        if obj not in visible_this_frame:

            missing_counter[obj] = (
                missing_counter.get(obj, 0) + 1
            )

            if (
                missing_counter[obj]
                >= DISAPPEAR_THRESHOLD
            ):

                print(f"{obj} disappeared")

                save_event(
                    obj,
                    "disappeared"
                )

                confirmed_objects.remove(obj)

                detection_counter[obj] = 0

                missing_counter[obj] = 0

    # ----------------------
    # SCENE MEMORY + IMAGE
    # ----------------------

    if (
        time.time()
        - last_scene_save
        >= SCENE_SAVE_INTERVAL
    ):

        saved = save_scene(
            confirmed_objects,
            frame
        )

        if saved:

            print(
                "Scene Saved:",
                confirmed_objects
            )

        last_scene_save = time.time()

    # ----------------------
    # DISPLAY
    # ----------------------

    annotated_frame = results[0].plot()

    cv2.imshow(
        "Eyes Of Rover",
        annotated_frame
    )

    key = cv2.waitKey(1)

    if key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()