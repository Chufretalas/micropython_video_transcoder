import utime
import LCD
from colour import colour

display = LCD.LCD_1inch3()

while True:
    with open("./video.txt", "r") as f:

        line_idx = 0
        for line in f:
            for col_idx in range(0, len(line)):
                if line[col_idx] == "1":
                    display.pixel(col_idx, line_idx, colour(255, 255, 255))
                else:
                    display.pixel(col_idx, line_idx, colour(0, 0, 0))

            line_idx += 1

            if line_idx >= 240:
                line_idx = 0
                display.show()
            
            print(f"Lines read: {line_idx}   ", end="\r")

