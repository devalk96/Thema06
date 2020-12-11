import os
import glob


class Trimmer_manager:
    def __init__(self, output, tool_path, file_list, quality=20, threads=8, skip=False):
        self.max_threads = threads
        self.skip_processed = skip
        self.output_path = output
        self.tool_path = tool_path
        self.file_list = file_list
        self.quality = quality

    def run_trimmer(self):
        for file in self.file_list:
            filename = file.filename.split(".")[0]
            command = f"{self.tool_path} {file.path} -o {self.output_path + filename} -j {self.max_threads}"
            os.system(command)
            print(f"Done with file {file.filename}")

    def settings(self):
        return f"Trimmer ran with the following parameters:\n" \
               f"Output path: {self.output_path}\n" \
               f"quality: {self.quality}\n" \
               f"Max threads: {self.max_threads}\n" \
               f"Skip files: {self.skip_processed}\n\n"

def main():
    data = Trimmer_manager(
        output="/homes/sjbouwman/Thema06/output/trimmed_data",
        threads=16,
        tool_path="/data/storix2/student/2020-2021/Thema10/tmp/tools/ptrimmer",
        skip=True)


if __name__ == '__main__':
    main()
