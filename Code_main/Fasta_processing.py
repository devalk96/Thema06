#!/usr/bin/env python3

"""
Fasta processing steps
"""


__author__ = "Team B"
__status__ = "Working Module"
__version__ = "1.0"

import os
import sys


class Fasta_processor:
    """
    Create neccecary aditional files
    """
    def __init__(self, fasta, picard_path):
        self.fasta = fasta
        self.picard_path = picard_path
        self.dict_name = self.create_dict_name()

    def create_fata_dict(self):
        """
        Creates the sequence dictionary for the fasta file if it doesn't exist
        """
        if not os.path.isfile(self.dict_name):
            os.system(f"java -jar {self.picard_path} CreateSequenceDictionary R={self.fasta} O={self.dict_name}")
        return 0

    def create_dict_name(self):
        """
        Create dictionary name
        """
        base = self.fasta.split(".")
        dict_name = f"{'.'.join(base[:-1])}.dict"
        return dict_name

    def create_fa_fai(self):
        """
        Creates the fasta.fai. file (fasta index) if it doesn't exist
        """
        if not os.path.isfile(f"{self.fasta}.fai"):
            os.system(f"samtool faidx {self.fasta}")
        return 0


def main():
    return 0


if __name__ == "__main__":
    sys.exit(main())
