#!usr/bin/env python3

"""
Script to map the reads.
"""
import os
import glob
import sys
import argparse


class Alignment:
    """
    Align the reads to a reference genome
    """
    def __init__(self, directory, tool_path, refseq, output_path):
        self.directory = directory
        self.tool_path = tool_path
        self.refseq = refseq
        self.output_path = output_path

    def processing(self):
        """
        Map the files and save them as filename_aligned.sam
        """
        os.chdir(self.directory)
        for filename in os.listdir():
            for file2 in os.listdir(filename):
                if file2.endswith(".fq.gz") or file2.endswith(".fasta.gz"):
                    print(f"{self.tool_path} -a {self.refseq} {filename}/{file2} > {self.output_path}/{file2.split('.')[0]}_aligned.sam")
                    os.system(f"{self.tool_path} -a {self.refseq} {filename}/{file2} > {self.output_path}/{file2.split('.')[0]}_aligned.sam")

       # data = glob.glob("*.fa") + glob.glob("*.fasta")
        #data = ["fa", "fa"]
        #for file in data:
        #    print(f"{self.tool_path} -a {self.refseq} {file} > {self.output_path}/{file.split('.')[0]}_aligned.sam")
        #    # os.system(f"{self.tool_path} -a {self.refseq} {file} > {file.split('.')[-1]}_aligned.sam")


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
    yes = Alignment(f"{args.outputDir}/output/trimmed_data", "/data/storix2/student/2020-2021/Thema10/tmp/tools/pipeline_tools/minimap2", "", f"{args.outputDir}/output/sam_files")
    yes.processing()

    return 0


if __name__ == '__main__':
    sys.exit(main())
