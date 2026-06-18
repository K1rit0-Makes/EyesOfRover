import cv2


def compare_images(
    previous_image_path,
    current_frame
):

    previous_image = cv2.imread(
        previous_image_path
    )

    if previous_image is None:

        print(
            "Could not load previous image"
        )

        return 0

    previous_gray = cv2.cvtColor(
        previous_image,
        cv2.COLOR_BGR2GRAY
    )

    current_gray = cv2.cvtColor(
        current_frame,
        cv2.COLOR_BGR2GRAY
    )

    previous_gray = cv2.resize(
        previous_gray,
        (300, 300)
    )

    current_gray = cv2.resize(
        current_gray,
        (300, 300)
    )

    difference = cv2.absdiff(
        previous_gray,
        current_gray
    )

    similarity = (
        100
        - (
            difference.mean()
            / 255
            * 100
        )
    )

    return round(
        similarity,
        2
    )