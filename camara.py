#Program that take a picture when there is a movement
#
#06-november-2016
# 
from time import sleep
from datetime import datetime
from sh import gphoto2 as gp
import signal, os, subprocess
import RPi.GPIO as GPIO

#ps -a
#gphoto2 --list-files capturetarget
#gphoto2 --set-config capturetarget=1

def configSensor():
	sensor = 17
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(sensor,GPIO.IN)

def killgphoto2Process():
	p = subprocess.Popen(['ps','-A'], stdout=subprocess.PIPE)
	out, err = p.communicate()

	for line in out.splitlines():
		if b'gvfsd-gphoto2' in line:
			pid = int(line.split(None,1)[0])
			os.kill(pid, signal.SIGKILL)

clearCommand = ["--folder", "/store_00020001/DCIM/100CANON", \
		"-R", "--delete-all-files"]
triggerCommand = ["--trigger-capture"]
downloadCommand = ["--get-all-files"]

save_location = "/home/pi/Desktop/project/server/public/fotos"

def createSaveFolder():
	try:
		os.makedirs(save_location)
	except:
		print("Failed to create")
	os.chdir(save_location)

def captureImages():
	try:
		gp(triggerCommand)
		sleep(3)
		gp(downloadCommand)
		gp(clearCommand)
	except:
		print("Error camera")

def renameFiles():
	for filename in os.listdir("."):
		if len(filename) < 13:
			if filename.endswith(".JPG"):
				os.rename(filename, ("1.jpg"))
				print("Rename")
			elif filename.endswith(".CR2"):
				os.rename(filename, ("1.cr2"))
				print("Rename CR2")

def take():
	killgphoto2Process()
	gp(clearCommand)
	createSaveFolder()
	captureImages()
	renameFiles()
	
def run():
	try:
		if(GPIO.input(sensor)):
			take()
			time.sleep(10)
	except:
		print("Error python")
