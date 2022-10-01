if __name__ != "__main__":
	print("Not a module")
	raise ImportError()

import os
import time
import threading as thr
import sys
# from lib import YoutubeDL

def parse(file): # OK
	comment, urllist, dirlisting, dirkey = False, {}, [], "."

	for line in file:
		line = line.strip()

		# Comment Check Block
		if line.startswith("/*"):
			comment = True
		if line.endswith("*/"):
			comment = False
			continue
		if not line or line.startswith("#") or comment:
			continue

		# Directory Check Block
		if line.startswith("[DIR ") and line.endswith("]"):
			if dirlisting:
				urllist[dirkey] = tuple(dirlisting)
				dirlisting.clear()
			dirkey = line[5:-1]

		# Root Directory Check Block
		elif line.startswith("[ROOT ") and line.endswith("]"):
			os.chdir(line[6:-1])

		# New URL Check Block
		else:
			urlpair = line.split(">>", 1)
			if len(urlpair) == 2:
				dirlisting.append((urlpair[0].strip(), urlpair[1].strip()))
	if dirlisting:
		urllist[dirkey] = tuple(dirlisting)
	return urllist

def dl(url, path):
	starttime = time.time_ns()
	attempts = 0
	while True:
		if os.system(DLCOMMAND %(os.devnull, YTDLPATH, os.path.join(path, url[1]), url[0])) == 1:
			attempts += 1
			print(" \033[93m%s\033[91m%s: An Error occured while trying to download \033[93m%s\033[0m" %(time.strftime("[%d %b %Y %H:%M:%S] ", time.gmtime()), attempts, url[1]))
			if attempts == 1:
				print(" Running second attempt...")
			elif attempts == 2:
				print(" Running third attempt...")
			elif attempts == 3:
				print(" Aborting download...")
				return
			time.sleep(5)
			continue
		else:
			print(" \033[93m%s\033[92m%s: Succesfully downloaded \033[93m%s\033[92m after \033[93m%s.%s\033[92m seconds\033[0m" %(time.strftime("[%d %b %Y %H:%M:%S] ", time.gmtime()), attempts, url[1], (time.time_ns() - starttime) // 1000000000, str((time.time_ns() - starttime) % 1000000000)[:4]))
			return

def sizeformat(size):
	table = {
		"PiB": 1024**5,
		"TiB": 1024**4,
		"GiB": 1024**3,
		"MiB": 1024**2,
		"KiB": 1024
	}
	for unit in table:
		if size >= table[unit]:
			return "%s %s" %(size // table[unit], unit)
	return "%s B" %size

def getfile():
	while True:
		raw = input(PROMPT()).strip()
		if not raw:
			continue
		print("")
		if raw.casefold().startswith("?"):
			raw = raw[1:].split(maxsplit=1)
			try:
				cmd = raw[0].casefold()
			except IndexError:
				print("Error: Command is empty")
			else:
				try:
					argv = raw[1].strip()
				except IndexError:
					argv = None
				if cmd in ("q", "quit", "exit"):
					print("Goodbye...")
					exit(0)
				elif cmd in ("cd", "chdir"):
					if argv:
						path = argv
					else:
						path = input("Directory: ")
					try:
						os.chdir(os.path.realpath(path))
					except:
						print("Error: Could not change directory")
					else:
						print("Successfully changed directory to '%s'" %os.getcwd())
				elif cmd in ("md", "mkdir"):
					if argv:
						path = argv
					else:
						path = input("Directory: ")
					try:
						os.mkdir(path)
					except:
						print("Error: Could not create directory")
					else:
						print("Successfully created directory '%s'" %os.path.abspath(path))
				elif cmd in ("ls", "dir"):
					try:
						print("   Directory listing of '%s':\n" %os.getcwd())
						dirlisting = os.listdir()
						if dirlisting:
							for item in dirlisting:
								if os.path.isdir(item):
									if os.path.abspath(item) == os.path.realpath(item):
										print(" <DIR>       \033[94m" + item + "\033[0m")
									else:
										print(" <JUNCTION>  \033[96m" + item + "\033[0m -> [\033[96m%s\033[0m]" %os.path.realpath(item))
								elif os.path.isfile(item):
									print(" %s %s" %(sizeformat(os.path.getsize(item)).ljust(11), item))
								elif os.path.islink(item):
									print(" <SYMLINK>   \033[96m" + item + "\033[0m -> [\033[96m%s\033[0m]" %os.path.realpath(item))
								else:
									print(" <???>       " + item)
						else:
							print(" Directory is empty.")
					except:
						print("Error: Could not list directory content")
				else:
					print("Error: Unknown command literal")
		else:
			check = os.path.abspath(raw)
			if os.path.isfile(check):
				return check
			else:
				print("Error: The input file either does not exist on the system or is not a file.")
		print("")

def choice():
	while True:
		check = input("%s: Choice::[Yes/No]$ " %os.getlogin()).strip().casefold()
		if not check:
			continue
		elif check in ("yes", "y"):
			print("Proceeding...")
			return True
		elif check in ("no", "n"):
			print("Aborting...")
			return False
		else:
			print("Unknown option. Recognized options are yes and no.")

def main():
	try:
		with open(getfile(), "r", encoding="utf-8") as file:
			urllist = parse(file)
	except UnicodeError:
		print("Error: Could not decode Unicode file.\n")
		return

	if urllist:
		for i in urllist:
			print("%s:" %("[Current]" if i == "." else i))
			for j in urllist[i]:
				print("~\t%s -> %s" %(j[0], j[1]))
		print("\nProceed downloading this list?\n")
	else:
		print("\nThe download index is empty.\n")
		return

	if not choice(): return

	rootdir = os.getcwd()

	dlthreads = {}

	for directory in urllist:
		os.chdir(rootdir)
		if not (os.path.exists(directory) and os.path.isdir(directory)):
			try:
				os.mkdir(directory)
			except OSError:
				print("Malformed Directory Name: %s" %directory)
				continue
		os.chdir(directory)
		print("Downloading to %s:" %directory)
		for index, downloader in enumerate(urllist[directory]):
			time.sleep(0.1)
			print("\tDownloading %s..." %downloader[1])
			dlthreads["Download Thread %s" %index] = thr.Thread(target=dl, kwargs={"url": downloader, "path": os.getcwd()})
			dlthreads["Download Thread %s" %index].start()

	for threadkey in dlthreads:
		dlthreads[threadkey].join()
#		except KeyboardInterrupt:
#			time.sleep(1)
#			print("User Interrupt: Aborting running operations due to Ctrl-C keystroke...")
#			dlthreads.clear()
#		del dlthreads[threadkey]

	print("\nAll Files Downloaded\n")
	os.chdir(rootdir)


print("Xtraordinary Media Downloadel version 1.0\nCopyright (c) 2022 by BinaryIsBloat\nAll rights reserved.\n")

print("Updating youtube-dl...")
def PROMPT():
	return "%s: %s$ " %(os.getlogin(), os.getcwd())
YTDLPATH = "youtube-dl" + ("" if os.name == "posix" else ".exe")
DLCOMMAND = "1>%s %s -c -x --audio-format mp3 -o \"%s.webm\" -- \"%s\""
os.system("%s -U" %YTDLPATH)

while True:
	main()
