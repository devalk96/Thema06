#!/usr/bin/env python3

"""
Module to make count file
"""


__author__ = "Team B"
__status__ = "Working Module"
__version__ = "1.0"

import argparse
import os
import sys


class Featurecounts:
    def __init__(self, outputdir, gtf):
        self.outputdir = outputdir
        self.gtf = gtf

    def make_count(self):
        """
        create count matrix
        :return:
        """
        if not os.path.exists(f"{self.outputdir}/output/countfile"):
            os.makedirs(f"{self.outputdir}/output/countfile")
        #os.system(featureCounts + " -a " + gtfFile + " -o " + outputDir + "RawData/counts/geneCounts.txt " + outputDir + "Preprocessing/markDuplicates/*_sorted.bam")
        #f"{self.featurcounts} -a {self.gtf} -o {self.outputdir}/output/countfile/Count_matrix.txt  {self.outputdir}/output/markDuplicates/*_sorted.bam"
        os.system(f"featureCounts -a {self.gtf} -o {self.outputdir}/output/countfile/Count_matrix.txt  {self.outputdir}/output/markDuplicates/*_sorted.sam")
        return 0



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
    yes = Featurecounts("/data/storix2/student/2020-2021/Thema10/tmp/tools/data_output/Skippybal", "/data/storix2/student/2020-2021/Thema10/tmp/tools/test_data/reference/hg38.ensGene.gtf.gz")
    yes.make_count()
    return 0


if __name__ == "__main__":
    sys.exit(main())
