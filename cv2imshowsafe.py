import os
import sys
import keyboard
import cv2
from hackyargparser import add_sysargv
from kthread_sleep import sleep

from subprocess_multipipe.start_pipethread import stdincollection

titlename = "pic"
killkeys = "ctrl+alt+q"
stopall = False


def cv2_waitkey():
    if cv2.waitKey(20):
        pass


def killit():
    global stopall
    stopall = True
    keyboard.remove_all_hotkeys()


@add_sysargv
def imagestart(title: str = "pic", exitkeys: str = "ctrl+alt+q"):
    global titlename
    global killkeys
    killkeys = exitkeys
    titlename = title
    keyboard.add_hotkey(exitkeys, killit)


imagestart()
cv2.startWindowThread()
cv2.namedWindow(titlename, cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)
while not stopall:
    if not stdincollection.stdin_deque:
        sleep(0.02)
        continue
    cv2.imshow(titlename, stdincollection.stdin_deque[-1])
    cv2_waitkey()
cv2.destroyAllWindows()
try:
    sys.exit(0)
finally:
    os._exit(0)
