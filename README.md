# Color-Pen-Reader
An open-source pen reader for dyslexic and visually impaired people that is able to read text written in any color on any colored background

To set this project up, you will have to buy all the parts listed, assemble everything together and make all the right physical connections according to the docs listed in the Final Senior Design Proposal pdf in the Proposals folder.

The software setup is done by first expanding the Raspi filesystem in raspi-config, then removing any extraneous programs the stock Raspi came with like Libreoffice and Wolfram Alpha, and then running the setup script in the ColorPenReader folder. If you have around 5-6 GB free on the SD card though, you can just run the setup script as is and not worry about storage space. The setup script installs all the required dependencies, tesseract-ocr, festival, virtualenv, pip, modifies the .profile file to accomodate the changes, and compiles OpenCV 3.4.1 on the Raspi.

If the setup script encounters issues with compiling OpenCV, refer to https://www.pyimagesearch.com/2017/09/04/raspbian-stretch-install-opencv-3-python-on-your-raspberry-pi/ for a tutorial on how to compile OpenCV by hand.

Once the setup is complete, you should be able to run the Color Pen Reader (assuming the hardware is set up properly too) by running the startup script. This script executes source ~/.profile, starts the cv Python virtual environment, and runs the main loop of the Color Pen Reader.

To use the Color Pen Reader, the camera must be positioned such that the macro lens is around 1 cm away from the text, then the scanning button is pressed and held down, the scanner is dragged across the text (letting the wheel rotate), and then the button is released to end scanning. The series of images taken is concatenated into one, the resulting image is filtered using edge detection + binarization, and then the filtered image is read by Tesseract, transforming the image into a string, which is then read out by festival.

# Issues

Tesseract is poor at dealing with slanted text. Tesseract OCR seems to depend on machine learning algorithms in order to read text, and it appears that it wasn't trained for this specific purpose. Perhaps there is a way to improve this reliability by training with a new data set?

The output sound is too quiet. Please find or assemble a louder amplifier.

The wheel that measures the distance that the scanner has traveled while scanning is too large. Minimizing it (and overall reworking the 3D printed model of the scanner) and exchanging the current rotary encoder with a more accurate one would go a long way toward improving reliability since this would minimize gaps and overlaps between images and make text more consistent.

Improving the speed of the algorithms used would benefit the project greatly. It seems that the color filter stage is slow at dealing with high-resolution images (or long scans). Improving the time complexity of the algorithms would improve the performance in the greatest way.

The camera's framerate is slow and does not accommodate fast scans. Finding a faster camera might require different hardware than the Raspi, which makes this a complex issue.

If there is a way to switch off most of the OS for when the Color Pen Reader was running (on boot of course), resources would be freed and the performance would be improved.

If there is a way to utilize all four cores in processing the input, the performance would be improved.
