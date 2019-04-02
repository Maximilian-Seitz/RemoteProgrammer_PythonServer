#!flask/bin/python

from flask import Flask
from flask import request

from threading import Thread

import subprocess

#Used to check simmilarity between the sent command, and the potential options
from difflib import SequenceMatcher

import os
import os.path

import json

import datetime
import time

#my files
import build as Builder


app = Flask(__name__)

#Path to the folder, in case this is executed in another environment (for example from autostart)
project_folder = os.path.dirname(os.path.realpath(__file__))


#Names of folders with the files and resources needed
received_file_folder = "user_files_new/"
received_file_storage_folder = "user_files/"
run_environment_folder = "run_environment/"

format_file_path = "/code_syntax/format.json"
language_file_path = "/code_syntax/lang.json"
categories_file_path = "/code_syntax/categories.json"


running_function_process = None


#Method that can be used to check if the server is running on a given ip + port
@app.route('/')
def index():
	return "<b>Hello, World!</b>"

#Method that gives the definitions for the code elements (the drag-and-drop items in the app)
@app.route('/code_syntax/format')
def code_syntax_format():
	data = open(project_folder + format_file_path, "r").read()
	return data

#Method that gives the language dependent strings (for localisation)
@app.route('/code_syntax/lang')
def code_syntax_lang():
	data = open(project_folder + language_file_path, "r").read()
	return data

#Method that gives the definitions of the categories
@app.route('/code_syntax/categories')
def code_syntax_categories():
	data = open(project_folder + categories_file_path, "r").read()
	return data

#Method that gives the status of the files in the folder (including the functions that are available)
@app.route('/info')
def info():
	data = {}
	
	data["time"] = int(time.time())
	
	data["categories"] = int(os.path.getmtime(project_folder + categories_file_path))
	data["format"] = int(os.path.getmtime(project_folder + format_file_path))
	data["lang"] = int(os.path.getmtime(project_folder + language_file_path))
	data["test"] = time.strftime('%d.%m.%Y-%H:%M:%S', time.gmtime(os.path.getmtime(project_folder + categories_file_path)))
	
	data["functions"] = {}
	
	for(dirpath, dirnames, filenames) in os.walk(project_folder + "/" + received_file_storage_folder):
		for filename in filenames:
			filename_no_extension, file_extension = os.path.splitext(filename)
			data["functions"][filename_no_extension] = int(os.path.getmtime(dirpath + filename))
	
	
	return json.dumps(data)

#Method that stores a sent function, and builds it
@app.route('/function/<string:name>/<int:updatetime>', methods=["POST"])
def function(name, updatetime):
	if request.json:
		filesReceived = False
		
		with open(project_folder + "/" + received_file_folder + name + '.json', 'w+') as function_file:
			function_file.write(json.dumps(request.json))
			
			filesReceived = True
		
		if filesReceived:
			Builder.build_folder(received_file_folder, run_environment_folder, received_file_storage_folder)
	
	return "{}"

#Method that executes a given command
@app.route('/command', methods=["POST"])
def command():
	global running_function_process
	
	return_data = {}
	return_data["text"] = "Function not found."
	
	if request.json:
		best_match = ""
		best_simmilarity = 0
		
		for filename in os.listdir(project_folder + "/" + run_environment_folder):
			if os.path.isfile(project_folder + "/" + run_environment_folder + filename):
				filename_no_extension, file_extension = os.path.splitext(filename)
				
				simmilarity_factor = SequenceMatcher(None, request.json["text"].lower(), filename_no_extension.lower()).ratio()
				
				if simmilarity_factor > best_simmilarity:
					best_simmilarity = simmilarity_factor
					best_match = filename
		
		if best_simmilarity >= 0.6:
			cmd = 'python "' + project_folder + "/" + run_environment_folder + best_match + '"'
			
			if running_function_process:
				running_function_process.kill()
			
			running_function_process = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
			
			return_data["text"] = "Executing:\n\t" + best_match
	
	return json.dumps(return_data)

if __name__ == '__main__':
	app.run(host = '10.48.223.2', debug = True)










