########################################################################
# Author    : M. Dubbelaar
# Date      : 11-sept-2018
# Purpose   : Create the necessary directories that need to be created.
########################################################################
#								Imports								   #
########################################################################
import os
import subprocess
########################################################################
def buildOutputDir(outputDir):
	'''
	Check if the output directory already exists, otherwise create it.
	'''
	if not os.path.exists(outputDir):
		os.makedirs(outputDir)
########################################################################
def extendOutputDir(outputDir):
	'''
	Check if the preprocessing folder already exists, if this is not the
	case. Create this directory with the other folders.
	'''
	if not os.path.exists(outputDir + "/Preprocessing/"):
		os.makedirs(outputDir + "/Preprocessing/")
		os.makedirs(outputDir + "/Preprocessing/trimmed")
		os.makedirs(outputDir + "/Preprocessing/aligned")
		os.makedirs(outputDir + "/Preprocessing/sortedBam")
		os.makedirs(outputDir + "/Preprocessing/addOrReplace")
		os.makedirs(outputDir + "/Preprocessing/mergeSam")
		os.makedirs(outputDir + "/Preprocessing/markDuplicates")
########################################################################
def createResultDir(outputDir):
	'''
	Check if the results directory exists, otherwise create it.
	'''
	if not os.path.exists(outputDir + "/Results/"):
		os.makedirs(outputDir + "/Results/")
		os.makedirs(outputDir + "/Results/alignment")
		os.makedirs(outputDir + "/Results/fastQC")
		os.makedirs(outputDir + "/Results/multiQC")
########################################################################
def createCodeDir(outputDir):
	'''
	Check if the code directory exists, otherwise create it.
	'''
	if not os.path.exists(outputDir + "/Code/"):
		os.makedirs(outputDir + "/Code/")
		os.makedirs(outputDir + "/Code/aligningPipeline")
		os.makedirs(outputDir + "/Code/analysis")
		
def createRawDataDir(outputDir):
	'''
	Check if the code directory exists, otherwise create it.
	'''
	if not os.path.exists(outputDir + "/RawData/"):
		os.makedirs(outputDir + "/RawData/")
		os.makedirs(outputDir + "/RawData/fastqFiles")
		os.makedirs(outputDir + "/RawData/counts")

def createAllDirs(outputDir):		
	buildOutputDir(outputDir)
	extendOutputDir(outputDir)
	createResultDir(outputDir)
	createCodeDir(outputDir)
	createRawDataDir(outputDir)
	
########################################################################
if __name__ == "__main__":
	directory = "/home/mldubbelaar/Desktop/testDir/"
	createAllDirs(directory)
	
