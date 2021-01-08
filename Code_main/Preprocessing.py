#!/usr/bin/env python3

"""
Preprossessing for count file
"""


__author__ = "Team B"
__status__ = "Working Module"
__version__ = "1.0"

import os
import sys
import glob
from parse_args import construct_parser


class Preprocessing:
    """
    Preporcessing steps before creating the count file
    """

    def __init__(self, data_dir, platform="illumina"):
        self.data_dir = data_dir
        self.platform = platform

    def getfile(self):
        """
        Get all sam files and precess them
        :return:
        """
        self.mak_dir()
        path = f"{self.data_dir}/output/sam_files/*.sam"
        for file in glob.glob(path):
            filename = file.split("/")[-1]
            filename = ".".join(filename.split(".")[:-1])
            self.process(filename, file)
        return 0

    def process(self, filename, filepath):
        """
        Preform nececerray processing
        :param filename:
        :param filepath:
        :return:
        """
        os.system(f"PicardCommandLine SortSam I={filepath} O={self.data_dir}/output/sortedBam/{filename}.sam SO=queryname")
        os.system(f"PicardCommandLine AddOrReplaceReadGroups INPUT={filepath} OUTPUT={self.data_dir}/output/addOrReplace/{filename}.sam LB={filename} PU={filename} SM={filename} PL={self.platform} CREATE_INDEX=TRUE")
        os.system(f"PicardCommandLine FixMateInformation INPUT={self.data_dir}/output/addOrReplace/{filename}.sam")
        os.system(f"PicardCommandLine MergeSamFiles INPUT={self.data_dir}/output/addOrReplace/{filename}.sam OUTPUT={self.data_dir}/output/mergeSam/{filename}.sam CREATE_INDEX=true USE_THREADING=true")
        os.system(f"PicardCommandLine MarkDuplicates INPUT={self.data_dir}/output/mergeSam/{filename}.sam OUTPUT={self.data_dir}/output/markDuplicates/{filename}.sam CREATE_INDEX=true METRICS_FILE={self.data_dir}/output/markDuplicates/{filename}.metrics.log")
        os.system(f"samtools sort -n {self.data_dir}/output/markDuplicates/{filename}.sam -o {self.data_dir}/output/Finalmark/{filename}.sam")

    def mak_dir(self):
        """
        Create directories
        :return:
        """
        dirs = ["sortedBam", "addOrReplace", "mergeSam", "markDuplicates", "Finalmark"]
        for dir in dirs:
            if not os.path.exists(f"{self.data_dir}/output/{dir}"):
                print(f"{self.data_dir}/output/{dir}")
                os.makedirs(f"{self.data_dir}/output/{dir}")
        return 0



def main():
    parser = construct_parser()
    args = parser.parse_args()
    yes = Preprocessing(f"{args.outputDir}")
    yes.getfile()
    return 0


if __name__ == "__main__":
    sys.exit(main())
