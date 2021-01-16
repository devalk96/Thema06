import os
import glob
import subprocess


class Trimmer_manager:
    def __init__(self, output, tool_path, cutadapt_path, file_list, quality=20, threads=8, skip=False):
        self.max_threads = threads  # Hardcoded
        self.skip_processed = skip
        self.output_path = output
        self.tool_path = tool_path
        self.file_list = file_list
        self.quality = quality
        self.cutadapt_path = cutadapt_path

    def run_trimmer(self):
        for file in self.file_list:
            print("\nStarted trimming file: ", file.filename)
            if file.file_corrupt:
                print(f"Skipping {file.filename} as it is marked corrupt by fastqc_manager")
                continue

            #basename = ".".join(file.filename.split('.')[:-2])
            basename = file.filename.split('.')[0]
            if "_" in basename and file.paired is not False:
                #output = f"{self.output_path}/{'_'.join(basename.split('_')[:-1])}"
                output = f"{self.output_path}/{basename.split('_')[0]}"
            else:
                output = f"{self.output_path}/{file.filename.split('.')[0]}"
            threads = self.max_threads if self.max_threads <= 8 else 8
            command = f"{self.tool_path} {file.path} -o {output} -j {threads} --path_to_cutadapt {self.cutadapt_path} -q {self.quality} {'--paired' if file.paired else ''} "
            try:
                process = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
                process = process.decode("utf-8")
                print(f"Successfully finished {file.filename}")
            except subprocess.CalledProcessError as e:
                error_string = e.output.decode("utf-8")
                if "SOLiD colorspace format" in error_string:
                    print(f"File {file.filename} seems to be in SOLiD colorspace format which is not supported by "
                          f"Trim Galore! Please "
                          "use Cutadapt on colorspace "
                          "files separately and check its documentation!")

                    file.colorspace = True
                else:
                    print(f"Encountered an unknown ERROR!\n", error_string)

                    file.error = error_string
                os.rmdir(output)

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
