# Encodes any vídeo into a square lower resolution version of itself and saves it to a txt file
# The output file has one frame per line with each pixel value separeted by a comma

import cv2
from struct import pack, unpack

video = cv2.VideoCapture("./assets/bad_apple_r5.mp4")

color_mode = 2

frame_number = 0
calculated_dimensions = False
xcrop = 0
ycrop = 0
padding = 0  # if the crop results are not integer

try:
    with open("video1.cvb", "wb") as f:
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

            # if not (color_mode == 0):
            #     frame = frame.mean(axis=2)
            #     for i in range(0, len(frame)):
            #         for j in range(0, len(frame[i])):
            #             frame[i, j] = int(frame[i, j])

            f.write(pack("H", 240))
            f.write(pack("H", 240))
            f.write(pack("B", color_mode))

            for line in frame:
                for idx, pixel in enumerate(line):
                    match color_mode:
                        case 0:  # RGB
                            f.write(pack("B", pixel[0]))
                            f.write(pack("B", pixel[1]))
                            f.write(pack("B", pixel[2]))

                        case 1:  # Grayscale
                            f.write(pack("B", int(pixel.mean())))

                        case 2:  # Black and White
                            f.write(pack("B", 255 if int(pixel.mean()) >= 127 else 0))

except OSError as err:
    print("Could not create the output file: ", err)


# with open("./video.cib", "rb") as f:
#     print(unpack("B", f.read(1))[0])
