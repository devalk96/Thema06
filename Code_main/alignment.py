#!usr/bin/env python3

"""
Script to map the reads.
"""
import os
import glob
import sys
from parse_args import construct_parser


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
            ext = ("*.fq.gz", "*.fastq.gz")
            files = []
            for extention in ext:
                files.extend(glob.glob(f"{filename}/{extention}"))

            if len(files) == 2:
                os.system(f"{self.tool_path} -ax sr {self.refseq} {files[0]} {files[1]} > {self.output_path}/{filename}.sam")

            elif len(files) == 0:
                print(f"No trimmed data to allign for {filename}")

            else:
                os.system(f"{self.tool_path} -ax sr {self.refseq} {files[0]} > {self.output_path}/{filename}.sam")


def main():
    parser = construct_parser()
    args = parser.parse_args()
    yes = Alignment(f"{args.outputDir}/output/trimmed_data", "/data/storix2/student/2020-2021/Thema10/tmp/tools/pipeline_tools/minimap2", "/data/storix2/student/2020-2021/Thema10/tmp/tools/test_data/reference/mouse/GCA_000001635.9_GRCm39_genomic.fna.gz", f"{args.outputDir}/output/sam_files")
    yes.processing()

    return 0


if __name__ == '__main__':
    sys.exit(main())
