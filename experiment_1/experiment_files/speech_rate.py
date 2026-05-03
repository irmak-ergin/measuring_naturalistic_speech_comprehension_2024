#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2023.2.3),
    on Mon Feb 12 15:58:03 2024
If you publish work using this script the most relevant publication is:

    Peirce J, Gray JR, Simpson S, MacAskill M, Höchenberger R, Sogo H, Kastman E, Lindeløv JK. (2019) 
        PsychoPy2: Experiments in behavior made easy Behav Res 51: 195. 
        https://doi.org/10.3758/s13428-018-01193-y

"""

# --- Import packages ---
from psychopy import locale_setup
from psychopy import prefs
from psychopy import plugins
plugins.activatePlugins()
prefs.hardware['audioLib'] = 'ptb'
prefs.hardware['audioLatencyMode'] = '4'
from psychopy import sound, gui, visual, core, data, event, logging, clock, colors, layout
from psychopy.tools import environmenttools
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER, priority)

import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle, choice as randchoice
import os  # handy system and path functions
import sys  # to get file system encoding

from psychopy.hardware import keyboard

# Run 'Before Experiment' code from slider_code
import serial
import time
import serial.tools.list_ports
import multiprocessing as mp
import csv

def workerBody(participant, session, stop, trial, ready, queue):
    output_data = []
    ports = serial.tools.list_ports.comports()
    for port, desc, hwid in sorted(ports):
        if desc == "Feather M0 Express":
            port2 = port

    ser = serial.Serial(port2, 500000, timeout=0.01)
    ready.set()
    while not stop.is_set():
        ser.readline()
        if trial.is_set():
            ready.clear()
            trial_start_time = time.monotonic()
            while trial.is_set():
                line = ser.readline()
                try:
                    output_data.append(
                        (int(line.decode("utf-8").split(' ')[0]), int(line.decode("utf-8").split(' ')[1])))
                except:
                    print("Warning: missing frame")

            try:
                real_time_elapsed = 1000 * (time.monotonic() - trial_start_time)
                drift = real_time_elapsed - (output_data[-1][1] - output_data[0][1])
                print((drift / (output_data[-1][1] - output_data[0][1])) * 100)

                offset = output_data[0][1]
                for i, pt in enumerate(output_data):
                    output_data[i] = (pt[0], pt[1] - offset)
                
                print(f"{_thisDir}/data/slider_{participant}_{session}_{queue.get()}.csv")
                with open(f"{_thisDir}/data/slider_{participant}_{session}_{queue.get()}.csv",'w') as out:
                    csv_out=csv.writer(out)
                    csv_out.writerow([drift, real_time_elapsed])
                    csv_out.writerow(['value','time'])
                    for row in output_data:
                        csv_out.writerow(row)

            except Exception as error:
                print("Error occured while processing last trial. Data discarded")
                print(error)

            output_data.clear()
            ready.set()
    ser.close()


class Slider:
    def __init__(self, participant, session):
        mp.set_start_method('spawn')
        self.stop = mp.Event()
        self.trial = mp.Event()
        self.ready = mp.Event()
        self.queue = mp.Queue()
        self.proc = mp.Process(target=workerBody, args=(
            participant, session, self.stop, self.trial, self.ready, self.queue))
        self.proc.start()

    def start_trial(self, wav_file):
        if not self.proc.is_alive():
            raise Exception("Error: Slider process exited")
        else:
            self.ready.wait()
            self.trial.set()
            self.queue.put(wav_file)

    def stop_trial(self):
        self.trial.clear()
        if not self.proc.is_alive():
            raise Exception("Error: Slider process exited")
        else:
            self.ready.wait()

    def __del__(self):
        self.stop.set()
        self.proc.join()

# Run 'Before Experiment' code from slider_code
import serial
import time
import serial.tools.list_ports
import multiprocessing as mp
import csv

def workerBody(participant, session, stop, trial, ready, queue):
    output_data = []
    ports = serial.tools.list_ports.comports()
    for port, desc, hwid in sorted(ports):
        if desc == "Feather M0 Express":
            port2 = port

    ser = serial.Serial(port2, 500000, timeout=0.01)
    ready.set()
    while not stop.is_set():
        ser.readline()
        if trial.is_set():
            ready.clear()
            trial_start_time = time.monotonic()
            while trial.is_set():
                line = ser.readline()
                try:
                    output_data.append(
                        (int(line.decode("utf-8").split(' ')[0]), int(line.decode("utf-8").split(' ')[1])))
                except:
                    print("Warning: missing frame")

            try:
                real_time_elapsed = 1000 * (time.monotonic() - trial_start_time)
                drift = real_time_elapsed - (output_data[-1][1] - output_data[0][1])
                print((drift / (output_data[-1][1] - output_data[0][1])) * 100)

                offset = output_data[0][1]
                for i, pt in enumerate(output_data):
                    output_data[i] = (pt[0], pt[1] - offset)
                
                print(f"{_thisDir}/data/slider_{participant}_{session}_{queue.get()}.csv")
                with open(f"{_thisDir}/data/slider_{participant}_{session}_{queue.get()}.csv",'w') as out:
                    csv_out=csv.writer(out)
                    csv_out.writerow([drift, real_time_elapsed])
                    csv_out.writerow(['value','time'])
                    for row in output_data:
                        csv_out.writerow(row)

            except Exception as error:
                print("Error occured while processing last trial. Data discarded")
                print(error)

            output_data.clear()
            ready.set()
    ser.close()


class Slider:
    def __init__(self, participant, session):
        mp.set_start_method('spawn')
        self.stop = mp.Event()
        self.trial = mp.Event()
        self.ready = mp.Event()
        self.queue = mp.Queue()
        self.proc = mp.Process(target=workerBody, args=(
            participant, session, self.stop, self.trial, self.ready, self.queue))
        self.proc.start()

    def start_trial(self, wav_file):
        if not self.proc.is_alive():
            raise Exception("Error: Slider process exited")
        else:
            self.ready.wait()
            self.trial.set()
            self.queue.put(wav_file)

    def stop_trial(self):
        self.trial.clear()
        if not self.proc.is_alive():
            raise Exception("Error: Slider process exited")
        else:
            self.ready.wait()

    def __del__(self):
        self.stop.set()
        self.proc.join()

# --- Setup global variables (available in all functions) ---
# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
# Store info about the experiment session
psychopyVersion = '2023.2.3'
expName = 'speech_rate'  # from the Builder filename that created this script
expInfo = {
    'participant': '',
    'session': '001',
    'date': data.getDateStr(),  # add a simple timestamp
    'expName': expName,
    'psychopyVersion': psychopyVersion,
}


def showExpInfoDlg(expInfo):
    """
    Show participant info dialog.
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    
    Returns
    ==========
    dict
        Information about this experiment.
    """
    # temporarily remove keys which the dialog doesn't need to show
    poppedKeys = {
        'date': expInfo.pop('date', data.getDateStr()),
        'expName': expInfo.pop('expName', expName),
        'psychopyVersion': expInfo.pop('psychopyVersion', psychopyVersion),
    }
    # show participant info dialog
    dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expName)
    if dlg.OK == False:
        core.quit()  # user pressed cancel
    # restore hidden keys
    expInfo.update(poppedKeys)
    # return expInfo
    return expInfo


def setupData(expInfo, dataDir=None):
    """
    Make an ExperimentHandler to handle trials and saving.
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    dataDir : Path, str or None
        Folder to save the data to, leave as None to create a folder in the current directory.    
    Returns
    ==========
    psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    """
    
    # data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
    if dataDir is None:
        dataDir = _thisDir
    filename = u'data/%s_%s_%s' % (expInfo['participant'], expName, expInfo['date'])
    # make sure filename is relative to dataDir
    if os.path.isabs(filename):
        dataDir = os.path.commonprefix([dataDir, filename])
        filename = os.path.relpath(filename, dataDir)
    
    # an ExperimentHandler isn't essential but helps with data saving
    thisExp = data.ExperimentHandler(
        name=expName, version='',
        extraInfo=expInfo, runtimeInfo=None,
        originPath='/Users/irmakergin/Desktop/Experiment/speech_rate.py',
        savePickle=True, saveWideText=True,
        dataFileName=dataDir + os.sep + filename, sortColumns='time'
    )
    thisExp.setPriority('thisRow.t', priority.CRITICAL)
    thisExp.setPriority('expName', priority.LOW)
    # return experiment handler
    return thisExp


def setupLogging(filename):
    """
    Setup a log file and tell it what level to log at.
    
    Parameters
    ==========
    filename : str or pathlib.Path
        Filename to save log file and data files as, doesn't need an extension.
    
    Returns
    ==========
    psychopy.logging.LogFile
        Text stream to receive inputs from the logging system.
    """
    # this outputs to the screen, not a file
    logging.console.setLevel(logging.EXP)


def setupWindow(expInfo=None, win=None):
    """
    Setup the Window
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    win : psychopy.visual.Window
        Window to setup - leave as None to create a new window.
    
    Returns
    ==========
    psychopy.visual.Window
        Window in which to run this experiment.
    """
    if win is None:
        # if not given a window to setup, make one
        win = visual.Window(
            size=[1512, 982], fullscr=False, screen=0,
            winType='pyglet', allowStencil=False,
            monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
            backgroundImage='', backgroundFit='none',
            blendMode='avg', useFBO=True,
            units='height'
        )
        if expInfo is not None:
            # store frame rate of monitor if we can measure it
            expInfo['frameRate'] = win.getActualFrameRate()
    else:
        # if we have a window, just set the attributes which are safe to set
        win.color = [0,0,0]
        win.colorSpace = 'rgb'
        win.backgroundImage = ''
        win.backgroundFit = 'none'
        win.units = 'height'
    win.mouseVisible = True
    win.hideMessage()
    return win


def setupInputs(expInfo, thisExp, win):
    """
    Setup whatever inputs are available (mouse, keyboard, eyetracker, etc.)
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    win : psychopy.visual.Window
        Window in which to run this experiment.
    Returns
    ==========
    dict
        Dictionary of input devices by name.
    """
    # --- Setup input devices ---
    inputs = {}
    ioConfig = {}
    ioSession = ioServer = eyetracker = None
    
    # create a default keyboard (e.g. to check for escape)
    defaultKeyboard = keyboard.Keyboard(backend='event')
    # return inputs dict
    return {
        'ioServer': ioServer,
        'defaultKeyboard': defaultKeyboard,
        'eyetracker': eyetracker,
    }

def pauseExperiment(thisExp, inputs=None, win=None, timers=[], playbackComponents=[]):
    """
    Pause this experiment, preventing the flow from advancing to the next routine until resumed.
    
    Parameters
    ==========
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    inputs : dict
        Dictionary of input devices by name.
    win : psychopy.visual.Window
        Window for this experiment.
    timers : list, tuple
        List of timers to reset once pausing is finished.
    playbackComponents : list, tuple
        List of any components with a `pause` method which need to be paused.
    """
    # if we are not paused, do nothing
    if thisExp.status != PAUSED:
        return
    
    # pause any playback components
    for comp in playbackComponents:
        comp.pause()
    # prevent components from auto-drawing
    win.stashAutoDraw()
    # run a while loop while we wait to unpause
    while thisExp.status == PAUSED:
        # make sure we have a keyboard
        if inputs is None:
            inputs = {
                'defaultKeyboard': keyboard.Keyboard(backend='Pyglet')
            }
        # check for quit (typically the Esc key)
        if inputs['defaultKeyboard'].getKeys(keyList=['escape']):
            endExperiment(thisExp, win=win, inputs=inputs)
        # flip the screen
        win.flip()
    # if stop was requested while paused, quit
    if thisExp.status == FINISHED:
        endExperiment(thisExp, inputs=inputs, win=win)
    # resume any playback components
    for comp in playbackComponents:
        comp.play()
    # restore auto-drawn components
    win.retrieveAutoDraw()
    # reset any timers
    for timer in timers:
        timer.reset()


def run(expInfo, thisExp, win, inputs, globalClock=None, thisSession=None):
    """
    Run the experiment flow.
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    psychopy.visual.Window
        Window in which to run this experiment.
    inputs : dict
        Dictionary of input devices by name.
    globalClock : psychopy.core.clock.Clock or None
        Clock to get global time from - supply None to make a new one.
    thisSession : psychopy.session.Session or None
        Handle of the Session object this experiment is being run from, if any.
    """
    # mark experiment as started
    thisExp.status = STARTED
    # make sure variables created by exec are available globally
    exec = environmenttools.setExecEnvironment(globals())
    # get device handles from dict of input devices
    ioServer = inputs['ioServer']
    defaultKeyboard = inputs['defaultKeyboard']
    eyetracker = inputs['eyetracker']
    # make sure we're running in the directory for this experiment
    os.chdir(_thisDir)
    # get filename from ExperimentHandler for convenience
    filename = thisExp.dataFileName
    frameTolerance = 0.001  # how close to onset before 'same' frame
    endExpNow = False  # flag for 'escape' or other condition => quit the exp
    # get frame duration from frame rate in expInfo
    if 'frameRate' in expInfo and expInfo['frameRate'] is not None:
        frameDur = 1.0 / round(expInfo['frameRate'])
    else:
        frameDur = 1.0 / 60.0  # could not measure, so guess
    
    # Start Code - component code to be run after the window creation
    # Make folder to store recordings from mic
    micRecFolder = filename + '_mic_recorded'
    if not os.path.isdir(micRecFolder):
        os.mkdir(micRecFolder)
    # Make folder to store recordings from mic
    micRecFolder = filename + '_mic_recorded'
    if not os.path.isdir(micRecFolder):
        os.mkdir(micRecFolder)
    
    # --- Initialize components for Routine "Instructions" ---
    text = visual.TextStim(win=win, name='text',
        text="Welcome!\n\nIn this experiment, you will hear 180 audio segments with varying speeds of speech and durations. You will be asked to:\n\n1. While listening to each segment, continuously indicate your level of comprehension using the slider.\n\n2. After the listening, rate your understanding on a scale from 1 to 10.\n\n3. Verbally summarize what you heard.\n\n4. Answer a multiple-choice question.\n\nThe segments you will hear are about an actress named Franny living in NYC with her two flatmates, Jane and Dan.\n\nDon't worry if it's not clear yet! We have two training rounds with the slowest and fastest speeds. ",
        font='Open Sans',
        pos=(0, 0), height=0.03, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    button = visual.ButtonStim(win, 
        text='Start Trial', font='Arvo',
        pos=(0,-0.4),
        letterHeight=0.03,
        size=(0.2, 0.1), borderWidth=0.0,
        fillColor='darkgrey', borderColor=None,
        color='white', colorSpace='rgb',
        opacity=None,
        bold=True, italic=False,
        padding=None,
        anchor='center',
        name='button',
        depth=-1
    )
    button.buttonClock = core.Clock()
    
    # --- Initialize components for Routine "Start_Segment_Train" ---
    Play_train = visual.ButtonStim(win, 
        text='Play', font='Arvo',
        pos=(0, 0),
        letterHeight=0.05,
        size=(0.5, 0.5), borderWidth=0.0,
        fillColor='darkgrey', borderColor=None,
        color='white', colorSpace='rgb',
        opacity=None,
        bold=True, italic=False,
        padding=None,
        anchor='center',
        name='Play_train',
        depth=0
    )
    Play_train.buttonClock = core.Clock()
    Trial_counter_train = visual.TextStim(win=win, name='Trial_counter_train',
        text='',
        font='Open Sans',
        pos=(0.3, 0.4), height=0.02, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    text_5 = visual.TextStim(win=win, name='text_5',
        text='Please reset the slider.',
        font='Open Sans',
        pos=(0, 0.3), height=0.03, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-2.0);
    
    # --- Initialize components for Routine "Training_Segment" ---
    Experimen_audio = sound.Sound('A', secs=-1, stereo=True, hamming=True,
        name='Experimen_audio')
    Experimen_audio.setVolume(1.0)
    # Run 'Begin Experiment' code from slider_code
    myslider = Slider(expInfo['participant'], expInfo['session'])
    
    
    # --- Initialize components for Routine "Rating" ---
    slider = visual.Slider(win=win, name='slider',
        startValue=None, size=(1.0, 0.1), pos=(0,0), units=win.units,
        labels=(1, 2, 3, 4, 5, 6, 7, 8, 9, 10), ticks=(1, 2, 3, 4, 5, 6, 7, 8, 9, 10), granularity=0.0,
        style='rating', styleTweaks=('labels45', 'triangleMarker'), opacity=None,
        labelColor='LightGray', markerColor='Red', lineColor='White', colorSpace='rgb',
        font='Open Sans', labelHeight=0.05,
        flip=False, ori=0.0, depth=0, readOnly=False)
    button_2 = visual.ButtonStim(win, 
        text='Confirm', font='Arvo',
        pos=(0,-0.4),
        letterHeight=0.03,
        size=(0.2, 0.1), borderWidth=0.0,
        fillColor='darkgrey', borderColor=None,
        color='white', colorSpace='rgb',
        opacity=None,
        bold=True, italic=False,
        padding=None,
        anchor='center',
        name='button_2',
        depth=-1
    )
    button_2.buttonClock = core.Clock()
    text_3 = visual.TextStim(win=win, name='text_3',
        text='How well did you understand it?',
        font='Open Sans',
        pos=(0, 0.4), height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-2.0);
    
    # --- Initialize components for Routine "Start_Summary" ---
    text_2 = visual.TextStim(win=win, name='text_2',
        text="Click on the 'Start Talking' button below to begin your verbal summary. You'll have 15 seconds to speak. \nIf you're unable to report anything, you may choose to skip the verbal summary by clicking on the 'Skip Summary' button.",
        font='Open Sans',
        pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    summary_button = visual.ButtonStim(win, 
        text='Start Talking', font='Arvo',
        pos=(0.5,-0.4),
        letterHeight=0.02,
        size=(0.2, 0.1), borderWidth=0.0,
        fillColor='darkgrey', borderColor=None,
        color='white', colorSpace='rgb',
        opacity=None,
        bold=True, italic=False,
        padding=None,
        anchor='center',
        name='summary_button',
        depth=-1
    )
    summary_button.buttonClock = core.Clock()
    skip_button = visual.ButtonStim(win, 
        text='Skip Summary', font='Arvo',
        pos=(-0.5,-0.4),
        letterHeight=0.02,
        size=(0.2, 0.1), borderWidth=0.0,
        fillColor='darkgrey', borderColor=None,
        color='white', colorSpace='rgb',
        opacity=None,
        bold=True, italic=False,
        padding=None,
        anchor='center',
        name='skip_button',
        depth=-2
    )
    skip_button.buttonClock = core.Clock()
    # create a microphone object for device: MacBook Pro Microphone
    macBookProMicrophone = sound.microphone.Microphone(
        device='0', channels=None, 
        sampleRateHz=48000, maxRecordingSize=24000.0
    )
    
    # --- Initialize components for Routine "Summary" ---
    # link mic to device object
    mic = macBookProMicrophone
    countdown = visual.TextStim(win=win, name='countdown',
        text='',
        font='Open Sans',
        pos=(0, 0), height=0.1, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    
    # --- Initialize components for Routine "Multiple_Choice_2" ---
    Question = visual.TextStim(win=win, name='Question',
        text='',
        font='Open Sans',
        pos=(0, 0.2), height=0.03, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    Option_1 = visual.TextStim(win=win, name='Option_1',
        text='',
        font='Open Sans',
        pos=(0, 0.1), height=0.03, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    Option_2 = visual.TextStim(win=win, name='Option_2',
        text='',
        font='Open Sans',
        pos=(0,0), height=0.03, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-2.0);
    Option_3 = visual.TextStim(win=win, name='Option_3',
        text='',
        font='Open Sans',
        pos=(0, -0.1), height=0.03, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-3.0);
    Option_4 = visual.TextStim(win=win, name='Option_4',
        text='',
        font='Open Sans',
        pos=(0, -0.2), height=0.03, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-4.0);
    A = visual.ButtonStim(win, 
        text='A', font='Arvo',
        pos=(-0.4,-0.4),
        letterHeight=0.03,
        size=(0.1, 0.1), borderWidth=0.0,
        fillColor='darkgrey', borderColor=None,
        color='white', colorSpace='rgb',
        opacity=None,
        bold=True, italic=False,
        padding=None,
        anchor='center',
        name='A',
        depth=-5
    )
    A.buttonClock = core.Clock()
    B = visual.ButtonStim(win, 
        text='B', font='Arvo',
        pos=(-0.1,-0.4),
        letterHeight=0.03,
        size=(0.1, 0.1), borderWidth=0.0,
        fillColor='darkgrey', borderColor=None,
        color='white', colorSpace='rgb',
        opacity=None,
        bold=True, italic=False,
        padding=None,
        anchor='center',
        name='B',
        depth=-6
    )
    B.buttonClock = core.Clock()
    C = visual.ButtonStim(win, 
        text='C', font='Arvo',
        pos=(0.2,-0.4),
        letterHeight=0.03,
        size=(0.1, 0.1), borderWidth=0.0,
        fillColor='darkgrey', borderColor=None,
        color='white', colorSpace='rgb',
        opacity=None,
        bold=True, italic=False,
        padding=None,
        anchor='center',
        name='C',
        depth=-7
    )
    C.buttonClock = core.Clock()
    D = visual.ButtonStim(win, 
        text='D', font='Arvo',
        pos=(0.5,-0.4),
        letterHeight=0.03,
        size=(0.1, 0.1), borderWidth=0.0,
        fillColor='darkgrey', borderColor=None,
        color='white', colorSpace='rgb',
        opacity=None,
        bold=True, italic=False,
        padding=None,
        anchor='center',
        name='D',
        depth=-8
    )
    D.buttonClock = core.Clock()
    
    # --- Initialize components for Routine "Start_Exp" ---
    Start_exp = visual.TextStim(win=win, name='Start_exp',
        text='Press the button below to start the experiment.',
        font='Open Sans',
        pos=(0, 0.4), height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    Start = visual.ButtonStim(win, 
        text='Start', font='Arvo',
        pos=(0, 0),
        letterHeight=0.05,
        size=(0.5, 0.5), borderWidth=0.0,
        fillColor='darkgrey', borderColor=None,
        color='white', colorSpace='rgb',
        opacity=None,
        bold=True, italic=False,
        padding=None,
        anchor='center',
        name='Start',
        depth=-1
    )
    Start.buttonClock = core.Clock()
    
    # --- Initialize components for Routine "Start_Segment" ---
    Play = visual.ButtonStim(win, 
        text='Play', font='Arvo',
        pos=(0, 0),
        letterHeight=0.05,
        size=(0.5, 0.5), borderWidth=0.0,
        fillColor='darkgrey', borderColor=None,
        color='white', colorSpace='rgb',
        opacity=None,
        bold=True, italic=False,
        padding=None,
        anchor='center',
        name='Play',
        depth=0
    )
    Play.buttonClock = core.Clock()
    Trial_counter = visual.TextStim(win=win, name='Trial_counter',
        text='',
        font='Open Sans',
        pos=(0.3, 0.4), height=0.02, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    text_6 = visual.TextStim(win=win, name='text_6',
        text='Please reset the slider.',
        font='Open Sans',
        pos=(0, 0.3), height=0.03, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-2.0);
    
    # --- Initialize components for Routine "Training_Segment" ---
    Experimen_audio = sound.Sound('A', secs=-1, stereo=True, hamming=True,
        name='Experimen_audio')
    Experimen_audio.setVolume(1.0)
    # Run 'Begin Experiment' code from slider_code
    myslider = Slider(expInfo['participant'], expInfo['session'])
    
    
    # --- Initialize components for Routine "Rating" ---
    slider = visual.Slider(win=win, name='slider',
        startValue=None, size=(1.0, 0.1), pos=(0,0), units=win.units,
        labels=(1, 2, 3, 4, 5, 6, 7, 8, 9, 10), ticks=(1, 2, 3, 4, 5, 6, 7, 8, 9, 10), granularity=0.0,
        style='rating', styleTweaks=('labels45', 'triangleMarker'), opacity=None,
        labelColor='LightGray', markerColor='Red', lineColor='White', colorSpace='rgb',
        font='Open Sans', labelHeight=0.05,
        flip=False, ori=0.0, depth=0, readOnly=False)
    button_2 = visual.ButtonStim(win, 
        text='Confirm', font='Arvo',
        pos=(0,-0.4),
        letterHeight=0.03,
        size=(0.2, 0.1), borderWidth=0.0,
        fillColor='darkgrey', borderColor=None,
        color='white', colorSpace='rgb',
        opacity=None,
        bold=True, italic=False,
        padding=None,
        anchor='center',
        name='button_2',
        depth=-1
    )
    button_2.buttonClock = core.Clock()
    text_3 = visual.TextStim(win=win, name='text_3',
        text='How well did you understand it?',
        font='Open Sans',
        pos=(0, 0.4), height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-2.0);
    
    # --- Initialize components for Routine "Start_Sum_Exp" ---
    text_4 = visual.TextStim(win=win, name='text_4',
        text="Click on the 'Start Talking' button below to begin your verbal summary. You'll have 15 seconds to speak. \nIf you're unable to report anything, you may choose to skip the verbal summary by clicking on the 'Skip Summary' button.",
        font='Open Sans',
        pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    summary_button_exp = visual.ButtonStim(win, 
        text='Start Talking', font='Arvo',
        pos=(0.5, -0.4),
        letterHeight=0.02,
        size=(0.2, 0.1), borderWidth=0.0,
        fillColor='darkgrey', borderColor=None,
        color='white', colorSpace='rgb',
        opacity=None,
        bold=True, italic=False,
        padding=None,
        anchor='center',
        name='summary_button_exp',
        depth=-1
    )
    summary_button_exp.buttonClock = core.Clock()
    skip_button_exp = visual.ButtonStim(win, 
        text='Skip Summary', font='Arvo',
        pos=(-0.5, -0.4),
        letterHeight=0.02,
        size=(0.2, 0.1), borderWidth=0.0,
        fillColor='darkgrey', borderColor=None,
        color='white', colorSpace='rgb',
        opacity=None,
        bold=True, italic=False,
        padding=None,
        anchor='center',
        name='skip_button_exp',
        depth=-2
    )
    skip_button_exp.buttonClock = core.Clock()
    
    # --- Initialize components for Routine "Summary" ---
    # link mic to device object
    mic = macBookProMicrophone
    countdown = visual.TextStim(win=win, name='countdown',
        text='',
        font='Open Sans',
        pos=(0, 0), height=0.1, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    
    # --- Initialize components for Routine "Multiple_Choice_2" ---
    Question = visual.TextStim(win=win, name='Question',
        text='',
        font='Open Sans',
        pos=(0, 0.2), height=0.03, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    Option_1 = visual.TextStim(win=win, name='Option_1',
        text='',
        font='Open Sans',
        pos=(0, 0.1), height=0.03, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    Option_2 = visual.TextStim(win=win, name='Option_2',
        text='',
        font='Open Sans',
        pos=(0,0), height=0.03, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-2.0);
    Option_3 = visual.TextStim(win=win, name='Option_3',
        text='',
        font='Open Sans',
        pos=(0, -0.1), height=0.03, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-3.0);
    Option_4 = visual.TextStim(win=win, name='Option_4',
        text='',
        font='Open Sans',
        pos=(0, -0.2), height=0.03, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-4.0);
    A = visual.ButtonStim(win, 
        text='A', font='Arvo',
        pos=(-0.4,-0.4),
        letterHeight=0.03,
        size=(0.1, 0.1), borderWidth=0.0,
        fillColor='darkgrey', borderColor=None,
        color='white', colorSpace='rgb',
        opacity=None,
        bold=True, italic=False,
        padding=None,
        anchor='center',
        name='A',
        depth=-5
    )
    A.buttonClock = core.Clock()
    B = visual.ButtonStim(win, 
        text='B', font='Arvo',
        pos=(-0.1,-0.4),
        letterHeight=0.03,
        size=(0.1, 0.1), borderWidth=0.0,
        fillColor='darkgrey', borderColor=None,
        color='white', colorSpace='rgb',
        opacity=None,
        bold=True, italic=False,
        padding=None,
        anchor='center',
        name='B',
        depth=-6
    )
    B.buttonClock = core.Clock()
    C = visual.ButtonStim(win, 
        text='C', font='Arvo',
        pos=(0.2,-0.4),
        letterHeight=0.03,
        size=(0.1, 0.1), borderWidth=0.0,
        fillColor='darkgrey', borderColor=None,
        color='white', colorSpace='rgb',
        opacity=None,
        bold=True, italic=False,
        padding=None,
        anchor='center',
        name='C',
        depth=-7
    )
    C.buttonClock = core.Clock()
    D = visual.ButtonStim(win, 
        text='D', font='Arvo',
        pos=(0.5,-0.4),
        letterHeight=0.03,
        size=(0.1, 0.1), borderWidth=0.0,
        fillColor='darkgrey', borderColor=None,
        color='white', colorSpace='rgb',
        opacity=None,
        bold=True, italic=False,
        padding=None,
        anchor='center',
        name='D',
        depth=-8
    )
    D.buttonClock = core.Clock()
    
    # create some handy timers
    if globalClock is None:
        globalClock = core.Clock()  # to track the time since experiment started
    if ioServer is not None:
        ioServer.syncClock(globalClock)
    logging.setDefaultClock(globalClock)
    routineTimer = core.Clock()  # to track time remaining of each (possibly non-slip) routine
    win.flip()  # flip window to reset last flip timer
    # store the exact time the global clock started
    expInfo['expStart'] = data.getDateStr(format='%Y-%m-%d %Hh%M.%S.%f %z', fractionalSecondDigits=6)
    
    # --- Prepare to start Routine "Instructions" ---
    continueRoutine = True
    # update component parameters for each repeat
    thisExp.addData('Instructions.started', globalClock.getTime())
    # reset button to account for continued clicks & clear times on/off
    button.reset()
    # keep track of which components have finished
    InstructionsComponents = [text, button]
    for thisComponent in InstructionsComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "Instructions" ---
    routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *text* updates
        
        # if text is starting this frame...
        if text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            text.frameNStart = frameN  # exact frame index
            text.tStart = t  # local t and not account for scr refresh
            text.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(text, 'tStartRefresh')  # time at next scr refresh
            # update status
            text.status = STARTED
            text.setAutoDraw(True)
        
        # if text is active this frame...
        if text.status == STARTED:
            # update params
            pass
        # *button* updates
        
        # if button is starting this frame...
        if button.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
            # keep track of start time/frame for later
            button.frameNStart = frameN  # exact frame index
            button.tStart = t  # local t and not account for scr refresh
            button.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(button, 'tStartRefresh')  # time at next scr refresh
            # update status
            button.status = STARTED
            button.setAutoDraw(True)
        
        # if button is active this frame...
        if button.status == STARTED:
            # update params
            pass
            # check whether button has been pressed
            if button.isClicked:
                if not button.wasClicked:
                    # if this is a new click, store time of first click and clicked until
                    button.timesOn.append(button.buttonClock.getTime())
                    button.timesOff.append(button.buttonClock.getTime())
                elif len(button.timesOff):
                    # if click is continuing from last frame, update time of clicked until
                    button.timesOff[-1] = button.buttonClock.getTime()
                if not button.wasClicked:
                    # end routine when button is clicked
                    continueRoutine = False
                if not button.wasClicked:
                    # run callback code when button is clicked
                    pass
        # take note of whether button was clicked, so that next frame we know if clicks are new
        button.wasClicked = button.isClicked and button.status == STARTED
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, inputs=inputs, win=win)
            return
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in InstructionsComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "Instructions" ---
    for thisComponent in InstructionsComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    thisExp.addData('Instructions.stopped', globalClock.getTime())
    # the Routine "Instructions" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # set up handler to look after randomisation of conditions etc
    training = data.TrialHandler(nReps=1.0, method='sequential', 
        extraInfo=expInfo, originPath=-1,
        trialList=data.importConditions('training.xlsx'),
        seed=None, name='training')
    thisExp.addLoop(training)  # add the loop to the experiment
    thisTraining = training.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisTraining.rgb)
    if thisTraining != None:
        for paramName in thisTraining:
            globals()[paramName] = thisTraining[paramName]
    
    for thisTraining in training:
        currentLoop = training
        thisExp.timestampOnFlip(win, 'thisRow.t')
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                inputs=inputs, 
                win=win, 
                timers=[routineTimer], 
                playbackComponents=[]
        )
        # abbreviate parameter names if possible (e.g. rgb = thisTraining.rgb)
        if thisTraining != None:
            for paramName in thisTraining:
                globals()[paramName] = thisTraining[paramName]
        
        # --- Prepare to start Routine "Start_Segment_Train" ---
        continueRoutine = True
        # update component parameters for each repeat
        thisExp.addData('Start_Segment_Train.started', globalClock.getTime())
        # reset Play_train to account for continued clicks & clear times on/off
        Play_train.reset()
        Trial_counter_train.setText('Completed = ' +str(training.thisN) + '\n Remaining = ' + str(training.nRemaining + 1))
        # keep track of which components have finished
        Start_Segment_TrainComponents = [Play_train, Trial_counter_train, text_5]
        for thisComponent in Start_Segment_TrainComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "Start_Segment_Train" ---
        routineForceEnded = not continueRoutine
        while continueRoutine:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            # *Play_train* updates
            
            # if Play_train is starting this frame...
            if Play_train.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
                # keep track of start time/frame for later
                Play_train.frameNStart = frameN  # exact frame index
                Play_train.tStart = t  # local t and not account for scr refresh
                Play_train.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(Play_train, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'Play_train.started')
                # update status
                Play_train.status = STARTED
                Play_train.setAutoDraw(True)
            
            # if Play_train is active this frame...
            if Play_train.status == STARTED:
                # update params
                pass
                # check whether Play_train has been pressed
                if Play_train.isClicked:
                    if not Play_train.wasClicked:
                        # if this is a new click, store time of first click and clicked until
                        Play_train.timesOn.append(Play_train.buttonClock.getTime())
                        Play_train.timesOff.append(Play_train.buttonClock.getTime())
                    elif len(Play_train.timesOff):
                        # if click is continuing from last frame, update time of clicked until
                        Play_train.timesOff[-1] = Play_train.buttonClock.getTime()
                    if not Play_train.wasClicked:
                        # end routine when Play_train is clicked
                        continueRoutine = False
                    if not Play_train.wasClicked:
                        # run callback code when Play_train is clicked
                        pass
            # take note of whether Play_train was clicked, so that next frame we know if clicks are new
            Play_train.wasClicked = Play_train.isClicked and Play_train.status == STARTED
            
            # *Trial_counter_train* updates
            
            # if Trial_counter_train is starting this frame...
            if Trial_counter_train.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                Trial_counter_train.frameNStart = frameN  # exact frame index
                Trial_counter_train.tStart = t  # local t and not account for scr refresh
                Trial_counter_train.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(Trial_counter_train, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'Trial_counter_train.started')
                # update status
                Trial_counter_train.status = STARTED
                Trial_counter_train.setAutoDraw(True)
            
            # if Trial_counter_train is active this frame...
            if Trial_counter_train.status == STARTED:
                # update params
                pass
            
            # *text_5* updates
            
            # if text_5 is starting this frame...
            if text_5.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                text_5.frameNStart = frameN  # exact frame index
                text_5.tStart = t  # local t and not account for scr refresh
                text_5.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(text_5, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'text_5.started')
                # update status
                text_5.status = STARTED
                text_5.setAutoDraw(True)
            
            # if text_5 is active this frame...
            if text_5.status == STARTED:
                # update params
                pass
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, inputs=inputs, win=win)
                return
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in Start_Segment_TrainComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "Start_Segment_Train" ---
        for thisComponent in Start_Segment_TrainComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        thisExp.addData('Start_Segment_Train.stopped', globalClock.getTime())
        training.addData('Play_train.numClicks', Play_train.numClicks)
        if Play_train.numClicks:
           training.addData('Play_train.timesOn', Play_train.timesOn)
           training.addData('Play_train.timesOff', Play_train.timesOff)
        else:
           training.addData('Play_train.timesOn', "")
           training.addData('Play_train.timesOff', "")
        # the Routine "Start_Segment_Train" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # --- Prepare to start Routine "Training_Segment" ---
        continueRoutine = True
        # update component parameters for each repeat
        thisExp.addData('Training_Segment.started', globalClock.getTime())
        Experimen_audio.setSound(wav_file, hamming=True)
        Experimen_audio.setVolume(1.0, log=False)
        Experimen_audio.seek(0)
        # Run 'Begin Routine' code from slider_code
        myslider.start_trial(0)
        # keep track of which components have finished
        Training_SegmentComponents = [Experimen_audio]
        for thisComponent in Training_SegmentComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "Training_Segment" ---
        routineForceEnded = not continueRoutine
        while continueRoutine:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # if Experimen_audio is starting this frame...
            if Experimen_audio.status == NOT_STARTED and tThisFlip >= 0.00-frameTolerance:
                # keep track of start time/frame for later
                Experimen_audio.frameNStart = frameN  # exact frame index
                Experimen_audio.tStart = t  # local t and not account for scr refresh
                Experimen_audio.tStartRefresh = tThisFlipGlobal  # on global time
                # add timestamp to datafile
                thisExp.addData('Experimen_audio.started', tThisFlipGlobal)
                # update status
                Experimen_audio.status = STARTED
                Experimen_audio.play(when=win)  # sync with win flip
            # update Experimen_audio status according to whether it's playing
            if Experimen_audio.isPlaying:
                Experimen_audio.status = STARTED
            elif Experimen_audio.isFinished:
                Experimen_audio.status = FINISHED
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, inputs=inputs, win=win)
                return
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in Training_SegmentComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "Training_Segment" ---
        for thisComponent in Training_SegmentComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        thisExp.addData('Training_Segment.stopped', globalClock.getTime())
        # Run 'End Routine' code from slider_code
        myslider.stop_trial()
        # the Routine "Training_Segment" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # --- Prepare to start Routine "Rating" ---
        continueRoutine = True
        # update component parameters for each repeat
        thisExp.addData('Rating.started', globalClock.getTime())
        slider.reset()
        # reset button_2 to account for continued clicks & clear times on/off
        button_2.reset()
        # keep track of which components have finished
        RatingComponents = [slider, button_2, text_3]
        for thisComponent in RatingComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "Rating" ---
        routineForceEnded = not continueRoutine
        while continueRoutine:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *slider* updates
            
            # if slider is starting this frame...
            if slider.status == NOT_STARTED and tThisFlip >= 0.2-frameTolerance:
                # keep track of start time/frame for later
                slider.frameNStart = frameN  # exact frame index
                slider.tStart = t  # local t and not account for scr refresh
                slider.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(slider, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'slider.started')
                # update status
                slider.status = STARTED
                slider.setAutoDraw(True)
            
            # if slider is active this frame...
            if slider.status == STARTED:
                # update params
                pass
            # *button_2* updates
            
            # if button_2 is starting this frame...
            if button_2.status == NOT_STARTED and slider.rating:
                # keep track of start time/frame for later
                button_2.frameNStart = frameN  # exact frame index
                button_2.tStart = t  # local t and not account for scr refresh
                button_2.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(button_2, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'button_2.started')
                # update status
                button_2.status = STARTED
                button_2.setAutoDraw(True)
            
            # if button_2 is active this frame...
            if button_2.status == STARTED:
                # update params
                pass
                # check whether button_2 has been pressed
                if button_2.isClicked:
                    if not button_2.wasClicked:
                        # if this is a new click, store time of first click and clicked until
                        button_2.timesOn.append(button_2.buttonClock.getTime())
                        button_2.timesOff.append(button_2.buttonClock.getTime())
                    elif len(button_2.timesOff):
                        # if click is continuing from last frame, update time of clicked until
                        button_2.timesOff[-1] = button_2.buttonClock.getTime()
                    if not button_2.wasClicked:
                        # end routine when button_2 is clicked
                        continueRoutine = False
                    if not button_2.wasClicked:
                        # run callback code when button_2 is clicked
                        pass
            # take note of whether button_2 was clicked, so that next frame we know if clicks are new
            button_2.wasClicked = button_2.isClicked and button_2.status == STARTED
            
            # *text_3* updates
            
            # if text_3 is starting this frame...
            if text_3.status == NOT_STARTED and tThisFlip >= 0.2-frameTolerance:
                # keep track of start time/frame for later
                text_3.frameNStart = frameN  # exact frame index
                text_3.tStart = t  # local t and not account for scr refresh
                text_3.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(text_3, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'text_3.started')
                # update status
                text_3.status = STARTED
                text_3.setAutoDraw(True)
            
            # if text_3 is active this frame...
            if text_3.status == STARTED:
                # update params
                pass
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, inputs=inputs, win=win)
                return
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in RatingComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "Rating" ---
        for thisComponent in RatingComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        thisExp.addData('Rating.stopped', globalClock.getTime())
        training.addData('slider.response', slider.getRating())
        training.addData('slider.rt', slider.getRT())
        training.addData('button_2.numClicks', button_2.numClicks)
        if button_2.numClicks:
           training.addData('button_2.timesOn', button_2.timesOn)
           training.addData('button_2.timesOff', button_2.timesOff)
        else:
           training.addData('button_2.timesOn', "")
           training.addData('button_2.timesOff', "")
        # Run 'End Routine' code from code_3
        if summary == "yes":
            summa = 1
        else:
            summa = 0
            
        # the Routine "Rating" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # set up handler to look after randomisation of conditions etc
        sum_true = data.TrialHandler(nReps=summa, method='random', 
            extraInfo=expInfo, originPath=-1,
            trialList=[None],
            seed=None, name='sum_true')
        thisExp.addLoop(sum_true)  # add the loop to the experiment
        thisSum_true = sum_true.trialList[0]  # so we can initialise stimuli with some values
        # abbreviate parameter names if possible (e.g. rgb = thisSum_true.rgb)
        if thisSum_true != None:
            for paramName in thisSum_true:
                globals()[paramName] = thisSum_true[paramName]
        
        for thisSum_true in sum_true:
            currentLoop = sum_true
            thisExp.timestampOnFlip(win, 'thisRow.t')
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    inputs=inputs, 
                    win=win, 
                    timers=[routineTimer], 
                    playbackComponents=[]
            )
            # abbreviate parameter names if possible (e.g. rgb = thisSum_true.rgb)
            if thisSum_true != None:
                for paramName in thisSum_true:
                    globals()[paramName] = thisSum_true[paramName]
            
            # --- Prepare to start Routine "Start_Summary" ---
            continueRoutine = True
            # update component parameters for each repeat
            thisExp.addData('Start_Summary.started', globalClock.getTime())
            # reset summary_button to account for continued clicks & clear times on/off
            summary_button.reset()
            # reset skip_button to account for continued clicks & clear times on/off
            skip_button.reset()
            # keep track of which components have finished
            Start_SummaryComponents = [text_2, summary_button, skip_button]
            for thisComponent in Start_SummaryComponents:
                thisComponent.tStart = None
                thisComponent.tStop = None
                thisComponent.tStartRefresh = None
                thisComponent.tStopRefresh = None
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            # reset timers
            t = 0
            _timeToFirstFrame = win.getFutureFlipTime(clock="now")
            frameN = -1
            
            # --- Run Routine "Start_Summary" ---
            routineForceEnded = not continueRoutine
            while continueRoutine:
                # get current time
                t = routineTimer.getTime()
                tThisFlip = win.getFutureFlipTime(clock=routineTimer)
                tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                
                # *text_2* updates
                
                # if text_2 is starting this frame...
                if text_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                    # keep track of start time/frame for later
                    text_2.frameNStart = frameN  # exact frame index
                    text_2.tStart = t  # local t and not account for scr refresh
                    text_2.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(text_2, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'text_2.started')
                    # update status
                    text_2.status = STARTED
                    text_2.setAutoDraw(True)
                
                # if text_2 is active this frame...
                if text_2.status == STARTED:
                    # update params
                    pass
                # *summary_button* updates
                
                # if summary_button is starting this frame...
                if summary_button.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
                    # keep track of start time/frame for later
                    summary_button.frameNStart = frameN  # exact frame index
                    summary_button.tStart = t  # local t and not account for scr refresh
                    summary_button.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(summary_button, 'tStartRefresh')  # time at next scr refresh
                    # update status
                    summary_button.status = STARTED
                    summary_button.setAutoDraw(True)
                
                # if summary_button is active this frame...
                if summary_button.status == STARTED:
                    # update params
                    pass
                    # check whether summary_button has been pressed
                    if summary_button.isClicked:
                        if not summary_button.wasClicked:
                            # if this is a new click, store time of first click and clicked until
                            summary_button.timesOn.append(summary_button.buttonClock.getTime())
                            summary_button.timesOff.append(summary_button.buttonClock.getTime())
                        elif len(summary_button.timesOff):
                            # if click is continuing from last frame, update time of clicked until
                            summary_button.timesOff[-1] = summary_button.buttonClock.getTime()
                        if not summary_button.wasClicked:
                            # end routine when summary_button is clicked
                            continueRoutine = False
                        if not summary_button.wasClicked:
                            # run callback code when summary_button is clicked
                            button_pressed= "next"
                # take note of whether summary_button was clicked, so that next frame we know if clicks are new
                summary_button.wasClicked = summary_button.isClicked and summary_button.status == STARTED
                # *skip_button* updates
                
                # if skip_button is starting this frame...
                if skip_button.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
                    # keep track of start time/frame for later
                    skip_button.frameNStart = frameN  # exact frame index
                    skip_button.tStart = t  # local t and not account for scr refresh
                    skip_button.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(skip_button, 'tStartRefresh')  # time at next scr refresh
                    # update status
                    skip_button.status = STARTED
                    skip_button.setAutoDraw(True)
                
                # if skip_button is active this frame...
                if skip_button.status == STARTED:
                    # update params
                    pass
                    # check whether skip_button has been pressed
                    if skip_button.isClicked:
                        if not skip_button.wasClicked:
                            # if this is a new click, store time of first click and clicked until
                            skip_button.timesOn.append(skip_button.buttonClock.getTime())
                            skip_button.timesOff.append(skip_button.buttonClock.getTime())
                        elif len(skip_button.timesOff):
                            # if click is continuing from last frame, update time of clicked until
                            skip_button.timesOff[-1] = skip_button.buttonClock.getTime()
                        if not skip_button.wasClicked:
                            # end routine when skip_button is clicked
                            continueRoutine = False
                        if not skip_button.wasClicked:
                            # run callback code when skip_button is clicked
                            button_pressed= "skip"
                # take note of whether skip_button was clicked, so that next frame we know if clicks are new
                skip_button.wasClicked = skip_button.isClicked and skip_button.status == STARTED
                
                # check for quit (typically the Esc key)
                if defaultKeyboard.getKeys(keyList=["escape"]):
                    thisExp.status = FINISHED
                if thisExp.status == FINISHED or endExpNow:
                    endExperiment(thisExp, inputs=inputs, win=win)
                    return
                
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    routineForceEnded = True
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in Start_SummaryComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # --- Ending Routine "Start_Summary" ---
            for thisComponent in Start_SummaryComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            thisExp.addData('Start_Summary.stopped', globalClock.getTime())
            sum_true.addData('summary_button.numClicks', summary_button.numClicks)
            if summary_button.numClicks:
               sum_true.addData('summary_button.timesOn', summary_button.timesOn)
               sum_true.addData('summary_button.timesOff', summary_button.timesOff)
            else:
               sum_true.addData('summary_button.timesOn', "")
               sum_true.addData('summary_button.timesOff', "")
            sum_true.addData('skip_button.numClicks', skip_button.numClicks)
            if skip_button.numClicks:
               sum_true.addData('skip_button.timesOn', skip_button.timesOn)
               sum_true.addData('skip_button.timesOff', skip_button.timesOff)
            else:
               sum_true.addData('skip_button.timesOn', "")
               sum_true.addData('skip_button.timesOff', "")
            # Run 'End Routine' code from code
            if button_pressed == "next":
                doSum = 1
            else:
                doSum = 0
            # the Routine "Start_Summary" was not non-slip safe, so reset the non-slip timer
            routineTimer.reset()
            
            # set up handler to look after randomisation of conditions etc
            dummy_loop = data.TrialHandler(nReps=doSum, method='random', 
                extraInfo=expInfo, originPath=-1,
                trialList=[None],
                seed=None, name='dummy_loop')
            thisExp.addLoop(dummy_loop)  # add the loop to the experiment
            thisDummy_loop = dummy_loop.trialList[0]  # so we can initialise stimuli with some values
            # abbreviate parameter names if possible (e.g. rgb = thisDummy_loop.rgb)
            if thisDummy_loop != None:
                for paramName in thisDummy_loop:
                    globals()[paramName] = thisDummy_loop[paramName]
            
            for thisDummy_loop in dummy_loop:
                currentLoop = dummy_loop
                thisExp.timestampOnFlip(win, 'thisRow.t')
                # pause experiment here if requested
                if thisExp.status == PAUSED:
                    pauseExperiment(
                        thisExp=thisExp, 
                        inputs=inputs, 
                        win=win, 
                        timers=[routineTimer], 
                        playbackComponents=[]
                )
                # abbreviate parameter names if possible (e.g. rgb = thisDummy_loop.rgb)
                if thisDummy_loop != None:
                    for paramName in thisDummy_loop:
                        globals()[paramName] = thisDummy_loop[paramName]
                
                # --- Prepare to start Routine "Summary" ---
                continueRoutine = True
                # update component parameters for each repeat
                thisExp.addData('Summary.started', globalClock.getTime())
                # keep track of which components have finished
                SummaryComponents = [mic, countdown]
                for thisComponent in SummaryComponents:
                    thisComponent.tStart = None
                    thisComponent.tStop = None
                    thisComponent.tStartRefresh = None
                    thisComponent.tStopRefresh = None
                    if hasattr(thisComponent, 'status'):
                        thisComponent.status = NOT_STARTED
                # reset timers
                t = 0
                _timeToFirstFrame = win.getFutureFlipTime(clock="now")
                frameN = -1
                
                # --- Run Routine "Summary" ---
                routineForceEnded = not continueRoutine
                while continueRoutine and routineTimer.getTime() < 15.0:
                    # get current time
                    t = routineTimer.getTime()
                    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
                    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                    # update/draw components on each frame
                    
                    # if mic is starting this frame...
                    if mic.status == NOT_STARTED and t >= 0.0-frameTolerance:
                        # keep track of start time/frame for later
                        mic.frameNStart = frameN  # exact frame index
                        mic.tStart = t  # local t and not account for scr refresh
                        mic.tStartRefresh = tThisFlipGlobal  # on global time
                        win.timeOnFlip(mic, 'tStartRefresh')  # time at next scr refresh
                        # update status
                        mic.status = STARTED
                        # start recording with mic
                        mic.start()
                    
                    # if mic is active this frame...
                    if mic.status == STARTED:
                        # update params
                        pass
                        # update recorded clip for mic
                        mic.poll()
                    
                    # if mic is stopping this frame...
                    if mic.status == STARTED:
                        # is it time to stop? (based on global clock, using actual start)
                        if tThisFlipGlobal > mic.tStartRefresh + 15.0-frameTolerance:
                            # keep track of stop time/frame for later
                            mic.tStop = t  # not accounting for scr refresh
                            mic.frameNStop = frameN  # exact frame index
                            # update status
                            mic.status = FINISHED
                            # stop recording with mic
                            mic.stop()
                    
                    # *countdown* updates
                    
                    # if countdown is starting this frame...
                    if countdown.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                        # keep track of start time/frame for later
                        countdown.frameNStart = frameN  # exact frame index
                        countdown.tStart = t  # local t and not account for scr refresh
                        countdown.tStartRefresh = tThisFlipGlobal  # on global time
                        win.timeOnFlip(countdown, 'tStartRefresh')  # time at next scr refresh
                        # update status
                        countdown.status = STARTED
                        countdown.setAutoDraw(True)
                    
                    # if countdown is active this frame...
                    if countdown.status == STARTED:
                        # update params
                        countdown.setText(int(round(15 - t, 3)), log=False)
                    
                    # if countdown is stopping this frame...
                    if countdown.status == STARTED:
                        # is it time to stop? (based on global clock, using actual start)
                        if tThisFlipGlobal > countdown.tStartRefresh + 15-frameTolerance:
                            # keep track of stop time/frame for later
                            countdown.tStop = t  # not accounting for scr refresh
                            countdown.frameNStop = frameN  # exact frame index
                            # update status
                            countdown.status = FINISHED
                            countdown.setAutoDraw(False)
                    
                    # check for quit (typically the Esc key)
                    if defaultKeyboard.getKeys(keyList=["escape"]):
                        thisExp.status = FINISHED
                    if thisExp.status == FINISHED or endExpNow:
                        endExperiment(thisExp, inputs=inputs, win=win)
                        return
                    
                    # check if all components have finished
                    if not continueRoutine:  # a component has requested a forced-end of Routine
                        routineForceEnded = True
                        break
                    continueRoutine = False  # will revert to True if at least one component still running
                    for thisComponent in SummaryComponents:
                        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                            continueRoutine = True
                            break  # at least one component has not yet finished
                    
                    # refresh the screen
                    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                        win.flip()
                
                # --- Ending Routine "Summary" ---
                for thisComponent in SummaryComponents:
                    if hasattr(thisComponent, "setAutoDraw"):
                        thisComponent.setAutoDraw(False)
                thisExp.addData('Summary.stopped', globalClock.getTime())
                # tell mic to keep hold of current recording in mic.clips and transcript (if applicable) in mic.scripts
                # this will also update mic.lastClip and mic.lastScript
                mic.stop()
                tag = data.utils.getDateStr()
                micClip, micScript = mic.bank(
                    tag=tag, transcribe='whisper',
                    language='en-US', expectedWords=None
                )
                dummy_loop.addData('mic.clip', os.path.join(micRecFolder, 'recording_mic_%s.wav' % tag))
                dummy_loop.addData('mic.script', micScript)
                # save transcription data
                with open(os.path.join(micRecFolder, 'recording_mic_%s.json' % tag), 'w') as fp:
                    fp.write(micScript.response)
                # save speaking start/stop times
                micWordData = []
                micSegments = mic.lastScript.responseData.get('segments', {})
                for thisSegment in micSegments.values():
                    # for each segment...
                    for thisWord in thisSegment.get('words', {}).values():
                        # append word data
                        micWordData.append(thisWord)
                # if there were any words, store the start of first & end of last 
                if len(micWordData):
                    thisExp.addData('mic.speechStart', micWordData[0]['start'])
                    thisExp.addData('mic.speechEnd', micWordData[-1]['end'])
                else:
                    thisExp.addData('mic.speechStart', '')
                    thisExp.addData('mic.speechEnd', '')
                # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
                if routineForceEnded:
                    routineTimer.reset()
                else:
                    routineTimer.addTime(-15.000000)
                thisExp.nextEntry()
                
                if thisSession is not None:
                    # if running in a Session with a Liaison client, send data up to now
                    thisSession.sendExperimentData()
            # completed doSum repeats of 'dummy_loop'
            
            thisExp.nextEntry()
            
            if thisSession is not None:
                # if running in a Session with a Liaison client, send data up to now
                thisSession.sendExperimentData()
        # completed summa repeats of 'sum_true'
        
        
        # --- Prepare to start Routine "Multiple_Choice_2" ---
        continueRoutine = True
        # update component parameters for each repeat
        thisExp.addData('Multiple_Choice_2.started', globalClock.getTime())
        Question.setText(question)
        Option_1.setText(C1)
        Option_2.setText(C2)
        Option_3.setText(C3)
        Option_4.setText(C4)
        # reset A to account for continued clicks & clear times on/off
        A.reset()
        # reset B to account for continued clicks & clear times on/off
        B.reset()
        # reset C to account for continued clicks & clear times on/off
        C.reset()
        # reset D to account for continued clicks & clear times on/off
        D.reset()
        # keep track of which components have finished
        Multiple_Choice_2Components = [Question, Option_1, Option_2, Option_3, Option_4, A, B, C, D]
        for thisComponent in Multiple_Choice_2Components:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "Multiple_Choice_2" ---
        routineForceEnded = not continueRoutine
        while continueRoutine:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *Question* updates
            
            # if Question is starting this frame...
            if Question.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                Question.frameNStart = frameN  # exact frame index
                Question.tStart = t  # local t and not account for scr refresh
                Question.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(Question, 'tStartRefresh')  # time at next scr refresh
                # update status
                Question.status = STARTED
                Question.setAutoDraw(True)
            
            # if Question is active this frame...
            if Question.status == STARTED:
                # update params
                pass
            
            # *Option_1* updates
            
            # if Option_1 is starting this frame...
            if Option_1.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                Option_1.frameNStart = frameN  # exact frame index
                Option_1.tStart = t  # local t and not account for scr refresh
                Option_1.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(Option_1, 'tStartRefresh')  # time at next scr refresh
                # update status
                Option_1.status = STARTED
                Option_1.setAutoDraw(True)
            
            # if Option_1 is active this frame...
            if Option_1.status == STARTED:
                # update params
                pass
            
            # *Option_2* updates
            
            # if Option_2 is starting this frame...
            if Option_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                Option_2.frameNStart = frameN  # exact frame index
                Option_2.tStart = t  # local t and not account for scr refresh
                Option_2.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(Option_2, 'tStartRefresh')  # time at next scr refresh
                # update status
                Option_2.status = STARTED
                Option_2.setAutoDraw(True)
            
            # if Option_2 is active this frame...
            if Option_2.status == STARTED:
                # update params
                pass
            
            # *Option_3* updates
            
            # if Option_3 is starting this frame...
            if Option_3.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                Option_3.frameNStart = frameN  # exact frame index
                Option_3.tStart = t  # local t and not account for scr refresh
                Option_3.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(Option_3, 'tStartRefresh')  # time at next scr refresh
                # update status
                Option_3.status = STARTED
                Option_3.setAutoDraw(True)
            
            # if Option_3 is active this frame...
            if Option_3.status == STARTED:
                # update params
                pass
            
            # *Option_4* updates
            
            # if Option_4 is starting this frame...
            if Option_4.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                Option_4.frameNStart = frameN  # exact frame index
                Option_4.tStart = t  # local t and not account for scr refresh
                Option_4.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(Option_4, 'tStartRefresh')  # time at next scr refresh
                # update status
                Option_4.status = STARTED
                Option_4.setAutoDraw(True)
            
            # if Option_4 is active this frame...
            if Option_4.status == STARTED:
                # update params
                pass
            # *A* updates
            
            # if A is starting this frame...
            if A.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
                # keep track of start time/frame for later
                A.frameNStart = frameN  # exact frame index
                A.tStart = t  # local t and not account for scr refresh
                A.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(A, 'tStartRefresh')  # time at next scr refresh
                # update status
                A.status = STARTED
                A.setAutoDraw(True)
            
            # if A is active this frame...
            if A.status == STARTED:
                # update params
                pass
                # check whether A has been pressed
                if A.isClicked:
                    if not A.wasClicked:
                        # if this is a new click, store time of first click and clicked until
                        A.timesOn.append(A.buttonClock.getTime())
                        A.timesOff.append(A.buttonClock.getTime())
                    elif len(A.timesOff):
                        # if click is continuing from last frame, update time of clicked until
                        A.timesOff[-1] = A.buttonClock.getTime()
                    if not A.wasClicked:
                        # end routine when A is clicked
                        continueRoutine = False
                    if not A.wasClicked:
                        # run callback code when A is clicked
                        pass
            # take note of whether A was clicked, so that next frame we know if clicks are new
            A.wasClicked = A.isClicked and A.status == STARTED
            # *B* updates
            
            # if B is starting this frame...
            if B.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
                # keep track of start time/frame for later
                B.frameNStart = frameN  # exact frame index
                B.tStart = t  # local t and not account for scr refresh
                B.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(B, 'tStartRefresh')  # time at next scr refresh
                # update status
                B.status = STARTED
                B.setAutoDraw(True)
            
            # if B is active this frame...
            if B.status == STARTED:
                # update params
                pass
                # check whether B has been pressed
                if B.isClicked:
                    if not B.wasClicked:
                        # if this is a new click, store time of first click and clicked until
                        B.timesOn.append(B.buttonClock.getTime())
                        B.timesOff.append(B.buttonClock.getTime())
                    elif len(B.timesOff):
                        # if click is continuing from last frame, update time of clicked until
                        B.timesOff[-1] = B.buttonClock.getTime()
                    if not B.wasClicked:
                        # end routine when B is clicked
                        continueRoutine = False
                    if not B.wasClicked:
                        # run callback code when B is clicked
                        pass
            # take note of whether B was clicked, so that next frame we know if clicks are new
            B.wasClicked = B.isClicked and B.status == STARTED
            # *C* updates
            
            # if C is starting this frame...
            if C.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
                # keep track of start time/frame for later
                C.frameNStart = frameN  # exact frame index
                C.tStart = t  # local t and not account for scr refresh
                C.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(C, 'tStartRefresh')  # time at next scr refresh
                # update status
                C.status = STARTED
                C.setAutoDraw(True)
            
            # if C is active this frame...
            if C.status == STARTED:
                # update params
                pass
                # check whether C has been pressed
                if C.isClicked:
                    if not C.wasClicked:
                        # if this is a new click, store time of first click and clicked until
                        C.timesOn.append(C.buttonClock.getTime())
                        C.timesOff.append(C.buttonClock.getTime())
                    elif len(C.timesOff):
                        # if click is continuing from last frame, update time of clicked until
                        C.timesOff[-1] = C.buttonClock.getTime()
                    if not C.wasClicked:
                        # end routine when C is clicked
                        continueRoutine = False
                    if not C.wasClicked:
                        # run callback code when C is clicked
                        pass
            # take note of whether C was clicked, so that next frame we know if clicks are new
            C.wasClicked = C.isClicked and C.status == STARTED
            # *D* updates
            
            # if D is starting this frame...
            if D.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
                # keep track of start time/frame for later
                D.frameNStart = frameN  # exact frame index
                D.tStart = t  # local t and not account for scr refresh
                D.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(D, 'tStartRefresh')  # time at next scr refresh
                # update status
                D.status = STARTED
                D.setAutoDraw(True)
            
            # if D is active this frame...
            if D.status == STARTED:
                # update params
                pass
                # check whether D has been pressed
                if D.isClicked:
                    if not D.wasClicked:
                        # if this is a new click, store time of first click and clicked until
                        D.timesOn.append(D.buttonClock.getTime())
                        D.timesOff.append(D.buttonClock.getTime())
                    elif len(D.timesOff):
                        # if click is continuing from last frame, update time of clicked until
                        D.timesOff[-1] = D.buttonClock.getTime()
                    if not D.wasClicked:
                        # end routine when D is clicked
                        continueRoutine = False
                    if not D.wasClicked:
                        # run callback code when D is clicked
                        pass
            # take note of whether D was clicked, so that next frame we know if clicks are new
            D.wasClicked = D.isClicked and D.status == STARTED
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, inputs=inputs, win=win)
                return
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in Multiple_Choice_2Components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "Multiple_Choice_2" ---
        for thisComponent in Multiple_Choice_2Components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        thisExp.addData('Multiple_Choice_2.stopped', globalClock.getTime())
        training.addData('A.numClicks', A.numClicks)
        if A.numClicks:
           training.addData('A.timesOn', A.timesOn[0])
           training.addData('A.timesOff', A.timesOff[0])
        else:
           training.addData('A.timesOn', "")
           training.addData('A.timesOff', "")
        training.addData('B.numClicks', B.numClicks)
        if B.numClicks:
           training.addData('B.timesOn', B.timesOn[0])
           training.addData('B.timesOff', B.timesOff[0])
        else:
           training.addData('B.timesOn', "")
           training.addData('B.timesOff', "")
        training.addData('C.numClicks', C.numClicks)
        if C.numClicks:
           training.addData('C.timesOn', C.timesOn[0])
           training.addData('C.timesOff', C.timesOff[0])
        else:
           training.addData('C.timesOn', "")
           training.addData('C.timesOff', "")
        training.addData('D.numClicks', D.numClicks)
        if D.numClicks:
           training.addData('D.timesOn', D.timesOn[0])
           training.addData('D.timesOff', D.timesOff[0])
        else:
           training.addData('D.timesOn', "")
           training.addData('D.timesOff', "")
        # the Routine "Multiple_Choice_2" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        thisExp.nextEntry()
        
        if thisSession is not None:
            # if running in a Session with a Liaison client, send data up to now
            thisSession.sendExperimentData()
    # completed 1.0 repeats of 'training'
    
    
    # --- Prepare to start Routine "Start_Exp" ---
    continueRoutine = True
    # update component parameters for each repeat
    thisExp.addData('Start_Exp.started', globalClock.getTime())
    # reset Start to account for continued clicks & clear times on/off
    Start.reset()
    # keep track of which components have finished
    Start_ExpComponents = [Start_exp, Start]
    for thisComponent in Start_ExpComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "Start_Exp" ---
    routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *Start_exp* updates
        
        # if Start_exp is starting this frame...
        if Start_exp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            Start_exp.frameNStart = frameN  # exact frame index
            Start_exp.tStart = t  # local t and not account for scr refresh
            Start_exp.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(Start_exp, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'Start_exp.started')
            # update status
            Start_exp.status = STARTED
            Start_exp.setAutoDraw(True)
        
        # if Start_exp is active this frame...
        if Start_exp.status == STARTED:
            # update params
            pass
        # *Start* updates
        
        # if Start is starting this frame...
        if Start.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
            # keep track of start time/frame for later
            Start.frameNStart = frameN  # exact frame index
            Start.tStart = t  # local t and not account for scr refresh
            Start.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(Start, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'Start.started')
            # update status
            Start.status = STARTED
            Start.setAutoDraw(True)
        
        # if Start is active this frame...
        if Start.status == STARTED:
            # update params
            pass
            # check whether Start has been pressed
            if Start.isClicked:
                if not Start.wasClicked:
                    # if this is a new click, store time of first click and clicked until
                    Start.timesOn.append(Start.buttonClock.getTime())
                    Start.timesOff.append(Start.buttonClock.getTime())
                elif len(Start.timesOff):
                    # if click is continuing from last frame, update time of clicked until
                    Start.timesOff[-1] = Start.buttonClock.getTime()
                if not Start.wasClicked:
                    # end routine when Start is clicked
                    continueRoutine = False
                if not Start.wasClicked:
                    # run callback code when Start is clicked
                    pass
        # take note of whether Start was clicked, so that next frame we know if clicks are new
        Start.wasClicked = Start.isClicked and Start.status == STARTED
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, inputs=inputs, win=win)
            return
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in Start_ExpComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "Start_Exp" ---
    for thisComponent in Start_ExpComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    thisExp.addData('Start_Exp.stopped', globalClock.getTime())
    thisExp.addData('Start.numClicks', Start.numClicks)
    if Start.numClicks:
       thisExp.addData('Start.timesOn', Start.timesOn)
       thisExp.addData('Start.timesOff', Start.timesOff)
    else:
       thisExp.addData('Start.timesOn', "")
       thisExp.addData('Start.timesOff', "")
    # the Routine "Start_Exp" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # set up handler to look after randomisation of conditions etc
    experiment = data.TrialHandler(nReps=1.0, method='random', 
        extraInfo=expInfo, originPath=-1,
        trialList=data.importConditions('exp_stimuli.xlsx'),
        seed=None, name='experiment')
    thisExp.addLoop(experiment)  # add the loop to the experiment
    thisExperiment = experiment.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisExperiment.rgb)
    if thisExperiment != None:
        for paramName in thisExperiment:
            globals()[paramName] = thisExperiment[paramName]
    
    for thisExperiment in experiment:
        currentLoop = experiment
        thisExp.timestampOnFlip(win, 'thisRow.t')
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                inputs=inputs, 
                win=win, 
                timers=[routineTimer], 
                playbackComponents=[]
        )
        # abbreviate parameter names if possible (e.g. rgb = thisExperiment.rgb)
        if thisExperiment != None:
            for paramName in thisExperiment:
                globals()[paramName] = thisExperiment[paramName]
        
        # --- Prepare to start Routine "Start_Segment" ---
        continueRoutine = True
        # update component parameters for each repeat
        thisExp.addData('Start_Segment.started', globalClock.getTime())
        # reset Play to account for continued clicks & clear times on/off
        Play.reset()
        Trial_counter.setText(str(round((experiment.thisN / experiment.nTotal) * 100)) + ' %' )
        # keep track of which components have finished
        Start_SegmentComponents = [Play, Trial_counter, text_6]
        for thisComponent in Start_SegmentComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "Start_Segment" ---
        routineForceEnded = not continueRoutine
        while continueRoutine:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            # *Play* updates
            
            # if Play is starting this frame...
            if Play.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
                # keep track of start time/frame for later
                Play.frameNStart = frameN  # exact frame index
                Play.tStart = t  # local t and not account for scr refresh
                Play.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(Play, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'Play.started')
                # update status
                Play.status = STARTED
                Play.setAutoDraw(True)
            
            # if Play is active this frame...
            if Play.status == STARTED:
                # update params
                pass
                # check whether Play has been pressed
                if Play.isClicked:
                    if not Play.wasClicked:
                        # if this is a new click, store time of first click and clicked until
                        Play.timesOn.append(Play.buttonClock.getTime())
                        Play.timesOff.append(Play.buttonClock.getTime())
                    elif len(Play.timesOff):
                        # if click is continuing from last frame, update time of clicked until
                        Play.timesOff[-1] = Play.buttonClock.getTime()
                    if not Play.wasClicked:
                        # end routine when Play is clicked
                        continueRoutine = False
                    if not Play.wasClicked:
                        # run callback code when Play is clicked
                        pass
            # take note of whether Play was clicked, so that next frame we know if clicks are new
            Play.wasClicked = Play.isClicked and Play.status == STARTED
            
            # *Trial_counter* updates
            
            # if Trial_counter is starting this frame...
            if Trial_counter.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                Trial_counter.frameNStart = frameN  # exact frame index
                Trial_counter.tStart = t  # local t and not account for scr refresh
                Trial_counter.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(Trial_counter, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'Trial_counter.started')
                # update status
                Trial_counter.status = STARTED
                Trial_counter.setAutoDraw(True)
            
            # if Trial_counter is active this frame...
            if Trial_counter.status == STARTED:
                # update params
                pass
            
            # *text_6* updates
            
            # if text_6 is starting this frame...
            if text_6.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                text_6.frameNStart = frameN  # exact frame index
                text_6.tStart = t  # local t and not account for scr refresh
                text_6.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(text_6, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'text_6.started')
                # update status
                text_6.status = STARTED
                text_6.setAutoDraw(True)
            
            # if text_6 is active this frame...
            if text_6.status == STARTED:
                # update params
                pass
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, inputs=inputs, win=win)
                return
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in Start_SegmentComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "Start_Segment" ---
        for thisComponent in Start_SegmentComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        thisExp.addData('Start_Segment.stopped', globalClock.getTime())
        experiment.addData('Play.numClicks', Play.numClicks)
        if Play.numClicks:
           experiment.addData('Play.timesOn', Play.timesOn)
           experiment.addData('Play.timesOff', Play.timesOff)
        else:
           experiment.addData('Play.timesOn', "")
           experiment.addData('Play.timesOff', "")
        # the Routine "Start_Segment" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # --- Prepare to start Routine "Training_Segment" ---
        continueRoutine = True
        # update component parameters for each repeat
        thisExp.addData('Training_Segment.started', globalClock.getTime())
        Experimen_audio.setSound(wav_file, hamming=True)
        Experimen_audio.setVolume(1.0, log=False)
        Experimen_audio.seek(0)
        # Run 'Begin Routine' code from slider_code
        myslider.start_trial(0)
        # keep track of which components have finished
        Training_SegmentComponents = [Experimen_audio]
        for thisComponent in Training_SegmentComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "Training_Segment" ---
        routineForceEnded = not continueRoutine
        while continueRoutine:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # if Experimen_audio is starting this frame...
            if Experimen_audio.status == NOT_STARTED and tThisFlip >= 0.00-frameTolerance:
                # keep track of start time/frame for later
                Experimen_audio.frameNStart = frameN  # exact frame index
                Experimen_audio.tStart = t  # local t and not account for scr refresh
                Experimen_audio.tStartRefresh = tThisFlipGlobal  # on global time
                # add timestamp to datafile
                thisExp.addData('Experimen_audio.started', tThisFlipGlobal)
                # update status
                Experimen_audio.status = STARTED
                Experimen_audio.play(when=win)  # sync with win flip
            # update Experimen_audio status according to whether it's playing
            if Experimen_audio.isPlaying:
                Experimen_audio.status = STARTED
            elif Experimen_audio.isFinished:
                Experimen_audio.status = FINISHED
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, inputs=inputs, win=win)
                return
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in Training_SegmentComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "Training_Segment" ---
        for thisComponent in Training_SegmentComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        thisExp.addData('Training_Segment.stopped', globalClock.getTime())
        # Run 'End Routine' code from slider_code
        myslider.stop_trial()
        # the Routine "Training_Segment" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # --- Prepare to start Routine "Rating" ---
        continueRoutine = True
        # update component parameters for each repeat
        thisExp.addData('Rating.started', globalClock.getTime())
        slider.reset()
        # reset button_2 to account for continued clicks & clear times on/off
        button_2.reset()
        # keep track of which components have finished
        RatingComponents = [slider, button_2, text_3]
        for thisComponent in RatingComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "Rating" ---
        routineForceEnded = not continueRoutine
        while continueRoutine:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *slider* updates
            
            # if slider is starting this frame...
            if slider.status == NOT_STARTED and tThisFlip >= 0.2-frameTolerance:
                # keep track of start time/frame for later
                slider.frameNStart = frameN  # exact frame index
                slider.tStart = t  # local t and not account for scr refresh
                slider.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(slider, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'slider.started')
                # update status
                slider.status = STARTED
                slider.setAutoDraw(True)
            
            # if slider is active this frame...
            if slider.status == STARTED:
                # update params
                pass
            # *button_2* updates
            
            # if button_2 is starting this frame...
            if button_2.status == NOT_STARTED and slider.rating:
                # keep track of start time/frame for later
                button_2.frameNStart = frameN  # exact frame index
                button_2.tStart = t  # local t and not account for scr refresh
                button_2.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(button_2, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'button_2.started')
                # update status
                button_2.status = STARTED
                button_2.setAutoDraw(True)
            
            # if button_2 is active this frame...
            if button_2.status == STARTED:
                # update params
                pass
                # check whether button_2 has been pressed
                if button_2.isClicked:
                    if not button_2.wasClicked:
                        # if this is a new click, store time of first click and clicked until
                        button_2.timesOn.append(button_2.buttonClock.getTime())
                        button_2.timesOff.append(button_2.buttonClock.getTime())
                    elif len(button_2.timesOff):
                        # if click is continuing from last frame, update time of clicked until
                        button_2.timesOff[-1] = button_2.buttonClock.getTime()
                    if not button_2.wasClicked:
                        # end routine when button_2 is clicked
                        continueRoutine = False
                    if not button_2.wasClicked:
                        # run callback code when button_2 is clicked
                        pass
            # take note of whether button_2 was clicked, so that next frame we know if clicks are new
            button_2.wasClicked = button_2.isClicked and button_2.status == STARTED
            
            # *text_3* updates
            
            # if text_3 is starting this frame...
            if text_3.status == NOT_STARTED and tThisFlip >= 0.2-frameTolerance:
                # keep track of start time/frame for later
                text_3.frameNStart = frameN  # exact frame index
                text_3.tStart = t  # local t and not account for scr refresh
                text_3.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(text_3, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'text_3.started')
                # update status
                text_3.status = STARTED
                text_3.setAutoDraw(True)
            
            # if text_3 is active this frame...
            if text_3.status == STARTED:
                # update params
                pass
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, inputs=inputs, win=win)
                return
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in RatingComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "Rating" ---
        for thisComponent in RatingComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        thisExp.addData('Rating.stopped', globalClock.getTime())
        experiment.addData('slider.response', slider.getRating())
        experiment.addData('slider.rt', slider.getRT())
        experiment.addData('button_2.numClicks', button_2.numClicks)
        if button_2.numClicks:
           experiment.addData('button_2.timesOn', button_2.timesOn)
           experiment.addData('button_2.timesOff', button_2.timesOff)
        else:
           experiment.addData('button_2.timesOn', "")
           experiment.addData('button_2.timesOff', "")
        # Run 'End Routine' code from code_3
        if summary == "yes":
            summa = 1
        else:
            summa = 0
            
        # the Routine "Rating" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # set up handler to look after randomisation of conditions etc
        sum_true_exp = data.TrialHandler(nReps=summa, method='random', 
            extraInfo=expInfo, originPath=-1,
            trialList=[None],
            seed=None, name='sum_true_exp')
        thisExp.addLoop(sum_true_exp)  # add the loop to the experiment
        thisSum_true_exp = sum_true_exp.trialList[0]  # so we can initialise stimuli with some values
        # abbreviate parameter names if possible (e.g. rgb = thisSum_true_exp.rgb)
        if thisSum_true_exp != None:
            for paramName in thisSum_true_exp:
                globals()[paramName] = thisSum_true_exp[paramName]
        
        for thisSum_true_exp in sum_true_exp:
            currentLoop = sum_true_exp
            thisExp.timestampOnFlip(win, 'thisRow.t')
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    inputs=inputs, 
                    win=win, 
                    timers=[routineTimer], 
                    playbackComponents=[]
            )
            # abbreviate parameter names if possible (e.g. rgb = thisSum_true_exp.rgb)
            if thisSum_true_exp != None:
                for paramName in thisSum_true_exp:
                    globals()[paramName] = thisSum_true_exp[paramName]
            
            # --- Prepare to start Routine "Start_Sum_Exp" ---
            continueRoutine = True
            # update component parameters for each repeat
            thisExp.addData('Start_Sum_Exp.started', globalClock.getTime())
            # reset summary_button_exp to account for continued clicks & clear times on/off
            summary_button_exp.reset()
            # reset skip_button_exp to account for continued clicks & clear times on/off
            skip_button_exp.reset()
            # keep track of which components have finished
            Start_Sum_ExpComponents = [text_4, summary_button_exp, skip_button_exp]
            for thisComponent in Start_Sum_ExpComponents:
                thisComponent.tStart = None
                thisComponent.tStop = None
                thisComponent.tStartRefresh = None
                thisComponent.tStopRefresh = None
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            # reset timers
            t = 0
            _timeToFirstFrame = win.getFutureFlipTime(clock="now")
            frameN = -1
            
            # --- Run Routine "Start_Sum_Exp" ---
            routineForceEnded = not continueRoutine
            while continueRoutine:
                # get current time
                t = routineTimer.getTime()
                tThisFlip = win.getFutureFlipTime(clock=routineTimer)
                tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                
                # *text_4* updates
                
                # if text_4 is starting this frame...
                if text_4.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                    # keep track of start time/frame for later
                    text_4.frameNStart = frameN  # exact frame index
                    text_4.tStart = t  # local t and not account for scr refresh
                    text_4.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(text_4, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'text_4.started')
                    # update status
                    text_4.status = STARTED
                    text_4.setAutoDraw(True)
                
                # if text_4 is active this frame...
                if text_4.status == STARTED:
                    # update params
                    pass
                # *summary_button_exp* updates
                
                # if summary_button_exp is starting this frame...
                if summary_button_exp.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
                    # keep track of start time/frame for later
                    summary_button_exp.frameNStart = frameN  # exact frame index
                    summary_button_exp.tStart = t  # local t and not account for scr refresh
                    summary_button_exp.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(summary_button_exp, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'summary_button_exp.started')
                    # update status
                    summary_button_exp.status = STARTED
                    summary_button_exp.setAutoDraw(True)
                
                # if summary_button_exp is active this frame...
                if summary_button_exp.status == STARTED:
                    # update params
                    pass
                    # check whether summary_button_exp has been pressed
                    if summary_button_exp.isClicked:
                        if not summary_button_exp.wasClicked:
                            # if this is a new click, store time of first click and clicked until
                            summary_button_exp.timesOn.append(summary_button_exp.buttonClock.getTime())
                            summary_button_exp.timesOff.append(summary_button_exp.buttonClock.getTime())
                        elif len(summary_button_exp.timesOff):
                            # if click is continuing from last frame, update time of clicked until
                            summary_button_exp.timesOff[-1] = summary_button_exp.buttonClock.getTime()
                        if not summary_button_exp.wasClicked:
                            # end routine when summary_button_exp is clicked
                            continueRoutine = False
                        if not summary_button_exp.wasClicked:
                            # run callback code when summary_button_exp is clicked
                            pressed= "next"
                # take note of whether summary_button_exp was clicked, so that next frame we know if clicks are new
                summary_button_exp.wasClicked = summary_button_exp.isClicked and summary_button_exp.status == STARTED
                # *skip_button_exp* updates
                
                # if skip_button_exp is starting this frame...
                if skip_button_exp.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
                    # keep track of start time/frame for later
                    skip_button_exp.frameNStart = frameN  # exact frame index
                    skip_button_exp.tStart = t  # local t and not account for scr refresh
                    skip_button_exp.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(skip_button_exp, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'skip_button_exp.started')
                    # update status
                    skip_button_exp.status = STARTED
                    skip_button_exp.setAutoDraw(True)
                
                # if skip_button_exp is active this frame...
                if skip_button_exp.status == STARTED:
                    # update params
                    pass
                    # check whether skip_button_exp has been pressed
                    if skip_button_exp.isClicked:
                        if not skip_button_exp.wasClicked:
                            # if this is a new click, store time of first click and clicked until
                            skip_button_exp.timesOn.append(skip_button_exp.buttonClock.getTime())
                            skip_button_exp.timesOff.append(skip_button_exp.buttonClock.getTime())
                        elif len(skip_button_exp.timesOff):
                            # if click is continuing from last frame, update time of clicked until
                            skip_button_exp.timesOff[-1] = skip_button_exp.buttonClock.getTime()
                        if not skip_button_exp.wasClicked:
                            # end routine when skip_button_exp is clicked
                            continueRoutine = False
                        if not skip_button_exp.wasClicked:
                            # run callback code when skip_button_exp is clicked
                            pressed= "skip"
                # take note of whether skip_button_exp was clicked, so that next frame we know if clicks are new
                skip_button_exp.wasClicked = skip_button_exp.isClicked and skip_button_exp.status == STARTED
                
                # check for quit (typically the Esc key)
                if defaultKeyboard.getKeys(keyList=["escape"]):
                    thisExp.status = FINISHED
                if thisExp.status == FINISHED or endExpNow:
                    endExperiment(thisExp, inputs=inputs, win=win)
                    return
                
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    routineForceEnded = True
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in Start_Sum_ExpComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # --- Ending Routine "Start_Sum_Exp" ---
            for thisComponent in Start_Sum_ExpComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            thisExp.addData('Start_Sum_Exp.stopped', globalClock.getTime())
            sum_true_exp.addData('summary_button_exp.numClicks', summary_button_exp.numClicks)
            if summary_button_exp.numClicks:
               sum_true_exp.addData('summary_button_exp.timesOn', summary_button_exp.timesOn)
               sum_true_exp.addData('summary_button_exp.timesOff', summary_button_exp.timesOff)
            else:
               sum_true_exp.addData('summary_button_exp.timesOn', "")
               sum_true_exp.addData('summary_button_exp.timesOff', "")
            sum_true_exp.addData('skip_button_exp.numClicks', skip_button_exp.numClicks)
            if skip_button_exp.numClicks:
               sum_true_exp.addData('skip_button_exp.timesOn', skip_button_exp.timesOn)
               sum_true_exp.addData('skip_button_exp.timesOff', skip_button_exp.timesOff)
            else:
               sum_true_exp.addData('skip_button_exp.timesOn', "")
               sum_true_exp.addData('skip_button_exp.timesOff', "")
            # Run 'End Routine' code from code_2
            if pressed == "next":
                doSumexp = 1
            else:
                doSumexp = 0
            # the Routine "Start_Sum_Exp" was not non-slip safe, so reset the non-slip timer
            routineTimer.reset()
            
            # set up handler to look after randomisation of conditions etc
            dummy_loop_exp = data.TrialHandler(nReps=doSumexp, method='random', 
                extraInfo=expInfo, originPath=-1,
                trialList=[None],
                seed=None, name='dummy_loop_exp')
            thisExp.addLoop(dummy_loop_exp)  # add the loop to the experiment
            thisDummy_loop_exp = dummy_loop_exp.trialList[0]  # so we can initialise stimuli with some values
            # abbreviate parameter names if possible (e.g. rgb = thisDummy_loop_exp.rgb)
            if thisDummy_loop_exp != None:
                for paramName in thisDummy_loop_exp:
                    globals()[paramName] = thisDummy_loop_exp[paramName]
            
            for thisDummy_loop_exp in dummy_loop_exp:
                currentLoop = dummy_loop_exp
                thisExp.timestampOnFlip(win, 'thisRow.t')
                # pause experiment here if requested
                if thisExp.status == PAUSED:
                    pauseExperiment(
                        thisExp=thisExp, 
                        inputs=inputs, 
                        win=win, 
                        timers=[routineTimer], 
                        playbackComponents=[]
                )
                # abbreviate parameter names if possible (e.g. rgb = thisDummy_loop_exp.rgb)
                if thisDummy_loop_exp != None:
                    for paramName in thisDummy_loop_exp:
                        globals()[paramName] = thisDummy_loop_exp[paramName]
                
                # --- Prepare to start Routine "Summary" ---
                continueRoutine = True
                # update component parameters for each repeat
                thisExp.addData('Summary.started', globalClock.getTime())
                # keep track of which components have finished
                SummaryComponents = [mic, countdown]
                for thisComponent in SummaryComponents:
                    thisComponent.tStart = None
                    thisComponent.tStop = None
                    thisComponent.tStartRefresh = None
                    thisComponent.tStopRefresh = None
                    if hasattr(thisComponent, 'status'):
                        thisComponent.status = NOT_STARTED
                # reset timers
                t = 0
                _timeToFirstFrame = win.getFutureFlipTime(clock="now")
                frameN = -1
                
                # --- Run Routine "Summary" ---
                routineForceEnded = not continueRoutine
                while continueRoutine and routineTimer.getTime() < 15.0:
                    # get current time
                    t = routineTimer.getTime()
                    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
                    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                    # update/draw components on each frame
                    
                    # if mic is starting this frame...
                    if mic.status == NOT_STARTED and t >= 0.0-frameTolerance:
                        # keep track of start time/frame for later
                        mic.frameNStart = frameN  # exact frame index
                        mic.tStart = t  # local t and not account for scr refresh
                        mic.tStartRefresh = tThisFlipGlobal  # on global time
                        win.timeOnFlip(mic, 'tStartRefresh')  # time at next scr refresh
                        # update status
                        mic.status = STARTED
                        # start recording with mic
                        mic.start()
                    
                    # if mic is active this frame...
                    if mic.status == STARTED:
                        # update params
                        pass
                        # update recorded clip for mic
                        mic.poll()
                    
                    # if mic is stopping this frame...
                    if mic.status == STARTED:
                        # is it time to stop? (based on global clock, using actual start)
                        if tThisFlipGlobal > mic.tStartRefresh + 15.0-frameTolerance:
                            # keep track of stop time/frame for later
                            mic.tStop = t  # not accounting for scr refresh
                            mic.frameNStop = frameN  # exact frame index
                            # update status
                            mic.status = FINISHED
                            # stop recording with mic
                            mic.stop()
                    
                    # *countdown* updates
                    
                    # if countdown is starting this frame...
                    if countdown.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                        # keep track of start time/frame for later
                        countdown.frameNStart = frameN  # exact frame index
                        countdown.tStart = t  # local t and not account for scr refresh
                        countdown.tStartRefresh = tThisFlipGlobal  # on global time
                        win.timeOnFlip(countdown, 'tStartRefresh')  # time at next scr refresh
                        # update status
                        countdown.status = STARTED
                        countdown.setAutoDraw(True)
                    
                    # if countdown is active this frame...
                    if countdown.status == STARTED:
                        # update params
                        countdown.setText(int(round(15 - t, 3)), log=False)
                    
                    # if countdown is stopping this frame...
                    if countdown.status == STARTED:
                        # is it time to stop? (based on global clock, using actual start)
                        if tThisFlipGlobal > countdown.tStartRefresh + 15-frameTolerance:
                            # keep track of stop time/frame for later
                            countdown.tStop = t  # not accounting for scr refresh
                            countdown.frameNStop = frameN  # exact frame index
                            # update status
                            countdown.status = FINISHED
                            countdown.setAutoDraw(False)
                    
                    # check for quit (typically the Esc key)
                    if defaultKeyboard.getKeys(keyList=["escape"]):
                        thisExp.status = FINISHED
                    if thisExp.status == FINISHED or endExpNow:
                        endExperiment(thisExp, inputs=inputs, win=win)
                        return
                    
                    # check if all components have finished
                    if not continueRoutine:  # a component has requested a forced-end of Routine
                        routineForceEnded = True
                        break
                    continueRoutine = False  # will revert to True if at least one component still running
                    for thisComponent in SummaryComponents:
                        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                            continueRoutine = True
                            break  # at least one component has not yet finished
                    
                    # refresh the screen
                    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                        win.flip()
                
                # --- Ending Routine "Summary" ---
                for thisComponent in SummaryComponents:
                    if hasattr(thisComponent, "setAutoDraw"):
                        thisComponent.setAutoDraw(False)
                thisExp.addData('Summary.stopped', globalClock.getTime())
                # tell mic to keep hold of current recording in mic.clips and transcript (if applicable) in mic.scripts
                # this will also update mic.lastClip and mic.lastScript
                mic.stop()
                tag = data.utils.getDateStr()
                micClip, micScript = mic.bank(
                    tag=tag, transcribe='whisper',
                    language='en-US', expectedWords=None
                )
                dummy_loop_exp.addData('mic.clip', os.path.join(micRecFolder, 'recording_mic_%s.wav' % tag))
                dummy_loop_exp.addData('mic.script', micScript)
                # save transcription data
                with open(os.path.join(micRecFolder, 'recording_mic_%s.json' % tag), 'w') as fp:
                    fp.write(micScript.response)
                # save speaking start/stop times
                micWordData = []
                micSegments = mic.lastScript.responseData.get('segments', {})
                for thisSegment in micSegments.values():
                    # for each segment...
                    for thisWord in thisSegment.get('words', {}).values():
                        # append word data
                        micWordData.append(thisWord)
                # if there were any words, store the start of first & end of last 
                if len(micWordData):
                    thisExp.addData('mic.speechStart', micWordData[0]['start'])
                    thisExp.addData('mic.speechEnd', micWordData[-1]['end'])
                else:
                    thisExp.addData('mic.speechStart', '')
                    thisExp.addData('mic.speechEnd', '')
                # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
                if routineForceEnded:
                    routineTimer.reset()
                else:
                    routineTimer.addTime(-15.000000)
                thisExp.nextEntry()
                
                if thisSession is not None:
                    # if running in a Session with a Liaison client, send data up to now
                    thisSession.sendExperimentData()
            # completed doSumexp repeats of 'dummy_loop_exp'
            
            thisExp.nextEntry()
            
            if thisSession is not None:
                # if running in a Session with a Liaison client, send data up to now
                thisSession.sendExperimentData()
        # completed summa repeats of 'sum_true_exp'
        
        
        # --- Prepare to start Routine "Multiple_Choice_2" ---
        continueRoutine = True
        # update component parameters for each repeat
        thisExp.addData('Multiple_Choice_2.started', globalClock.getTime())
        Question.setText(question)
        Option_1.setText(C1)
        Option_2.setText(C2)
        Option_3.setText(C3)
        Option_4.setText(C4)
        # reset A to account for continued clicks & clear times on/off
        A.reset()
        # reset B to account for continued clicks & clear times on/off
        B.reset()
        # reset C to account for continued clicks & clear times on/off
        C.reset()
        # reset D to account for continued clicks & clear times on/off
        D.reset()
        # keep track of which components have finished
        Multiple_Choice_2Components = [Question, Option_1, Option_2, Option_3, Option_4, A, B, C, D]
        for thisComponent in Multiple_Choice_2Components:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "Multiple_Choice_2" ---
        routineForceEnded = not continueRoutine
        while continueRoutine:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *Question* updates
            
            # if Question is starting this frame...
            if Question.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                Question.frameNStart = frameN  # exact frame index
                Question.tStart = t  # local t and not account for scr refresh
                Question.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(Question, 'tStartRefresh')  # time at next scr refresh
                # update status
                Question.status = STARTED
                Question.setAutoDraw(True)
            
            # if Question is active this frame...
            if Question.status == STARTED:
                # update params
                pass
            
            # *Option_1* updates
            
            # if Option_1 is starting this frame...
            if Option_1.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                Option_1.frameNStart = frameN  # exact frame index
                Option_1.tStart = t  # local t and not account for scr refresh
                Option_1.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(Option_1, 'tStartRefresh')  # time at next scr refresh
                # update status
                Option_1.status = STARTED
                Option_1.setAutoDraw(True)
            
            # if Option_1 is active this frame...
            if Option_1.status == STARTED:
                # update params
                pass
            
            # *Option_2* updates
            
            # if Option_2 is starting this frame...
            if Option_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                Option_2.frameNStart = frameN  # exact frame index
                Option_2.tStart = t  # local t and not account for scr refresh
                Option_2.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(Option_2, 'tStartRefresh')  # time at next scr refresh
                # update status
                Option_2.status = STARTED
                Option_2.setAutoDraw(True)
            
            # if Option_2 is active this frame...
            if Option_2.status == STARTED:
                # update params
                pass
            
            # *Option_3* updates
            
            # if Option_3 is starting this frame...
            if Option_3.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                Option_3.frameNStart = frameN  # exact frame index
                Option_3.tStart = t  # local t and not account for scr refresh
                Option_3.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(Option_3, 'tStartRefresh')  # time at next scr refresh
                # update status
                Option_3.status = STARTED
                Option_3.setAutoDraw(True)
            
            # if Option_3 is active this frame...
            if Option_3.status == STARTED:
                # update params
                pass
            
            # *Option_4* updates
            
            # if Option_4 is starting this frame...
            if Option_4.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                Option_4.frameNStart = frameN  # exact frame index
                Option_4.tStart = t  # local t and not account for scr refresh
                Option_4.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(Option_4, 'tStartRefresh')  # time at next scr refresh
                # update status
                Option_4.status = STARTED
                Option_4.setAutoDraw(True)
            
            # if Option_4 is active this frame...
            if Option_4.status == STARTED:
                # update params
                pass
            # *A* updates
            
            # if A is starting this frame...
            if A.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
                # keep track of start time/frame for later
                A.frameNStart = frameN  # exact frame index
                A.tStart = t  # local t and not account for scr refresh
                A.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(A, 'tStartRefresh')  # time at next scr refresh
                # update status
                A.status = STARTED
                A.setAutoDraw(True)
            
            # if A is active this frame...
            if A.status == STARTED:
                # update params
                pass
                # check whether A has been pressed
                if A.isClicked:
                    if not A.wasClicked:
                        # if this is a new click, store time of first click and clicked until
                        A.timesOn.append(A.buttonClock.getTime())
                        A.timesOff.append(A.buttonClock.getTime())
                    elif len(A.timesOff):
                        # if click is continuing from last frame, update time of clicked until
                        A.timesOff[-1] = A.buttonClock.getTime()
                    if not A.wasClicked:
                        # end routine when A is clicked
                        continueRoutine = False
                    if not A.wasClicked:
                        # run callback code when A is clicked
                        pass
            # take note of whether A was clicked, so that next frame we know if clicks are new
            A.wasClicked = A.isClicked and A.status == STARTED
            # *B* updates
            
            # if B is starting this frame...
            if B.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
                # keep track of start time/frame for later
                B.frameNStart = frameN  # exact frame index
                B.tStart = t  # local t and not account for scr refresh
                B.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(B, 'tStartRefresh')  # time at next scr refresh
                # update status
                B.status = STARTED
                B.setAutoDraw(True)
            
            # if B is active this frame...
            if B.status == STARTED:
                # update params
                pass
                # check whether B has been pressed
                if B.isClicked:
                    if not B.wasClicked:
                        # if this is a new click, store time of first click and clicked until
                        B.timesOn.append(B.buttonClock.getTime())
                        B.timesOff.append(B.buttonClock.getTime())
                    elif len(B.timesOff):
                        # if click is continuing from last frame, update time of clicked until
                        B.timesOff[-1] = B.buttonClock.getTime()
                    if not B.wasClicked:
                        # end routine when B is clicked
                        continueRoutine = False
                    if not B.wasClicked:
                        # run callback code when B is clicked
                        pass
            # take note of whether B was clicked, so that next frame we know if clicks are new
            B.wasClicked = B.isClicked and B.status == STARTED
            # *C* updates
            
            # if C is starting this frame...
            if C.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
                # keep track of start time/frame for later
                C.frameNStart = frameN  # exact frame index
                C.tStart = t  # local t and not account for scr refresh
                C.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(C, 'tStartRefresh')  # time at next scr refresh
                # update status
                C.status = STARTED
                C.setAutoDraw(True)
            
            # if C is active this frame...
            if C.status == STARTED:
                # update params
                pass
                # check whether C has been pressed
                if C.isClicked:
                    if not C.wasClicked:
                        # if this is a new click, store time of first click and clicked until
                        C.timesOn.append(C.buttonClock.getTime())
                        C.timesOff.append(C.buttonClock.getTime())
                    elif len(C.timesOff):
                        # if click is continuing from last frame, update time of clicked until
                        C.timesOff[-1] = C.buttonClock.getTime()
                    if not C.wasClicked:
                        # end routine when C is clicked
                        continueRoutine = False
                    if not C.wasClicked:
                        # run callback code when C is clicked
                        pass
            # take note of whether C was clicked, so that next frame we know if clicks are new
            C.wasClicked = C.isClicked and C.status == STARTED
            # *D* updates
            
            # if D is starting this frame...
            if D.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
                # keep track of start time/frame for later
                D.frameNStart = frameN  # exact frame index
                D.tStart = t  # local t and not account for scr refresh
                D.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(D, 'tStartRefresh')  # time at next scr refresh
                # update status
                D.status = STARTED
                D.setAutoDraw(True)
            
            # if D is active this frame...
            if D.status == STARTED:
                # update params
                pass
                # check whether D has been pressed
                if D.isClicked:
                    if not D.wasClicked:
                        # if this is a new click, store time of first click and clicked until
                        D.timesOn.append(D.buttonClock.getTime())
                        D.timesOff.append(D.buttonClock.getTime())
                    elif len(D.timesOff):
                        # if click is continuing from last frame, update time of clicked until
                        D.timesOff[-1] = D.buttonClock.getTime()
                    if not D.wasClicked:
                        # end routine when D is clicked
                        continueRoutine = False
                    if not D.wasClicked:
                        # run callback code when D is clicked
                        pass
            # take note of whether D was clicked, so that next frame we know if clicks are new
            D.wasClicked = D.isClicked and D.status == STARTED
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, inputs=inputs, win=win)
                return
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in Multiple_Choice_2Components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "Multiple_Choice_2" ---
        for thisComponent in Multiple_Choice_2Components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        thisExp.addData('Multiple_Choice_2.stopped', globalClock.getTime())
        experiment.addData('A.numClicks', A.numClicks)
        if A.numClicks:
           experiment.addData('A.timesOn', A.timesOn[0])
           experiment.addData('A.timesOff', A.timesOff[0])
        else:
           experiment.addData('A.timesOn', "")
           experiment.addData('A.timesOff', "")
        experiment.addData('B.numClicks', B.numClicks)
        if B.numClicks:
           experiment.addData('B.timesOn', B.timesOn[0])
           experiment.addData('B.timesOff', B.timesOff[0])
        else:
           experiment.addData('B.timesOn', "")
           experiment.addData('B.timesOff', "")
        experiment.addData('C.numClicks', C.numClicks)
        if C.numClicks:
           experiment.addData('C.timesOn', C.timesOn[0])
           experiment.addData('C.timesOff', C.timesOff[0])
        else:
           experiment.addData('C.timesOn', "")
           experiment.addData('C.timesOff', "")
        experiment.addData('D.numClicks', D.numClicks)
        if D.numClicks:
           experiment.addData('D.timesOn', D.timesOn[0])
           experiment.addData('D.timesOff', D.timesOff[0])
        else:
           experiment.addData('D.timesOn', "")
           experiment.addData('D.timesOff', "")
        # the Routine "Multiple_Choice_2" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        thisExp.nextEntry()
        
        if thisSession is not None:
            # if running in a Session with a Liaison client, send data up to now
            thisSession.sendExperimentData()
    # completed 1.0 repeats of 'experiment'
    
    # Run 'End Experiment' code from slider_code
    del myslider
    # save mic recordings
    for tag in mic.clips:
        for i, clip in enumerate(mic.clips[tag]):
            clipFilename = 'recording_mic_%s.wav' % tag
            # if there's more than 1 clip with this tag, append a counter for all beyond the first
            if i > 0:
                clipFilename += '_%s' % i
            clip.save(os.path.join(micRecFolder, clipFilename))
    # Run 'End Experiment' code from slider_code
    del myslider
    # save mic recordings
    for tag in mic.clips:
        for i, clip in enumerate(mic.clips[tag]):
            clipFilename = 'recording_mic_%s.wav' % tag
            # if there's more than 1 clip with this tag, append a counter for all beyond the first
            if i > 0:
                clipFilename += '_%s' % i
            clip.save(os.path.join(micRecFolder, clipFilename))
    
    # mark experiment as finished
    endExperiment(thisExp, win=win, inputs=inputs)


def saveData(thisExp):
    """
    Save data from this experiment
    
    Parameters
    ==========
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    """
    filename = thisExp.dataFileName
    # these shouldn't be strictly necessary (should auto-save)
    thisExp.saveAsWideText(filename + '.csv', delim='auto')
    thisExp.saveAsPickle(filename)


def endExperiment(thisExp, inputs=None, win=None):
    """
    End this experiment, performing final shut down operations.
    
    This function does NOT close the window or end the Python process - use `quit` for this.
    
    Parameters
    ==========
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    inputs : dict
        Dictionary of input devices by name.
    win : psychopy.visual.Window
        Window for this experiment.
    """
    if win is not None:
        # remove autodraw from all current components
        win.clearAutoDraw()
        # Flip one final time so any remaining win.callOnFlip() 
        # and win.timeOnFlip() tasks get executed
        win.flip()
    # mark experiment handler as finished
    thisExp.status = FINISHED
    # shut down eyetracker, if there is one
    if inputs is not None:
        if 'eyetracker' in inputs and inputs['eyetracker'] is not None:
            inputs['eyetracker'].setConnectionState(False)


def quit(thisExp, win=None, inputs=None, thisSession=None):
    """
    Fully quit, closing the window and ending the Python process.
    
    Parameters
    ==========
    win : psychopy.visual.Window
        Window to close.
    inputs : dict
        Dictionary of input devices by name.
    thisSession : psychopy.session.Session or None
        Handle of the Session object this experiment is being run from, if any.
    """
    thisExp.abort()  # or data files will save again on exit
    # make sure everything is closed down
    if win is not None:
        # Flip one final time so any remaining win.callOnFlip() 
        # and win.timeOnFlip() tasks get executed before quitting
        win.flip()
        win.close()
    if inputs is not None:
        if 'eyetracker' in inputs and inputs['eyetracker'] is not None:
            inputs['eyetracker'].setConnectionState(False)
    if thisSession is not None:
        thisSession.stop()
    # terminate Python process
    core.quit()


# if running this experiment as a script...
if __name__ == '__main__':
    # call all functions in order
    expInfo = showExpInfoDlg(expInfo=expInfo)
    thisExp = setupData(expInfo=expInfo)
    logFile = setupLogging(filename=thisExp.dataFileName)
    win = setupWindow(expInfo=expInfo)
    inputs = setupInputs(expInfo=expInfo, thisExp=thisExp, win=win)
    run(
        expInfo=expInfo, 
        thisExp=thisExp, 
        win=win, 
        inputs=inputs
    )
    saveData(thisExp=thisExp)
    quit(thisExp=thisExp, win=win, inputs=inputs)
