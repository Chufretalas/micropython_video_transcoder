import cv2
from numpy import ndarray
from typing import BinaryIO
from struct import pack
from os import path
from sys import exit
from tkinter import filedialog, Tk
from ctypes import windll

windll.shcore.SetProcessDpiAwareness(1)


def main():

    tk = Tk()
    tk.withdraw()
    tk.iconify()

    input_path: str
    video: cv2.VideoCapture

    while True:
        try:
            input_path = filedialog.askopenfilename(
                title="Choose a video file to encode", initialdir=path.dirname(__file__)
            )

            if input_path == "":
                exit(0)

            video = cv2.VideoCapture(input_path)

            if video.isOpened():
                break

        except Exception as e:
            print(e)

        print(f'Could not open file: "{input_path}"\nPlease choose a valid video file.')

    print()

    color_mode = ""
    while True:
        color_mode = input(
            "Please choose a color mode to encode the video. Only type the desired number.\n[0] RGB\n[1] Grayscale\n[2] Black and White\nYour choise: "
        )

        if color_mode in ("0", "1", "2"):
            break

        print("Invalid option! Please try again.")

    print()

    # TODO: enable non-square outputs
    output_size = -1
    while True:
        try:
            output_size = int(input("Write the dimensions of the output in pixels: "))

            if output_size > 0:
                break

        except:
            pass

        print("Invalid option! Please try again.")

    frame_number = 0
    calculated_dimensions = False
    xcrop = 0
    ycrop = 0
    padding = 0  # if the crop results are not integer

    bytes_written = 0

    try:
        output_path = filedialog.asksaveasfilename(
            title="Save output as",
            initialdir=path.dirname(input_path),
            defaultextension="cvb",
        )
        tk.destroy()

        f: BinaryIO
        with open(output_path, "wb") as f:
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
                frame: ndarray = cv2.resize(
                    frame, (output_size, output_size)
                )  # resize to the display's resolution

                f.write(pack("H", output_size))
                bytes_written += 2
                f.write(pack("H", output_size))
                bytes_written += 2
                f.write(pack("B", int(color_mode)))
                bytes_written += 1

                if color_mode == "2":
                    buffer = 0
                    shift_counter = 0
                    for line in frame:
                        for pixel in line:
                            buffer <<= 1
                            buffer += 1 if int(pixel.mean()) >= 127 else 0
                            shift_counter += 1
                            if shift_counter == 8:
                                f.write(pack("B", buffer))
                                bytes_written += 1
                                shift_counter = 0
                                buffer = 0

                    if shift_counter != 0:
                        buffer <<= 8 - shift_counter
                        f.write(pack("B", buffer))
                        bytes_written += 1

                else:
                    for line in frame:
                        for pixel in line:
                            match color_mode:
                                case "0":  # RGB
                                    # pixel[0] == blue, [1] == green, [2] == red
                                    f.write(pack("B", pixel[2]))
                                    bytes_written += 1
                                    f.write(pack("B", pixel[1]))
                                    bytes_written += 1
                                    f.write(pack("B", pixel[0]))
                                    bytes_written += 1

                                case "1":  # Grayscale
                                    f.write(pack("B", int(pixel.mean())))
                                    bytes_written += 1

            print()

    except OSError as err:
        print("Could not create the output file: ", err)
        exit(1)

    print(f"Bytes written: {bytes_written}")


if __name__ == "__main__":
    main()
