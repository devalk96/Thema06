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


class Preprocessing:
    """
    Preporcessing steps before creating the count file
    """

    def __init__(self, output_dir, picard, platform="illumina"):
        self.output_dir = output_dir
        self.picard = picard
        self.platform = platform

    def getfile(self):
        path = f"{self.output_dir}/Ijsbrandsmapje/*.bam"
        for file in glob.glob(path):
            filename = file.split("/")[-1]
            filename = ".".join(filename.split(".")[:-1])
            process(filename, file)
        return 0

    def process(self, filename, filepath):
        os.system(f"java -jar {self.picard} SortSam I={filepath} O={self.output_dir}/output/sortedBam/{filename}.bam SO=queryname")
        os.system(f"java -jar {self.picard} AddOrReplaceReadGroups INPUT={filepath} OUTPUT={self.output_dir}/output/addOrReplace/{filename}.bam LB={filename} PU={filename} SM={filename} PL={self.platform} CREATE_INDEX=TRUE")
        os.system(f"java -jar {self.picard} FixMateInformation INPUT={self.output_dir}/Preprocessing/addOrReplace/{filename}.bam")
        os.system(f"java -jar {self.picard} MergeSamFiles INPUT={self.output_dir}/Preprocessing/addOrReplace/{filename}.bam OUTPUT={self.output_dir}Preprocessing/mergeSam/{filename}.bam CREATE_INDEX=true USE_THREADING=true")
        os.system(f"java -jar {self.picard} MarkDuplicates INPUT={self.output_dir}/Preprocessing/mergeSam/{filename}.bam OUTPUT={self.output_dir}/Preprocessing/markDuplicates/{filename}.bam CREATE_INDEX=true METRICS_FILE={self.output_dir}/Preprocessing/markDuplicates/{filename}.metrics.log")
        os.system(f"samtools sort -n {self.output_dir}/Preprocessing/markDuplicates/{filename}.bam -o {self.output_dir}/Preprocessing/markDuplicates/{filename}_sorted.bam")


def main():
    return 0


if __name__ == "__main__":
    sys.exit(main())
