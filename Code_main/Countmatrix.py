#!/usr/bin/env python3

"""
Module to make count file
"""


__author__ = "Team B"
__status__ = "Working Module"
__version__ = "1.0"

from parse_args import construct_parser
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
        os.system(f"featureCounts -a {self.gtf} -o {self.outputdir}/output/countfile/Count_matrix.txt  {self.outputdir}/output/Finalmark/*_sorted.sam")
        return 0




def main():
    parser = construct_parser()
    args = parser.parse_args()
    yes = Featurecounts("/data/storix2/student/2020-2021/Thema10/tmp/tools/data_output/Skippybal", "/data/storix2/student/2020-2021/Thema10/tmp/tools/test_data/reference/hg38.ensGene.gtf.gz")
    yes.make_count()
    return 0


if __name__ == "__main__":
    sys.exit(main())
