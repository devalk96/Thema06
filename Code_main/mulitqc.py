#!usr/bin/env python3

"""
Script to run multiqc.
"""

import multiqc
from parse_args import construct_parser
import sys
import os


class Multiqc:
    def __init__(self, files):
        self.files = files

    def run_qc(self):
        if not os.path.exists(f"{self.files}/MultiQC"):
            os.makedirs(f"{self.files}/MultiQC")
        multiqc.run(analysis_dir=self.files, outdir=f"{self.files}/MultiQC", force=True, make_pdf=True)


def main():
    parser = construct_parser()
    args = parser.parse_args()
    yes = Multiqc(f"{args.outputDir}")
    yes.run_qc()

    return 0


if __name__ == '__main__':
    sys.exit(main())