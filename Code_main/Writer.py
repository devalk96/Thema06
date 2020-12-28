#!usr/bin/env python3

"""
Script to write status
"""

import argparse
import sys
import os
#from fpdf import FPDF
from pylatex import Document, Section, Subsection, Tabular, Math, TikZ, Axis, \
    Plot, Figure, Matrix, Alignat

from zipfile import ZipFile


class File_status:
    def __init__(self, main_dir, filepath, corrupt, paired_status, colorspace, trimmer_error, low_quality):
        self.main_dir = main_dir
        self.filepath = filepath
        self.corrupt = corrupt
        self.filename = os.path.basename(self.filepath).split(".")[0]
        self.is_paired = paired_status
        self.low_quality = low_quality

        self.colorspace = colorspace
        self.trimmer_error = trimmer_error

        status = self.get_status()
        self.mito = status[0]
        self.colorspace = status[1]
        self.short_read = status[2]
        self.duplicate = status[3]
        self.low_alignment = status[4]

    def write_status(self):
        # pdf = FPDF()
        # pdf.addpage()
        # pdf.set_font("DejaVu", "B", "15")

        if not os.path.exists(f"./Reports"):
            os.makedirs("./Reports")

        doc = Document(f"./Reports/{self.filename}")

        with doc.create(Subsection("Trimming:")):
            if self.colorspace is True:
                doc.append(f"File {self.filename} seems to be in SOLiD colorspace format which is currently not supported by this pipeline."
                           f"This means the file has not been trimmed and it was not processed")
            if self.trimmer_error is not None:
                doc.append("There seems to have been a problem while trimming this file."
                           "This means the file has not been trimmed and it was not processed")
                doc.append(f"{self.trimmer_error}")
            if self.corrupt:
                doc.append("This file is corrupt, this probably means all of the quality scores in the fasta files where the same.")
                with ZipFile(f"{self.main_dir}/fastqc/reports/{self.filename}_fastqc.zip", "r") as zip:
                    image = zip.read("{self.filename}_fastqc/Images/per_base_quality.png")
                with doc.create(Figure(position="h!")) as graph:
                    #graph.add_image(f"{self.main_dir}/fastqc/reports/{self.filename}_fastqc.zip/{self.filename}_fastqc/Images/per_base_quality.png")
                    graph.add_image(image)
            if self.low_quality:
                doc.append("It seems like there where no reads with a high enough quality to survive the trimming process.")
            if [self.colorspace, self.trimmer_error, self.corrupt] == [False, None, False, False]:
                doc.append("No problems encountered while trimming")



        # Messages
        "There seems to be a lot of Mitochondrial dna in the reads, this could mean that the sample was taken from a cel in apoptosis"
        "resultaten mito alignment? of bij lage ilignment met het reference genome"

        "A lot/long poly nucleotide repetition was found, this could mean that there is a primer in the sequence"
        "Fastqc ?"

        "There seem to be a lot of duplications where found in the reads, this probably means that there is not enough input materia"
        "Fastqc ? maybe featurecounts?"

        "There wheren't many reads alligned to the chosen genome, this probably means that there weren't enough high quality reads in the input data"
        "featurecounts thingy here"

        "All the reads seem to have been trimmed, this means that all the reads where of a to low quality"
        "fastqc image here"

        return 0

    def get_status(self):

        return []



def construct_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--fastqDir', help='Directory to the fq.gz/fastq.gz files')
    parser.add_argument('-o', '--organism',
                        help='Define the two letter id for the organism for the '
                             'alignment:\nHuman=hs\nMouse=mm\nMacaque=mmu\nRat=rn')
    parser.add_argument('-out', '--outputDir', help='Pathways to output directory')
    parser.add_argument('-s', '--seqType',
                        help='Define SE for single end sequencing or PE for paired end sequencing')
    parser.add_argument('-p', '--threads', help='Define number of threads to use', default=4, type=int)
    parser.add_argument('-t', '--trim', help='Define the last bp to keep for trimming')
    parser.add_argument('-S', '--skip', help='Skip already processed files', action="store_true", default=False)
    parser.add_argument('-q', '--quality', help='Define cut-off value for trimming', type=int, default=20)
    return parser


def main():
    parser = construct_parser()
    args = parser.parse_args()
    return 0


if __name__ == '__main__':
    sys.exit(main())
