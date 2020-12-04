import os
import glob


class Trimmer_manager:
    def __init__(self, fastq_folder, output, threads=8, skip=False, tool_path):
        self.fastq_path = fastq_folder
        self.max_threads = threads
        self.skip_processed = skip
        self.output_path = output
        self.tool_path = tool_path



def main():
    data = Trimmer_manager(
        fastq_folder="/data/storix2/student/2019-2020/Thema06/project-data/How_to_deal_with_difficult_data/Data",
        output="/homes/sjbouwman/Thema06/output/trimmed_data",
        threads=16,
        tool_path="/data/storix2/student/2020-2021/Thema10/tmp/tools/ptrimmer",
        skip=True)


if __name__ == '__main__':
    main()
