`# **Installation Guide**
Install the following softwares.
1. Arduino IDE  - any version (better latest)
2. Python 3.8 - **Do not use other versions**
3. A preffered Python IDE - PyCharm would be better

## **Setup Guide**

------**Arduino IDE Setup**------


1. Get a clone of this repository.
2. Go to CameraWebServer direcotory and open CameraWebServer.ino file using Arduino IDE
3. Go to Display directory and open stringWithPeriod.ino file using another window of Arduino IDE
4. Then go to library manager of Arduino IDE and install following:
			AsyncTimer.h - by Aasim-A
			SevSeg.h - by Dean Reading
			ArduinoHttpClient - by Arduino
			AsyncTCP - by dvarrel
5. Go to Sketch menu and include ESPAsyncWebServer.zip that I have uploaded to this repo as a .zip library.
6. Go to Boards manager and install esp32 - by expressif
7. Go to preferences through the file menu and add the following as additional board manager urls(Use a comma to seperate the two. Do not leave blanks)
		http://arduino.esp8266.com/stable/package_esp8266com_index.json
		https://raw.githubusercontent.com/espressif/arduino-esp32/gh-    				pages/package_esp32_index.json
8. Then, click the verify button on both the screens and see whether the setup is correct.


------**Python Setup**------

1. Open a console window and install the following by entering the following commands:
			pip install opencv-python
			pip install ultralytics
2. Open object_tracking directory in your IDE. Do not run the code as it won't work unless all the peripherals are connected. But, let PyCharm analyse your code.


------------
###### Now, you have successfully setup your system.



`
