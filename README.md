# Micropython Video Transcoder

Two programs that encode a video into a special binary file, which can later be read and displayed by a microcontroller running micropython.

![video of a small LCD display playing a very choppy version of bad apple](readme_video.webp)

This project consists of two programs: the **encoder `encoder.py`** and the **decoder `main.py`**.

## About the encoder

The encoder can be found in `video encoder/encoder.py`. It is suposed to be ran in a normal computer.  
It will ask for an input file (the majority of the most common video formats are accepted), then a color mode, that determines if the output will be in full color (RGB), gray tones (Grayscale) ou a binary black and white (Black and White), then the resolution of the output that should match your display's resolution (it only outputs square videos for now, so that's why it only asks for one value), finally, you will be prompted for a place to save the file. Keep in mind the it asks for the save destination before it starts processing the video, so check the *Bytes Written:* print to check if it actually did anything.

## About the decoder

Found in the `main.py` file, it requires that the `colour.py` and `LCD.py` library files are both installed in your target device to work.  
The only change you should need to make to run different files is altering the parameter in the first *open* function, the rest, such as display resolution and color mode, can be determined by the .cvb file itself.

******

> Keep in mind the both the encoder and the decoder are hellishly slow. Use this code more as an easy way to show a slide show from your microcontroller, don't expect it to encode Shrek in thirty seconds and then decode it at 60fps super smoothly, that will never happen, and that .cvb file would probably be in the 50GB range. Most importantly, have fun :)

## Binary .cvb (chufretalas video binary) structure

In order in wich they appear in the file

- 2 bytes: vertical size (number of lines)
- 2 bytes: horizontal size (number of columns)
- 1 byte: color mode
  - 0 == RGB (three bytes per pixel)
  - 1 == Grayscale (one byte per pixel)
  - 2 == Black and White (one bit per pixel)

- The rest is the actual video. The data will appear **frame by frame**, **line by line** going **left to right**.

## Sample Files

- **bad_apple.cvb** - A very reduced version of the Bad Apple music clip
  - *Frame Count*: 52
  - *Color Mode*: Black and white
  - *Output size*: 240x240

- **grayscale.cvb** - A bunch of game screenshots, mostly fallout 4
  - *Frame Count*: 4
  - *Color Mode*: Grayscale
  - *Output size*: 240x240

- **RGB.cvb** - More game screenshots
  - *Frame Count*: 2
  - *Color Mode*: RGB
  - *Output size*: 240x240

- **red_test.cvb** - A solid color red frame
  - *Frame Count*: 1
  - *Color Mode*: RGB
  - *Output size*: 240x240

- **green_test.cvb** - A solid color green frame
  - *Frame Count*: 1
  - *Color Mode*: RGB
  - *Output size*: 240x240

- **blue_test.cvb** - A solid color blue frame
  - *Frame Count*: 1
  - *Color Mode*: RGB
  - *Output size*: 240x240

## External libraries disclaimer

Both `colour.py` and `LCD.py` are micropython library files not made by me, files which I obtained through a course from makerhero.com, so, unfortunately, I am not sure about who the original autors are.
