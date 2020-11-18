########################################################################
# Author    : M. Dubbelaar
# Date      : 11-sept-2018
# Purpose   : Act as a main for the alignment procedure.
########################################################################
#								Imports								   #
########################################################################
import os
import re
import sys
import glob
import shutil
import commands
import argparse

# Import the self-made files
import createDirs
import determineGenomeInfo
########################################################################
# 							Used directories				 		   #
########################################################################
## TODO: Download the following 4 tools and define the pathway to these functions
picard = ""
hisat = ""
featureCounts = ""
trimGalore = ""
########################################################################
# 						  Predefined variables						   #
########################################################################
fastqDir = ""
outputDir = ""
organism = ""
seqType = ""
threads = ""
trim = ""

uniqueFileNames = []
uniqueSamples = []

genomeHiSat2 = ""
gtfFile = ""
genomeFasta = ""
########################################################################
#							Annotated functions						   #
########################################################################
def arguments ():
	'''
		This functions defines the different parameters used for this function and gives a help output if the parameters are not given.
	'''
	parser = argparse.ArgumentParser()
	parser.add_argument('-d', '--fastqDir', help='Directory to the fq.gz/fastq.gz files')
	parser.add_argument('-o','--organism', help='Define the two letter id for the organism for the alignment:\nHuman=hs\nMouse=mm\nMacaque=mmu\nRat=rn')
	parser.add_argument('-out', '--outputDir', help='Pathways to output directory')
	parser.add_argument('-s', '--seqType', help='Define SE for single end sequencing or PE for paired end sequencing')	
	parser.add_argument('-p', '--threads', help='Define number of threads to use')	
	parser.add_argument('-t', '--trim', help='Define the last bp to keep for trimming')	
	# Save all of the defined parameters in the variable args.
	args = parser.parse_args()

	# define the global variables, enabling local changes. 
	global fastqDir
	global outputDir
	global organism
	global seqType
	global threads
	global trim
	
	# When the user does not specify one of the three required parameters, the help will be displayed
	if (not args.fastqDir or not args.outputDir or not args.organism): # Maybe add a -h statement
		print('''		Usage: python AligningPipeline.py -d [fastq directory] -o [hg|mm|rn|mmu] -out [out directory] -s [SE|PE] -p [number of threads] -t [last bp | first and last bp]
		-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
			-d/--fastqDir 					|		[Required] Directory to the fq.gz/fastq.gz files
			-o/--organism					|		[Required] Define the two letter id for the organism for the alignment:
									|			Homo sapiens = hs
									|			Mus musculus = mm
									|			Macaca mulatta = mmu
									|			Rattus norvegicus = rn
			-out/--outputDir 				|		[Required] Pathways to output directory
			-s/--seqType 					|		[Optional] Define SE for single end sequencing or PE for paired end sequencing
			-p/--threads 					|		[Optional] Define number of threads to use
			-t/--trim 					|		[Optional] Define the last bp that needs to be kept for trimming or the first and the last bp (seperated by -)
		-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------''')
		# The program will exit after showing the help message
		sys.exit()
	else:
		# Define the global variables with the use of the parameters stored in args
		fastqDir = args.fastqDir
		outputDir = args.outputDir
		organism = args.organism
		seqType = args.seqType
		if args.threads == None:
			# The half of the number of threads in the PC is used when the number of threads is not defined
			threads = int(commands.getoutput("grep -c processor /proc/cpuinfo"))/2
		else:
			threads = args.threads
		trim = args.trim
########################################################################

def fastaProcessing(genomeFasta):
	'''
		The first step is to determine if the additional dict and index file of the organism fasta are created.
	'''
	
	print('''########################################################################
Checking and creating the necessary additional files of the genome fasta
########################################################################''')
	# It is determined if the fasta.dict has been created already
	if not os.path.isfile(genomeFasta.replace("fa", "dict")):
		# If this is not the case, the file will be created
		os.system("java -jar " + picard + " CreateSequenceDictionary R=" + genomeFasta + " O=" + genomeFasta.replace("fa", "dict"))
	# It is determined if the fasta.fa.fai has been created already
	if not os.path.isfile(genomeFasta + "fai"):
		# If this is not the case, the file will be created
		os.system("samtools faidx " + genomeFasta)
		
