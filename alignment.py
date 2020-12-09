#!usr/bin/env python3

"""
Script to map the reads.
"""
import os


class Alignment:
    """
    Align the reads to a reference genome
    """
    def __init__(self, directory, tool, refseq):
        self.directory = directory
        self.tool = tool
        self.refseq = refseq

    def getting_ready(self):
        """
        Get the filenames in a list
        """
        uniquefiles = []
        for file in self.directory:
            filename = file.split('.')[0]
            if filename not in uniquefiles:
                uniquefiles.append(filename)
        return uniquefiles

    def processing(self):
        """
        Map the files and save them as filename_aligned.sam
        """
        for file in self.getting_ready():
            os.system(f"{self.tool} -a {self.refseq} {file} > {file}_aligned.sam")
