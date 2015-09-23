import os

import scipy.io.wavfile as wavfile

import glob


def convertDirMp3ToWav(dirName):

	'''
		This function converts MP3 files in a directory to WAV files
	'''

	#create a tuple of file types
	
	fs = 44100

	nC = 1

	types = (dirName + os.sep + '*.mp3',)

	filesToProcess = []

	for files in types:

		filesToProcess.extend(glob.glob(files))

	for f in filesToProcess:

		wavFileName = f.replace(".mp3",".wav")

		command = "avconv -i \"" + f + "\" -ar " + str(fs) +" -ac " + str(nC) +" \"" + wavFileName +"\"";

		print command

		os.system(command.decode('unicode_escape').encode('ascii','ignore').replace("\0",""))



def readAudio(path):

	'''
		input is the path of the file

		output are Fs and X

		Fs is the sample rate in Hz

		X is the signal array
	'''

	#get the type(.wav) of the file in the path

	fileType = os.path.splitext(path)[1]
	
	#check if the file type is wav, read the wav file
	try:
		if fileType.lower() == '.wav':
		
			[Fs, X] = wavfile.read(path)

		else:
			print "Error in readAudio(): Unknown file type"
			
			return (-1, -1)

	except IOError:
		print "File Type not found or other IO error"
		
		return (-1, -1)

	return (Fs, X)

		
	