def qualityCheck():
	'''
		The function qualityCheck performs the fastQC check and writes the output to the Results/fastQC/ folder.
	'''
	print('''########################################################################
			Perform the quality check
########################################################################''')
	os.system("fastqc " + fastqDir + "*.gz -o " + outputDir + "/Results/fastQC/ -t " + str(threads))

def trimFiles():
	'''
		The files are trimmed based on trim_galore if no parameter is given or by fastx_trimmer.
		trim_galore determined the cut off based on the quality of the reads and removes the adapters if necessary.
		fastx_trimmer requires an end bp or a beginning and an end bp for the trimming.
	'''
	
	# The executable is saved for further notice (fq/fastq), since this can differ
	ext = ""
	# All of the files in the fastqDir are obtained
	for files in glob.glob(fastqDir + "*.gz"):
		# The filename, extention and the 'gz' are obtained
		filesNameComp = files.split("/")[-1]
		filesName, ext, gz = filesNameComp.split(".")
		# Copy-paste the gzipped file to the RawData dir
		if not os.path.exists(outputDir + "/RawData/fastqFiles/" + filesNameComp):
			os.system("cp " + files + " " + outputDir + "/RawData/fastqFiles/" + filesNameComp)   
		# The files are unzipped for the trimming, only when this is not done yet
		if not os.path.exists(fastqDir + "/" + filesName + "." + ext):
			os.system('gunzip -k ' + files)
		# If there is no trimming parameter given, the tool trim_galore is initiated
		if trim == None:
			print(''' ########################################################################
			Perform the trimming with the use of trim_galore
########################################################################''')
			os.system(trimGalore + " --path_to_cutadapt ~/.local/bin/cutadapt " + files.replace("."+ ext+".gz","."+ext) + " -o " + outputDir + "/Preprocessing/trimmed/")
		else:
			print('''########################################################################
			Perform the trimming with the use of fastx_trimmer
########################################################################''')
			# The number of trimming parameters is determined
			sepTrim = trim.split("-")
			# If there is only 1 parameter, fastx_trimmer is initiated with only the -l option
			if len(sepTrim) == 1:
				os.system("fastx_trimmer -l " + trim + " -i " + files.replace("."+ ext+".gz","."+ext) + " -o " + outputDir + "/Preprocessing/trimmed/"  + filesName + "_trimmed." + ext )
			# If there are 2 parameters, fastx_trimmer is initiated with both the -f and -l option
			else:
				os.system("fastx_trimmer -f " + sepTrim[0] + " -l " + sepTrim[1] + " -i " + files.replace("."+ ext+".gz","."+ext) + " -o " + outputDir + "/Preprocessing/trimmed/" + filesName + "_trimmed." + ext )
	# The ext is passed through for the rest of the analysis
	return(ext)

def alignment(ext, genomeHiSat2):
	'''
		The actual alignment is performed in this function.
		The trimmed reads are obtained from the trimmed folder and are used of the alignment.
		The log file of the alignment is written to the Results/alignment folder and the .bam file is created.
	'''
	
	print('''########################################################################
			Perform the alignment
########################################################################''')
	for files in glob.glob(outputDir+"/Preprocessing/trimmed/*." + ext):
		if files not in uniqueFileNames:
			uniqueFileNames.append(files)
			name = files.split("/")
			fastqName, ext = name[-1].split(".")
			#---------------------------------------------------------------------------------------------------
			# TODO: Include the component for paired end data here
			#---------------------------------------------------------------------------------------------------
			os.system(hisat + " -x ./" + genomeHiSat2 + " -U " + files + " -p " + str(threads) + " 2>> " + outputDir + "/Results/alignment/" + fastqName.replace("_trimmed", "") + ".log | samtools view -Sbo " + outputDir + "/Preprocessing/aligned/" + fastqName.replace("_trimmed", "") + ".bam -")

