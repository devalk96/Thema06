"""
Module which handles the backend of fastqc.
"""

import os
import glob
import zipfile
import gzip


class Fastqc_file:
    """
    Fastqc objects contains all the needed parameters.
    """

    def __init__(self, filepath, output_folder):
        self.path = filepath
        self.output_folder = output_folder
        self.filename = os.path.basename(self.path)
        self.processed_status = process_status(filename=self.filename, output_folder=self.output_folder)
        self.file_corrupt = False
        self.paired = self.isPaired()

    def isPaired(self):
        """
        Checks if file is paired or not. If the identifier contains a '/' symbol, this method will return a 1 or 2.
        If there is no '/' symbol. Method will return False.
        Uses find method to check if '/' in identifier. If there is no '/'. Find returns -1 else index is returned.
        """

        # If file is compressed as gz. Module gzip is used instead of built-in open function
        if self.filename.split(".")[-1] == "gz":
            with gzip.open(self.path, "r") as stream:
                identifier = stream.readline().decode("utf-8").rstrip()
        else:
            with open(self.path, "r") as stream:
                identifier = stream.readline().rstrip()

        return identifier[identifier.find("/")] if identifier.find("/") != -1 else False


class Fastqc_manager:
    """
    Fastqc_manager is used to process the fastqc tool.
    """

    def __init__(self, fastq_folder, output, tool_path, skip=True, threads=4):
        self.fastq_path = fastq_folder
        self.max_threads = threads
        self.skip_processed = skip
        self.output_path = output
        self.files_list = self.grab_fastq()
        self.tool_path = tool_path

    def grab_fastq(self):
        """
        This function creates a list with fastqc_file objects.
        """
        os.chdir(self.fastq_path)
        filenames = glob.glob("*.gz") + glob.glob("*.fastq")  # return all files with the right extention
        files = [f"{self.fastq_path}/{file}" for file in filenames]  # returns full path for every file
        return [Fastqc_file(file, self.output_path) for file in files]  # construct Fastqc_file object for each file

    def run_fastqc(self):
        """
        This function run the fastqc tool. First all file paths are appended to a list. If skipping already processed
        files is set to True. The already proccesed files won't be added to the list. After construction of this list
        the max amount of threads to be used is calculated. Then the os.system() method will be called and executed,
        which will start the fastqc tool.
        """
        # IF skipping processed file is enabled. Checks if file is already processed. If not file gets appended to
        # a list, containing all the files that needs to be processed.
        if self.skip_processed:
            files = []
            for file in self.files_list:
                if not file.processed_status:
                    files.append(file.path)
        else:
            files = [file.path for file in self.files_list]  # Append all file paths to a list

        thread_amount = len(files) if len(files) <= self.max_threads else self.max_threads  # Calculate max threads

        # Create string which will be used to run the FastQC tool.
        parameters = f"{self.tool_path} {' '.join(files)} " \
                     f"-t {thread_amount} " \
                     f"-o {self.output_path} "
        if len(files) == 0:
            print("No fastqc files to process")
        else:
            os.system(parameters)
        self.validate_results()

    def validate_results(self):
        for file in self.files_list:
            accession_code = file.filename.split(".")[0]
            os.chdir(f"{self.output_path}")
            zip_file = self.output_path + "/" + glob.glob(f"{accession_code}*.zip")[0]
            with zipfile.ZipFile(zip_file, allowZip64=True) as archive:
                path = accession_code + "_fastqc/fastqc_data.txt"
                with archive.open(path, "r") as stream:
                    averages, score = self._read_file(stream)
            if averages:
                print(f"{accession_code} has no variance in quality! (score: {score})")
                file.file_corrupt = averages

    def _read_file(self, stream_object):
        """
        Checks if all values in file are the same. e.g. ALl files with the score 14
        """
        starting_line_found = False
        file = []
        score = None
        for line in stream_object:
            line = str(line.decode("utf-8").rstrip())
            if line.startswith("#Base"):
                starting_line_found = True
                continue

            if line.startswith(">>END_MODULE") and starting_line_found:
                break

            if starting_line_found:
                line = line.split("\t")[1:]
                line = [value.replace("NaN", "").replace("'", "") for value in line]  # REMOVE NON AND '
                line = [float(x) for x in list(filter(None, line))]
                score = line[0]
                file.append(all([x == line[0] for x in line]))  # Are all values of lines true
        return all(file), score

    def settings(self):
        """
        Returns parameters which will be run with the fastQC tool
        """
        return f"fastqc ran with the following parameters:\n" \
               f"Output path: {self.output_path}\n" \
               f"input folder: {self.fastq_path}\n" \
               f"Max threads: {self.max_threads}\n" \
               f"Skip files: {self.skip_processed}\n\n"


def process_status(filename, output_folder):
    """Checks if both html and zipfile are already in the output file."""
    filename = os.path.basename(filename)
    html = f"{output_folder}/{filename.split('.')[0]}_fastqc.html"
    zip_file = f"{output_folder}/{filename.split('.')[0]}_fastqc.zip"
    if os.path.exists(html) and os.path.exists(zip_file):
        return True
    else:
        return False


def main():
    # Example of how this module could be run
    data = Fastqc_manager(
        fastq_folder="/data/storix2/student/2019-2020/Thema06/project-data/How_to_deal_with_difficult_data/Data",
        output="/homes/sjbouwman/Thema06/fastqc/reports",
        threads=16,
        tool_path="fastqc",
        skip=True)
    data.run_fastqc()


if __name__ == '__main__':
    main()
