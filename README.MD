# cv2.imshow without freezing - Windows only 

#### Tested against Windows 10 / Python 3.10 / Anaconda

### pip install cv2imshow

This module provides a solution for the freezing issue encountered when updating images using OpenCV's cv2.imshow function
By addressing the freezing issue and providing non-blocking image display, this module enables smoother real-time image visualization 
in OpenCV applications and allows for improved user experience when working with image processing and computer vision tasks.

#### Non-blocking image display:

The module enables displaying images without freezing the execution of the program. 
It utilizes subprocess to offload the image display to a separate process, 
allowing the main program to continue running smoothly.

####  Multi-process support: 

The module supports displaying images in a multi-process environment, 
where multiple images can be shown simultaneously in separate windows without 
interfering with each other or causing freezing issues.
(Important: each window has to have a different title and a different combination for killkeys)

####  Keyboard control: 

The module provides an option to define a key combination that can be used to toggle the image display on and off. 
This allows for convenient control of image visualization during program execution.
When the specified kill shortcut is triggered, the module gracefully terminates the image display process, 
freeing system resources and ensuring a clean exit. This allows for easy and controlled termination 
of the image display functionality without causing any disruption or instability in the main program.

####  Memory efficiency: 

The module utilizes a queue-based mechanism to pass images between processes, 
ensuring efficient memory usage even when displaying large images or 
multiple images simultaneously.





### How to use it 

```python
from adbblitz import AdbShotTCP
from kthread_sleep import sleep
from cv2imshow.cv2imshow import cv2_imshow_single, cv2_imshow_multi
import numpy as np

shosho2 = AdbShotTCP(
    device_serial="localhost:5555",
    adb_path=r"C:\ProgramData\chocolatey\lib\scrcpy\tools\scrcpy-win64-v2.0\adb.exe",
    ip="127.0.0.1",
    port=5555,
    max_frame_rate=60,
    max_video_width=960,
    scrcpy_server_version="2.0",
    forward_port=None,
    frame_buffer=24,
    byte_package_size=131072,
    sleep_after_exception=0.01,
    log_level="info",
    lock_video_orientation=0,
)
bi = shosho2.get_one_screenshot()
cv2_imshow_single(
    title="pic2",
    image=bi.copy(),
    killkeys="ctrl+alt+q", # kills imshow
)
sleep(0.02)


with AdbShotTCP(
    device_serial="localhost:5555",
    adb_path=r"C:\ProgramData\chocolatey\lib\scrcpy\tools\scrcpy-win64-v2.0\adb.exe",
    ip="127.0.0.1",
    port=5555,
    max_frame_rate=60,
    max_video_width=960,
    scrcpy_server_version="2.0",
    forward_port=None,
    frame_buffer=24,
    byte_package_size=131072,
    sleep_after_exception=0.01,
    log_level="info",
    lock_video_orientation=0,
) as shosho:
    for bi in shosho:
        if bi.dtype == np.uint16:
            continue
        cv2_imshow_multi(
            title="pic3",
            image=bi,
            killkeys="ctrl+alt+h", # switch on/off
        )
        sleep(0.001)
```