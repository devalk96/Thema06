import os
import sys


def process_status(filename, output_folder):
    """Checks if both html and zipfile are already in the output file."""
    filename = os.path.basename(filename)
    html = f"{output_folder}/{filename.split('.')[0]}_fastqc.html"
    zip_file = f"{output_folder}/{filename.split('.')[0]}_fastqc.zip"
    if os.path.exists(html) and os.path.exists(zip_file):
        return True
    else:
        return False


class Fastqc_file:
    """
    Fastqc objects has various properties
    """

    def __init__(self, filepath, output_folder):
        self.path = filepath
        self.output_folder = output_folder
        self.filename = os.path.basename(self.path)
        self.procced_status = process_status(filename=self.filename, output_folder=self.output_folder)


class Fastqc_manager:
    """
    Fastqc_manager is used to process the fastqc tool.
    """

    def __init__(self, fastq_folder, output, threads=8, skip=False):
        self.fastq_path = fastq_folder
        self.max_threads = threads
        self.skip_processed = skip
        self.output_path = output
        self.files_list = self.grab_fastq()

    def grab_fastq(self):
        """
        This function creates a list with fastqc_file objects.
        """
        files = [f"{self.fastq_path}/{file}" for file in
                 os.listdir(self.fastq_path)]  # returns full path for every file
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
                if not file.procced_status:
                    files.append(file.path)
        else:
            files = [file.path for file in self.files_list]  # Append all file paths to a list
        thread_amount = len(files) if len(files) <= self.max_threads else self.max_threads  # Calculate max threads
        parameters = f"fastqc {' '.join(files)} " \
                     f"-t {thread_amount} " \
                     f"-o {self.output_path} "
        if len(files) == 0:
            print("No files to process")
        else:
            os.system(parameters)


def main():
    # Example of how this module could be run
    data = Fastqc_manager(
        fastq_folder="/data/storix2/student/2019-2020/Thema06/project-data/How_to_deal_with_difficult_data/Data",
        output="/homes/sjbouwman/Thema06/fastqc/reports",
        threads=16,
        skip=True)
    data.run_fastqc()


if __name__ == '__main__':
    main()
