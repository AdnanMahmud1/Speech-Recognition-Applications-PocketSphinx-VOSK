import webbrowser
import re
import pyautogui
import time
from pyaudio import PyAudio, paInt16
from sphinxwrapper import *
from timeit import default_timer as timer


def main():
    cfg = DefaultConfig()
    cfg.set_string('-logfn', 'nul')
    ps = PocketSphinx(cfg)
    keywords_list = {

        "move": 1e-5,
        "left": 1e-5,
        "right": 1e-5,
        "up": 1e-5,
        "down": 1e-7,
        "click": 1e-10,
        "enter": 1e-10,
        "tab": 1e-8,
        "scroll": 1e-10,
        "type": 1e-8,
        "undo": 1e-8,
        "show menu": 1e-15,
        "start browser": 1e-8,
        "start paint": 1e-25,
        "exit program": 1e-20,

    }

    # Set a keywords search using a dictionary
    ps.set_kws_list("kws", keywords_list)
    ps.active_search = "kws"

    def hyp_callback(hyp):
        s = hyp.hypstr if hyp else None
        print(format(timer() - start, '.2f') + ' sec')
        if s:
            #print("----main Speech:", s)

            if 'move' in str(s):
                if 'left' in str(s):
                    print("Moving Left")
                    pyautogui.moveRel(-30, 0, duration=0.5)
                elif 'right' in str(s):
                    print("Moving Right")
                    pyautogui.moveRel(30, 0, duration=0.5)
                elif 'up' in str(s):
                    print("Moving Up")
                    pyautogui.moveRel(0, -30, duration=0.5)
                elif 'down' in str(s):
                    print('Moving Down')
                    pyautogui.moveRel(0, 30, duration=0.5)
            elif 'scroll' in str(s):
                if 'down' in str(s):
                    print("scrolling down." + s)
                    pyautogui.scroll(-300)
                elif 'up':
                    print("scrolling up." + s)
                    pyautogui.scroll(300)
            elif 'show menu' in str(s):
                print("Showing menu" % s)
                pyautogui.click(button='right')
            elif 'click' in s:
                print("Clicking")
                pyautogui.click()
            elif 'undo' in s:
                print("undoing")
            elif 'start paint' in s:
                print("Paint Command detected")
                distance = 200
                pyautogui.drag(distance, 0, duration=0.5)  # move right
                distance -= 5
                pyautogui.drag(0, distance, duration=0.5)  # move down
                pyautogui.drag(-distance, 0, duration=0.5)  # move left
                distance -= 5
                pyautogui.drag(0, -distance, duration=0.5)  # move up

            elif 'start browser' in s:
                print("Opening Browser")
                webbrowser.open('https://www.google.co.uk/')
               ##returnHello, world!
            elif 'tab' in s:
                print("-----tab Pressed")
                pyautogui.hotkey('tab')
            elif 'type' in s:
                print("Type ")
                pyautogui.click()
                pyautogui.write('Hello, world!')
            elif 'enter' in s:
                print("Enter command found")
                pyautogui.press('enter')
            elif 'exit program' in s:
                print("Exiting Program")

           ##exit(0)Hello, world!
        else:
            print("Didn't hear keyphrase. Continuing....")

    # Set up callbacks
    ##ps.speech_start_callback = speech_start_callback
    ps.hypothesis_callback = hyp_callback

    # Recognise from the mic in a loop
    p = PyAudio()
    stream = p.open(format=paInt16, channels=1, rate=16000, input=True,
                    frames_per_buffer=2048)
    stream.start_stream()
    while True:
        start = timer()
        ps.process_audio(stream.read(2048))
        #time.sleep(0.05)


if __name__ == "__main__":
    main()
