#!usr/bin/env python3

"""
Script remove some directories.
"""

import os
import sys
import shutil
from parse_args import construct_parser


class Remover:
    def __init__(self, path):
        self.path = path

    def removedirs(self):
        dirs = ["sortedBam", "addOrReplace", "mergeSam", "markDuplicates"]
        for directory in dirs:
            if os.path.exists(f"{self.path}/output/{directory}"):
                try:
                    shutil.rmtree(f"{self.path}/output/{directory}")
                except OSError as e:
                    print("Error: %s : %s" % (f"{self.path}/output/{directory}", e.strerror))


def main():
    parser = construct_parser()
    args = parser.parse_args()
    yes = Remover(args.outputDir)
    yes.removedirs()

    return 0


if __name__ == '__main__':
    sys.exit(main())