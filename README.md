## Binary .cvb (chufretalas video binary) structure

In order in wich they appear in the file

- 2 bytes: vertical size (number of lines)
- 2 bytes: horizontal size (number of columns)
- 1 byte: color mode
  - 0 == RGB (three bytes per pixel)
  - 1 == Grayscale (one byte per pixel)
  - 2 == Black and White (one bit per pixel)

- The rest is the actual video. The data will appear **line by line** going **left to right**.
