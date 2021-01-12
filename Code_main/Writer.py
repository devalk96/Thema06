#!usr/bin/env python3

"""
Script to write status
"""

import argparse
import sys
import os
from parse_args import construct_parser
import pandas as pd
#from fpdf import FPDF
from io import StringIO
from PIL import Image
import imghdr
from pylatex import Document, Section, Subsection, Tabular, Math, TikZ, Axis, \
    Plot, Figure, Matrix, Alignat

from zipfile import ZipFile


class Tables:
    def __init__(self, outputdir):
        self.table_general = pd.read_table(f"{outputdir}/MultiQC/multiqc_data/multiqc_general_stats.txt", "\t")


class File_status:
    def __init__(self, main_dir, filepath, corrupt, paired_status, colorspace, trimmer_error, paired, table_object):
        self.main_dir = main_dir
        self.filepath = filepath

        self.filename = os.path.basename(self.filepath)
        self.filebasename = ".".join(self.filename.split(".")[:-2])
        if "_" in self.filebasename:
            #self.identifier = "_".join(self.filebasename.split("_")[:-1])
            self.identifier = self.filebasename.split("_")[0]
        else:
            self.identifier = self.filebasename
        #self.is_paired = paired_status
       # self.low_quality = low_quality
        #self.mito = False
        self.is_paired = paired_status
        self.pre_row = None
        self.paired_row = None
        self.getrows(table_object)

        #trimming
        # self.colorspace = False
        # self.low_quality = low_quality


        self.short_read = False
        #self.duplicate = False
        #self.low_alignment = float(self.aligned_sorted_row["featureCounts_mqc-generalstats-featurecounts-percent_assigned"])
        #self.high_duplicate = False


        # Input
        self.high_duplicate = float(self.pre_row["FastQC_mqc-generalstats-fastqc-percent_duplicates"])
        self.short_read = float(self.pre_row["FastQC_mqc-generalstats-fastqc-avg_sequence_length"])

        # Trimming
        self.colorspace = colorspace
        self.trimmer_error = trimmer_error
        self.all_trimmed = float(self.pre_row["Cutadapt_mqc-generalstats-cutadapt-percent_trimmed"])
        self.corrupt = corrupt

        #alignment
        if self.paired_row is None:
            self.low_alignment = float(self.pre_row["featureCounts_mqc-generalstats-featurecounts-percent_assigned"])
        else:
            self.low_alignment = float(self.paired_row["featureCounts_mqc-generalstats-featurecounts-percent_assigned"])

    def write_status(self):

        if not os.path.exists(f"{self.main_dir}/Reports"):
            os.makedirs(f"{self.main_dir}/Reports")

        if not os.path.exists(f"{self.main_dir}/Reports/images"):
            os.makedirs(f"{self.main_dir}/Reports/images")

        doc = Document(f"{self.main_dir}/Reports/{self.filebasename}.pdf")

        with doc.create(Subsection("Input:")):
            if self.all_trimmed == 100:
                doc.append("It seems like there where no reads with a high enough quality to survive the trimming process.")
                with doc.create(Figure(position="h!")) as graph:
                    with ZipFile(f"{self.main_dir}/fastqc/reports/{self.filebasename}_fastqc.zip", "r") as zip:
                        with zip.open(f"{self.filebasename}_fastqc/Images/per_base_quality.png") as file:
                            image = Image.open(file)
                            print(image)
                            image.save(f"{self.main_dir}/Reports/images/{self.filebasename}.jpg", "JPEG")
                            graph.add_image(f"{self.main_dir}/Reports/images/{self.filebasename}.jpg")
                            graph.add_caption('This is the reads before trimming')
            if self.high_duplicate > 70:
                doc.append(f"\nThe precentage of duplicate reads in the input file is {self.high_duplicate}."
                           f" This could be considered high, which means that there is probably a low amount of input data.")

            doc.append(f"\nThe average sequence length is {self.short_read}")
            if self.high_duplicate < 70 and not self.all_trimmed == 100:
                doc.append(f"\nThere doesn't seem to be any problems with the input data.")

        with doc.create(Subsection("Trimmer:")):
            if self.colorspace is True:
                doc.append(f"File {self.filename} seems to be in SOLiD colorspace format which is currently not supported by this pipeline."
                           f" This means the file has not been trimmed and it was not processed")
            if self.trimmer_error is not None:
                doc.append("There seems to have been a problem while trimming this file."
                           " This means the file has not been trimmed and it was not processed")
                doc.append(f"{self.trimmer_error}")
            if self.corrupt:
                doc.append("This file is corrupt, this probably means all of the quality scores in the fasta files where the same.")
                with doc.create(Figure(position="h!")) as graph:
                    with ZipFile(f"{self.main_dir}/fastqc/reports/{self.filebasename}_fastqc.zip", "r") as zip:
                        with zip.open(f"{self.filebasename}_fastqc/Images/per_base_quality.png") as file:
                            image = Image.open(file)
                            print(image)
                            image.save(f"{self.main_dir}/Reports/images/{self.filebasename}.jpg", "JPEG")
                            graph.add_image(f"{self.main_dir}/Reports/images/{self.filebasename}.jpg")
                            graph.add_caption('This is the reads before trimming')
            if [self.colorspace, self.trimmer_error, self.corrupt] == [False, None, False]:
                doc.append("\nTrimmer ran without a problem")

        if self.low_alignment is not None:
            with doc.create(Subsection("Alignment:")):
                if self.low_alignment < 40:
                    doc.append("\nThe alignment seems to be verry low, this could mean a coupple of things. It could mean that you are aligning the reads to the wrong genome."
                               " If you alligned to the human genome this could also mean that there is a lot of mtDNA in your sequence, to check this you could take this file and allign it to"
                               " mitochondrial dna."
                               "\nAlso make sure you used the right gtf file for the genome.")
                    doc.append(f"\nAlignment percentage: {self.low_alignment}%.")

        doc.generate_pdf(filepath=f"{self.main_dir}/Reports/{self.filebasename}")



        # Messages
        "There seems to be a lot of Mitochondrial dna in the reads, this could mean that the sample was taken from a cel in apoptosis"
        "resultaten mito alignment? of bij lage ilignment met het reference genome"

        "A lot/long poly nucleotide repetition was found, this could mean that there is a primer in the sequence"
        "Fastqc ?"

        #"There seem to be a lot of duplications where found in the reads, this probably means that there is not enough input materia"
        #"Fastqc ? maybe featurecounts?"

        #"There wheren't many reads alligned to the chosen genome, this probably means that there weren't enough high quality reads in the input data"
        #"featurecounts thingy here"

        "All the reads seem to have been trimmed, this means that all the reads where of a to low quality"
        "fastqc image here"

        "The alignment seems to be verry low, this could mean a coupple of things. It could mean that you are aligning the reads to the wrong genome. " \
        "If you alligned to the human genome this could also mean that there is a lot of mtDNA in your sequence, to check this you could take this file and allign it to" \
        " mitochondrial dna"
        "Also make sure to use the right gtf file for the genome"

        return 0

    def getrows(self, count_table):
        self.pre_row = count_table.loc[count_table["Sample"] == f'{self.filebasename}']
        if self.pre_row.empty:
            self.pre_row = None

        if self.is_paired is not False:
            self.paired_row = count_table.loc[count_table["Sample"] == f'{self.identifier}']

        return 0

