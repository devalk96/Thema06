"""
Main script.
"""

import sys
import argparse
import os
import Code_Sander.directory_manager as directorymanager
import Code_Sander.fastqc_manager as fastqc_manager
import glob

# Data can be found at: /data/storix2/student/2019-2020/Thema06/project-data/How_to_deal_with_difficult_data/Data"
# default_output = "/homes/sjbouwman/Thema06"
# example run parameters:   python3 --fastqDir /data/storix2/student/2019-2020/Thema06/project-data/How_to_deal_with_difficult_data/Data --out /homes/sjbouwman/Thema06 --threads 16





# Nested dictionaries for creating directories
SUBDIRS = {'fastqc': {'reports': None},
           'output': {'trimmed_data': None}}

# Tool location
TOOL_LOCATION = {"fastqc": "fastqc",
                 "ptrimmer": "/data/storix2/student/2020-2021/Thema10/tmp/tools/ptrimmer"}


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
    return parser


def validate_input(parser, args):
    """
    Checks if the received user input is valid.
    Currently only checks if the directory which contain the fastq files exists.
    """
    if not os.path.exists(args.fastqDir):
        parser.error(f"Path to {args} not found!")


class Qualitycheck():
    def __init__(self, input_path, output_path, threads=4, skip_existing=False):
        self.fastq_files = [f"{input_path}/{x}" for x in os.listdir(input_path)]
        self.output_path = directorymanager.create_dirs(file_root=output_path, subdirs=SUBDIRS)
        self.threads = threads
        self.skip_existing = skip_existing

        self.fastQC_manager = fastqc_manager.Fastqc_manager(fastq_folder=input_path,
                                                            output=f"{self.output_path}/fastqc/reports",
                                                            threads=self.threads,
                                                            skip=self.skip_existing,
                                                            tool_path=TOOL_LOCATION["fastqc"])
        self.file_list = self.fastQC_manager.files_list
        

    def generate_multiqc(self):
        pass




def main():
    parser = construct_parser()
    args = parser.parse_args()
    validate_input(parser, args)

    data = Qualitycheck(input_path=args.fastqDir,
                        output_path=args.outputDir,
                        threads=args.threads,
                        skip_existing=args.skip)

    print(data.fastQC_manager.settings())
    data.fastQC_manager.run_fastqc()

    return 0


if __name__ == '__main__':
    sys.exit(main())
