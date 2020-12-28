#!usr/bin/env python3

"""
Script to run multiqc.
"""

#import multiqc
import argparse
import sys
import os


class Multiqc:
    def __init__(self, files):
        self.files = files

    def run_qc(self):
        #multiqc.run(self.files)
        if not os.path.exists(f"{self.files}/MultiQC"):
            os.makedirs(f"{self.files}/MultiQC")
        os.system(f"python3 -m multiqc -f -o {self.files}/MultiQC {self.files}")


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
    yes = Multiqc(f"{args.outputDir}")
    yes.run_qc()

    return 0


if __name__ == '__main__':
    sys.exit(main())