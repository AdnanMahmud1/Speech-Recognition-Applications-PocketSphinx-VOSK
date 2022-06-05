import argparse
import json
import os
import queue
import webbrowser

import sounddevice as sd
import vosk
import sys
import pyautogui
import pyttsx3
import subprocess
from timeit import default_timer as timer

engine = pyttsx3.init()
q = queue.Queue()


def speech_start_callback(msg):

    engine.say(msg)
    engine.runAndWait()


def notepad_function():
    subprocess.Popen(["notepad", "filename.txt"])



def paint_function():
    speech_start_callback("Paint Started")
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
    main()


def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text


def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))


def functionToProcess(parser):
    ##parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument(
        '-l', '--list-devices', action='store_true',
        help='show list of audio devices and exit')
    args, remaining = parser.parse_known_args()
    if args.list_devices:
        print(sd.query_devices())
        parser.exit(0)
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        parents=[parser])
    parser.add_argument(
        '-f', '--filename', type=str, metavar='FILENAME',
        help='audio file to store recording to')
    parser.add_argument(
        '-m', '--model', type=str, metavar='MODEL_PATH',
        help='Path to the model')
    parser.add_argument(
        '-d', '--device', type=int_or_str,
        help='input device (numeric ID or substring)')
    parser.add_argument(
        '-r', '--samplerate', type=int, help='sampling rate')
    args = parser.parse_args(remaining)
    return args


def main():

    parser = argparse.ArgumentParser(add_help=False)
    args = functionToProcess(parser)
    try:
        if args.model is None:
            args.model = "model"
        if not os.path.exists(args.model):
            parser.exit(0)
        if args.samplerate is None:
            device_info = sd.query_devices(args.device, 'input')
            # soundfile expects an int, sounddevice provides a float:
            args.samplerate = int(device_info['default_samplerate'])
        model = vosk.Model(args.model)
        if args.filename:
            dump_fn = open(args.filename, "wb")
        else:
            dump_fn = None
        with sd.RawInputStream(samplerate=args.samplerate, blocksize=16000, device=args.device, dtype='int16',
                               channels=1, callback=callback):
            speech_start_callback("Please start your speech")
            phrases = '["start open mouse paint browser type show menu click enter please exit tab undo move scroll left right up down program", "[unk]"]'
            rec = vosk.KaldiRecognizer(model, args.samplerate, phrases)
            while True:
                start = timer()

                data = q.get()
                if rec.AcceptWaveform(data):
                    sp = rec.Result()
                    textResults = []
                    if sp:
                        print(sp)
                        resultDict = json.loads(sp)
                        getRawText = resultDict.get("text", "")
                        textResults.append(getRawText)
                        #print("main Speech:"+ getRawText)
                        print(format(timer() - start, '.2f') + ' sec')
                        processAutomation(sp)



                else:
                    texts = rec.PartialResult()
                if dump_fn is not None:
                    dump_fn.write(data)
    except KeyboardInterrupt:
        print('\nDone')
        parser.exit(0)
    except Exception as e:
        parser.exit(type(e).__name__ + ': ' + str(e))


def processAutomation(sp):
    if 'start paint' in sp:
        ##paint_function()
        print("-----Paint Started")
        ##exit(0)
    elif 'start browser' in sp:
        print("-----Browser Started")
        webbrowser.open('https://www.google.co.uk/')
    elif 'move left' in sp:
        print("-----Moving Left")

        pyautogui.moveRel(-50, 0, duration=0.5)
    elif 'move right' in sp:
        print("-----Moving Right")
        pyautogui.moveRel(50, 0, duration=0.5)
    elif 'move up' in sp:
        print("-----Moving Up")
        pyautogui.moveRel(0, -50, duration=0.5)
    elif 'move down' in sp:
        print('-----Moving Down')
        pyautogui.moveRel(0, 50, duration=0.5)

    elif 'scroll up' in sp:
        print("-----scrolling Up")
        pyautogui.scroll(300)
    elif 'scroll down' in sp:
        print("-----scrolling down")
        pyautogui.scroll(-300)

    elif 'show menu' in sp:
        pyautogui.click(button='right')
        print("-----Showing Menu")
    elif 'click' in sp:
        pyautogui.click()
        print("-----clicked")
    elif 'type' in sp:
        pyautogui.click()

        pyautogui.write('Hello, world!')
    elif 'undo' in sp:
        print("-----undoing")
        pyautogui.hotkey('ctrl', 'z')
    elif 'enter' in sp:
        print("-----Enter Pressed")
        pyautogui.press('enter')
    elif 'tab' in sp:
        print("-----tab Pressed")
        pyautogui.hotkey('tab')
    elif 'exit program' in sp:
        print("-----Exiting program")
        speech_start_callback("Exiting program")
        exit(0)


if __name__ == "__main__":
    main()
