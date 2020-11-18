########################################################################
# Author    : M. Dubbelaar
# Date      : 11-sept-2018
# Purpose   : Determine the right genome for the analysis.
########################################################################
#								Imports								   #
########################################################################
import os
import subprocess

def determineRightGenome(organismIdentifier):
	'''
	Determine the right function based on the given organismIdentifier.
	If another organism can be used for the alignment, then add the 
	following lines:
	
	elif organismIdentifier.lower() == [organism identifier]:
		result = getInfo[organism]()
		
	and create a new def (getInfo[organism]) that contains the directory
	to the fasta file, gtf file and the HiSat2 directory.
	'''
	
	
	
	# If the lowercase name of organismIdentifier == "hs"
	if organismIdentifier.lower() == "hs":
		# Call the belonging function and save the directories
		result = getInfoHuman()
	elif organismIdentifier.lower() == "mmu":
		result = getInfoMacaque()
	elif organismIdentifier.lower() == "mm":
		result = getInfoMouse()
	elif organismIdentifier.lower() == "rn":
		result = getInfoRat()
	elif organismIdentifier.lower() == "dr":
		result = getInfoZebrafish()
	# return the directories for further use
	return result
########################################################################
def getInfoHuman():
	'''
	This fundtion and the other getInfo functions contain 3 different 
	directories:
	
	- genomeHisat2, that contains the directory in this tool to the 
	indexes of HiSat2 of the beloning genome.
	- gtfFile, that contains the directory in this tool. This file consists
	of the genome annotation.
	- genomeFast, that contains the directory in this tool. This file 
	is the fasta file that is used to build the genomeHisat2 index in 
	HiSat2.
	'''
	genomeHiSat2 = "Genome/HiSat2/Homo_sapiens/GRCh38.92"
	gtfFile = "Genome/Homo_sapiens.GRCh38.92.gtf"
	genomeFasta = "Genome/Homo_sapiens.GRCh38.dna_sm.primary_assembly.fa"
	# Return the three variables in a list for further use.
	return [genomeHiSat2, gtfFile, genomeFasta]
########################################################################	
def getInfoMacaque():
	genomeHiSat2 = "Genome/HiSat2/Macaca_mulatta/genome"
	gtfFile = "Genome/Macaca_mulatta.Mmul_8.0.1.92.gtf"
	genomeFasta = "Macaca_mulatta.Mmul_8.0.1.dna.toplevel.fa"
	return [genomeHiSat2, gtfFile, genomeFasta]
########################################################################		
def getInfoMouse():
	genomeHiSat2 = "Genome/HiSat2/Mus_musculus/GRCm38"
	gtfFile = "Genome/Mus_musculus.GRCm38.92.gtf"
	genomeFasta = "Genome/Mus_musculus.GRCm38.dna_sm.primary_assembly.fa"
	return [genomeHiSat2, gtfFile, genomeFasta]
########################################################################	
def getInfoRat():
	genomeHiSat2 = "Genome/HiSat2/Rattus_norvegicus/Rnor6.0"
	gtfFile = "Genome/Rattus_norvegicus.Rnor_6.0.93.gtf"
	genomeFasta = "Genome/Rattus_norvegicus.Rnor_6.0.dna_sm.toplevel.fa"
	return [genomeHiSat2, gtfFile, genomeFasta]
	
def getInfoZebrafish():
	genomeHiSat2 = "Genome/HiSat2/Danio_rerio/GRCz11.93"
	gtfFile = "Genome/Danio_rerio.GRCz11.93.gtf"
	genomeFasta = "Genome/Danio_rerio.GRCz11.93.dna_sm.primary_assembly.fa"
	return [genomeHiSat2, gtfFile, genomeFasta]
	
########################################################################	
if __name__ == "__main__":
	information = determineRightGenome("hs")
	print(information)
	
