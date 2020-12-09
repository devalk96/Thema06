#!usr/bin/env python3

"""
Script to map the reads.
"""
import os
import glob


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
        data = glob.glob("*.fa") + glob.glob("*.fasta")
        for file in data:
            print(f"{self.tool_path} -a {self.refseq} {file} > {self.output_path}/{file.split('.')[0]}_aligned.sam")
            # os.system(f"{self.tool_path} -a {self.refseq} {file} > {file.split('.')[-1]}_aligned.sam")
