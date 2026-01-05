#!/usr/bin/env python3

"""
About
  A simple Python script to easily hide and make visible files or directories on Windows and Linux.

  How it works
    On Linux:
    * It adds a dot at the beginning of a file or directory (target) to hide it.
    * It removes the dot from the beginning of the target to make it visible.

   On Windows:
	* It changes target's properties (to hidden) by running "attrib +H" to hide.
    * It changes target's properties by running "attrib -H" to make visible.

More
  It doesn't do anything special at a low level. 
  After hiding the targets, they can still be easily seen by just toggling an option in the file explorer, or with 'ls -a' on Linux.
  Requires Python 3.10+, because of the match-case statement (but it can be changed to if-elif-else statement).
"""

import os
import platform
import sys
import os.path

filename: str = sys.argv[0]

# 	Detect OS
if platform.system() == "Windows":
	import subprocess # <-- For executing CMD / PowerShell 'attrib' command
	OS: str = "Windows"

elif platform.system() == "Linux":
	OS: str = "Linux"

else:
	print("Sorry, your OS is not supported")
	sys.exit(1)

class Script:
	def __init__(self, operating_system:str):
		self.operating_system: str = operating_system

	def usage():
		print(f"""
Usage: {filename} ACTION FILE_OR_DIRECTORY

Actions:
hide, -hide, --hide, hd           --> Make a file/directory visible
unhide, -unhide, --unhide, ud     --> Hide a file/directory
""")

	"""Checks if the file/directory (target) that the user provided exists"""
	def check_target(self, target:str) -> bool:
		return True if os.path.isfile(target) or os.path.isdir(target) else False

	def hide(self, target: str):
#		Windows, use "attrib" command
		if self.operating_system == "Windows":
			subprocess.run(["attrib","+H", target],check=True)

#		Linux, just add a dot
		elif self.operating_system == "Linux":
#		If the target is already hidden (has a dot in the beginning), won't do anything
			if target[0] == ".":
				return True
#			Otherwise
			hidden_target: str = "." + target
			os.rename(target, hidden_target)

	def unhide(self, target:str):
#		Windows
		if self.operating_system == "Windows":
			subprocess.run(["attrib","-H", target],check=True)

#		Linux
		elif self.operating_system == "Linux":
#			If the target is already visible, won't do anything
			if target[0] != ".":
				return True

			visible_target: str = target[1:] # <-- This removes the fist char from the string
			os.rename(target, visible_target)

if __name__ == '__main__':
	if len(sys.argv) == 1:
		Script.usage()
		sys.exit()

	script: Script = Script(OS)

#	Check user arguments
	user_action: str = str( sys.argv[1].lower() )
	match user_action:
		case "hide" | "-hide" | "--hide" | "hd":
#			check if user has multiple targets or just a single one
			if len(sys.argv) > 3:
				for each_target in sys.argv[2:]:
					if script.check_target(each_target) is True:
						script.hide(each_target)
					else:
						print(f"File '{each_target}' doesn't exist")
			else:
#				Same code as above but in one line
				script.hide(sys.argv[2]) if script.check_target(sys.argv[2]) is True else print(f"File '{sys.argv[2]}' doesn't exist")


		case "unhide" | "-unhide" | "--unhide" | "ud":
			if len(sys.argv) > 3:
				for each_target in sys.argv[2:]:
					if script.check_target(each_target) is True:
						script.unhide(each_target)
					else:
						print(f"File '{each_target}' doesn't exist")
			else:
				script.unhide(sys.argv[2]) if script.check_target(sys.argv[2]) is True else print(f"File '{sys.argv[2]}' doesn't exist")

		case _:
			print(f"Unsupported argument/action: {user_action}")
			sys.exit(1)
