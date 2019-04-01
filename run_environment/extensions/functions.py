#!/usr/bin/env python3
# -*- coding: utf8 -*-

import pyttsx3
import time

tts_engine = pyttsx3.init()

def say(text):
	global tts_engine
	tts_engine.say(str(text))
	tts_engine.runAndWait()

def wait(secs):
	time.sleep(secs)