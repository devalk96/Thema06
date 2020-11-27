import sys
import argparse
import os
import Code_Sander.directorymanager
import glob
from multiprocessing import process, queues
import multiqc

# Data can be found at: /data/storix2/student/2019-2020/Thema06/project-data/How_to_deal_with_difficult_data/Data"
# default_output = "/homes/sjbouwman/Thema06"
picard = ""
hisat = ""
featureCounts = ""
trimGalore = ""

SUBDIRS = {'fastqc': {'reports': None},
           'output': {'trimmed_data': None}}


class Inputargs():
    """
    Argparser class
    """

    def __init__(self):
        self.parser = self.construct_parser()
        self.args = self.parser.parse_args()
        self.threads = self.args.threads
        self.validate_input()

    def construct_parser(self):
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

    def error(self, message):
        return self.parser.error(message)

    def validate_input(self):
        if not os.path.exists(self.args.fastqDir):
            self.error(f"Path to {self.args.fastqDir} not found!")


class Qualitycheck():
    def __init__(self, input_path, output_path, threads=4, skip_existing=False):
        self.fastq_files = [f"{input_path}/{x}" for x in os.listdir(input_path)]
        self.output_path = Code_Sander.directorymanager.create_dirs(file_root=output_path, subdirs=SUBDIRS)
        self.threads = threads
        self.skip_existing = skip_existing

    def fastqc(self, files):
        """Checks if files is a list otherwise creates a list"""
        if type(files) != list:
            files = [files]

        for file in files:
            if self.skip_existing:
                file_and_ext = os.path.split(f"{self.output_path}/{file}")
                filename = file_and_ext[1].split(".fastq")[0]
                if os.path.exists(f"{self.output_path}/fastqc/reports/{filename}_fastqc.html") and \
                        os.path.exists(f"{self.output_path}/fastqc/reports/{filename}_fastqc.zip"):
                    print(f"{filename} analysis already complete")
                    files.remove(file)

        if len(files) == 0:
            print("No fastqc files to process...")
            return 0

        self.run_fastqc(file=files, output=f"{self.output_path}/fastqc/reports")

    def run_fastqc(self, file, output):
        """Generates basic fastqc report using provided multiple threads. The maximum amount of threads is calculated"""
        print(f"Max allowed threads: {self.threads}\nFile amount: {len(file)}\n"
              f"Will use {len(file) if len(file) <= self.threads else self.threads} threads")

        os.system(f"fastqc {' '.join(file)} -t {len(file) if len(file) <= self.threads else self.threads} -o {output}")

    def generate_multiqc(self):
        pass

    def settings(self):
        return f"output path: {self.output_path}\ninput path: {self.fastq_files}\nMax threads: {self.threads}\nSkip " \
               f"files: {self.skip_existing} "


def main():
    # data = os.listdir("/data/storix2/student/2019-2020/Thema06/project-data/How_to_deal_with_difficult_data/Data")
    # print(data)
    parser = Inputargs()
    data = Qualitycheck(input_path=parser.args.fastqDir,
                        output_path=parser.args.outputDir,
                        threads=parser.args.threads,
                        skip_existing=parser.args.skip)
    data.settings()
    data.fastqc(data.fastq_files)
    return 0


if __name__ == '__main__':
    sys.exit(main())