def preprocessing():
	'''
		The step between the alignment and the creation of the count file is done in this function.
		These steps consists of the sorting, add or replace groups, fix mate information, merging, marking of duplicated and a sorting for the creation of the count files.
	'''
	
	print('''########################################################################
			Perform the processing steps necessary to create the count file
########################################################################''')
	for alignedFiles in glob.glob(outputDir + '/Preprocessing/aligned/*.bam'):
		alignedFilesSep = alignedFiles.split("/")
		currentFile = alignedFilesSep[-1].replace(".bam", "")
		os.system("java -jar " + picard + " SortSam I=" + outputDir + "/Preprocessing/aligned/" + currentFile +  ".bam O=" + outputDir + "/Preprocessing/sortedBam/" + currentFile + ".bam SO=queryname")
		os.system("java -jar " + picard + " AddOrReplaceReadGroups INPUT=" + outputDir + "/Preprocessing/sortedBam/" + currentFile + ".bam OUTPUT=" + outputDir + "/Preprocessing/addOrReplace/" + currentFile + ".bam " + " LB=" + currentFile + " PU=" + currentFile + " SM=" + currentFile + " PL=illumina CREATE_INDEX=true")
		os.system("java -jar " + picard + " FixMateInformation INPUT=" + outputDir + "/Preprocessing/addOrReplace/" + currentFile + ".bam")
		os.system("java -jar " + picard + " MergeSamFiles INPUT=" + outputDir + "/Preprocessing/addOrReplace/" + currentFile + ".bam OUTPUT=" + outputDir + "/Preprocessing/mergeSam/" + currentFile + ".bam " + " CREATE_INDEX=true USE_THREADING=true")
		os.system("java -jar " + picard + " MarkDuplicates INPUT=" + outputDir + "/Preprocessing/mergeSam/" + currentFile + ".bam OUTPUT=" + outputDir + "/Preprocessing/markDuplicates/" + currentFile + ".bam " + " CREATE_INDEX=true METRICS_FILE=" + outputDir + "/Preprocessing/markDuplicates/" + currentFile + ".metrics.log")
		os.system("samtools sort -n " + outputDir + "/Preprocessing/markDuplicates/" + currentFile + ".bam -o " + outputDir + "/Preprocessing/markDuplicates/" + currentFile + "_sorted.bam")

def createCountMat(gtfFile):
	'''
		The last step is the creation of the count matrix file.
		This is done with the tool feature counts.
	'''
	os.system(featureCounts + " -a " + gtfFile +  " -o " + outputDir + "RawData/counts/geneCounts.txt " + outputDir + "Preprocessing/markDuplicates/*_sorted.bam")

def performMultiQC():
	print('''########################################################################
			Perform the multiqc step
########################################################################''')
	os.system("multiqc " + outputDir + " -o " + outputDir + "/Results/multiQC/")

def copyPasteAligningCode():
	print('''########################################################################
			Transfer first code files
########################################################################''')
	# Determine which files in the current working directory end with '.py' 
	for files in glob.glob(os.getcwd() + "/*.py"):
		# Obtain the name of the files
		pythonFile = files.split("/")[-1]
		# Copy - paste the files to the Code/aligningPipeline directory
		os.system("cp " + files + " " + outputDir + "/Code/aligningPipeline/" + pythonFile)   

def removeFolders():
	if os.path.exists(outputDir + "/Preprocessing/"):
		shutil.rmtree(outputDir + "/Preprocessing/")
		
def main():
	'''
	This def acts as a main for the whole aligning process.
	The different functions are called here. '''
	# Obtain all of the arguments when calling this script
	arguments()
	# Create the necessary directories for the study
	createDirs.createAllDirs(outputDir)
	# The fastQC files are created
	qualityCheck()
	# The files are trimmed based on the input of the user
	ext = trimFiles()
	# Determine right genome annotation
	genomeHiSat2, gtfFile, genomeFasta = determineGenomeInfo.determineRightGenome(organism)
	# Make sure that the fasta file of the right organism is chosen
	fastaProcessing(genomeFasta)
	# Perform the alignment, given the ext and the HiSat2 genome
	alignment(ext, genomeHiSat2)
	# The prepocessing steps, the steps after the alignment and before the generation of the count files
	preprocessing()
	# Generation of the count matrix
	createCountMat(gtfFile)
	performMultiQC()
	copyPasteAligningCode()
	removeFolders()
	
	print('''
########################################################################
			 Alignment Finished
########################################################################
If you used the pipeline properly, the files should be generated by now.
In the Result directory you can find files that depect the quality of
the samples in different timepoints (fastQC, alignment, etc.).

This pipeline was created by Marissa L. Dubbelaar 
	e-mail: (marissa.dubbelaar@hotmail.com)
	''')

if __name__ == "__main__":
	main()
