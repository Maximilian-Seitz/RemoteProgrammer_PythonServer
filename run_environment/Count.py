#!/usr/bin/env python3

from extensions import functions
import math

var = {}

#Add code here, which needs to be executed before the main code

for i0 in range(int("10")):
	var["x"] = str(i0)
	functions.say(str(float(var["x"]) + float("1")))
	functions.wait(float("2"))

#Add code here, which needs to be executed after the main code