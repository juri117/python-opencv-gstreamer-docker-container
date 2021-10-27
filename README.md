# docker container with opencv + gstreamer in python for openHD

This is a tutorial how to setup a docker container containing opencv with gstreamer integration for usage in python e.g. for [openHD](https://openhd.gitbook.io/open-hd/).
Tested with windows host.

## build container

```
docker build -t opencv-test .
```

## run container

* with windows file system folder mounted
```
winpty docker run -v //c/data:/home/data -p 5000:5000/udp -it opencv-test
```
* with wsl file system folder mounted
	* this is faster since docker and wsl share the same filesystem
```
winpty docker run -v //wsl$/Ubuntu-20.04/home/<user_name>/data:/home/data -it opencv-test
```
* note: `winpty` is required when executing on windows from git-bash

### setup wsl

in power shell:
```
wsl --set-default-version 2
wsl --install -d Ubuntu-20.04
wsl -l -o // options
wsl -l -v // installed

// to delete it:
wsl --unregister Ubuntu-20.04
```

in explorer: `\\wsl$`

### testing

* check for data traffic : `netcat -ul 5000`
* send test signal from console:
```
// sample signal
gst-launch-1.0 videotestsrc ! x264enc ! video/x-h264, stream-format=byte-stream ! udpsink host=127.0.0.1 port=5000
// from cam (untested)
gst-launch-1.0 v4l2src device=/dev/video0 ! h264parse ! avdec_h264 ! udpsink host=127.0.0.1 port=5000
```
* receive signal from console [source](https://openhd.gitbook.io/open-hd/ground-station-software/gstreamer):
```
gst-launch-1.0 udpsrc port=5000 ! h264parse ! avdec_h264 ! autovideosink sync=false
```


### run opencv + gstreamer in python

* create a new file *test.py* in your mounted data folder (e.g. *C:/data*) 
```
import time
import cv2

cap = cv2.VideoCapture("udpsrc port=5000 ! h264parse ! decodebin ! videoconvert ! appsink", cv2.CAP_GSTREAMER)
while True:
    ret,frame = cap.read()
    if not ret:
        print("no frame")
        time.sleep(1)
        continue
    print("got frame")
    cv2.imwrite('test.jpg', frame)
cv2.destroyAllWindows()
cap.release()
```
* connect your wifi to the openHD network, pw: `wifiopenhd`
* run the container and the python file
```
winpty docker run -v //c/data:/home/data -p 5000:5000/udp -it opencv-test
cd /home/data
python3 test.py
```
* end python script by pressing `ctrl + C`
