import subprocess
import sys
from collections import defaultdict, deque

from kthread_sleep import sleep
from varpickler import encode_var
import numpy as np
from subprocess_multipipe.run_multipipe_subproc import start_subprocess
import os
import keyboard

cv2_show_image = sys.modules[__name__]

nested_dict = lambda: defaultdict(nested_dict)
cv2_show_image.mp_dict = nested_dict()
startp = os.path.normpath(os.path.join(os.path.dirname(__file__), "cv2imshowsafe.py"))
from subprocess_alive import is_process_alive

startupinfo = subprocess.STARTUPINFO()
creationflags = 0 | subprocess.CREATE_NO_WINDOW
startupinfo.wShowWindow = subprocess.SW_HIDE
invisibledict = {
    "startupinfo": startupinfo,
    "creationflags": creationflags,
}


def on_off(title, multi):
    cv2_show_image.mp_dict[title]["showscreenshot"] = not cv2_show_image.mp_dict[title][
        "showscreenshot"
    ]
    if not cv2_show_image.mp_dict[title]["showscreenshot"]:
        kill_cv2_imshow(title,multi)
    if not multi:
        cv2_show_image.mp_dict[title]["showscreenshot"] = True


def taskkill(pid):
    _ = subprocess.run(
        f"taskkill.exe /F /PID {pid}",
        start_new_session=True,
        **invisibledict,
        shell=False,
    )


def kill_cv2_imshow(title,multi=True):
    if multi:
        sleep(0.05)
    else:
        sleep(0.001)
    try:
        p = cv2_show_image.mp_dict[title]["cv2showprocesses"][-1].sub_process
    except Exception:
        pass
    try:
        runningthread = cv2_show_image.mp_dict[title]["cv2showprocesses"][
            -1
        ].write_thread
    except Exception:
        pass
    try:
        taskkill(p.pid)
    except Exception:
        pass
    try:
        while is_process_alive(p.pid):
            try:
                taskkill(p.pid)
            except Exception:
                pass
            try:
                if runningthread.is_alive():
                    try:
                        runningthread.kill()
                    except Exception:
                        pass
            except Exception:
                pass
    except Exception:
        pass


def cv2_imshow_multi(image: np.ndarray, title: str, killkeys: str = "ctrl+alt+q"):
    """Display multiple images using OpenCV's cv2.imshow function in a multi-process environment.

    Args:
        image (np.ndarray): The image to be displayed.
        title (str): The title of the image window.
        killkeys (str, optional): The key combination to toggle the image display on and off. Defaults to "ctrl+alt+q".
    """
    _cv2_imshow(image, title, killkeys, multi=True)


def cv2_imshow_single(image: np.ndarray, title: str, killkeys: str = "ctrl+alt+e"):
    """Display an image using OpenCV's cv2.imshow function in a single-process environment.

    Args:
        image (np.ndarray): The image to be displayed.
        title (str): The title of the image window.
        killkeys (str, optional): The key combination to toggle the image display on and off. Defaults to "ctrl+alt+e".
    """
    _cv2_imshow(image, title, killkeys, multi=False)


def _cv2_imshow(image: np.ndarray, title: str, killkeys="ctrl+alt+q", multi=True):
    if title not in cv2_show_image.mp_dict:
        cv2_show_image.mp_dict[title]["cv2showprocesses"] = deque([], 5)
        cv2_show_image.mp_dict[title]["showscreenshot"] = True
    if killkeys not in keyboard.__dict__["_hotkeys"]:
        keyboard.add_hotkey(killkeys, lambda: on_off(title, multi))
    if not cv2_show_image.mp_dict[title]["showscreenshot"]:
        return
    if cv2_show_image.mp_dict[title]["cv2showprocesses"]:
        wasok = cv2_show_image.mp_dict[title]["cv2showprocesses"][-1].write_function(
            image
        )
        if wasok:
            if not multi:
                if cv2_show_image.mp_dict[title]["showscreenshot"]:
                    wasok = cv2_show_image.mp_dict[title]["cv2showprocesses"][
                        -1
                    ].write_function(image)
            return
        else:
            imagesize = len(encode_var(image))
            cv2_show_image.mp_dict[title]["cv2showprocesses"].append(
                start_subprocess(
                    pyfile=startp,
                    bytesize=imagesize,
                    pipename=None,
                    deque_size=2,
                    pickle_or_dill="dill",
                    other_args=("--title", str(title), "--exitkeys", killkeys),
                )
            )
    else:
        imagesize = len(encode_var(image))
        cv2_show_image.mp_dict[title]["cv2showprocesses"].append(
            start_subprocess(
                pyfile=startp,
                bytesize=imagesize,
                pipename=None,
                deque_size=2,
                pickle_or_dill="dill",
                other_args=("--title", str(title), "--exitkeys", killkeys),
            )
        )

    _cv2_imshow(title=title, image=image, killkeys=killkeys, multi=multi)
