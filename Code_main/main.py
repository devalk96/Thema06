"""
Main script.
"""

import sys
import argparse
import os
import Code_main.directory_manager as directorymanager
import Code_main.fastqc_manager as fastqc_manager
import Code_main.thrimmer_manager as thrimmer_manager
import Code_main.alignment as alignment
import Code_main.Preprocessing as preprocessing
import Code_main.mulitqc as multiqc
import Code_main.Countmatrix as feature
import glob

# Data can be found at: /data/storix2/student/2019-2020/Thema06/project-data/How_to_deal_with_difficult_data/Data"
# default_output = "/homes/sjbouwman/Thema06"
# example run parameters:   python3 --fastqDir /data/storix2/student/2019-2020/Thema06/project-data/How_to_deal_with_difficult_data/Data --out /homes/sjbouwman/Thema06 --threads 16

# Make sure cutadapt is install --> pip3 install cutadapt --user

# Nested dictionaries for creating directories
SUBDIRS = {'fastqc': {'reports': None},
           'output': {'trimmed_data': None,
                      'sam_files': None}}

# Tool location
TOOL_LOCATION = {"fastqc": "fastqc",
                 "trimgalore": "/data/storix2/student/2020-2021/Thema10/tmp/tools/pipeline_tools/TrimGalore/trim_galore",
                 "minimap2": "",
                 "cutadapt": "/homes/kanotebomer/.local/bin/cutadapt"}


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
    parser.add_argument('-r', '--refseq', help='Reference genome to align to', type=str, required=True)
    parser.add_argument('-g', '--gtf', help='Gtf file', type=str, required=True)
    return parser


def validate_input(parser, args):
    """
    Checks if the received user input is valid.
    Currently only checks if the directory which contain the fastq files exists.
    """
    if not os.path.exists(args.fastqDir):
        parser.error(f"Path to {args} not found!")


def main():
    parser = construct_parser()
    args = parser.parse_args()
    validate_input(parser, args)
    directorymanager.create_dirs(file_root=args.outputDir, subdirs=SUBDIRS)
    manager = fastqc_manager.Fastqc_manager(fastq_folder=args.fastqDir,
                                            output=f"{args.outputDir}/fastqc/reports",
                                            tool_path=TOOL_LOCATION["fastqc"],
                                            skip=args.skip,
                                            threads=args.threads)
    # print(manager.settings())
    manager.run_fastqc()
    trimmer = thrimmer_manager.Trimmer_manager(output=f"{args.outputDir}/output/trimmed_data",
                                               tool_path=TOOL_LOCATION["trimgalore"],
                                               file_list=manager.files_list,
                                               threads=args.threads,
                                               skip=args.skip,
                                               quality=args.quality,
                                               cutadapt_path=TOOL_LOCATION["cutadapt"])
    # print(trimmer.settings())
    trimmer.run_trimmer()

    # aligner = alignment.Alignment(directory=f"{args.outputDir}/output/trimmed_data",
    #                               tool_path=TOOL_LOCATION["minimap2"],
    #                               refseq="",
    #                               output_path=f"{args.outputDir}/output/sam_files")
    # aligner.processing()

    aligner = alignment.Alignment(directory=f"{args.outputDir}/output/trimmed_data",
                                  tool_path=TOOL_LOCATION["minimap2"],
                                  refseq=args.refseq,
                                  output_path=f"{args.outputDir}/output/sam_files")
    aligner.processing()

    preprocessor = preprocessing.Preprocessing(args.outputDir)
    preprocessor.getfile()

    featurecounts = feature.Featurecounts(args.outputDir, args.gtf)
    featurecounts.make_count()

    multiqc_manager = multiqc.Multiqc(args.outputDir)
    multiqc_manager.run_qc()

    return 0


if __name__ == '__main__':
    sys.exit(main())
