import re
import subprocess
import webbrowser
import pyautogui
from pyaudio import PyAudio, paInt16
from sphinxwrapper import *
import time
from timeit import default_timer as timer


def paint_function():

    subprocess.Popen(['C:\Windows\system32\mspaint.exe'])
    pyautogui.moveTo(450, 450, 2)
    distance = 200
    while distance > 0:
        pyautogui.drag(distance, 0, duration=0.05)  # move right
        distance -= 5
        pyautogui.drag(0, distance, duration=0.05)  # move down
        pyautogui.drag(-distance, 0, duration=0.05)  # move left
        distance -= 5
        pyautogui.drag(0, -distance, duration=0.05)  # move up
    mouseMain()


def mouseMain():
    MODELDIR = get_model_path()
    cfg = DefaultConfig()

    cfg.set_string('-logfn', 'nul')

    cfg.set_string("-jsgf", "mouseMovements.jsgf")

    ps = PocketSphinx(cfg)

    def mouseMoveFunctionWithJSGF(hyp):
        sp = hyp.hypstr if hyp else None
        print(format(timer() - start, '.2f') + ' sec')
        #print("main Speech:", sp)
        if sp:
            if 'move left' in sp:
                print("-----Left")
                pyautogui.moveRel(-50, 0, duration=0.5)
            elif 'move right' in sp:
                print("-----Right")
                pyautogui.moveRel(50, 0, duration=0.5)
            elif 'move up' in sp:
                print("-----Up")
                pyautogui.moveRel(0, -50, duration=0.5)
            elif 'move down' in sp:
                print('-----Down')
                pyautogui.moveRel(0, 50, duration=0.5)
            elif 'scroll up' in sp:
                print("-----scrolling Up")
                pyautogui.scroll(300)
            elif 'scroll down' in sp:
                print("-----scrolling down")
                pyautogui.scroll(-300)
            elif 'show menu' in sp:
                print("-----showing Menu")


                pyautogui.click(button='right')
            elif 'click' in sp:
                print("-----Single left click or select")
                pyautogui.click()
            elif 'enter' in sp:
                print("-----Enter Pressed")
                pyautogui.press('enter')
            elif 'tab' in sp:
                print("-----tab")
                pyautogui.click()
                pyautogui.write('Hello, world!')
            elif 'type' in sp:
                print("-----typing")
                pyautogui.click()
                pyautogui.write('Hello, world!')
            elif 'tab' in sp:
                print("-----tab Pressed")
                pyautogui.hotkey('tab')
            elif 'undo' in sp:
                print("-----undoing")
                pyautogui.hotkey('ctrl', 'z')
            if 'start' in sp:
                if 'paint' in sp:
                    print("-----start Painting")
                    #paint_function()
                    #exit(0)
                elif 'browser' in sp:
                    print("-----Opening Browser")
                    webbrowser.open('https://www.google.co.uk/')
            elif 'exit program' in sp:
                #print("-----Exiting Program")

                exit(0)

        else:


            print("Didn't hear keyphrase. Continuing.")

    ps.hypothesis_callback = mouseMoveFunctionWithJSGF

    # Recognise from the mic in a loop

    p = PyAudio()
    stream = p.open(format=paInt16, channels=1, rate=16000, input=True,
                    frames_per_buffer=2048)

    stream.start_stream()
    while True:
        start = timer()
        ps.process_audio(stream.read(2048))
        #time.sleep(0.1)


if __name__ == "__main__":
    mouseMain()
