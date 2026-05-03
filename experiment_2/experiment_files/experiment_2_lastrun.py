#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2024.2.4),
    on Sat Jul  5 12:23:09 2025
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
from psychopy import sound, gui, visual, core, data, event, logging, clock, colors, layout, hardware
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

# Run 'Before Experiment' code from slider_setup
import serial
import time
import serial.tools.list_ports
import multiprocessing as mp
import csv
import sys

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
            trial_offset = 0
            while trial.is_set():
                line = ser.readline()
                if trial_offset == 0:
                    trial_offset = time.monotonic()
                    
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
                    output_data[i] = (pt[0], pt[1] - offset + ((trial_offset - trial_start_time) * 1000))
                
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

        while not self.ready.is_set():
            if not self.proc.is_alive():
                raise Exception("Error: Slider process exited")
            time.sleep(0.01)

    def start_trial(self, wav_file):
        if not self.proc.is_alive():
            raise Exception("Error: Slider process exited")
        else:
            while not self.ready.is_set():
                if not self.proc.is_alive():
                    raise Exception("Error: Slider process exited")
                time.sleep(0.01)
            self.trial.set()
            self.queue.put(wav_file)

    def stop_trial(self):
        self.trial.clear()
        if not self.proc.is_alive():
            raise Exception("Error: Slider process exited")
        else:
            while not self.ready.is_set():
                if not self.proc.is_alive():
                    raise Exception("Error: Slider process exited")
                time.sleep(0.01)

    def __del__(self):
        self.stop.set()
        self.proc.join()
# --- Setup global variables (available in all functions) ---
# create a device manager to handle hardware (keyboards, mice, mirophones, speakers, etc.)
deviceManager = hardware.DeviceManager()
# ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
# store info about the experiment session
psychopyVersion = '2024.2.4'
expName = 'speech_rate'  # from the Builder filename that created this script
# information about this experiment
expInfo = {
    'participant': '',
    'session': '001',
    'date|hid': data.getDateStr(),
    'expName|hid': expName,
    'psychopyVersion|hid': psychopyVersion,
}

# --- Define some variables which will change depending on pilot mode ---
'''
To run in pilot mode, either use the run/pilot toggle in Builder, Coder and Runner, 
or run the experiment with `--pilot` as an argument. To change what pilot 
#mode does, check out the 'Pilot mode' tab in preferences.
'''
# work out from system args whether we are running in pilot mode
PILOTING = core.setPilotModeFromArgs()
# start off with values from experiment settings
_fullScr = True
_winSize = [1512, 982]
# if in pilot mode, apply overrides according to preferences
if PILOTING:
    # force windowed mode
    if prefs.piloting['forceWindowed']:
        _fullScr = False
        # set window size
        _winSize = prefs.piloting['forcedWindowSize']

def showExpInfoDlg(expInfo):
    """
    Show participant info dialog.
    Parameters
    ==========
    expInfo : dict
        Information about this experiment.
    
    Returns
    ==========
    dict
        Information about this experiment.
    """
    # show participant info dialog
    dlg = gui.DlgFromDict(
        dictionary=expInfo, sortKeys=False, title=expName, alwaysOnTop=True
    )
    if dlg.OK == False:
        core.quit()  # user pressed cancel
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
    # remove dialog-specific syntax from expInfo
    for key, val in expInfo.copy().items():
        newKey, _ = data.utils.parsePipeSyntax(key)
        expInfo[newKey] = expInfo.pop(key)
    
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
        originPath='/Users/irmakergin/Desktop/experiment_2/experiment_2_lastrun.py',
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
    # set how much information should be printed to the console / app
    if PILOTING:
        logging.console.setLevel(
            prefs.piloting['pilotConsoleLoggingLevel']
        )
    else:
        logging.console.setLevel('warning')


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
    if PILOTING:
        logging.debug('Fullscreen settings ignored as running in pilot mode.')
    
    if win is None:
        # if not given a window to setup, make one
        win = visual.Window(
            size=_winSize, fullscr=_fullScr, screen=0,
            winType='pyglet', allowGUI=True, allowStencil=True,
            monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
            backgroundImage='', backgroundFit='none',
            blendMode='avg', useFBO=True,
            units='height',
            checkTiming=False  # we're going to do this ourselves in a moment
        )
    else:
        # if we have a window, just set the attributes which are safe to set
        win.color = [0,0,0]
        win.colorSpace = 'rgb'
        win.backgroundImage = ''
        win.backgroundFit = 'none'
        win.units = 'height'
    if expInfo is not None:
        # get/measure frame rate if not already in expInfo
        if win._monitorFrameRate is None:
            win._monitorFrameRate = win.getActualFrameRate(infoMsg='Attempting to measure frame rate of screen, please wait...')
        expInfo['frameRate'] = win._monitorFrameRate
    win.hideMessage()
    # show a visual indicator if we're in piloting mode
    if PILOTING and prefs.piloting['showPilotingIndicator']:
        win.showPilotingIndicator()
    
    return win