def get_status(count_table):
    pre_row = count_table.loc[count_table["Sample"] == 'SRR057599']
    aligned_row = count_table.loc[count_table["Sample"] == 'SRR057599_aligned']
    aligned_sorted_row = count_table.loc[count_table["Sample"] == 'SRR057599_aligned_sorted']
    if float(aligned_sorted_row["featureCounts_mqc-generalstats-featurecounts-percent_assigned"]) < 40:
        print("self.low_alignment = True")
    if float(pre_row["FastQC_mqc-generalstats-fastqc-percent_duplicates"]) > 70:
        print("self.high_duplciate = True")
        x = "There seems to be a lot of duplicate reads, this could mean that there isn't a lot of input material"
    #print(float(row["featureCounts_mqc-generalstats-featurecounts-percent_assigned"]))

    #Is row of column voor een sample?

    return 0


def main():
    #parser = construct_parser()
    #args = parser.parse_args()
    table = Tables("/data/storix2/student/2020-2021/Thema10/tmp/tools/data_output/Skippybal")
    #get_status(table.table_general)
    yes = File_status("/data/storix2/student/2020-2021/Thema10/tmp/tools/data_output/clean", "/data/storix2/student/2019-2020/Thema06/project-data/How_to_deal_with_difficult_data/Data/SRR057598.fastq.gz",
                      False, False, False, None, table.table_general)
    yes.write_status()
    return 0


if __name__ == '__main__':
    sys.exit(main())
