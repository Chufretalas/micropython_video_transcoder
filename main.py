from struct import unpack
import LCD
from colour import colour

display = LCD.LCD_1inch3()

while True:
    with open("./bad_apple.cvb", "rb") as f:

        V_size = unpack("H", f.read(2))[0]
        H_size = unpack("H", f.read(2))[0]
        color_mode = unpack("B", f.read(1))[0]

        EOF = False

        frame_count = 0

        print("Reading!")

        if color_mode == 2: # BW
            while not EOF:
                BW_counter = 0  # a counter to ensure the display only shows the image when it reads a full frame
                while True:
                    chunk = f.read(1)
                    if chunk == b"":
                        EOF = True
                        break

                    chunk = chunk[0]

                    for i in range(7, -1, -1):
                        bit = (chunk >> i) & 1  # read the byte from the MSB to the LSB
                        l_idx = BW_counter // H_size
                        c_idx = BW_counter - l_idx * H_size
                        display.pixel(
                            c_idx,
                            l_idx,
                            colour(255, 255, 255) if bit == 1 else colour(0, 0, 0),
                        )
                        BW_counter += 1

                        print(f"Lines read: {l_idx+1}   ", end="\r")

                        if BW_counter == H_size * V_size:
                            # this means it has read a full frame
                            BW_counter = 0
                            display.show()
                            frame_count += 1
                            print(f"\nFrame {frame_count}")

        else:
            while not EOF:
                for l_idx in range(0, V_size):
                    for c_idx in range(0, H_size):
                        if color_mode == 0: # RGB
                            chunk = f.read(1)
                            if chunk == b"":
                                EOF = True
                                break
                            R = unpack("B", chunk)[0]

                            chunk = f.read(1)
                            if chunk == b"":
                                EOF = True
                                break
                            G = unpack("B", chunk)[0]

                            chunk = f.read(1)
                            if chunk == b"":
                                EOF = True
                                break
                            B = unpack("B", chunk)[0]

                            display.pixel(c_idx, l_idx, colour(R, G, B))

                        else:  # grayscale
                            chunk = f.read(1)
                            if chunk == b"":
                                EOF = True
                                break
                            pixel = unpack("B", chunk)[0]
                            display.pixel(c_idx, l_idx, colour(pixel, pixel, pixel))

                        if EOF:
                            break

                    if EOF:
                        break

                    print(f"Lines read: {l_idx+1}   ", end="\r")

                display.show()
                frame_count += 1
                print(f"\nFrame {frame_count}")

    print("")