def setupDevices(expInfo, thisExp, win):
    """
    Setup whatever devices are available (mouse, keyboard, speaker, eyetracker, etc.) and add them to 
    the device manager (deviceManager)
    
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
    bool
        True if completed successfully.
    """
    # --- Setup input devices ---
    ioConfig = {}
    ioSession = ioServer = eyetracker = None
    
    # store ioServer object in the device manager
    deviceManager.ioServer = ioServer
    
    # create a default keyboard (e.g. to check for escape)
    if deviceManager.getDevice('defaultKeyboard') is None:
        deviceManager.addDevice(
            deviceClass='keyboard', deviceName='defaultKeyboard', backend='event'
        )
    # create speaker 'Experimen_audio'
    deviceManager.addDevice(
        deviceName='Experimen_audio',
        deviceClass='psychopy.hardware.speaker.SpeakerDevice',
        index=-1
    )
    # create speaker 'Experimen_audio_2'
    deviceManager.addDevice(
        deviceName='Experimen_audio_2',
        deviceClass='psychopy.hardware.speaker.SpeakerDevice',
        index=-1
    )
    # return True if completed successfully
    return True

def pauseExperiment(thisExp, win=None, timers=[], playbackComponents=[]):
    """
    Pause this experiment, preventing the flow from advancing to the next routine until resumed.
    
    Parameters
    ==========
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
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
    
    # start a timer to figure out how long we're paused for
    pauseTimer = core.Clock()
    # pause any playback components
    for comp in playbackComponents:
        comp.pause()
    # make sure we have a keyboard
    defaultKeyboard = deviceManager.getDevice('defaultKeyboard')
    if defaultKeyboard is None:
        defaultKeyboard = deviceManager.addKeyboard(
            deviceClass='keyboard',
            deviceName='defaultKeyboard',
            backend='Pyglet',
        )
    # run a while loop while we wait to unpause
    while thisExp.status == PAUSED:
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=['escape']):
            endExperiment(thisExp, win=win)
        # sleep 1ms so other threads can execute
        clock.time.sleep(0.001)
    # if stop was requested while paused, quit
    if thisExp.status == FINISHED:
        endExperiment(thisExp, win=win)
    # resume any playback components
    for comp in playbackComponents:
        comp.play()
    # reset any timers
    for timer in timers:
        timer.addTime(-pauseTimer.getTime())


def run(expInfo, thisExp, win, globalClock=None, thisSession=None):
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
    globalClock : psychopy.core.clock.Clock or None
        Clock to get global time from - supply None to make a new one.
    thisSession : psychopy.session.Session or None
        Handle of the Session object this experiment is being run from, if any.
    """
    # mark experiment as started
    thisExp.status = STARTED
    # make sure window is set to foreground to prevent losing focus
    win.winHandle.activate()
    # make sure variables created by exec are available globally
    exec = environmenttools.setExecEnvironment(globals())
    # get device handles from dict of input devices
    ioServer = deviceManager.ioServer
    # get/create a default keyboard (e.g. to check for escape)
    defaultKeyboard = deviceManager.getDevice('defaultKeyboard')
    if defaultKeyboard is None:
        deviceManager.addDevice(
            deviceClass='keyboard', deviceName='defaultKeyboard', backend='Pyglet'
        )
    eyetracker = deviceManager.getDevice('eyetracker')
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
    
    # --- Initialize components for Routine "Instructions" ---
    text = visual.TextStim(win=win, name='text',
        text='Welcome!\n\nIn this experiment, you will hear 2 audio segments with varying speeds of speech. You will be asked to continuously indicate your level of comprehension using the slider.\n\nWhile listening to the first segment, please use your *left hand* for the slider.\n\nThere will be a break between 2 segments. You can use this time to rest. Before you play the second one, we will ask you to switch the slider potision so you can use it with your *right hand*.',
        font='Open Sans',
        pos=(0, 0), draggable=False, height=0.03, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    button = visual.ButtonStim(win, 
        text='Next', font='Arvo',
        pos=(0,-0.4),
        letterHeight=0.02,
        size=(0.2, 0.1), 
        ori=0.0
        ,borderWidth=0.0,
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
    # Run 'Begin Experiment' code from slider_setup
    myslider = Slider(expInfo['participant'], expInfo['session'])
    
    
    # --- Initialize components for Routine "Start_Exp" ---
    Start_exp = visual.TextStim(win=win, name='Start_exp',
        text='Press the button below to start the experiment.',
        font='Open Sans',
        pos=(0, 0.4), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    Start = visual.ButtonStim(win, 
        text='Start', font='Arvo',
        pos=(0, 0),
        letterHeight=0.05,
        size=(0.5, 0.5), 
        ori=0.0
        ,borderWidth=0.0,
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
        size=(0.5, 0.5), 
        ori=0.0
        ,borderWidth=0.0,
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
    text_6 = visual.TextStim(win=win, name='text_6',
        text='Please reset the slider and get ready to use it!',
        font='Open Sans',
        pos=(0, 0.3), draggable=False, height=0.03, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    
    # --- Initialize components for Routine "Training_Segment" ---
    Experimen_audio = sound.Sound(
        'A', 
        secs=-1, 
        stereo=True, 
        hamming=True, 
        speaker='Experimen_audio',    name='Experimen_audio'
    )
    Experimen_audio.setVolume(1.0)
    polygon = visual.ShapeStim(
        win=win, name='polygon', vertices='cross',
        size=(0.03, 0.03),
        ori=180.0, pos=(0, 0), draggable=False, anchor='center',
        lineWidth=1.0,
        colorSpace='rgb', lineColor='white', fillColor='white',
        opacity=None, depth=-2.0, interpolate=True)
    
    # --- Initialize components for Routine "Break" ---
    Start_exp_2 = visual.TextStim(win=win, name='Start_exp_2',
        text='You can take a break to rest.\n\nWhen you are ready, please position your *right hand* on the slider.\n\nPress the button below to start the second half.\n',
        font='Open Sans',
        pos=(0, 0.4), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    Start_2 = visual.ButtonStim(win, 
        text='Start', font='Arvo',
        pos=(0, 0),
        letterHeight=0.05,
        size=(0.5, 0.5), 
        ori=0.0
        ,borderWidth=0.0,
        fillColor='darkgrey', borderColor=None,
        color='white', colorSpace='rgb',
        opacity=None,
        bold=True, italic=False,
        padding=None,
        anchor='center',
        name='Start_2',
        depth=-1
    )
    Start_2.buttonClock = core.Clock()
    
    # --- Initialize components for Routine "Start_Segment" ---
    Play = visual.ButtonStim(win, 
        text='Play', font='Arvo',
        pos=(0, 0),
        letterHeight=0.05,
        size=(0.5, 0.5), 
        ori=0.0
        ,borderWidth=0.0,
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
    text_6 = visual.TextStim(win=win, name='text_6',
        text='Please reset the slider and get ready to use it!',
        font='Open Sans',
        pos=(0, 0.3), draggable=False, height=0.03, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    
    # --- Initialize components for Routine "Segment_2" ---
    Experimen_audio_2 = sound.Sound(
        'A', 
        secs=-1, 
        stereo=True, 
        hamming=True, 
        speaker='Experimen_audio_2',    name='Experimen_audio_2'
    )
    Experimen_audio_2.setVolume(1.0)
    polygon_2 = visual.ShapeStim(
        win=win, name='polygon_2', vertices='cross',
        size=(0.03, 0.03),
        ori=180.0, pos=(0, 0), draggable=False, anchor='center',
        lineWidth=1.0,
        colorSpace='rgb', lineColor='white', fillColor='white',
        opacity=None, depth=-2.0, interpolate=True)
    
    # --- Initialize components for Routine "Thanks" ---
    text_7 = visual.TextStim(win=win, name='text_7',
        text='Thank you!',
        font='Open Sans',
        pos=(0, 0), draggable=False, height=0.07, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    
    # create some handy timers
    
    # global clock to track the time since experiment started
    if globalClock is None:
        # create a clock if not given one
        globalClock = core.Clock()
    if isinstance(globalClock, str):
        # if given a string, make a clock accoridng to it
        if globalClock == 'float':
            # get timestamps as a simple value
            globalClock = core.Clock(format='float')
        elif globalClock == 'iso':
            # get timestamps in ISO format
            globalClock = core.Clock(format='%Y-%m-%d_%H:%M:%S.%f%z')
        else:
            # get timestamps in a custom format
            globalClock = core.Clock(format=globalClock)
    if ioServer is not None:
        ioServer.syncClock(globalClock)
    logging.setDefaultClock(globalClock)
    # routine timer to track time remaining of each (possibly non-slip) routine
    routineTimer = core.Clock()
    win.flip()  # flip window to reset last flip timer
    # store the exact time the global clock started
    expInfo['expStart'] = data.getDateStr(
        format='%Y-%m-%d %Hh%M.%S.%f %z', fractionalSecondDigits=6
    )
    
    # --- Prepare to start Routine "Instructions" ---
    # create an object to store info about Routine Instructions
    Instructions = data.Routine(
        name='Instructions',
        components=[text, button],
    )
    Instructions.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # reset button to account for continued clicks & clear times on/off
    button.reset()
    # store start times for Instructions
    Instructions.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    Instructions.tStart = globalClock.getTime(format='float')
    Instructions.status = STARTED
    thisExp.addData('Instructions.started', Instructions.tStart)
    Instructions.maxDuration = None
    # keep track of which components have finished
    InstructionsComponents = Instructions.components
    for thisComponent in Instructions.components:
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
    Instructions.forceEnded = routineForceEnded = not continueRoutine
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
            win.callOnFlip(button.buttonClock.reset)
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
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer], 
                playbackComponents=[]
            )
            # skip the frame we paused on
            continue
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            Instructions.forceEnded = routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in Instructions.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "Instructions" ---
    for thisComponent in Instructions.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for Instructions
    Instructions.tStop = globalClock.getTime(format='float')
    Instructions.tStopRefresh = tThisFlipGlobal
    thisExp.addData('Instructions.stopped', Instructions.tStop)
    thisExp.nextEntry()
    # the Routine "Instructions" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "Start_Exp" ---
    # create an object to store info about Routine Start_Exp
    Start_Exp = data.Routine(
        name='Start_Exp',
        components=[Start_exp, Start],
    )
    Start_Exp.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # reset Start to account for continued clicks & clear times on/off
    Start.reset()
    # store start times for Start_Exp
    Start_Exp.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    Start_Exp.tStart = globalClock.getTime(format='float')
    Start_Exp.status = STARTED
    thisExp.addData('Start_Exp.started', Start_Exp.tStart)
    Start_Exp.maxDuration = None
    # keep track of which components have finished
    Start_ExpComponents = Start_Exp.components
    for thisComponent in Start_Exp.components:
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
    Start_Exp.forceEnded = routineForceEnded = not continueRoutine
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
            win.callOnFlip(Start.buttonClock.reset)
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
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer], 
                playbackComponents=[]
            )
            # skip the frame we paused on
            continue
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            Start_Exp.forceEnded = routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in Start_Exp.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "Start_Exp" ---
    for thisComponent in Start_Exp.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for Start_Exp
    Start_Exp.tStop = globalClock.getTime(format='float')
    Start_Exp.tStopRefresh = tThisFlipGlobal
    thisExp.addData('Start_Exp.stopped', Start_Exp.tStop)
    thisExp.addData('Start.numClicks', Start.numClicks)
    if Start.numClicks:
       thisExp.addData('Start.timesOn', Start.timesOn)
       thisExp.addData('Start.timesOff', Start.timesOff)
    else:
       thisExp.addData('Start.timesOn', "")
       thisExp.addData('Start.timesOff', "")
    thisExp.nextEntry()
    # the Routine "Start_Exp" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "Start_Segment" ---
    # create an object to store info about Routine Start_Segment
    Start_Segment = data.Routine(
        name='Start_Segment',
        components=[Play, text_6],
    )
    Start_Segment.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # reset Play to account for continued clicks & clear times on/off
    Play.reset()
    # store start times for Start_Segment
    Start_Segment.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    Start_Segment.tStart = globalClock.getTime(format='float')
    Start_Segment.status = STARTED
    thisExp.addData('Start_Segment.started', Start_Segment.tStart)
    Start_Segment.maxDuration = None
    # keep track of which components have finished
    Start_SegmentComponents = Start_Segment.components
    for thisComponent in Start_Segment.components:
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
    Start_Segment.forceEnded = routineForceEnded = not continueRoutine
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
            win.callOnFlip(Play.buttonClock.reset)
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
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer], 
                playbackComponents=[]
            )
            # skip the frame we paused on
            continue
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            Start_Segment.forceEnded = routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in Start_Segment.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "Start_Segment" ---
    for thisComponent in Start_Segment.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for Start_Segment
    Start_Segment.tStop = globalClock.getTime(format='float')
    Start_Segment.tStopRefresh = tThisFlipGlobal
    thisExp.addData('Start_Segment.stopped', Start_Segment.tStop)
    thisExp.addData('Play.numClicks', Play.numClicks)
    if Play.numClicks:
       thisExp.addData('Play.timesOn', Play.timesOn)
       thisExp.addData('Play.timesOff', Play.timesOff)
    else:
       thisExp.addData('Play.timesOn', "")
       thisExp.addData('Play.timesOff', "")
    thisExp.nextEntry()
    # the Routine "Start_Segment" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # set up handler to look after randomisation of conditions etc
    trials = data.TrialHandler2(
        name='trials',
        nReps=1.0, 
        method='random', 
        extraInfo=expInfo, 
        originPath=-1, 
        trialList=data.importConditions('part1.xlsx'), 
        seed=None, 
    )
    thisExp.addLoop(trials)  # add the loop to the experiment
    thisTrial = trials.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
    if thisTrial != None:
        for paramName in thisTrial:
            globals()[paramName] = thisTrial[paramName]
    if thisSession is not None:
        # if running in a Session with a Liaison client, send data up to now
        thisSession.sendExperimentData()
    
    for thisTrial in trials:
        currentLoop = trials
        thisExp.timestampOnFlip(win, 'thisRow.t', format=globalClock.format)
        if thisSession is not None:
            # if running in a Session with a Liaison client, send data up to now
            thisSession.sendExperimentData()
        # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
        if thisTrial != None:
            for paramName in thisTrial:
                globals()[paramName] = thisTrial[paramName]
        
        # --- Prepare to start Routine "Training_Segment" ---
        # create an object to store info about Routine Training_Segment
        Training_Segment = data.Routine(
            name='Training_Segment',
            components=[Experimen_audio, polygon],
        )
        Training_Segment.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        Experimen_audio.setSound(wav_file, hamming=True)
        Experimen_audio.setVolume(1.0, log=False)
        Experimen_audio.seek(0)
        # Run 'Begin Routine' code from slider_rt
        myslider.start_trial(wav_file)
        # store start times for Training_Segment
        Training_Segment.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        Training_Segment.tStart = globalClock.getTime(format='float')
        Training_Segment.status = STARTED
        thisExp.addData('Training_Segment.started', Training_Segment.tStart)
        Training_Segment.maxDuration = None
        # keep track of which components have finished
        Training_SegmentComponents = Training_Segment.components
        for thisComponent in Training_Segment.components:
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
        # if trial has changed, end Routine now
        if isinstance(trials, data.TrialHandler2) and thisTrial.thisN != trials.thisTrial.thisN:
            continueRoutine = False
        Training_Segment.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *Experimen_audio* updates
            
            # if Experimen_audio is starting this frame...
            if Experimen_audio.status == NOT_STARTED and t >= 0.00-frameTolerance:
                # keep track of start time/frame for later
                Experimen_audio.frameNStart = frameN  # exact frame index
                Experimen_audio.tStart = t  # local t and not account for scr refresh
                Experimen_audio.tStartRefresh = tThisFlipGlobal  # on global time
                # add timestamp to datafile
                thisExp.addData('Experimen_audio.started', t)
                # update status
                Experimen_audio.status = STARTED
                Experimen_audio.play()  # start the sound (it finishes automatically)
            
            # if Experimen_audio is stopping this frame...
            if Experimen_audio.status == STARTED:
                if bool(False) or Experimen_audio.isFinished:
                    # keep track of stop time/frame for later
                    Experimen_audio.tStop = t  # not accounting for scr refresh
                    Experimen_audio.tStopRefresh = tThisFlipGlobal  # on global time
                    Experimen_audio.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.addData('Experimen_audio.stopped', t)
                    # update status
                    Experimen_audio.status = FINISHED
                    Experimen_audio.stop()
            
            # *polygon* updates
            
            # if polygon is starting this frame...
            if polygon.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                polygon.frameNStart = frameN  # exact frame index
                polygon.tStart = t  # local t and not account for scr refresh
                polygon.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(polygon, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'polygon.started')
                # update status
                polygon.status = STARTED
                polygon.setAutoDraw(True)
            
            # if polygon is active this frame...
            if polygon.status == STARTED:
                # update params
                pass
            
            # if polygon is stopping this frame...
            if polygon.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > polygon.tStartRefresh + duration-frameTolerance:
                    # keep track of stop time/frame for later
                    polygon.tStop = t  # not accounting for scr refresh
                    polygon.tStopRefresh = tThisFlipGlobal  # on global time
                    polygon.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'polygon.stopped')
                    # update status
                    polygon.status = FINISHED
                    polygon.setAutoDraw(False)
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[routineTimer], 
                    playbackComponents=[Experimen_audio]
                )
                # skip the frame we paused on
                continue
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                Training_Segment.forceEnded = routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in Training_Segment.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "Training_Segment" ---
        for thisComponent in Training_Segment.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for Training_Segment
        Training_Segment.tStop = globalClock.getTime(format='float')
        Training_Segment.tStopRefresh = tThisFlipGlobal
        thisExp.addData('Training_Segment.stopped', Training_Segment.tStop)
        # Run 'End Routine' code from slider_rt
        myslider.stop_trial()
        # the Routine "Training_Segment" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        thisExp.nextEntry()
        
    # completed 1.0 repeats of 'trials'
    
    if thisSession is not None:
        # if running in a Session with a Liaison client, send data up to now
        thisSession.sendExperimentData()
    
    # --- Prepare to start Routine "Break" ---
    # create an object to store info about Routine Break
    Break = data.Routine(
        name='Break',
        components=[Start_exp_2, Start_2],
    )
    Break.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # reset Start_2 to account for continued clicks & clear times on/off
    Start_2.reset()
    # store start times for Break
    Break.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    Break.tStart = globalClock.getTime(format='float')
    Break.status = STARTED
    thisExp.addData('Break.started', Break.tStart)
    Break.maxDuration = None
    # keep track of which components have finished
    BreakComponents = Break.components
    for thisComponent in Break.components:
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
    
    # --- Run Routine "Break" ---
    Break.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *Start_exp_2* updates
        
        # if Start_exp_2 is starting this frame...
        if Start_exp_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            Start_exp_2.frameNStart = frameN  # exact frame index
            Start_exp_2.tStart = t  # local t and not account for scr refresh
            Start_exp_2.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(Start_exp_2, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'Start_exp_2.started')
            # update status
            Start_exp_2.status = STARTED
            Start_exp_2.setAutoDraw(True)
        
        # if Start_exp_2 is active this frame...
        if Start_exp_2.status == STARTED:
            # update params
            pass
        # *Start_2* updates
        
        # if Start_2 is starting this frame...
        if Start_2.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
            # keep track of start time/frame for later
            Start_2.frameNStart = frameN  # exact frame index
            Start_2.tStart = t  # local t and not account for scr refresh
            Start_2.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(Start_2, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'Start_2.started')
            # update status
            Start_2.status = STARTED
            win.callOnFlip(Start_2.buttonClock.reset)
            Start_2.setAutoDraw(True)
        
        # if Start_2 is active this frame...
        if Start_2.status == STARTED:
            # update params
            pass
            # check whether Start_2 has been pressed
            if Start_2.isClicked:
                if not Start_2.wasClicked:
                    # if this is a new click, store time of first click and clicked until
                    Start_2.timesOn.append(Start_2.buttonClock.getTime())
                    Start_2.timesOff.append(Start_2.buttonClock.getTime())
                elif len(Start_2.timesOff):
                    # if click is continuing from last frame, update time of clicked until
                    Start_2.timesOff[-1] = Start_2.buttonClock.getTime()
                if not Start_2.wasClicked:
                    # end routine when Start_2 is clicked
                    continueRoutine = False
                if not Start_2.wasClicked:
                    # run callback code when Start_2 is clicked
                    pass
        # take note of whether Start_2 was clicked, so that next frame we know if clicks are new
        Start_2.wasClicked = Start_2.isClicked and Start_2.status == STARTED
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer], 
                playbackComponents=[]
            )
            # skip the frame we paused on
            continue
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            Break.forceEnded = routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in Break.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "Break" ---
    for thisComponent in Break.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for Break
    Break.tStop = globalClock.getTime(format='float')
    Break.tStopRefresh = tThisFlipGlobal
    thisExp.addData('Break.stopped', Break.tStop)
    thisExp.addData('Start_2.numClicks', Start_2.numClicks)
    if Start_2.numClicks:
       thisExp.addData('Start_2.timesOn', Start_2.timesOn)
       thisExp.addData('Start_2.timesOff', Start_2.timesOff)
    else:
       thisExp.addData('Start_2.timesOn', "")
       thisExp.addData('Start_2.timesOff', "")
    thisExp.nextEntry()
    # the Routine "Break" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "Start_Segment" ---
    # create an object to store info about Routine Start_Segment
    Start_Segment = data.Routine(
        name='Start_Segment',
        components=[Play, text_6],
    )
    Start_Segment.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # reset Play to account for continued clicks & clear times on/off
    Play.reset()
    # store start times for Start_Segment
    Start_Segment.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    Start_Segment.tStart = globalClock.getTime(format='float')
    Start_Segment.status = STARTED
    thisExp.addData('Start_Segment.started', Start_Segment.tStart)
    Start_Segment.maxDuration = None
    # keep track of which components have finished
    Start_SegmentComponents = Start_Segment.components
    for thisComponent in Start_Segment.components:
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
    Start_Segment.forceEnded = routineForceEnded = not continueRoutine
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
            win.callOnFlip(Play.buttonClock.reset)
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
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer], 
                playbackComponents=[]
            )
            # skip the frame we paused on
            continue
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            Start_Segment.forceEnded = routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in Start_Segment.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "Start_Segment" ---
    for thisComponent in Start_Segment.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for Start_Segment
    Start_Segment.tStop = globalClock.getTime(format='float')
    Start_Segment.tStopRefresh = tThisFlipGlobal
    thisExp.addData('Start_Segment.stopped', Start_Segment.tStop)
    thisExp.addData('Play.numClicks', Play.numClicks)
    if Play.numClicks:
       thisExp.addData('Play.timesOn', Play.timesOn)
       thisExp.addData('Play.timesOff', Play.timesOff)
    else:
       thisExp.addData('Play.timesOn', "")
       thisExp.addData('Play.timesOff', "")
    thisExp.nextEntry()
    # the Routine "Start_Segment" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # set up handler to look after randomisation of conditions etc
    trials_2 = data.TrialHandler2(
        name='trials_2',
        nReps=1.0, 
        method='random', 
        extraInfo=expInfo, 
        originPath=-1, 
        trialList=data.importConditions('part2.xlsx'), 
        seed=None, 
    )
    thisExp.addLoop(trials_2)  # add the loop to the experiment
    thisTrial_2 = trials_2.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisTrial_2.rgb)
    if thisTrial_2 != None:
        for paramName in thisTrial_2:
            globals()[paramName] = thisTrial_2[paramName]
    if thisSession is not None:
        # if running in a Session with a Liaison client, send data up to now
        thisSession.sendExperimentData()
    
    for thisTrial_2 in trials_2:
        currentLoop = trials_2
        thisExp.timestampOnFlip(win, 'thisRow.t', format=globalClock.format)
        if thisSession is not None:
            # if running in a Session with a Liaison client, send data up to now
            thisSession.sendExperimentData()
        # abbreviate parameter names if possible (e.g. rgb = thisTrial_2.rgb)
        if thisTrial_2 != None:
            for paramName in thisTrial_2:
                globals()[paramName] = thisTrial_2[paramName]
        
        # --- Prepare to start Routine "Segment_2" ---
        # create an object to store info about Routine Segment_2
        Segment_2 = data.Routine(
            name='Segment_2',
            components=[Experimen_audio_2, polygon_2],
        )
        Segment_2.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        Experimen_audio_2.setSound(wav_file, hamming=True)
        Experimen_audio_2.setVolume(1.0, log=False)
        Experimen_audio_2.seek(0)
        # Run 'Begin Routine' code from slider_rt_2
        myslider.start_trial(wav_file)
        # store start times for Segment_2
        Segment_2.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        Segment_2.tStart = globalClock.getTime(format='float')
        Segment_2.status = STARTED
        thisExp.addData('Segment_2.started', Segment_2.tStart)
        Segment_2.maxDuration = None
        # keep track of which components have finished
        Segment_2Components = Segment_2.components
        for thisComponent in Segment_2.components:
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
        
        # --- Run Routine "Segment_2" ---
        # if trial has changed, end Routine now
        if isinstance(trials_2, data.TrialHandler2) and thisTrial_2.thisN != trials_2.thisTrial.thisN:
            continueRoutine = False
        Segment_2.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *Experimen_audio_2* updates
            
            # if Experimen_audio_2 is starting this frame...
            if Experimen_audio_2.status == NOT_STARTED and t >= 0.00-frameTolerance:
                # keep track of start time/frame for later
                Experimen_audio_2.frameNStart = frameN  # exact frame index
                Experimen_audio_2.tStart = t  # local t and not account for scr refresh
                Experimen_audio_2.tStartRefresh = tThisFlipGlobal  # on global time
                # add timestamp to datafile
                thisExp.addData('Experimen_audio_2.started', t)
                # update status
                Experimen_audio_2.status = STARTED
                Experimen_audio_2.play()  # start the sound (it finishes automatically)
            
            # if Experimen_audio_2 is stopping this frame...
            if Experimen_audio_2.status == STARTED:
                if bool(False) or Experimen_audio_2.isFinished:
                    # keep track of stop time/frame for later
                    Experimen_audio_2.tStop = t  # not accounting for scr refresh
                    Experimen_audio_2.tStopRefresh = tThisFlipGlobal  # on global time
                    Experimen_audio_2.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.addData('Experimen_audio_2.stopped', t)
                    # update status
                    Experimen_audio_2.status = FINISHED
                    Experimen_audio_2.stop()
            
            # *polygon_2* updates
            
            # if polygon_2 is starting this frame...
            if polygon_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                polygon_2.frameNStart = frameN  # exact frame index
                polygon_2.tStart = t  # local t and not account for scr refresh
                polygon_2.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(polygon_2, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'polygon_2.started')
                # update status
                polygon_2.status = STARTED
                polygon_2.setAutoDraw(True)
            
            # if polygon_2 is active this frame...
            if polygon_2.status == STARTED:
                # update params
                pass
            
            # if polygon_2 is stopping this frame...
            if polygon_2.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > polygon_2.tStartRefresh + duration-frameTolerance:
                    # keep track of stop time/frame for later
                    polygon_2.tStop = t  # not accounting for scr refresh
                    polygon_2.tStopRefresh = tThisFlipGlobal  # on global time
                    polygon_2.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'polygon_2.stopped')
                    # update status
                    polygon_2.status = FINISHED
                    polygon_2.setAutoDraw(False)
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[routineTimer], 
                    playbackComponents=[Experimen_audio_2]
                )
                # skip the frame we paused on
                continue
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                Segment_2.forceEnded = routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in Segment_2.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "Segment_2" ---
        for thisComponent in Segment_2.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for Segment_2
        Segment_2.tStop = globalClock.getTime(format='float')
        Segment_2.tStopRefresh = tThisFlipGlobal
        thisExp.addData('Segment_2.stopped', Segment_2.tStop)
        # Run 'End Routine' code from slider_rt_2
        myslider.stop_trial()
        # the Routine "Segment_2" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        thisExp.nextEntry()
        
    # completed 1.0 repeats of 'trials_2'
    
    if thisSession is not None:
        # if running in a Session with a Liaison client, send data up to now
        thisSession.sendExperimentData()
    
    # --- Prepare to start Routine "Thanks" ---
    # create an object to store info about Routine Thanks
    Thanks = data.Routine(
        name='Thanks',
        components=[text_7],
    )
    Thanks.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # store start times for Thanks
    Thanks.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    Thanks.tStart = globalClock.getTime(format='float')
    Thanks.status = STARTED
    thisExp.addData('Thanks.started', Thanks.tStart)
    Thanks.maxDuration = None
    # keep track of which components have finished
    ThanksComponents = Thanks.components
    for thisComponent in Thanks.components:
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
    
    # --- Run Routine "Thanks" ---
    Thanks.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine and routineTimer.getTime() < 15.0:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *text_7* updates
        
        # if text_7 is starting this frame...
        if text_7.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            text_7.frameNStart = frameN  # exact frame index
            text_7.tStart = t  # local t and not account for scr refresh
            text_7.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(text_7, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'text_7.started')
            # update status
            text_7.status = STARTED
            text_7.setAutoDraw(True)
        
        # if text_7 is active this frame...
        if text_7.status == STARTED:
            # update params
            pass
        
        # if text_7 is stopping this frame...
        if text_7.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > text_7.tStartRefresh + 15-frameTolerance:
                # keep track of stop time/frame for later
                text_7.tStop = t  # not accounting for scr refresh
                text_7.tStopRefresh = tThisFlipGlobal  # on global time
                text_7.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'text_7.stopped')
                # update status
                text_7.status = FINISHED
                text_7.setAutoDraw(False)
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer], 
                playbackComponents=[]
            )
            # skip the frame we paused on
            continue
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            Thanks.forceEnded = routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in Thanks.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "Thanks" ---
    for thisComponent in Thanks.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for Thanks
    Thanks.tStop = globalClock.getTime(format='float')
    Thanks.tStopRefresh = tThisFlipGlobal
    thisExp.addData('Thanks.stopped', Thanks.tStop)
    # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
    if Thanks.maxDurationReached:
        routineTimer.addTime(-Thanks.maxDuration)
    elif Thanks.forceEnded:
        routineTimer.reset()
    else:
        routineTimer.addTime(-15.000000)
    thisExp.nextEntry()
    # Run 'End Experiment' code from slider_setup
    del myslider
    
    # mark experiment as finished
    endExperiment(thisExp, win=win)


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


def endExperiment(thisExp, win=None):
    """
    End this experiment, performing final shut down operations.
    
    This function does NOT close the window or end the Python process - use `quit` for this.
    
    Parameters
    ==========
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    win : psychopy.visual.Window
        Window for this experiment.
    """
    if win is not None:
        # remove autodraw from all current components
        win.clearAutoDraw()
        # Flip one final time so any remaining win.callOnFlip() 
        # and win.timeOnFlip() tasks get executed
        win.flip()
    # return console logger level to WARNING
    logging.console.setLevel(logging.WARNING)
    # mark experiment handler as finished
    thisExp.status = FINISHED


def quit(thisExp, win=None, thisSession=None):
    """
    Fully quit, closing the window and ending the Python process.
    
    Parameters
    ==========
    win : psychopy.visual.Window
        Window to close.
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
    setupDevices(expInfo=expInfo, thisExp=thisExp, win=win)
    run(
        expInfo=expInfo, 
        thisExp=thisExp, 
        win=win,
        globalClock='float'
    )
    saveData(thisExp=thisExp)
    quit(thisExp=thisExp, win=win)
