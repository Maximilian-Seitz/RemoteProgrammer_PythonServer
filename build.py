import os
import json
import re
import time

def get_indentations(indentations):
	return "\t" * indentations


def convert_code_element_to_python( code_element, indentations ):
	if not isinstance(code_element,dict):
		return '\"' + code_element + '\"'
	
	indents = get_indentations(indentations)
	
	
	code_id = code_element["id"];
	param_str = []
	code_block_str = []
	
	
	if "params" in code_element:
		params = code_element["params"]
		
		for param in params:
			param_str.append(convert_code_element_to_python(param, 0))
	
	
	if "blocks" in code_element:
		code_blocks = code_element["blocks"]
		
		for code_block in code_blocks:
			code_block_str.append(convert_code_block_to_python(code_block, indentations + 1))
	
	
	with open("functions/" + code_id) as code_format:
		code = indents + code_format.read().replace("\n", "\n" + indents)
		code = code.replace(indents + "%c%", "%c%")
	
	for param in param_str:
		code = code.replace('%p%', param, 1)

	
	m = True
	while m:
		m = re.search('%p([0-9]+)%', code)
		
		if m:
			code = code.replace("%p" + m.group(1) + "%", param_str[int(m.group(1))])
	
	code = code.replace('%t%', str(indentations))
	
	for code_block in code_block_str:
		code = code.replace('%c%', code_block, 1)
	
	return code


def convert_code_block_to_python( code_block, indentations ):
	code = ""
	
	for code_element in code_block:
		code += convert_code_element_to_python(code_element, indentations) + "\n"
	
	if len(code_block) > 0:
		code = code[:-1]
	
	return code


def build_file( path_json_file, path_python_file ):
	pre_code_file = "output_additions/precode"
	post_code_file = "output_additions/postcode"
	
	if not os.path.isfile(path_json_file):
		return False
	
	with open(path_json_file) as json_data:
		code_block = json.load(json_data)
		
		code = convert_code_block_to_python(code_block, 0)
		
		if os.path.isfile(pre_code_file):
			with open(pre_code_file) as pre_code:
				code = pre_code.read() + "\n" + code
		
		if os.path.isfile(post_code_file):
			with open(post_code_file) as post_code:
				code = code + "\n" + post_code.read()
		
		python_file = open(path_python_file, 'w')
		python_file.write(code)
	
	return True


def build_folder( path_json_folder, path_python_folder, path_json_backup_folder ):
	for(dirpath, dirnames, filenames) in os.walk(path_json_folder):
		for filename in filenames:
			filename_no_extension, file_extension = os.path.splitext(filename)
			build_file(path_json_folder + filename, path_python_folder + filename_no_extension + ".py")
			
			#Delete json backup file
			if os.path.isfile(path_json_backup_folder + filename):
				os.remove(path_json_backup_folder + filename)
			
			#Create json backup folder
			if not os.path.exists(path_json_backup_folder):
				os.makedirs(path_json_backup_folder)
			
			#Move processed file into backup folder
			os.rename(path_json_folder + filename, path_json_backup_folder + filename)


if __name__ == "__main__":
	build_folder("user_files_new/", "run_environment/", "user_files/")

