# Encodes any vídeo into a square lower resolution version of itself and saves it to a txt file
# The output file has one frame per line with each pixel value separeted by a comma

import cv2

video = cv2.VideoCapture("./assets/bad_apple_r5.mp4")

color = False
binary = True

frame_number = 0
calculated_dimensions = False
xcrop = 0
ycrop = 0
padding = 0  # if the crop results are not integer

with open("video.txt", "w", encoding="ASCII") as f:
    while True:
        ok, frame = video.read()
        if not ok:
            break

        frame_number += 1

        print(f"reading frame: {frame_number}", end="\r")

        if not calculated_dimensions:
            if len(frame) > len(frame[0]):
                # vertical
                ycrop = (len(frame) - len(frame[0])) // 2

                if (len(frame) - len(frame[0])) % 2 != 0:
                    padding = 1

            elif len(frame) < len(frame[0]):
                # horizontal
                xcrop = (len(frame[0]) - len(frame)) // 2

                if (len(frame[0]) - len(frame)) % 2 != 0:
                    padding = 1

            calculated_dimensions = True

        frame = frame[
            ycrop + padding : len(frame) - ycrop,
            xcrop + padding : len(frame[0]) - xcrop,
        ]  # make the image square by cropping the sides
        frame = cv2.resize(frame, (240, 240))  # resize to the display's resolution

        if (not color) or binary:
            frame = frame.mean(axis=2)
            for i in range(0, len(frame)):
                for j in range(0, len(frame[i])):
                    frame[i, j] = int(frame[i, j])

        for line in frame:
            for idx, pixel in enumerate(line):
                if color:
                    f.write(
                        f"{int(pixel[0])},{int(pixel[1])},{int(pixel[2])}{'' if idx == len(line) -1 else ','}"
                    )
                    continue

                if binary:
                    f.write(f"{'1' if pixel >= 127 else '0'}")
                    continue

                f.write(f"{int(pixel)}{'' if idx == len(line) -1 else ','}")
            f.write("\n")

