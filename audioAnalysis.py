#!/usr/bin/env python 2.7

import argparse

import os

import audioFeatureExtraction as aF



def parse_Arguments():

	parser = argparse.ArgumentParser(description = " script for feature extraction")

	tasks = parser.add_subparsers(
       	title="subcommands", description="available tasks", dest="task",metavar="")

	featExtDir = tasks.add_parser("featureExtractionDir", help="Extract audio features from files in a folder")

	featExtDir.add_argument("-i", "--input", required=True, help="Input directory")

	featExtDir.add_argument("-w", "--win", type=float, default=0.050, help="window size")

	featExtDir.add_argument("-s", "--step", type=float, default=0.025, help="step size")

	return parser.parse_args()

def featureExtractionDirWrapper(directory, win, step):
	
	if not os.path.isdir(directory):

		raise Exception("Input path not found")

	aF.stFeatureExtractionToFileDir(directory, win, step)


	
if __name__ == "__main__":

	args = parse_Arguments()

	if args.task == "featureExtractionDir":

		featureExtractionDirWrapper(args.input, args.win, args.step)




