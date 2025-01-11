import utime
from struct import unpack
import LCD
import os
from colour import colour

display = LCD.LCD_1inch3()


def eof(f):
    return os.fstat(f.fileno()).st_size == f.tell()


while True:
    with open("./video1.cvb", "rb") as f:

        V_size = unpack("H", f.read(2))[0]
        H_size = unpack("H", f.read(2))[0]
        color_mode = unpack("B", f.read(1))[0]

        EOF = False

        print("Lendo!")

        while not EOF:
            for l_idx in range(0, V_size):
                for c_idx in range(0, H_size):
                    if color_mode == 0:
                        chunk = f.read(1)
                        if chunk == b"":
                            EOF = True
                            break
                        R = unpack("B", chunk)[0]
                        G = unpack("B", f.read(1))[0]
                        B = unpack("B", f.read(1))[0]
                        display.pixel(c_idx, l_idx, colour(R, G, B))

                    else:
                        chunk = f.read(1)
                        if chunk == b"":
                            EOF = True
                            break
                        pixel = unpack("B", chunk)[0]
                        display.pixel(c_idx, l_idx, colour(pixel, pixel, pixel))
                if EOF:
                    break

                print(f"Lines read: {l_idx+1}   ", end="\r")

            print("")
            display.show()
