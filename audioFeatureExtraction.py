import os

import numpy

import scipy

from scipy.fftpack import fft

from scipy.fftpack.realtransforms import dct

import glob

import readAudio as r

eps = 0.00000001

def stFeatureExtraction(signal, Fs, Win, Step):
	"""
        signal: input signal samples
	Fs : the sampling freq (in Hz)
	Win : Duration of the window in samples( Time * Fs)
	Step : Duration of the step in sample( Time * Fs)
	"""
	
	Win = int(Win)
	
	Step = int(Step)

	signal = numpy.double(signal)

	signal = signal / (2.0 ** 15)	

	DC = signal.mean()

	MAX = (numpy.abs(signal)).max()

	signal = (signal - DC) / MAX

	N =len(signal)

	curPos = 0
	
	countFrames = 0

	nFFT = Win / 2

	[fbank, freqs] = mfccInitFilterBanks(Fs, nFFT)

	nceps = 13
	
	stFeatures = numpy.array([], dtype = numpy.float64)
	
	while(curPos + Win - 1 < N):
	
		countFrames += 1

		x = signal[curPos:curPos + Win]

		curPos = curPos + Step

		X = abs(fft(x))

		X = X[0:nFFT]

		X = X / len(X)
		
		curFV = numpy.zeros((nceps, 1))

		curFV[0:nceps,0] = stMFCC(X, fbank, nceps).copy()

		if countFrames == 1:
	
			stFeatures = curFV
		else:
			stFeatures = numpy.concatenate((stFeatures, curFV), 1)


	stFeatures = numpy.mean(stFeatures, axis = 1)

	return numpy.array(stFeatures)


def mfccInitFilterBanks(fs, nfft):

	lowfreq =133.33

	linsc = 200/3.

	logsc = 1.0711703

	numLinFiltTotal = 13

	numLogFilt = 27

	if fs < 8000:
		
		nlogfil = 5
	
	nFiltTotal = numLinFiltTotal + numLogFilt	

	freqs = numpy.zeros(nFiltTotal + 2)

	freqs[:numLinFiltTotal] = lowfreq + numpy.arange(numLinFiltTotal) * linsc

	freqs[numLinFiltTotal:] = freqs[numLinFiltTotal - 1] * logsc ** numpy.arange(1, numLogFilt + 3)

	heights = 2. / (freqs[2:] - freqs[0:-2])

	fbank = numpy.zeros((nFiltTotal, nfft))

	nfreqs = numpy.arange(nfft) / (1. * nfft) * fs

	for i in range(nFiltTotal):
		
		lowTrFreq = freqs[i]
		
		cenTrFreq = freqs[i + 1]
		
		highTrFreq = freqs[i + 2]
		
		lid = numpy.arange(numpy.floor(lowTrFreq * nfft / fs) + 1, 
				   numpy.floor(cenTrFreq * nfft / fs) + 1, dtype = numpy.int) 
		
		lslope = heights[i] /(cenTrFreq - lowTrFreq)

		rid = numpy.arange(numpy.floor(cenTrFreq * nfft / fs) + 1,
				   numpy.floor(highTrFreq * nfft / fs) + 1, dtype = numpy.int)

		rslope = heights[i] / (highTrFreq - cenTrFreq)

		fbank[i][lid] = lslope * (nfreqs[lid] - lowTrFreq)

		fbank[i][rid] = rslope * (highTrFreq - nfreqs[rid])

	return fbank, freqs




def stMFCC(X, fbank, nceps):
	
	mspec = numpy.log10(numpy.dot(X, fbank.T)+eps)
	
	ceps = dct(mspec, type = 2, norm = 'ortho', axis = -1)[:nceps]

	return ceps


def stFeatureExtractionToFile(filename, win, step, outPutFile):

	[Fs, X] = r.readAudio(filename)

	ceps = stFeatureExtraction(X, Fs, win * Fs, step * Fs)

	numpy.save(outPutFile, ceps)

	numpy.savetxt(outPutFile + "*.csv", ceps.T, delimiter = ",")

	
def stFeatureExtractionToFileDir(dirname, win, step):

	types = (dirname + os.sep + '*.wav')

	filesToProcess = []

	for files in types:
		
		filesToProcess.extend(glob.glob(files))

	for f in filesToProcess:
	
		outPath = f

		stFeatureExtractionToFile(f, win, step, outPath)
	
		


		

		

	
