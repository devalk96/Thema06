#!usr/bin/env python3

"""
Script to map the reads.
"""
import os
import glob
import sys
from parse_args import construct_parser
import tarfile


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
                os.system(f"{self.tool_path} -ax sr {self.refseq} {files[0]} {files[1]} > {self.output_path}/{filename}_aligned.sam")

            elif len(files) == 0:
                print(f"No trimmed data to allign for {filename}")
            else:
                os.system(f"{self.tool_path} -a {self.refseq} {files[0]} > {self.output_path}/{filename}_aligned.sam")


            # for file2 in os.listdir(filename):
            #     if file2.endswith(".fq.gz") or file2.endswith(".fasta.gz"):
            #         print(f"{self.tool_path} -a {self.refseq} {filename}/{file2} > {self.output_path}/{file2.split('.')[0]}_aligned.sam")
            #         # cwd = os.getcwd()
            #         # print(cwd)
            #         # print(file2)
            #         # print(f"./{filename}/{file2}")
            #         #os.system(f"gunzip {filename}/{file2}")
            #         os.system(f"{self.tool_path} -a {self.refseq} {filename}/{file2} > {self.output_path}/{file2.split('.')[0]}_aligned.sam")

       # data = glob.glob("*.fa") + glob.glob("*.fasta")
        #data = ["fa", "fa"]
        #for file in data:
        #    print(f"{self.tool_path} -a {self.refseq} {file} > {self.output_path}/{file.split('.')[0]}_aligned.sam")
        #    # os.system(f"{self.tool_path} -a {self.refseq} {file} > {file.split('.')[-1]}_aligned.sam")


def main():
    parser = construct_parser()
    args = parser.parse_args()
    yes = Alignment(f"{args.outputDir}/output/trimmed_data", "/data/storix2/student/2020-2021/Thema10/tmp/tools/pipeline_tools/minimap2", "/data/storix2/student/2020-2021/Thema10/tmp/tools/test_data/reference/hg38_UCSC.fa.gz", f"{args.outputDir}/output/sam_files")
    yes.processing()

    return 0


if __name__ == '__main__':
    sys.exit(main())
