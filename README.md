# CS373 Assignment extension

This extension uses openCV to run qr code detection in real time. Detection is faster but less robust as a trade off. For a review of the thought process behind this choice, read report.pdf (its kinda interesting, I promise)

----------

## Installation
You probably know how to do this

1. Clone this repo into a directory
2. Create a new virtual environment
3. Install requirements.txt

## Usage
##### If you just want to see the code running, watch `qrExample.mp4`

Run `QRCodeDetectionExtension.py`, it will prompt you to choose input of either your webcam or a short sample mp4 file.

The program will run until you press `q`, or it reaches the end of the mp4 file.

If you want to try your own mp4 file, you can change the file name/path on line 58 of the file.

----------

## Note
Code dectection is not perfect (explained in the report pdf), it will probably flicker around especially if you have other visually noisy objects near the qr code that might get detected. The bounding rectangle also doesn't support perspective warping, so viewing a qr code from a sharp angle may look a bit wonky. The goal is fast detection, even if it is less reliable.

