#!/usr/bin/env python3

"""
Main script.
"""

import sys
from parse_args import construct_parser
import shutil
import os
import directory_manager as directorymanager
import fastqc_manager as fastqc_manager
import thrimmer_manager as thrimmer_manager
import alignment as alignment
import Preprocessing as preprocessing
import mulitqc as multiqc
import Countmatrix as feature
import Removedirs as remove
import glob

# Data can be found at: /data/storix2/student/2019-2020/Thema06/project-data/How_to_deal_with_difficult_data/Data"

# Nested dictionaries for creating directories
SUBDIRS = {'fastqc': {'reports': None},
           'output': {'trimmed_data': None,
                      'sam_files': None}}


def validate_input(parser, args, tool_location: dict):
    """
    Checks if the received user input is valid.
    Checks if the directory which contain the fastq files exists.
    Checks for existence of tool locations
    """
    if not (args.fastqDir or args.files):
        parser.error("--fastqDir OR --files are required")
    if args.fastqDir and args.files:
        parser.error("Please give one, --fastqDir or --files")

    if args.fastqDir is not None:
        if not os.path.exists(args.fastqDir):
            parser.error(f"Path to {args} not found!")

    for tool_name, tool_location in tool_location.items():
        tool_loc = shutil.which(tool_location)
        if not tool_loc:
            parser.error(f"{tool_name} at path \"{tool_location}\" not found!")
        else:
            print(F"Tool:\t{tool_name} found at\t{tool_loc}")


def main():
    parser = construct_parser()
    args = parser.parse_args()

    tool_location = {"fastqc": args.fastqc,
                     "trimgalore": args.trimgalore,
                     "minimap2": args.minimap2,
                     "cutadapt": args.cutadapt,
                     "featureCounts": args.featurecounts}

    validate_input(parser, args, tool_location)
    directorymanager.create_dirs(file_root=args.outputDir, subdirs=SUBDIRS)

    manager = fastqc_manager.Fastqc_manager(fastq_folder=args.fastqDir,
                                            qclist=args.files,
                                            output=f"{args.outputDir}/fastqc/reports",
                                            tool_path=tool_location["fastqc"],
                                            skip=args.skip,
                                            threads=args.threads)
    # print(manager.settings())
    manager.run_fastqc()
    trimmer = thrimmer_manager.Trimmer_manager(output=f"{args.outputDir}/output/trimmed_data",
                                               tool_path=tool_location["trimgalore"],
                                               file_list=manager.files_list,
                                               threads=args.threads,
                                               skip=args.skip,
                                               quality=args.quality,
                                               cutadapt_path=tool_location["cutadapt"])
    # print(trimmer.settings())
    trimmer.run_trimmer()

    aligner = alignment.Alignment(directory=f"{args.outputDir}/output/trimmed_data",
                                  tool_path=tool_location["minimap2"],
                                  refseq=args.refseq,
                                  output_path=f"{args.outputDir}/output/sam_files")
    aligner.processing()

    preprocessor = preprocessing.Preprocessing(args.outputDir)
    preprocessor.getfile()

    featurecounts = feature.Featurecounts(outputdir=args.outputDir,
                                          gtf=args.gtf,
                                          toolpath=tool_location["featureCounts"])
    featurecounts.make_count()

    multiqc_manager = multiqc.Multiqc(files=args.outputDir)
    multiqc_manager.run_qc()

    remover = remove.Remover(path=args.outputDir)
    remover.removedirs()

    print("\n\nEverything is Done!")
    return 0


if __name__ == '__main__':
    sys.exit(main())
