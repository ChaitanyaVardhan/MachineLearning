import os
import scipy.io.wavfile as wavfile

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

		
	
